"""Tests for agov.cost."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agov.cost import check_budget, estimate, estimate_batch, load_prices


class TestEstimate(unittest.TestCase):
    def test_balanced_call(self):
        result = estimate("balanced", 1000, 500)
        self.assertEqual(result["input_cost_usd"], 0.003)
        self.assertEqual(result["output_cost_usd"], 0.0075)
        self.assertEqual(result["total_cost_usd"], 0.0105)

    def test_unknown_model(self):
        with self.assertRaises(ValueError):
            estimate("no-such-model", 10, 10)

    def test_negative_tokens(self):
        with self.assertRaises(ValueError):
            estimate("balanced", -1, 0)

    def test_zero_tokens(self):
        result = estimate("efficient", 0, 0)
        self.assertEqual(result["total_cost_usd"], 0.0)


class TestBatch(unittest.TestCase):
    def test_batch_total_and_by_model(self):
        calls = [
            {"model": "balanced", "input_tokens": 1000, "output_tokens": 500,
             "label": "draft"},
            {"model": "efficient", "input_tokens": 2000, "output_tokens": 1000,
             "label": "classify"},
            {"model": "balanced", "input_tokens": 500, "output_tokens": 100,
             "label": "summarize"},
        ]
        result = estimate_batch(calls)
        self.assertEqual(len(result["calls"]), 3)
        self.assertEqual(result["calls"][0]["label"], "draft")
        self.assertAlmostEqual(result["total_usd"], 0.0105 + 0.003 + 0.003)
        self.assertEqual(result["by_model"]["balanced"], 0.0135)


class TestBudget(unittest.TestCase):
    def test_within_budget_no_warning(self):
        check = check_budget(5.0, 10.0)
        self.assertTrue(check["within_budget"])
        self.assertFalse(check["warning"])
        self.assertEqual(check["remaining_usd"], 5.0)

    def test_warning_at_80_percent(self):
        check = check_budget(8.5, 10.0)
        self.assertTrue(check["within_budget"])
        self.assertTrue(check["warning"])

    def test_over_budget(self):
        check = check_budget(12.0, 10.0)
        self.assertFalse(check["within_budget"])
        self.assertEqual(check["remaining_usd"], -2.0)

    def test_bad_budget(self):
        with self.assertRaises(ValueError):
            check_budget(1.0, 0)


class TestLoadPrices(unittest.TestCase):
    def test_custom_table_overrides_and_adds(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json",
                                         delete=False) as handle:
            json.dump({"balanced": {"input": 1.0, "output": 2.0},
                       "custom": {"input": 0.1, "output": 0.1}}, handle)
            path = handle.name
        try:
            prices = load_prices(path)
            self.assertEqual(prices["balanced"]["input"], 1.0)
            self.assertIn("flagship", prices)
            self.assertIn("custom", prices)
            result = estimate("custom", 1_000_000, 0, prices)
            self.assertEqual(result["total_cost_usd"], 0.1)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
