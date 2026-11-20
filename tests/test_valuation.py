"""
Unit tests for src/valuation.py
Asserts mathematical accuracy, model categorization, ETF NAV tracking,
and graceful fallbacks.
"""

import unittest
from src.valuation import (
    compute_fair_value,
    equity_value_per_listing,
    fcff_multistage,
    fcff_revenue_dcf,
    MODEL_CONFIGS,
    market_implied_growth,
    VALUATION_INPUTS,
    get_all_valuations,
    get_valuation,
    justified_pb,
    stable_firm_value,
)


class TestValuationEngine(unittest.TestCase):
    def test_bac_banking_model(self):
        val = get_valuation("BAC", current_price=50.00)
        self.assertEqual(val["ticker"], "BAC")
        # 1.384615 x BVPS 39.26 = 54.36
        self.assertEqual(val["fair_price"], 54.36)
        self.assertAlmostEqual(val["upside_pct"], 8.72, places=1)
        self.assertEqual(val["status"], "FAIR")
        self.assertEqual(val["fair_value_method"], "computed")
        self.assertIn("Justified P/B", val["math_details"]["formula"])
        self.assertEqual(len(val["pillars"]), 3)

    def test_nvda_blended_growth_model(self):
        val = get_valuation("NVDA", current_price=150.00)
        self.assertEqual(val["ticker"], "NVDA")
        self.assertEqual(val["fair_price"], 291.28)
        self.assertAlmostEqual(val["upside_pct"], 94.19, places=1)
        self.assertEqual(val["status"], "UNDERVALUED")
        self.assertEqual(val["fair_value_method"], "computed")
        self.assertIn("3-Stage FCFF DCF", val["math_details"]["formula"])

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
        val = get_valuation("NOK", current_price=7.00)
        self.assertEqual(val["ticker"], "NOK")
        # (EUR 23.519B operations + EUR 2.584B net cash) x 1.14 / 5.745378B shares
        self.assertEqual(val["fair_price"], 5.18)
        self.assertAlmostEqual(val["upside_pct"], -26.0, places=1)
        self.assertEqual(val["status"], "OVERVALUED")
        self.assertIn("Stable-Growth", val["primary_model"])

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
            "NVDA": {"price": 150.00},
            "VOO": {"price": 698.35},
        }
        res = get_all_valuations(["BAC", "NVDA", "VOO"], meta)
        self.assertIn("BAC", res)
        self.assertIn("NVDA", res)
        self.assertIn("VOO", res)
        self.assertEqual(res["BAC"]["fair_price"], 54.36)
        self.assertEqual(res["NVDA"]["fair_price"], 291.28)
        self.assertEqual(res["VOO"]["fair_price"], 698.35)


    def test_every_stock_is_computed(self):
        # ETFs track NAV. Every other ticker must come from a formula, not a typed-in price.
        stocks = [t for t, c in MODEL_CONFIGS.items() if c["model_type"] != "INDEX_ETF"]
        self.assertEqual(len(stocks), 47)
        for t in stocks:
            self.assertEqual(get_valuation(t, current_price=100.0)["fair_value_method"], "computed", t)

    def test_negative_equity_shows_zero_not_market_price(self):
        cfg = dict(VALUATION_INPUTS["RDW"], debt=50.0)
        try:
            VALUATION_INPUTS["RDW"] = cfg
            val = get_valuation("RDW", current_price=6.51)
        finally:
            del VALUATION_INPUTS["RDW"]
            from src.valuation import _register_revenue_dcf_inputs
            _register_revenue_dcf_inputs()
        self.assertEqual(val["fair_price"], 0.0)
        self.assertEqual(val["upside_pct"], -100.0)
        self.assertEqual(val["status"], "OVERVALUED")


class TestDamodaranMath(unittest.TestCase):
    def test_justified_pb(self):
        self.assertAlmostEqual(justified_pb(0.115, 0.025, 0.09), 0.09 / 0.065, places=12)
        with self.assertRaises(ValueError):
            justified_pb(0.115, 0.09, 0.09)

    def test_stable_firm_value(self):
        # 2.35 x 1.025 x 0.74 = 1.782475; x (1 - 0.025/0.12) = 1.4111260; / 0.06 = 23.518767
        self.assertAlmostEqual(stable_firm_value(2.35, 0.26, 0.025, 0.12, 0.085), 23.518767, places=5)

    def test_growth_adds_no_value_when_roic_equals_wacc(self):
        # Damodaran: ROIC = WACC means growth creates no value: EBIT0 x (1+g) / r for any g.
        for g in (0.0, 0.02, 0.04):
            self.assertAlmostEqual(stable_firm_value(100.0, 0.0, g, 0.10, 0.10), 100.0 * (1 + g) / 0.10, places=9)

    def test_fcff_multistage_one_year_hand_calc(self):
        # NOPAT1 = 110, FCFF1 = 110 x (1 - 0.1/0.5) = 88, PV = 80.
        # TV = 110 x 1.03 x (1 - 0.03/0.1) / 0.07 = 1133, PV = 1030. EV = 1110.
        r = fcff_multistage(100.0, 0.10, 0.50, 0.10, 0.03, 0.10, years_high=1, years_transition=0)
        self.assertAlmostEqual(r["pv_high"], 80.0, places=9)
        self.assertAlmostEqual(r["terminal_value"], 1133.0, places=9)
        self.assertAlmostEqual(r["pv_terminal"], 1030.0, places=9)
        self.assertAlmostEqual(r["enterprise_value"], 1110.0, places=9)

    def test_transition_ends_at_terminal_growth(self):
        r = fcff_multistage(100.0, 0.18, 0.75, 0.09, 0.035, 0.20)
        self.assertEqual(len(r["rows"]), 10)
        self.assertAlmostEqual(r["rows"][4]["growth"], 0.18, places=12)
        self.assertAlmostEqual(r["rows"][9]["growth"], 0.035, places=12)
        self.assertAlmostEqual(r["rows"][9]["roic"], 0.20, places=12)

    def test_terminal_reinvestment_lowers_value(self):
        high = fcff_multistage(100.0, 0.10, 0.50, 0.09, 0.035, 1e9, years_high=1, years_transition=0)
        low = fcff_multistage(100.0, 0.10, 0.50, 0.09, 0.035, 0.09, years_high=1, years_transition=0)
        self.assertAlmostEqual(low["terminal_value"] / high["terminal_value"], 1 - 0.035 / 0.09, places=6)

    def test_invalid_inputs_raise(self):
        with self.assertRaises(ValueError):
            fcff_multistage(100.0, 0.10, 0.50, 0.03, 0.035, 0.10)
        with self.assertRaises(ValueError):
            fcff_multistage(100.0, 0.10, 0.50, 0.09, 0.035, 0.03)

    def test_equity_value_per_listing(self):
        # (100 + 20 + 5 - 10) / 2 x 5 shares per ADR x 0.5 USD = 143.75
        self.assertAlmostEqual(equity_value_per_listing(100.0, 20.0, 10.0, 2.0, 5.0, 0.5, 5.0), 143.75, places=9)

    def test_computed_tickers(self):
        expected = {
            "NVDA": 291.28, "TSM": 413.18, "ASML": 1387.97, "BAC": 54.36, "NOK": 5.18,
            "GOOGL": 308.23, "SKHY": 144.79, "ANT": 77.60, "TSLA": 31.69, "RDW": 0.61, "SPCX": 68.75,
        }
        for t, fv in expected.items():
            self.assertAlmostEqual(compute_fair_value(t)["fair_price"], fv, places=2, msg=t)
        self.assertAlmostEqual(compute_fair_value("NVDA")["terminal_share"], 0.678, places=3)


    def test_market_implied_growth_reproduces_price(self):
        for t, price in (("TSLA", 374.41), ("NVDA", 145.98), ("SPCX", 138.43)):
            cfg = VALUATION_INPUTS[t]
            g = market_implied_growth(cfg, price)
            self.assertIsNotNone(g, t)
            self.assertAlmostEqual(compute_fair_value(t, dict(cfg, g_high=g))["fair_price"], price, places=4, msg=t)
        self.assertAlmostEqual(market_implied_growth(VALUATION_INPUTS["TSLA"], 374.41), 0.7936, places=3)
        self.assertIsNone(market_implied_growth(VALUATION_INPUTS["BAC"], 48.57))

    def test_revenue_dcf_hand_calc(self):
        # Year 1: revenue 110, margin 15%, NOPAT 16.5 x 0.75 = 12.375, reinvest 10 / 2 = 5, FCFF 7.375, PV 6.7045.
        # Year 2: growth fades to 3%, revenue 113.3, margin 20%, NOPAT 16.995, reinvest 1.65, FCFF 15.345, PV 12.6818.
        # TV = 113.3 x 1.03 x 0.20 x 0.75 x (1 - 0.03/0.10) / 0.07 = 175.0485, PV 144.668. EV = 164.0545.
        r = fcff_revenue_dcf(100, 0.10, 0.20, 0.10, 2.0, 0.25, 0.10, 0.03, 0.10,
                             years_high=1, years_transition=1, margin_years=2)
        self.assertAlmostEqual(r["rows"][0]["fcff"], 7.375, places=9)
        self.assertAlmostEqual(r["rows"][1]["fcff"], 15.345, places=9)
        self.assertAlmostEqual(r["terminal_value"], 175.0485, places=6)
        self.assertAlmostEqual(r["enterprise_value"], 164.054545, places=5)
        self.assertAlmostEqual(r["implied_roic_high"], 0.20 * 0.75 * 2.0, places=12)

    def test_revenue_dcf_fades_wacc_to_mature(self):
        # Year 2 discounts at 8%: disc = 1 / (1.10 x 1.08). TV = 17.50485 x 0.7 / 0.05 = 245.0679.
        r = fcff_revenue_dcf(100, 0.10, 0.20, 0.10, 2.0, 0.25, 0.10, 0.03, 0.10,
                             years_high=1, years_transition=1, margin_years=2, wacc_term=0.08)
        self.assertAlmostEqual(r["terminal_value"], 245.0679, places=6)
        self.assertAlmostEqual(r["enterprise_value"], 225.907323, places=5)

    def test_revenue_dcf_losses_pay_no_tax(self):
        r = fcff_revenue_dcf(100, -0.20, 0.10, 0.0, 2.0, 0.25, 0.10, 0.03, 0.10,
                             years_high=1, years_transition=1, margin_years=4)
        # Year 1 margin = -0.20 + 0.30 / 4 = -0.125, EBIT -12.5, no tax.
        self.assertAlmostEqual(r["rows"][0]["nopat"], -12.5, places=9)

    def test_revenue_dcf_invalid_inputs_raise(self):
        with self.assertRaises(ValueError):
            fcff_revenue_dcf(100, 0.1, 0.2, 0.1, 2.0, 0.25, 0.10, 0.03, 0.10, wacc_term=0.03)
        with self.assertRaises(ValueError):
            fcff_revenue_dcf(100, 0.1, 0.0, 0.1, 2.0, 0.25, 0.10, 0.03, 0.10)


class TestFetchValuationFundamentals(unittest.TestCase):
    def test_parse_snapshot_record(self):
        from scripts.fetch_valuation_fundamentals import parse

        def pts(key, vals, ccy="USD"):
            dates = ["2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30", "2026-09-30"][-len(vals):]
            return {"meta": {"type": [key]}, key: [
                {"asOfDate": d, "currencyCode": ccy, "reportedValue": {"raw": v}} for d, v in zip(dates, vals)]}

        raw = {"timeseries": {"result": [
            pts("quarterlyTotalRevenue", [10e9, 11e9, 12e9, 13e9, 15e9]),
            pts("quarterlyOperatingIncome", [1e9, 2e9, 3e9, 4e9, 5e9]),
            pts("quarterlyCashCashEquivalentsAndShortTermInvestments", [7e9]),
            pts("quarterlyTotalDebt", [2e9]),
            pts("quarterlyDilutedAverageShares", [1.0e9]),
            pts("quarterlyOrdinarySharesNumber", [0.98e9]),
            pts("quarterlyTaxRateForCalcs", [0.2]),
        ]}}
        r = parse("TEST", raw)
        self.assertAlmostEqual(r["revenue_ttm"], 51.0)  # 11 + 12 + 13 + 15
        self.assertAlmostEqual(r["ebit_ttm"], 14.0)  # 2 + 3 + 4 + 5
        self.assertAlmostEqual(r["revenue_growth_yoy_q"], 0.5)  # 15 / 10 - 1
        self.assertAlmostEqual(r["shares"], 1.0)  # larger of diluted and ordinary
        self.assertEqual(r["currency"], "USD")
        self.assertEqual(r["as_of"], "2026-09-30")


if __name__ == "__main__":
    unittest.main()
