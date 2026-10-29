# Fusion execution and validation

This skill provides a workflow and evidence helper, not a Fusion control server. Discover actual capabilities. Prefer an available suitable connector/API; otherwise use computer control with Fusion's native Python console or Scripts and Add-Ins. If neither is available, prepare runnable scripts/records and report application execution pending.

## Preserve the design

Inspect active document, hierarchy, occurrences, timeline, units, parameters, and visibility. Save a version/copy first. Record accepted geometry/transforms. Scope edits to requested components; do not rebuild an approved case to repair a hinge or lettering.

Name components, sketches, bodies, parameters, and features by purpose. Separate estimated parameters. Read/write project scripts and records explicitly as UTF-8. Inspect API documentation for unfamiliar methods.

Fusion real-valued geometry API lengths normally use internal centimetres: convert mm explicitly (`mm / 10.0`) where required. Prefer unit-bearing parameter expressions (`"70 mm"`). Check each API's units, including angles. Independently measure the BRep envelope immediately. Avoid blind whole-model rescaling when units are mixed.

## Assemblies and details

Use meaningful components, not merely many bodies under one root. Separate enclosure, display, hinge parts, keyboard/markings as evidence/task requires. Ground the intended base; use rigid relationships for parts moving together and revolute joints about supported axes. Record rest pose and opening limits. Inferred limits remain estimates.

Account for occurrence transforms when comparing local BRep geometry with assembly coordinates. Inspect motion across relevant angles, gaps, interference, and closed alignment; preserve a restorable pose. Motion checks cannot prove the mechanism matches the original.

Changing upstream text topology after copying/moving its bodies can break downstream dependencies. Inspect history first; prefer local additions/replacements in the responsible component when that preserves accepted geometry. Verify actual resulting glyph islands, counters, size, placement, orientation, and engraving depth. A text object alone does not prove visible lettering exists.

## Three separate validation passes

1. Geometry: independently measured final BRep dimensions, ports, axes, sections, edge treatments, offsets; timeline health and expected bodies/components. Parameter equality is not independent measurement.
2. Source fidelity: registered matching-view overlays, silhouette/landmark discrepancies, uncertainty. Attractive renders are not dimensional evidence.
3. Assembly/export: joint motion/interference; native/exchange export then reopen/reimport where possible. STEP alone does not preserve the full native parametric history and joint setup.

Record executed values, units, revision, and failures. If a call hangs or export fails, inspect current state and use a bounded retry/available computer-control fallback. A started script is not a completed build. Do not discard unsaved work automatically.

Deliver native editable files, requested exchange files, comparison views and evidence/results. Draft exports are allowed with unresolved estimates clearly identified; do not relabel them as verified final geometry.
