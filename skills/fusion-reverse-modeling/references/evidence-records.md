# Project records and helper

Store evidence beside the user's model, not in the installed skill. Suggested project files: `sources.json`, `evidence.json`, `calibration/` (images/endpoints/registrations), project Fusion scripts, `views/`, `checks.json`, editable `.f3d`, and requested `.step`.

Record every important feature's exact source location, datum/frame, value, evidence class, assumptions, and check method. Include unknown critical features. User-supplied files may have local document IDs/page/detail instead of public URLs. Add publisher, revision, access date, and model match when applicable. Do not publish private reference files or user paths.

Minimal schema is illustrated by `examples/drawing.json` and `examples/photo.json` inside this skill. Additional metadata is allowed.

| Field | Definition |
|---|---|
| schema_version, model | Integer 1; exact product/configuration |
| sources[].id, kind | Unique ID; drawing/official_spec/official_photo/repair_manual/measured/third_party |
| model_match, locator | exact/shared/unconfirmed; retrievable source/page/detail |
| dimensioned | Boolean: source actually states dimensions |
| features[].id, critical, source_ids | Unique feature, boolean importance, source references |
| basis | dimensioned / derived / photo / unknown |
| target_mm | Nominal length/coordinate; coordinates may be negative |
| source_tolerance_mm | Symmetric tolerance actually stated in source; omit if absent |
| verification_tolerance_mm | CAD construction deviation allowed by this check |
| uncertainty_mm | Estimate uncertainty; omit/null if unquantified; document method |
| derivation | Required for derived values; equation and datums |
| cad_measurement | value_mm, method, locator; independent final geometry uses method brep |

Keep full asymmetric tolerances, angular/curve checks, clearance zones and GD&T in `checks.json`; do not force them into a scalar symmetric field. This helper only compares scalar millimetre records.

From the installed skill directory:

```sh
python3 scripts/evidence_tools.py audit examples/drawing.json --output audit.json
python3 scripts/evidence_tools.py calibrate --reference-mm 100 --reference-px 1000 --feature-px 200 --reference-uncertainty-mm 0.1 --pixel-error-px 1
```

Calibration requires an already rectified coplanar image. Pixel error bounds each measured pixel **length**, not each endpoint or a standard deviation. The first-order bound is `|p/P|eL + |L/P|ep + |Lp/P²|eP`, using the supplied pixel error for ep and eP. It is not a confidence interval; add systematic errors separately. Large errors require a suitable interval calculation.

Audit exit codes: 0 records processed with no open critical checks; 1 malformed input/I/O error; 2 unresolved/mismatched/unmeasured critical records. Exit 0 may include photo estimates: inspect critical_estimates and unquantified_estimates. certifies_real_world_accuracy is always false. The helper trusts supplied numbers and cannot inspect BRep, authenticate sources, prove calibration/derivations, or detect omitted features. It must not be the sole basis for a precision claim.
