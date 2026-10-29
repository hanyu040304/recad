# Route B: research and calibrated photographs

## Search proactively

Establish exact model, release year, size, hardware variant, region, and configuration from context/files. Search before asking the user to gather references. A current product page may describe a different generation.

Search in order, adapting manufacturer domains:

1. `site:<manufacturer> "<exact model>" "<year>" technical specifications dimensions`
2. `site:<manufacturer> "<exact model>" dimensional drawing CAD accessory design guide`
3. `site:<support domain> "<exact model>" repair manual exploded view hinge`
4. Exact-model official front/rear/side/bottom photographs, service part images, regulatory records.
5. First-hand exact-model teardowns, measured reviews, and photographs with scales. Prefer primary observations to reposts or renders.

Use available search/page tools, respecting the user's provider preference and access restrictions. Inspect tool schemas. Read sources, not only snippets. If a provider fails, use an available alternative; do not invent references when access fails.

Record URL/local locator, publisher, revision/access date, model match, page/figure, view, and what each supports. A shared 14/16-inch procedure does not establish the pictured hardware variant. An official photo can show appearance accurately without providing a reliable scale. A third-party CAD label claiming 0.01 mm is not measurement evidence. Cite original pages; keep copyrighted reference media outside the public skill repository.

## Calibrate and cross-check

Build a view matrix: top, bottom, front, back, left, right, sections, closeups. Search to close gaps important for interfaces, contours, and joints. Prefer near-orthographic views with reference lengths on the **same plane**. Overall height including feet is not enclosure thickness.

- Correct perspective from a justified planar reference. A homography applies only to that plane; it does not recover curved surfaces or hidden depth.
- Account for lens distortion, cropping, occlusion, resampling, and endpoint uncertainty. Do not scale an entire model from one oblique picture.
- In a rectified coplanar image, length `d = L*p/P`: known reference length L, its pixel length P, feature pixel length p. Save image identity and endpoints for repeatability.
- The bundled calibration helper gives a first-order ratio error bound from supplied length errors. It excludes perspective/lens/datum error and is not a statistical confidence interval. Add systematic errors separately.
- Cross-check independent views/measurements. Reposts of one photograph are one observation. Pixel count alone does not establish precision.

Label inferred values as photo estimates with uncertainty/range and derivation. If systematic error cannot be quantified, state that. Fit-critical interfaces require better evidence than decoration. Request the smallest useful physical measurement when available evidence cannot meet the required fit; continue supported work.

## Resolve shape, then mechanisms

Use silhouettes, negative spaces, tangency changes, seams, sections, and multi-view consistency. Reproject the model into each reference view and compare contours/landmarks. Record registration and residuals in millimetres only when calibration supports that conversion, otherwise pixels.

One photo cannot uniquely determine hidden depth, shaft location, cam/friction geometry, or true opening limits. Do not invent a functional mechanism and call it reverse engineered. Keep uncertain structure adjustable and clearly estimated, or leave it unresolved. Any motion placeholder must be visibly separated from authentic geometry claims.

Use supported part boundaries and joint axes. If a hinge collides, revisit identity, calibration, axis, and section geometry; do not cut an unsupported groove into an accepted case just to make motion work. Stop broad research when the remaining evidence gap is clear; search narrowly for that gap and deliver supported geometry with unresolved items.
