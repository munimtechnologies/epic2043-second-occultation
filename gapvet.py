# Copyright 2026 Munim, Inc.
# SPDX-License-Identifier: Apache-2.0
# Made with AI agents working in MV2's name.
"""Rules of the pixel-level test of the TESS Sector 91 gap-edge feature of EPIC 204376071
(AMENDMENT-2026-11-25-gapvet.md). Stdlib only; the per-event labels come from pixvet.py
(unchanged copy of munimtechnologies/epic2202-second-eclipse commit c9e0c5fa).
"""

RA, DEC = 241.042141, -22.579427
SECTOR = 91

# The two edges of the feature (times and widths fixed from results/v0.1.0/tess_s091_30min.csv).
EVENTS = [
    {"name": "S91_pregap", "sector": SECTOR, "t_mid": 2460800.350, "width": 0.06},
    {"name": "S91_postgap", "sector": SECTOR, "t_mid": 2460802.115, "width": 0.04},
]
# Reference: the first cadences after the sector's other long gap, which showed the same kind of
# edge deficit (0.603 in the first 30-min bin) with normal data before the gap.
REFERENCE = {"name": "S91_after_midgap", "sector": SECTOR, "t_mid": 2460788.125, "width": 0.03}
# Gate: a flat stretch of the same sector, without and with an injected 30% dip of the target.
CONTROLS = [
    {"name": "S91_negative", "sector": SECTOR, "t_mid": 2460796.700, "width": 0.06, "inject": 0.0},
    {"name": "S91_positive", "sector": SECTOR, "t_mid": 2460796.700, "width": 0.06, "inject": 0.30},
]

# K2 C15 event core measured by the main job (results/v0.1.0/results.json, core.lo / core.hi).
K2_CORE = (2458001.2554551377, 2458001.684533717)
P_MIN, P_MAX = 70.0, 2000.0


def overall_gap(gate, lab_pre, lab_post, lab_ref):
    """Pre-registered overall outcome.
    UNINTERPRETED: the control gate failed.
    EDGE_AMBIGUOUS: an edge is ON_TARGET but so is the reference edge (an on-target edge effect).
    CANDIDATE_OCCULTATION: an edge is ON_TARGET and the reference edge is not.
    GAP_EDGE_SYSTEMATIC: both edges SYSTEMATIC.
    MIXED: anything else."""
    if gate != "CONTROLS_OK":
        return "UNINTERPRETED"
    on = lab_pre == "ON_TARGET" or lab_post == "ON_TARGET"
    if on and lab_ref == "ON_TARGET":
        return "EDGE_AMBIGUOUS"
    if on:
        return "CANDIDATE_OCCULTATION"
    if lab_pre == "SYSTEMATIC" and lab_post == "SYSTEMATIC":
        return "GAP_EDGE_SYSTEMATIC"
    return "MIXED"


def implied_periods(gap_lo, gap_hi, core_lo=K2_CORE[0], core_hi=K2_CORE[1], p_min=P_MIN, p_max=P_MAX):
    """Period ranges for which the n-th repeat of the K2 core overlaps [gap_lo, gap_hi]:
    core_lo + nP <= gap_hi and core_hi + nP >= gap_lo. Returns [(n, P_lo, P_hi)] clipped to
    [p_min, p_max], for n = 1, 2, ... until the range falls below p_min."""
    out = []
    n = 1
    while True:
        lo = (gap_lo - core_hi) / n
        hi = (gap_hi - core_lo) / n
        if hi < p_min:
            break
        if lo <= p_max:
            out.append((n, max(lo, p_min), min(hi, p_max)))
        n += 1
    return out


def gap_edges(times, t_from, t_to, min_gap=0.5):
    """Longest run without cadences between t_from and t_to (sorted times): (last before, first after),
    or None if no gap longer than min_gap."""
    sel = [t for t in times if t_from <= t <= t_to]
    best = None
    for a, b in zip(sel, sel[1:]):
        if b - a >= min_gap and (best is None or b - a > best[1] - best[0]):
            best = (a, b)
    return best
