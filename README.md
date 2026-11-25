# epic2043-second-occultation

Did the young M dwarf **EPIC 204376071** (TIC 9855014, Upper Scorpius) go dark again?

In K2 Campaign 15 (September 2017) something blocked about 80% of its light for a day
([Rappaport et al. 2019](https://arxiv.org/abs/1902.08152)). It was seen once, the period is
unknown (only P >~ 79 d), and the discoverers hoped TESS or LSST would catch a repeat. This repo
is an open, pre-registered test: reproduce the discoverers' K2 result first, then search the
public ZTF (2018-2025) and TESS Sector 91 (2025) data for a second occultation and say which
periods from 70 to 2000 days are ruled out.

- `PREREGISTRATION.md`: rules fixed on 2026-11-25 before the TESS data and scans were computed.
- `occ.py`: core (stdlib; tested by `test_occ.py`). `io_k2.py`: K2 light curves from MAST.
  `job.py`: the full run. `fetch_deps.py`: fetches `io_tess.py` unchanged from
  munimtechnologies/epic2202-second-eclipse at commit 9dfda1bf.
- `notes/scoop-check-2026-11-25.md`: what was searched to check nobody did this first.

Run: `pip install numpy astropy && python -m unittest -v test_occ && python job.py --data-dir data --out-dir out`.

By MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name; no human
expert has checked it yet. Code: Apache-2.0. Results and text: CC BY 4.0.
