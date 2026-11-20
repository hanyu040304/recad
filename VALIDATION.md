# Validation — 2026-10-29

Version: 0.1.0. This is a workflow skill, not an independently certified reverse-engineering system.

## Executable helper

Python 3.9.6, standard library only. `python3 -m unittest discover -s tests -v`: **23 tests passed**. Cases cover final-geometry tenfold unit errors, parameter-only checks, unresolved critical features, photo estimates, shared-model sources, missing/duplicate evidence, derivations, tolerances, invalid numeric inputs, calibration, UTF-8 output, and command exit codes. Both synthetic ledger examples are exercised; unresolved critical items intentionally produce exit 2.

The helper cannot inspect Fusion, authenticate a source, validate a photo camera, detect omitted features, or certify real-world precision. A successful record audit is not a model-fidelity test.

## Offline workflow scenarios

Five fresh-context controls without the skill and five fresh-context responses with the skill were collected. Scenarios/rubric are in `evals/`; observations are in `evals/results-2026-10-29.md`.

The assisted responses retained evidence classes, independent geometry checks, official-model filtering, scope protection and truthful execution status. Controls also generally handled these risks well. This small qualitative comparison does **not** establish a measurable improvement, a lower failure rate, or geometric accuracy. No numeric success-rate claim is made.

## Package checks

YAML syntax and metadata checked with Ruby Psych plus explicit field/name/length/default-prompt checks. Local Markdown reference targets and JSON syntax checked. The bundled skill-creator `quick_validate.py` was attempted but could not complete because PyYAML is absent from the available Python environments; the package does not require PyYAML at runtime. Its relevant frontmatter checks were independently applied, rather than reporting that validator as passed.

## Not verified in this release

No new end-to-end Fusion build, visual overlay, actual joint motion, native export or STEP round-trip was performed while packaging this skill. Earlier project experience motivated the workflow, but is not a test of this published package. Live connector/computer-control availability, Fusion versions, product geometry and reference quality vary. Test these in the target environment and retain the measured evidence before making a fidelity claim.

## Sharing preparation — 2026-11-20

The skill instructions and executable helper are unchanged from version 0.1.0. The Chinese README now includes a workflow summary, the intended GitHub clone URL, and macOS/Linux/Windows installation examples.

Re-ran `python3 -m unittest discover -s tests -v` under Python 3.9.6: **23 tests passed**. The stock skill-creator validator still cannot run because PyYAML is absent in both system Python and the available bundled Python 3.12.14. This is a validator dependency, not a runtime dependency of the skill. Publication status is reported separately; a clone URL in the README does not establish that the remote repository exists.

Independently checked YAML syntax and the validator's metadata/name/description/scaffold requirements with Ruby Psych, plus UI invocation metadata, JSON syntax, UTF-8 text, local Markdown references, and distribution content. Copied the standalone skill into a temporary installation and ran both documented helper commands there; audit returned the expected unresolved-item code 2 and calibration returned 0. These checks establish package portability for the helper, not live Fusion compatibility.

## ReCAD presentation — version 0.1.1

Renamed the project display name to ReCAD. The existing `fusion-reverse-modeling` skill identifier and directory remain compatible. The README and examples now describe general product reconstruction, with Autodesk Fusion explicitly identified as the current execution environment. Detailed usage moved to `docs/usage.md`; the new SVG illustrates a synthetic mounting bracket, not a measured manufacturer product. Helper code is unchanged.

Re-ran all 23 helper tests and checked skill/UI YAML metadata, local Markdown references, JSON and SVG syntax. Rendered the README at desktop and mobile widths; neither preview had horizontal page overflow. The stock PyYAML-dependent validator remains unavailable as noted above. These are documentation/package checks, not a new end-to-end Fusion reconstruction test.
