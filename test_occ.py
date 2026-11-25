# Copyright 2026 Munim, Inc.
# SPDX-License-Identifier: Apache-2.0
# Made with AI agents working in MV2's name.
"""Stdlib tests for the EPIC 204376071 second-occultation test (hand-traced values)."""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import occ  # noqa: E402


class TestBasics(unittest.TestCase):
    def test_scatter(self):
        self.assertAlmostEqual(occ.robust_scatter([1, 2, 3, 4, 100]), 1.4826, places=9)
        self.assertTrue(math.isnan(occ.robust_scatter([1.0])))

    def test_dates(self):
        self.assertEqual(occ.bjd_to_date(2451545.0), "2000-01-01 12:00")
        self.assertEqual(occ.bjd_to_date(2458001.5), "2017-09-05 00:00")
        self.assertAlmostEqual(occ.T_MIN_PUBLISHED, 2458001.4, places=6)

    def test_normalise(self):
        t = [float(k) for k in range(10)]
        self.assertEqual(occ.normalise_binned(t, [2.0] * 10), [1.0] * 10)
        r = occ.normalise_binned(t, [2.0] * 5 + [4.0] * 5)
        self.assertAlmostEqual(r[0], 1.0)
        self.assertAlmostEqual(r[4], 2.0 / 2.8)
        self.assertAlmostEqual(r[7], 1.0)
        self.assertAlmostEqual(r[9], 1.0)

    def test_bin_series(self):
        w = 1.0 / 48
        b = occ.bin_series([0.0, 0.01, w, 0.03], [1.0, 3.0, 5.0, 7.0], w)
        self.assertEqual(len(b), 2)
        self.assertAlmostEqual(b[0][0], 0.005)
        self.assertAlmostEqual(b[0][1], 2.0)
        self.assertEqual(b[0][2], 2)
        self.assertAlmostEqual(b[1][0], (w + 0.03) / 2)
        self.assertAlmostEqual(b[1][1], 6.0)


class TestCore(unittest.TestCase):
    def _series(self, half):
        T = 1000.0
        t = [T + k * 0.0204 for k in range(-20, 21)]
        r = [0.2 if abs(k) <= half else (0.6 if abs(k) == half + 1 else 1.0) for k in range(-20, 21)]
        return T, t, r

    def test_measured(self):
        T, t, r = self._series(5)
        m = occ.measure_core(t, r, t_guess=T)
        self.assertAlmostEqual(m["lo"], T - 0.102)
        self.assertAlmostEqual(m["hi"], T + 0.102)
        self.assertEqual(m["n"], 11)
        self.assertAlmostEqual(m["t_min"], T - 0.102)
        lo, hi, how = occ.choose_core(m)
        self.assertEqual(how, "measured")
        self.assertAlmostEqual(hi - lo, 0.204)

    def test_short_run_falls_back(self):
        T, t, r = self._series(2)
        m = occ.measure_core(t, r, t_guess=T)
        self.assertEqual(m["n"], 5)
        lo, hi, how = occ.choose_core(m)
        self.assertEqual(how, "default")
        self.assertAlmostEqual(lo, occ.T_MIN_PUBLISHED - 0.25)
        self.assertAlmostEqual(hi, occ.T_MIN_PUBLISHED + 0.25)

    def test_no_points_or_no_dip(self):
        self.assertIsNone(occ.measure_core([1.0, 2.0], [1.0, 1.0], t_guess=50.0))
        m = occ.measure_core([50.0, 50.1], [0.9, 0.95], t_guess=50.0)
        self.assertIsNone(m["lo"])
        self.assertEqual(occ.choose_core(m)[2], "default")
        self.assertEqual(occ.choose_core(None)[2], "default")


def _veto_points():
    return occ.Points([
        (100.0, 1.0, 0.01, "ztf", 0.5),   # capable, strong (0.5 > 10 x 0.01)
        (101.0, 0.80, 0.01, "ztf", 0.5),  # dip 0.2 >= 0.15: not capable
        (102.0, 1.0, 0.2, "ztf", 0.5),    # 0.5 < 4 x 0.2: not capable
        (103.0, 1.0, 0.1, "ztf", 0.5),    # capable, weak (0.5 > 0.4, not > 1.0)
    ])


class TestVeto(unittest.TestCase):
    def test_capable_and_strong(self):
        pts = _veto_points()
        self.assertEqual(pts.vt, [100.0, 103.0])
        self.assertEqual(occ.vetoes(pts, 99.0, 104.0), [(100.0, "ztf", True), (103.0, "ztf", False)])
        self.assertEqual(occ.vetoes(pts, 100.5, 102.9), [])

    def test_vetoed_rule(self):
        self.assertFalse(occ.vetoed([(103.0, "ztf", False)]))
        self.assertTrue(occ.vetoed([(103.0, "ztf", False), (103.1, "ztf", False)]))
        self.assertTrue(occ.vetoed([(100.0, "ztf", True)]))
        self.assertFalse(occ.vetoed([]))

    def test_tess_threshold(self):
        # TESS: dip must be < 0.03 to veto
        pts = occ.Points([(1.0, 0.98, 0.001, "tess", 0.8), (2.0, 0.965, 0.001, "tess", 0.8)])
        self.assertEqual(pts.vt, [1.0])

    def test_event_refs(self):
        core = (1000.0, 1000.5)
        self.assertEqual(occ.event_refs(100.0, core, 750.0, 1260.0), [-2, -1, 1, 2])
        self.assertEqual(occ.event_refs(100.0, core, 750.0, 1200.2), [-2, -1, 1, 2])
        self.assertEqual(occ.event_refs(100.0, core, 750.0, 1199.9), [-2, -1, 1])

    def test_trial(self):
        core = (1000.0, 1000.5)
        pts = occ.Points([(1100.25, 1.0, 0.01, "ztf", 0.5)])
        ex, inf = occ.trial(100.0, pts, core, 900.0, 1200.0)
        self.assertTrue(ex)
        self.assertEqual(inf["n"], 1)
        self.assertEqual(inf["by"], ["ztf"])
        self.assertFalse(occ.trial(100.3, pts, core, 900.0, 1200.0)[0])
        self.assertTrue(occ.trial(99.8, pts, core, 900.0, 1200.0)[0])

    def test_scan_and_fraction(self):
        core = (1000.0, 1000.5)
        pts = occ.Points([(1100.25, 1.0, 0.01, "ztf", 0.5)])
        grid = [99.0, 99.5, 100.0, 100.5]
        n_ex, runs = occ.scan(pts, grid, core, 900.0, 1200.0)
        self.assertEqual(n_ex, 1)
        self.assertEqual(runs, [[99.0, 99.5, 2], [100.5, 100.5, 1]])
        fr = occ.binned_fraction(grid, runs, [99.0, 100.0, 101.0])
        self.assertEqual(fr[0][2:], (2, 2, 1.0))
        self.assertEqual(fr[1][2:], (2, 1, 0.5))

    def test_grid(self):
        g = occ.period_grid(70.0, 71.0, 1000.0, 0.0, 1000.0, tol=0.02)
        self.assertEqual(g[0], 70.0)
        self.assertTrue(all(x <= 71.0 for x in g))
        self.assertTrue(705 <= len(g) <= 715)
        self.assertAlmostEqual(g[1] / g[0], 1.00002, places=12)


class TestBound(unittest.TestCase):
    def test_reproduced(self):
        runs = [[78.0, 79.5, 3], [84.0, 85.0, 2], [92.0, 93.0, 2], [100.0, 101.0, 2], [110.0, 111.0, 2]]
        b = occ.bound_check(runs)
        self.assertEqual(b["smallest_allowed"], 78.0)
        self.assertEqual(b["verdict"], "BOUND_REPRODUCED")

    def test_different(self):
        runs = [[70.0, 75.0, 10], [78.0, 79.5, 3], [84.0, 85.0, 2], [92.0, 93.0, 2], [100.0, 101.0, 2],
                [110.0, 111.0, 2]]
        b = occ.bound_check(runs)
        self.assertEqual(b["smallest_allowed"], 70.0)
        self.assertEqual(b["verdict"], "BOUND_DIFFERENT")
        runs2 = [[78.0, 79.5, 3], [84.0, 85.0, 2], [92.0, 93.0, 2], [100.0, 101.0, 2]]
        b2 = occ.bound_check(runs2)
        self.assertFalse(b2["windows"][4]["has_allowed"])
        self.assertEqual(b2["verdict"], "BOUND_DIFFERENT")
        self.assertEqual(occ.bound_check([])["verdict"], "BOUND_DIFFERENT")

    def test_periods_from_event(self):
        self.assertEqual(occ.periods_from_event(1300.0, 1000.0, 70.0, 2000.0),
                         [(1, 300.0), (2, 150.0), (3, 100.0), (4, 75.0)])
        self.assertEqual(occ.periods_from_event(700.0, 1000.0, 70.0, 200.0),
                         [(-2, 150.0), (-3, 100.0), (-4, 75.0)])


def _noisy_series(with_dip):
    t, r = [], []
    for k in range(500):
        tk = k * 0.02
        x = 1.0 + 0.01 * (((k * 7919) % 101) - 50) / 50.0
        if with_dip and abs(tk - 5.0) < 0.21:
            x = 0.5
        t.append(tk)
        r.append(x)
    return t, r


class TestSearch(unittest.TestCase):
    def test_box_finds_dip(self):
        t, r = _noisy_series(True)
        best, dets = occ.box_search(t, r, 0.02)
        self.assertEqual(len(dets), 1)
        self.assertLessEqual(abs(dets[0]["t_mid"] - 5.0), 0.15)
        self.assertGreaterEqual(dets[0]["depth"], 0.3)
        self.assertGreaterEqual(best["snr"], occ.BOX_MIN_SNR)

    def test_box_null(self):
        t, r = _noisy_series(False)
        _, dets = occ.box_search(t, r, 0.02)
        self.assertEqual(dets, [])

    def test_injected_dip_found(self):
        t, r = _noisy_series(False)
        _, dets = occ.box_search(t, occ.inject(t, r, 6.0, 0.3), 0.02)
        self.assertGreaterEqual(len(dets), 1)
        self.assertTrue(any(abs(d["t_mid"] - 6.0) <= 0.3 for d in dets))
        self.assertTrue(all(abs(d["t_mid"] - 6.0) <= 0.8 for d in dets))

    def test_inject_shape(self):
        out = occ.inject([0.0, 0.2, 0.3, 0.5, 0.6], [1.0] * 5, 0.0, 0.4)
        self.assertAlmostEqual(out[0], 0.6)
        self.assertAlmostEqual(out[1], 0.6)
        self.assertAlmostEqual(out[2], 0.68)
        self.assertAlmostEqual(out[3], 1.0)
        self.assertAlmostEqual(out[4], 1.0)

    def test_dips_and_groups(self):
        pts = occ.Points([(5.0, 0.6, 0.02, "ztf", 0.5), (6.0, 0.6, 0.1, "ztf", 0.5),
                          (7.0, 0.6, 0.02, "tess", 0.8)])
        d = occ.dip_points(pts)
        self.assertEqual([x[0] for x in d], [5.0])
        ev = occ.group_events([(10.0, 0.5, 0.05, "ztf"), (10.5, 0.4, 0.05, "ztf"), (13.0, 0.5, 0.05, "ztf")])
        self.assertEqual(len(ev), 2)
        self.assertAlmostEqual(ev[0]["t_mid"], 10.25)
        self.assertTrue(ev[0]["strong"])
        self.assertAlmostEqual(ev[0]["depth_max"], 0.6)
        self.assertFalse(ev[1]["strong"])


class TestTessAndZtf(unittest.TestCase):
    def test_share(self):
        f = occ.TESS_ZP_FLUX * 10 ** (-0.4 * (occ.TMAG - 10.0)) * occ.TESS_PSF_FRAC
        self.assertAlmostEqual(occ.tess_share(f / 0.4), 0.4, places=9)
        self.assertTrue(math.isnan(occ.tess_share(0.0)))
        self.assertAlmostEqual(occ.tess_fexp(0.4), 0.8)
        self.assertAlmostEqual(occ.tess_fexp(1.5), 0.5)
        self.assertIsNone(occ.tess_fexp(0.1))
        self.assertIsNone(occ.tess_fexp(float("nan")))

    def test_parse_ztf(self):
        lines = ["oid,hjd,mag,magerr,catflags,filtercode"]
        for k in range(9):
            lines.append("A,%.1f,17.0,0.02,0,zr" % (2458300.5 + k))
        lines.append("A,58310.5,18.0,0.02,0,zr")
        lines.append("A,2458320.5,17.0,0.02,4,zr")
        lines.append("A,2458321.5,17.0,0.5,0,zr")
        for k in range(3):
            lines.append("B,%.1f,15.0,0.01,0,zg" % (2458300.5 + k))
        pts, meta = occ.parse_ztf("\n".join(lines) + "\n")
        self.assertEqual(len(pts), 10)
        self.assertFalse(meta["oids"]["B"]["used"])
        last = [p for p in pts if p[1] < 0.5][0]
        self.assertAlmostEqual(last[0], 2458311.0)
        self.assertAlmostEqual(last[1], 10 ** -0.4, places=9)
        self.assertAlmostEqual(last[2], 0.921 * 0.02, places=9)
        self.assertEqual(last[3:], ("ztf", "A", "zr"))

    def test_headline(self):
        self.assertEqual(occ.headline("K2_EVENT_RECOVERED", [], 0), "NO_NEW_DATA")
        self.assertEqual(occ.headline("K2_EVENT_RECOVERED", [{"t_mid": 1}], 10), "SECOND_EVENT_CANDIDATE")
        self.assertEqual(occ.headline("K2_EVENT_RECOVERED", [], 10), "NO_SECOND_EVENT")


if __name__ == "__main__":
    unittest.main()
