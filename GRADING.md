# Grading of the EPIC 204376071 second-occultation test (job epic2043-occ-v1, v0.1.0)

Graded 2026-11-25 by AI agents working in MV2's name (MV2, Munim, Inc., mv2@munimtech.com), against
`PREREGISTRATION.md` (fixed 2026-11-25 before the TESS data and the period scans were computed). No
human expert has checked it yet. Job output: `results/v0.1.0/` (results.json, summary.md, stdout.txt
and the CSV files). The job ran on 2026-11-25 (exit 0, 79 s of analysis).

## 1. Pre-registered outcome

`NO_SECOND_EVENT`, G1 = `K2_EVENT_RECOVERED_PLUS_OTHERS`, G2 = `BOUND_REPRODUCED`,
excluded fraction of 70-2000 d: **0.455** with all data, 0.320 with K2 alone, 0.279 with ZTF + TESS alone.

## 2. Gate G1: the K2 event (passed, extra detections judged)

- The C15 event was found at BJD 2458001.53 (0.75-d box, depth 0.554, S/N 122). The measured core
  (flux <= 0.5) is BJD 2458001.255-2458001.685 (2017-09-04 18:07 to 2017-09-05 04:25 UTC, 0.43 d,
  minimum 0.207 at 2458001.398), consistent with Rappaport et al. (2019).
- The label carries `PLUS_OTHERS` because the box search also flagged seven other boxes (two in C2,
  five in C15). We inspected each in `results/v0.1.0/k2_c02_sap_norm.csv` and `k2_c15_sap_norm.csv`:
  - 2458002.05 (C15) is the event's own egress (flux climbs from 0.66 at 2458001.81 to 1.00 at 2458002.07).
  - 2456912.71 and 2456942.17 (C2) and 2457990.95, 2458053.69, 2458059.87 and 2458068.67 (C15) are each
    the bottom of a K2 roll sawtooth in the SAP flux: the flux slides from about 1.0 down to 0.71-0.82
    over about six hours and jumps back after a thruster firing. In the pipeline PDCSAP flux the same
    stretches stay within about 2% of 1 except for the last one or two cadences before a firing.
  - They are spacecraft-pointing systematics, not occultations. They cannot create false vetoes:
    a point only vetoes if it is less than 5% below normal, so sawtooth points make the K2 vetoes
    weaker, never stronger.
- Verdict: the K2 event is recovered and nothing else in K2 is astrophysical. G1 is treated as passed.

## 3. Gate G2: the authors' bound (passed)

With K2 alone the smallest allowed period is 78.87 d (pre-registered range 76-82 d), and every one of
the authors' windows (77.5-80.5, 83.5-86.5, 91.5-94.5, 99.5-104.5, 109.5-115.5 d) keeps allowed
periods. `BOUND_REPRODUCED`.

## 4. New data

- **ZTF** (2018-04 to 2025-08; 180 g and 149 r points, all used): 0 dip points. As disclosed in the
  pre-registration, this part was not blind.
- **TESS Sector 91** (2025-04-09 to 2025-05-07, 200-s FFI cutout, 8,447 good cadences): no detection.
  Injection-recovery of a 1-d, 50%-deep occultation: 6 of 7 covered injections recovered. The
  estimated target share of the 3x3 aperture is 1.19 (the code caps it at 1), so in-core flux is
  expected at 0.5, as for K2 and ZTF.

## 5. A flagged feature at a TESS data gap (not a pre-registered detection; under pixel check)

The deepest TESS box (BJD 2460800.34, depth 0.139, S/N 25.7) failed the flank rule because it sits at
the edge of a data gap. In `results/v0.1.0/tess_s091_30min.csv`:

| BJD (30-min bin) | relative flux | cadences |
|---|---|---|
| 2460800.287 | 0.946 | 9 |
| 2460800.329 | 0.868 | 9 |
| 2460800.350 | 0.609 | 9 |
| 2460800.366 | 0.189 | 5 |
| (no data for 1.74 d) | | |
| 2460802.104 | 0.302 | 5 |
| 2460802.120 | 0.829 | 9 |
| 2460802.141 | 1.027 | 9 |

Read at face value, the star would have faded by 80% on 2025-05-04 about 20:45 UTC and recovered on
2025-05-06 about 14:50 UTC, which would be a second occultation. We think this is unlikely, for
three reasons noted before any pixel analysis:

1. Both ramps sit exactly at the two edges of a data gap.
2. The same kind of edge deficit appears after the sector's other long gap: the first bin after it
   (BJD 2460788.121) is at 0.603, the next at 0.899 and then 1.057, although the data before that gap
   were normal.
3. The ramps take about an hour (0.95 to 0.19 in about 0.06 d; 0.30 to 1.03 in about 0.04 d). The
   K2 event's egress took about 0.26 d (0.66 at 2458001.81 to 1.00 at 2458002.07).

The feature is not used as a veto, and the period scan already treats the gap as unobserved, so it
changes no number in section 1. It is not ruled out either. A dated amendment,
`AMENDMENT-2026-11-25-gapvet.md`, fixes a pixel-level test (job `epic2043-gapvet-v1`) before any pixel
data are analysed. ZTF has no point inside the gap; its nearest points (2025-05-02 and 2025-05-08)
are normal.

## 6. What the new data rule out

| Periods | allowed, K2 only | allowed, all data |
|---|---|---|
| 70-100 d | 6.1% (3,137 of 51,669 trials) | 1.6% (836 of 51,669) |
| 100-200 d | 46.3% (46,451 of 100,410) | 23.1% (23,175 of 100,410) |
| 70-2000 d | 68.0% | 54.5% |

- The smallest allowed period with all data is 79.10 d. The authors' short windows survive only as
  narrow slivers: 79.10-79.17, 84.93-85.76, 92.30-93.54, 100.67-102.68 and 110.41-... d
  (`results/v0.1.0/allowed_periods_all.csv`).
- Exclusion means "no repeat at least 50% deep through the whole 0.43-d core"; a shallower or
  shorter repeat is not excluded.

## 7. Verdict

The pre-registered headline is `NO_SECOND_EVENT`: in 11 years of K2, ZTF and TESS data no second
occultation meets the rules, and 45.5% of periods from 70 to 2000 d are now excluded (98.4% of
70-100 d). One TESS gap-edge feature is flagged and goes to a pre-registered pixel test. No article
until that test has run.

## 8. People to tell (after the pixel test, with Sheehan's OK)

S. Rappaport, G. Zhou, A. Vanderburg, A. W. Mann, T. L. Jacobs, D. M. LaCourse and co-authors of
Rappaport et al. (2019, MNRAS 485, 2681; arXiv:1902.08152); I. S. Savanov.
