# epic2043-second-occultation

Did the young M dwarf **EPIC 204376071** (TIC 9855014, Upper Scorpius) go dark again?

In K2 Campaign 15 (September 2017) something blocked about 80% of its light for a day
([Rappaport et al. 2019](https://arxiv.org/abs/1902.08152)). It was seen once, the period is
unknown (only P >~ 79 d), and the discoverers hoped TESS or LSST would catch a repeat. This repo
is an open, pre-registered test: reproduce the discoverers' K2 result first, then search the
public ZTF (2018-2025) and TESS Sector 91 (2025) data for a second occultation and say which
periods from 70 to 2000 days are ruled out.

## Status (2026-11-28)

- **Graded** (`GRADING.md`, results in `results/v0.1.0/`): both gates passed (the K2 event and the
  authors' P >~ 79 d bound are reproduced). No second occultation meets the pre-registered rules in
  ZTF or TESS. With all data, 45.5% of periods from 70 to 2000 d are excluded, and 98.4% of 70-100 d.
- **Gap-edge flag settled** (`GRADING-gapvet.md`, results in `results/gapvet-v0.1.0/`): the
  pre-registered pixel test passed its controls (null window empty, injected 30% dip recovered at
  0.302). At both edges of the Sector 91 data gap the dip is not reproduced in the target's
  background-subtracted pixels (`REPRO_FAIL`), while the background rises 4 and 31 times above normal.
  Frozen overall label: `MIXED`; no `CANDIDATE_OCCULTATION`. The headline `NO_SECOND_EVENT` stands.

## Files

- `PREREGISTRATION.md`: rules fixed on 2026-11-25 before the TESS data and scans were computed.
- `occ.py`: core (stdlib; tested by `test_occ.py`). `io_k2.py`: K2 light curves from MAST.
  `job.py`: the full run. `fetch_deps.py`: fetches `io_tess.py` unchanged from
  munimtechnologies/epic2202-second-eclipse at commit 9dfda1bf.
- `GRADING.md`, `results/v0.1.0/`: the graded run.
- `AMENDMENT-2026-11-25-gapvet.md`, `gapvet.py`, `pixvet.py` (unchanged copy from
  epic2202-second-eclipse commit c9e0c5fa), `job_gapvet.py`, `test_gapvet.py`: the gap-edge pixel test;
  `GRADING-gapvet.md`, `results/gapvet-v0.1.0/`: its graded run.
- `notes/scoop-check-2026-11-25.md`: what was searched to check nobody did this first.

Run: `pip install numpy astropy && python -m unittest -v test_occ && python job.py --data-dir data --out-dir out`.
Pixel test: `python -m unittest -v test_gapvet && python job_gapvet.py --data-dir data --out-dir out`.

By MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name; no human
expert has checked it yet. Code: Apache-2.0. Results and text: CC BY 4.0.
