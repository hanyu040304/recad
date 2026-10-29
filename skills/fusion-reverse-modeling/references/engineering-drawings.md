# Route A: engineering drawings

## Extract before tracing

Inspect every relevant sheet, section, detail, note, and revision at readable resolution. Combine PDF text/vector extraction with rendered inspection: extraction can scramble dimension order. Use an available PDF tool/skill where appropriate.

Confirm exact product/configuration, units, revision, projection, scale warnings, and document purpose. An accessory clearance envelope is not necessarily a product surface. Define a millimetre model frame and a named observer for left/right; record transforms for front/rear/side/section views. Rear views reverse apparent left/right.

Create a feature table containing feature ID, datum/frame, nominal, tolerance, source sheet/detail, evidence class, and criticality. Distinguish diameter/radius, overall/local, reference dimensions, maximum envelopes, and inferred dimensions.

Priority: explicit dimension and datum → valid derivation → calibrated illustration only where scaling is permitted. “DO NOT SCALE” prohibits using illustration measurements as dimensions. PDF zoom and raster resolution cannot supply missing engineering information.

For dimension chains, write signed equations and identify both endpoints. If a datum/arrow is illegible, search for a clearer official copy or corroborating view before requesting targeted clarification. Never choose a plausible endpoint silently. Record conflicting revisions rather than averaging values.

## Build and inspect

Build the envelope and main sections, then interfaces and smaller details. Follow actual section/transition geometry; convenience of a CAD feature is not evidence for its shape. Unmarked bevels, fillets, and hidden structure remain unknown/estimated. A highlight cannot reliably distinguish a chamfer from a fillet. Best-effort estimates must be named, adjustable, and explicitly unverified.

Measure final BRep surfaces, centres, axes, and sections in the documented frame. Compare every critical dimension with its source; record the actual measurement locator and method. Re-reading input parameters is not independent verification.

Keep drawing tolerance, CAD construction/check tolerance, and source/measurement uncertainty separate. Tighter CAD checks do not improve knowledge of the real product; an exact nominal model does not describe manufacturing variation.

Overlay equivalent model/drawing projections. Check silhouette, transitions, concentricity, opening shapes, spacing, handedness, and depth sections. Report source dimension checks separately from visual, assembly, and export checks. Inherited “35/35” results do not verify this revision.

Example: W=70.00±0.05, H=150.00, T=8.00 mm; ring centre (18.00,132.00), diameter 16.00 from the front lower-left datum. Measure these final geometries. A printed side view suggesting X=19.5 does not override X=18.00. An unmarked bevel remains unverified even if all marked dimensions pass.
