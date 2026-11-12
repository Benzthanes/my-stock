"""
Unit tests for src/valuation.py
Asserts mathematical accuracy, model categorization, ETF NAV tracking,
and graceful fallbacks.
"""

import unittest
from src.valuation import get_valuation, get_all_valuations


class TestValuationEngine(unittest.TestCase):
    def test_bac_banking_model(self):
        val = get_valuation("BAC", current_price=50.00)
        self.assertEqual(val["ticker"], "BAC")
        self.assertEqual(val["fair_price"], 57.50)
        self.assertAlmostEqual(val["upside_pct"], 15.00, places=1)
        self.assertEqual(val["status"], "UNDERVALUED")
        self.assertIn("1.385x", val["math_details"]["formula"])
        self.assertEqual(len(val["pillars"]), 3)

    def test_nvda_blended_growth_model(self):
        val = get_valuation("NVDA", current_price=200.00)
        self.assertEqual(val["ticker"], "NVDA")
        self.assertEqual(val["fair_price"], 280.00)
        self.assertAlmostEqual(val["upside_pct"], 40.00, places=1)
        self.assertEqual(val["status"], "UNDERVALUED")
        self.assertIn("Blended Model", val["math_details"]["formula"])

    def test_etf_nav_tracking(self):
        # VOO tracking test
        val_voo = get_valuation("VOO", current_price=698.35)
        self.assertEqual(val_voo["ticker"], "VOO")
        self.assertEqual(val_voo["fair_price"], 698.35)
        self.assertEqual(val_voo["upside_pct"], 0.0)
        self.assertEqual(val_voo["status"], "FAIR")
        self.assertIn("NAV Tracking", val_voo["status_label"])

        # QQQI tracking test
        val_qqqi = get_valuation("QQQI", current_price=51.77)
        self.assertEqual(val_qqqi["ticker"], "QQQI")
        self.assertEqual(val_qqqi["fair_price"], 51.77)
        self.assertEqual(val_qqqi["upside_pct"], 0.0)
        self.assertEqual(val_qqqi["status"], "FAIR")

    def test_nok_turnaround_currency_conversion(self):
        val = get_valuation("NOK", current_price=10.00)
        self.assertEqual(val["ticker"], "NOK")
        self.assertEqual(val["fair_price"], 11.50)
        self.assertAlmostEqual(val["upside_pct"], 15.00, places=1)
        self.assertIn("EUR to USD", val["primary_model"])

    def test_unrated_ticker_fallback(self):
        val = get_valuation("XYZ_UNKNOWN", current_price=123.45)
        self.assertEqual(val["ticker"], "XYZ_UNKNOWN")
        self.assertEqual(val["fair_price"], 123.45)
        self.assertEqual(val["upside_pct"], 0.0)
        self.assertEqual(val["status"], "SPECULATIVE")
        self.assertIn("อยู่ระหว่างประเมิน", val["status_label"])
        self.assertIsInstance(val["pillars"], list)

    def test_get_all_valuations(self):
        meta = {
            "BAC": {"price": 50.00},
            "NVDA": {"price": 200.00},
            "VOO": {"price": 698.35},
        }
        res = get_all_valuations(["BAC", "NVDA", "VOO"], meta)
        self.assertIn("BAC", res)
        self.assertIn("NVDA", res)
        self.assertIn("VOO", res)
        self.assertEqual(res["BAC"]["fair_price"], 57.50)
        self.assertEqual(res["NVDA"]["fair_price"], 280.00)
        self.assertEqual(res["VOO"]["fair_price"], 698.35)


if __name__ == "__main__":
    unittest.main()
