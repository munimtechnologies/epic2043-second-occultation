# Pre-registration: did EPIC 204376071's deep occultation happen again?

Fixed on 2026-11-25, before the TESS data, the period scans or any grade were computed.
MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name. Apache-2.0.

## 1. The near miss

Rappaport et al. (2019, MNRAS 485, 2681; [arXiv:1902.08152](https://arxiv.org/abs/1902.08152))
found that the young Upper Scorpius M dwarf EPIC 204376071 (TIC 9855014; 0.16 Msun, 135 pc) was
dimmed by about 80% for about a day in K2 Campaign 15 (minimum near KBJD 3168.4 =
BJD 2458001.4 = 2017-09-04), with an egress twice as long as the ingress. The star was quiet
for the rest of C2 (2014) and C15 (2017). They proposed a dusty disk around an orbiting body,
or a transient dusty accretion event. From C2 alone they bounded any period at P >~ 79 d,
with allowed windows near 79, 85, 93, 101-103 and 111-114 d. They wrote that ground-based
monitoring of this V = 16.3 star was "not very likely", that TESS "may observe" it in an
extended mission, and that LSST would expect to see another dip.

Since then TESS observed it once (Sector 91, 2025) and ZTF imaged it about 150 nights in r and
180 in g (2018-2025). Our searches on 2026-11-25 (notes/scoop-check-2026-11-25.md) found no
paper, note or catalogue that reports a search for a second occultation, a period, or the
TESS Sector 91 light curve of this star. The only later paper on the star (Savanov 2023,
Astrophysics 66, 344) studies spots and flares in the K2 C15 data.

**Disclosure.** While scouting we looked at a short summary of the public ZTF light curve
(329 rows, two filters, no point more than 0.8 mag below its median). The ZTF part of this
test is therefore not blind. The TESS Sector 91 data and every period scan were not looked at.

## 2. Data (all public; fetched by job.py)

- K2 long-cadence light curves C2 and C15 from MAST (SAP flux; quality bits 1, 2, 4, 8, 32,
  128, 32768 and 1048576 dropped), each divided by 5-day bin medians.
- ZTF DR light curves from IRSA (catflags = 0, magerr <= 0.30; per-object median
  normalisation; sigma = max(0.921 magerr, robust scatter of the object)).
- TESS: every TESScut sector (expected: 91), 11x11 cutout, 3x3 aperture and peak pixel with
  local background (io_tess.py, pinned unchanged from munimtechnologies/epic2202-second-eclipse
  commit 9dfda1bf), divided by 5-day bin medians, 30-minute bins for vetoes. The target's
  share of the aperture flux is estimated from TIC Tmag 14.548 (15000 e-/s at Tmag 10, 75% of
  the PSF in 3x3) over the measured median aperture flux.

## 3. Gates (known answers first)

- **G1, K2 event.** The box search (section 5) must find the C15 event within 0.5 d of
  BJD 2458001.4 with depth >= 0.5, and nothing else in C2 or C15. Labels: K2_EVENT_RECOVERED,
  K2_EVENT_RECOVERED_PLUS_OTHERS (then each extra detection is shown and judged in the
  grading), K2_EVENT_MISSED, K2_UNAVAILABLE.
- **G2, the authors' bound.** The period scan on K2 data alone must give a smallest allowed
  period in 76-82 d and at least one allowed period in each of 77.5-80.5, 83.5-86.5,
  91.5-94.5, 99.5-104.5 and 109.5-115.5 d. Labels: BOUND_REPRODUCED / BOUND_DIFFERENT.
  A failed gate is reported first, with the results, and the article says so.

## 4. The event core and vetoes

- **Core.** In K2 C15 the job takes the lowest point within 1 d of BJD 2458001.4 and the
  contiguous run of points around it with flux <= 0.5 (a gap > 0.1 d ends the run). If that
  run is at least 0.2 d long it is the core; otherwise the core is BJD 2458001.4 +- 0.25 d.
- **Prediction.** For a trial period P, the core repeats at core + nP (n != 0).
- **Veto point.** A point inside a predicted core vetoes if its dip 1 - r is below 0.05 (K2),
  0.15 (ZTF) or 0.03 (TESS 30-min bins) and r - f_exp > 4 sigma, where f_exp is the flux the
  source would show in the core: 0.5 for K2 and ZTF, 1 - 0.5 x share for TESS (TESS is not used
  for vetoes if share < 0.2). It is a strong veto if r - f_exp > 10 sigma.
- **Excluded period.** One predicted core with two veto points, or one strong veto point.
  Exclusion therefore means "no repeat at least 50% deep through the whole core": a shallower
  or shorter repeat is not excluded.

## 5. Second-event search

- **K2 and TESS:** box search with widths 0.25, 0.5 and 0.75 d in 0.02 d steps; detection =
  depth >= 0.10 in the aperture, S/N >= 10, >= 60% of in-box cadences present, >= 10 points
  on each flank (0.05-1.5 d outside the box) with median within 0.02 of 1; detections within
  0.5 d merged. A TESS detection is strong if the peak-pixel depth is at least half the
  aperture depth.
- **ZTF:** dip point = depth >= 0.30 and >= 5 sigma; points within 1 d grouped; an event is
  strong with >= 2 dip points. Single dip points are listed for inspection only.
- **TESS injection-recovery:** a 1.0-d trapezoid (0.5-d flat bottom) of depth 0.5 x share,
  injected at 10 evenly spaced times; recovered if detected within 0.5 d.
- Every strong event is inspected by eye and in pixel data before any claim (lesson of the
  EPIC 220208795 test, where three flagged TESS events were scattered light). A strong event is
  only ever called a candidate.

## 6. Period scan and outcomes

- Trial periods 70-2000 d, geometric grid with at most 0.02 d drift of the farthest predicted
  core between steps. Three scans: K2 only (the authors' state; gate G2), all data, and ZTF +
  TESS only (what is new since 2019). Reported: excluded fraction overall and in bins
  70-80-90-100-125-150-200-300-400-500-700-1000-1500-2000 d, and the allowed period runs.
- **Headline:** SECOND_EVENT_CANDIDATE (any strong event in ZTF or TESS; then the implied
  periods with the K2 event and whether each survives all data), NO_SECOND_EVENT, or
  NO_NEW_DATA.
- Any strong candidate goes to a pre-registered follow-up (pixel-level vetting) before an
  article calls it more than a flagged dip.

## 7. Later amendments (dated, before the data are looked at)

- Gaia DR4 epoch photometry (2014-07 to 2020-01; release 2026-12-02) as a further veto set.
- Rubin/LSST public alerts if the star is in a public alert stream.

## 8. People to tell (after grading, with Sheehan's OK)

S. Rappaport, G. Zhou, A. Vanderburg, A. W. Mann, T. L. Jacobs, D. M. LaCourse and the other
authors of Rappaport et al. (2019); I. S. Savanov.
