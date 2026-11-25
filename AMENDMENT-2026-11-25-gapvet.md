# Amendment 2026-11-25: pixel-level test of the TESS Sector 91 gap-edge feature

Frozen 2026-11-25 (UTC), after the main job (epic2043-occ-v1) was graded (GRADING.md) and before any
pixel-level data were analysed. MV2, Munim, Inc.; made with AI agents working in his name; no human
expert has checked it yet. Code: `gapvet.py` (rules, stdlib), `pixvet.py` (an unchanged copy of the
label rules of munimtechnologies/epic2202-second-eclipse at commit c9e0c5fa, pre-registered there in
its own AMENDMENT-2026-11-25-pixvet.md), `job_gapvet.py` (I/O), tests in `test_gapvet.py`.
Job: `epic2043-gapvet-v1`. This amendment changes no verdict of the main test.

## Why

In the Sector 91 light curve the target's 3x3-aperture flux falls from 0.95 to 0.19 in the hour
before a 1.74-day data gap (BJD 2460800.37-2460802.10) and climbs from 0.30 to 1.03 in the hour after
it (GRADING.md section 5). Read at face value that is a second 80%-deep occultation, the result the
discoverers hoped TESS would deliver. Our light-curve reading says it is a gap-edge systematic, but
that reading was not pre-registered, so the feature gets a fixed test.

## Data

The MAST TESScut 21x21-pixel cutout of Sector 91 centred on the target (RA 241.042141,
Dec -22.579427). Same quality-bit mask as io_tess.py (bits 1, 2, 4, 8, 32, 128). Only cadences within
0.5 d of each window are analysed. The quality flags of every cadence within 1.4 d of the gap centre
are written out for the record.

## Windows

| name | role | t_mid (BJD) | width (d) |
|---|---|---|---|
| S91_pregap | edge before the gap | 2460800.350 | 0.06 |
| S91_postgap | edge after the gap | 2460802.115 | 0.04 |
| S91_after_midgap | reference: first cadences after the sector's other long gap (0.603 there) | 2460788.125 | 0.03 |
| S91_negative | control, flat stretch, nothing injected | 2460796.700 | 0.06 |
| S91_positive | control, same stretch, 30% dip of the target's own 5x5 image injected | 2460796.700 | 0.06 |

In-window cadences: |t - t_mid| <= width/2. Comparison cadences: 0.15-0.50 d from t_mid (one-sided at
a gap edge, because the other side has no data).

## Measurements and labels (identical to the EPIC 220208795 pixel test)

d_t (background-subtracted 3x3 depth), d_1 (peak-pixel depth), ratio_peak = d_1/d_t (about 1 for a
dip of the target's light; near 1/(9 x peak share), about 0.23 here, for a background error),
corr_psf (5x5 correlation of the difference image with the target's image, near +1 for a dip of the
target), and the median depth of up to 8 control stars in the cutout. Labels by
`pixvet.label_event`: REPRO_FAIL (d_t < 0.03); SYSTEMATIC (>= 2 controls with median depth >=
0.5 d_t, or corr_psf < 0.3); ON_TARGET (corr_psf >= 0.7, ratio_peak >= 0.75, and controls absent or
within 0.25 d_t of zero); UNCLEAR otherwise.

Reported but not used in any label: the raw 3x3 depth without background subtraction, the background
level in and out of each window, and the background change expressed as an aperture depth.

## Gate and overall outcome (`gapvet.overall_gap`)

Gate CONTROLS_OK only if S91_negative is REPRO_FAIL and S91_positive is ON_TARGET.

- **UNINTERPRETED**: gate failed; labels are reported, not interpreted.
- **CANDIDATE_OCCULTATION**: an edge is ON_TARGET and the reference edge is not. We would then report
  a candidate (not confirmed) second occultation with its implied periods (`gapvet.implied_periods`,
  checked against `results/v0.1.0/allowed_periods_all.csv`), and ask for independent photometry
  (SPOC/QLP/eleanor) before any stronger claim.
- **EDGE_AMBIGUOUS**: an edge is ON_TARGET but so is the reference edge, so an on-target edge effect
  cannot be told apart from an occultation. The feature stays open.
- **GAP_EDGE_SYSTEMATIC**: both edges SYSTEMATIC; the feature is closed as an artefact.
- **MIXED**: anything else.

A failed download is retried as a new job version without changing these rules.
