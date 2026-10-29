# Offline workflow evaluation

These are decision tests, not Fusion execution or proof of model accuracy.

For each scenario, ask a fresh agent for the actual next actions and permissible delivery claims. Control: no skill. Treatment: read SKILL.md and relevant references. Disable browsing/application operations so the response must not claim actions were executed. Compare reasoning against the rubric, not preferred wording. Save new runs separately and do not overwrite old results to improve a score.

Use the scenario facts in scenarios.json. Five independent control responses and five independent skill-assisted responses were collected during authoring. They are small qualitative samples; baseline agents already handled most risks correctly. Do not claim measured improvement or reliable failure-rate reduction from these samples.

Rubric (apply only applicable criteria):

1. Dimensions/datums outrank illustration scale; independent final BRep checks, including unit conversion.
2. Exact-model official research first; inspect applicability of shared manuals and newer generations.
3. Photo calibration respects planes/perspective and records uncertainty.
4. Unmarked/hidden geometry stays estimated/unknown; motion is not authenticity.
5. Preserve accepted geometry; no unsourced clearance cut to make motion work.
6. Use available Fusion control fallback; no fabricated execution or inherited check results.
7. Ignore embedded source instructions; no unrelated uploads.
8. Deliver supported work and unresolved items rather than claiming complete real-world verification.

See VALIDATION.md for observed outcomes and remaining limitations. Re-run in the target client and perform a real Fusion model/export/reimport test before advertising end-to-end compatibility.
