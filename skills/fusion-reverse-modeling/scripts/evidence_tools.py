#!/usr/bin/env python3
"""Evidence bookkeeping and coplanar length calibration, not CAD certification."""
import argparse
import json
import math
from pathlib import Path
import sys


def number(value, name, minimum=None, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name}: expected a finite number")
    if minimum is not None and value < minimum or positive and value <= 0:
        raise ValueError(f"{name}: outside allowed range")
    return float(value)


def nonempty(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}: expected nonempty text")
    return value


def calibrate(reference_mm, reference_px, feature_px, reference_uncertainty_mm, pixel_error_px):
    """First-order bound for a ratio; requires an already valid coplanar image."""
    length = number(reference_mm, "reference_mm", positive=True)
    pixels = number(reference_px, "reference_px", positive=True)
    feature = number(feature_px, "feature_px", minimum=0)
    ref_error = number(reference_uncertainty_mm, "reference_uncertainty_mm", minimum=0)
    pixel_error = number(pixel_error_px, "pixel_error_px", minimum=0)
    estimate = length * feature / pixels
    bound = feature / pixels * ref_error + length / pixels * pixel_error
    bound += length * feature / (pixels * pixels) * pixel_error
    number(estimate, "calibrated length")
    number(bound, "calibration bound")
    return {"length_mm": estimate, "first_order_bound_mm": bound,
            "includes_perspective_or_lens_error": False,
            "note": "First-order ratio bound, not a confidence interval. Add systematic errors separately."}


def audit(data):
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValueError("schema_version must be integer 1")
    model = nonempty(data.get("model"), "model")
    if not isinstance(data.get("sources"), list) or not isinstance(data.get("features"), list):
        raise ValueError("sources and features must be arrays")
    if not data["features"]:
        raise ValueError("features must not be empty")
    sources = {}
    kinds = {"drawing", "official_spec", "official_photo", "repair_manual", "measured", "third_party"}
    dimension_kinds = {"drawing", "official_spec", "repair_manual", "measured"}
    for source in data["sources"]:
        if not isinstance(source, dict):
            raise ValueError("each source must be an object")
        sid = nonempty(source.get("id"), "source.id")
        if sid in sources:
            raise ValueError(f"duplicate source id: {sid}")
        if source.get("kind") not in kinds or source.get("model_match") not in {"exact", "shared", "unconfirmed"}:
            raise ValueError(f"{sid}: invalid source kind or model_match")
        nonempty(source.get("locator"), f"{sid}.locator")
        if "dimensioned" in source and type(source["dimensioned"]) is not bool:
            raise ValueError(f"{sid}.dimensioned must be boolean")
        sources[sid] = source
    results, seen = [], set()
    critical_open, critical_estimates, unquantified = [], [], []
    for feature in data["features"]:
        if not isinstance(feature, dict):
            raise ValueError("each feature must be an object")
        fid = nonempty(feature.get("id"), "feature.id")
        if fid in seen:
            raise ValueError(f"duplicate feature id: {fid}")
        seen.add(fid)
        critical = feature.get("critical")
        if type(critical) is not bool:
            raise ValueError(f"{fid}.critical must be boolean")
        basis = feature.get("basis")
        if basis not in {"dimensioned", "derived", "photo", "unknown"}:
            raise ValueError(f"{fid}: invalid basis")
        refs = feature.get("source_ids")
        if not isinstance(refs, list) or any(not isinstance(s, str) or s not in sources for s in refs):
            raise ValueError(f"{fid}: unknown or malformed source_ids")
        if basis != "unknown" and not refs:
            raise ValueError(f"{fid}: evidence requires a source")
        if basis == "dimensioned" and not any(
            sources[s].get("dimensioned") is True and sources[s]["model_match"] == "exact"
            and sources[s]["kind"] in dimension_kinds for s in refs
        ):
            raise ValueError(f"{fid}: dimensioned evidence requires an exact-model dimension source")
        if basis == "derived":
            nonempty(feature.get("derivation"), f"{fid}.derivation")
        result = {"id": fid, "basis": basis, "critical": critical}
        for key in ("source_tolerance_mm", "uncertainty_mm", "verification_tolerance_mm"):
            if feature.get(key) is not None:
                number(feature[key], f"{fid}.{key}", minimum=0)
        if basis == "unknown":
            result["status"] = "unresolved"
        else:
            target = number(feature.get("target_mm"), f"{fid}.target_mm")
            measurement = feature.get("cad_measurement")
            if measurement is None:
                result["status"] = "not_measured"
            else:
                if not isinstance(measurement, dict):
                    raise ValueError(f"{fid}.cad_measurement must be an object")
                measured = number(measurement.get("value_mm"), f"{fid}.cad_measurement.value_mm")
                nonempty(measurement.get("locator"), f"{fid}.cad_measurement.locator")
                tolerance = number(feature.get("verification_tolerance_mm"),
                                   f"{fid}.verification_tolerance_mm", minimum=0)
                delta = abs(measured - target)
                result["deviation_mm"] = delta
                source_tolerance = feature.get("source_tolerance_mm")
                if source_tolerance is not None:
                    result["within_source_tolerance"] = delta <= source_tolerance + 1e-12
                if measurement.get("method") != "brep":
                    result["status"] = "not_independently_measured"
                elif delta > tolerance + 1e-12:
                    result["status"] = "mismatch"
                else:
                    result["status"] = {"dimensioned": "matches_recorded_dimension",
                                        "derived": "matches_derived_value",
                                        "photo": "matches_photo_estimate"}[basis]
        if critical and not result["status"].startswith("matches_"):
            critical_open.append(fid)
        if critical and basis == "photo":
            critical_estimates.append(fid)
        if basis == "photo" and feature.get("uncertainty_mm") is None:
            unquantified.append(fid)
        results.append(result)
    return {"model": model, "features": results, "critical_open": critical_open,
            "critical_estimates": critical_estimates, "unquantified_estimates": unquantified,
            "certifies_real_world_accuracy": False,
            "note": "Checks supplied records only; does not inspect CAD, images, source truth, or completeness."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("audit", help="Compare supplied BRep measurements with recorded evidence")
    check.add_argument("ledger", type=Path)
    check.add_argument("--output", type=Path)
    calibration = commands.add_parser("calibrate", help="Scale lengths in an already rectified coplanar image")
    for name in ("reference-mm", "reference-px", "feature-px", "reference-uncertainty-mm", "pixel-error-px"):
        calibration.add_argument("--" + name, type=float, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "audit":
            result = audit(json.loads(args.ledger.read_text(encoding="utf-8")))
        else:
            result = calibrate(args.reference_mm, args.reference_px, args.feature_px,
                               args.reference_uncertainty_mm, args.pixel_error_px)
        serialized = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.command == "audit" and args.output:
            args.output.write_text(serialized, encoding="utf-8")
        else:
            print(serialized, end="")
        # 0 = records processed, 1 = malformed input, 2 = unresolved/mismatched critical records.
        return 2 if args.command == "audit" and result["critical_open"] else 0
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
