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
