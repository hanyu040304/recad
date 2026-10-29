import copy
import importlib.util
import math
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/fusion-reverse-modeling/scripts/evidence_tools.py"
spec = importlib.util.spec_from_file_location("evidence_tools", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def ledger():
    return {
        "schema_version": 1,
        "model": "Example Instrument A / revision 1",
        "sources": [{"id": "D1", "kind": "drawing", "model_match": "exact",
                     "locator": "user-supplied drawing, sheet 1, dimension W", "dimensioned": True}],
        "features": [{"id": "width", "critical": True, "basis": "dimensioned",
                      "source_ids": ["D1"], "target_mm": 70.0,
                      "source_tolerance_mm": 0.05, "verification_tolerance_mm": 0.001,
                      "cad_measurement": {"value_mm": 70.0, "method": "brep",
                                          "locator": "Case:1, opposed planar faces"}}]
    }


class EvidenceTests(unittest.TestCase):
    def test_recorded_dimension_can_be_compared_but_never_certified(self):
        report = module.audit(ledger())
        self.assertEqual(report["features"][0]["status"], "matches_recorded_dimension")
        self.assertFalse(report["certifies_real_world_accuracy"])

    def test_centimeter_mistake_is_detected_from_final_geometry(self):
        data = ledger()
        data["features"][0]["cad_measurement"]["value_mm"] = 700
        self.assertEqual(module.audit(data)["features"][0]["status"], "mismatch")

    def test_parameter_equation_is_not_an_independent_measurement(self):
        data = ledger()
        data["features"][0]["cad_measurement"]["method"] = "parameter_equation"
        self.assertEqual(module.audit(data)["features"][0]["status"], "not_independently_measured")

    def test_unknown_chamfer_keeps_critical_item_open(self):
        data = ledger()
        data["features"].append({"id": "ring_chamfer", "critical": True,
                                 "basis": "unknown", "source_ids": []})
        self.assertEqual(module.audit(data)["critical_open"], ["ring_chamfer"])

    def test_photo_estimate_does_not_become_a_drawing_dimension(self):
        data = ledger()
        data["features"][0]["basis"] = "photo"
        data["features"][0]["uncertainty_mm"] = 0.3
        report = module.audit(data)
        self.assertEqual(report["features"][0]["status"], "matches_photo_estimate")
        self.assertEqual(report["critical_estimates"], ["width"])

    def test_unquantified_photo_error_is_reported(self):
        data = ledger()
        data["features"][0]["basis"] = "photo"
        self.assertEqual(module.audit(data)["unquantified_estimates"], ["width"])

    def test_shared_model_drawing_cannot_assert_exact_model_dimension(self):
        data = ledger()
        data["sources"][0]["model_match"] = "shared"
        with self.assertRaises(ValueError):
            module.audit(data)

    def test_photo_source_cannot_assert_dimensioned_evidence(self):
        data = ledger()
        data["sources"][0]["kind"] = "official_photo"
        with self.assertRaises(ValueError):
            module.audit(data)

    def test_missing_source_is_rejected(self):
        data = ledger()
        data["features"][0]["source_ids"] = ["absent"]
        with self.assertRaises(ValueError):
            module.audit(data)

    def test_duplicate_ids_are_rejected(self):
        data = ledger()
        data["features"].append(copy.deepcopy(data["features"][0]))
        with self.assertRaises(ValueError):
            module.audit(data)

    def test_derivation_is_required(self):
        data = ledger()
        data["features"][0]["basis"] = "derived"
        with self.assertRaises(ValueError):
            module.audit(data)

    def test_derived_value_remains_distinct(self):
        data = ledger()
        data["features"][0].update(basis="derived", derivation="W = 2 * 35.0 mm")
        self.assertEqual(module.audit(data)["features"][0]["status"], "matches_derived_value")

    def test_missing_cad_measurement_is_open(self):
        data = ledger()
        del data["features"][0]["cad_measurement"]
        self.assertEqual(module.audit(data)["critical_open"], ["width"])

    def test_source_and_construction_tolerances_stay_separate(self):
        data = ledger()
        data["features"][0]["cad_measurement"]["value_mm"] = 70.01
        result = module.audit(data)["features"][0]
        self.assertEqual(result["status"], "mismatch")
        self.assertTrue(result["within_source_tolerance"])

    def test_nonfinite_and_boolean_dimensions_are_rejected(self):
        for value in [float("nan"), float("inf"), True, "70"]:
            data = ledger()
            data["features"][0]["target_mm"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                module.audit(data)

    def test_negative_tolerance_is_rejected(self):
        data = ledger()
        data["features"][0]["verification_tolerance_mm"] = -0.1
        with self.assertRaises(ValueError):
            module.audit(data)


class CalibrationTests(unittest.TestCase):
    def test_known_coplanar_length(self):
        result = module.calibrate(100, 1000, 200, 0.1, 1)
        self.assertAlmostEqual(result["length_mm"], 20)
        self.assertAlmostEqual(result["first_order_bound_mm"], 0.14)
        self.assertFalse(result["includes_perspective_or_lens_error"])

    def test_negative_coordinate_is_not_a_negative_length(self):
        with self.assertRaises(ValueError):
            module.calibrate(100, 1000, -200, 0, 1)

    def test_zero_reference_and_nonfinite_errors_are_rejected(self):
        for values in [(100, 0, 200, 0, 1), (0, 1000, 200, 0, 1),
                       (100, 1000, 200, -1, 1), (100, 1000, 200, 0, math.nan)]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                module.calibrate(*values)


class CommandTests(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True, encoding="utf-8")

    def test_successful_audit_writes_utf8_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / "in.json", Path(directory) / "out.json"
            data = ledger()
            data["model"] = "虚构仪器 A"
            source.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            result = self.run_tool("audit", source, "--output", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["model"], "虚构仪器 A")
            self.assertFalse(report["certifies_real_world_accuracy"])

    def test_unresolved_example_returns_two_with_a_report(self):
        result = self.run_tool("audit", SCRIPT.parent.parent / "examples/drawing.json")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("ring_chamfer", json.loads(result.stdout)["critical_open"])

    def test_malformed_json_returns_one(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.json"
            source.write_text("{not json", encoding="utf-8")
            result = self.run_tool("audit", source)
            self.assertEqual(result.returncode, 1)
            self.assertIn("error:", result.stderr)

    def test_calibration_command(self):
        result = self.run_tool("calibrate", "--reference-mm", "100", "--reference-px", "1000",
                               "--feature-px", "200", "--reference-uncertainty-mm", "0.1",
                               "--pixel-error-px", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertAlmostEqual(json.loads(result.stdout)["length_mm"], 20)


if __name__ == "__main__":
    unittest.main()
