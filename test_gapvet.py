# Copyright 2026 Munim, Inc.
# SPDX-License-Identifier: Apache-2.0
# Made with AI agents working in MV2's name.
import unittest

import gapvet
import pixvet


class TestOverall(unittest.TestCase):
    def test_overall_gap(self):
        O = gapvet.overall_gap
        self.assertEqual(O("CONTROL_FAIL", "ON_TARGET", "ON_TARGET", "REPRO_FAIL"), "UNINTERPRETED")
        self.assertEqual(O("CONTROLS_OK", "ON_TARGET", "SYSTEMATIC", "SYSTEMATIC"), "CANDIDATE_OCCULTATION")
        self.assertEqual(O("CONTROLS_OK", "UNCLEAR", "ON_TARGET", "UNCLEAR"), "CANDIDATE_OCCULTATION")
        self.assertEqual(O("CONTROLS_OK", "ON_TARGET", "ON_TARGET", "ON_TARGET"), "EDGE_AMBIGUOUS")
        self.assertEqual(O("CONTROLS_OK", "SYSTEMATIC", "SYSTEMATIC", "ON_TARGET"), "GAP_EDGE_SYSTEMATIC")
        self.assertEqual(O("CONTROLS_OK", "SYSTEMATIC", "UNCLEAR", "SYSTEMATIC"), "MIXED")
        self.assertEqual(O("CONTROLS_OK", "REPRO_FAIL", "REPRO_FAIL", "REPRO_FAIL"), "MIXED")


class TestPeriods(unittest.TestCase):
    def test_implied_periods_simple(self):
        ip = gapvet.implied_periods(1000.0, 1001.0, 0.0, 0.0)
        self.assertEqual(len(ip), 14)
        self.assertEqual(ip[0], (1, 1000.0, 1001.0))
        self.assertEqual(ip[-1][0], 14)
        self.assertAlmostEqual(ip[-1][2], 1001.0 / 14, places=9)

    def test_implied_periods_clip(self):
        ip = gapvet.implied_periods(3000.0, 3001.0, 0.0, 0.0)
        self.assertEqual(ip[0][0], 2)
        self.assertAlmostEqual(ip[0][1], 1500.0, places=9)
        ip2 = gapvet.implied_periods(140.5, 141.5, 0.0, 0.0)
        # n=2 gives 70.25-70.75; n=1 gives 140.5-141.5; nothing below 70 kept
        self.assertEqual([x[0] for x in ip2], [1, 2])

    def test_implied_periods_real(self):
        ip = gapvet.implied_periods(2460800.37, 2460802.10)
        self.assertTrue(all(70.0 <= lo <= hi <= 2000.0 for _, lo, hi in ip))
        self.assertEqual(ip[0][0], 2)          # n=1 would be ~2800 d, beyond 2000 d


class TestGap(unittest.TestCase):
    def test_gap_edges(self):
        ts = [0.0, 0.1, 0.2, 2.0, 2.1, 5.0]
        self.assertEqual(gapvet.gap_edges(ts, 0.0, 3.0), (0.2, 2.0))
        self.assertEqual(gapvet.gap_edges(ts, 0.0, 6.0), (2.1, 5.0))
        self.assertIsNone(gapvet.gap_edges([0.0, 0.1, 0.2], 0.0, 1.0))


class TestWindows(unittest.TestCase):
    def test_pregap_window_one_sided(self):
        ev = gapvet.EVENTS[0]
        ts = [2460799.80 + k * 0.002315 for k in range(247)]   # data end ~2460800.3695
        ins, outs = pixvet.window_idx(ts, ev["t_mid"], ev["width"])
        self.assertGreaterEqual(len(ins), 3)
        self.assertGreaterEqual(len(outs), 10)
        self.assertTrue(all(ts[i] < ev["t_mid"] for i in outs))

    def test_postgap_window_one_sided(self):
        ev = gapvet.EVENTS[1]
        ts = [2460802.100 + k * 0.002315 for k in range(300)]
        ins, outs = pixvet.window_idx(ts, ev["t_mid"], ev["width"])
        self.assertGreaterEqual(len(ins), 3)
        self.assertGreaterEqual(len(outs), 10)
        self.assertTrue(all(ts[i] > ev["t_mid"] for i in outs))

    def test_names(self):
        names = [e["name"] for e in gapvet.EVENTS + [gapvet.REFERENCE] + gapvet.CONTROLS]
        self.assertEqual(len(names), len(set(names)))
        self.assertIn("S91_positive", names)
        self.assertIn("S91_negative", names)


class TestPixvetCopy(unittest.TestCase):
    def test_labels_unchanged(self):
        L = pixvet.label_event
        self.assertEqual(L(0.01, 0.9, 1.0, [0.0, 0.0]), "REPRO_FAIL")
        self.assertEqual(L(0.1, 0.9, 1.0, [0.0, 0.01, -0.01]), "ON_TARGET")
        self.assertEqual(L(0.1, 0.9, 1.0, [0.08, 0.06]), "SYSTEMATIC")
        self.assertEqual(L(0.1, 0.1, 1.0, [0.0, 0.0]), "SYSTEMATIC")
        self.assertEqual(L(0.1, 0.9, 0.5, [0.0, 0.0]), "UNCLEAR")
        self.assertEqual(pixvet.control_gate("ON_TARGET", "REPRO_FAIL"), "CONTROLS_OK")


if __name__ == "__main__":
    unittest.main()
