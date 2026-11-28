# Grading of the pixel-level test of the TESS Sector 91 gap-edge feature (job epic2043-gapvet-v1)

Graded 2026-11-28 by AI agents working in MV2's name (MV2, Munim, Inc., mv2@munimtech.com), against
`AMENDMENT-2026-11-25-gapvet.md` (frozen 2026-11-25, before any pixel data were analysed). No human
expert has checked it yet. The job ran once on the Blade, 2026-11-28 01:18-01:31 UTC (unit tests and
analysis exit 0). Its output is committed unchanged in `results/gapvet-v0.1.0/`.

## 1. Pre-registered outcome

**Gate `CONTROLS_OK`; overall `MIXED`.** No edge is `ON_TARGET`, so the outcome is not
`CANDIDATE_OCCULTATION`. Because the two edges are `REPRO_FAIL` rather than `SYSTEMATIC`, it is not
`GAP_EDGE_SYSTEMATIC` either; by the frozen rules that leaves `MIXED`.

| window | label | d_t (3x3, bkg-subtracted) | ratio_peak | corr_psf | control median depth | background in / out (e-/s/px) |
|---|---|---|---|---|---|---|
| S91_pregap | REPRO_FAIL | -0.256 | 3.93 | 0.19 | -0.376 | 2344 / 599 |
| S91_postgap | REPRO_FAIL | -0.782 | 1.48 | -0.76 | -1.029 | 5483 / 177 |
| S91_after_midgap (reference) | SYSTEMATIC | +0.199 | -0.37 | -0.08 | -0.003 | 5502 / 341 |
| S91_negative (control) | REPRO_FAIL | -0.003 | - | -0.26 | -0.002 | 194 / 197 |
| S91_positive (control, 30% injected) | ON_TARGET | +0.302 | 0.97 | 0.99 | -0.004 | 194 / 197 |

Both controls behaved as required: nothing is found where nothing was injected, and the injected 30%
dip of the target's own image is recovered at 0.302 with corr_psf 0.99.

## 2. What it means

- **The 80%-deep "dip" at the gap edges is not a dip of the target's light.** In the target's own
  background-subtracted pixels the flux at both edges is not lower than in the comparison cadences
  (d_t is negative, i.e. the aperture reads brighter), and the difference image does not have the
  target's shape (corr_psf 0.19 and -0.76, against 0.99 for the injected dip).
- **The edges are dominated by scattered light.** The per-pixel background is 3.9 times its
  comparison level before the gap and 31 times after it, and 16 times after the sector's other gap
  (the reference edge). Expressed as an aperture depth, the background change is 244, 738 and 355
  times the target's flux (`bkg_change_equiv`, reported, not used in a label). Small errors in that
  background swing the target's measured flux either way, which is how the light-curve job saw a
  fall to 0.19 and this test sees a rise.
- The control stars at the post-gap edge "brighten" by a median 103% too, which a dip of the target
  cannot do.

**Verdict:** the gap-edge feature is not a candidate second occultation. The pre-registered headline
of the main test, `NO_SECOND_EVENT` (GRADING.md), stands unchanged: no second occultation of
EPIC 204376071 in 11 years of K2, ZTF and TESS data, with 45.5% of periods from 70 to 2000 d and
98.4% of 70-100 d excluded. The gap itself (BJD 2460800.37-2460802.10) stays unobserved, as the period
scan already assumed.

## 3. Limits

- One sector, one cutout, one background estimator (the one fixed in the amendment). A
  scattered-light model (e.g. the SPOC or QLP pipelines) could recover usable photometry closer to
  the gap; these were not used.
- `MIXED` is the frozen label. The reading in section 2 is ours, made after the labels were computed.
- Made with AI agents working in MV2's name; no human expert has checked it yet.
