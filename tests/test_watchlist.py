"""
Tests for Watchlist Engine & Fibonacci Support Analysis (src/watchlist.py).
Asserts classification boundaries, data integrity, and fallback rendering when network is unreachable.
"""

import json
import os
import shutil
import tempfile
import unittest
import urllib.error
import zoneinfo
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from src.watchlist import (
    SOURCE_AUTHOR,
    SOURCE_UPDATED,
    WATCHLIST_STOCKS,
    analyze_watchlist,
    classify_support_distance,
    generate_watchlist_html,
    generate_watchlist_page,
    get_us_market_session,
)


class TestWatchlist(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.old_env = os.environ.get("FILTER_STOCK_DATA_DIR")
        os.environ["FILTER_STOCK_DATA_DIR"] = self.temp_dir

        # Setup mock portfolio.json in temp_dir
        mock_port = {
            "portfolio_name": "Test Port",
            "holdings": [
                {"ticker": "GOOGL", "shares": 10},
                {"ticker": "VRT", "shares": 5},
            ],
        }
        (Path(self.temp_dir) / "portfolio.json").write_text(json.dumps(mock_port), encoding="utf-8")

    def tearDown(self):
        if self.old_env is not None:
            os.environ["FILTER_STOCK_DATA_DIR"] = self.old_env
        else:
            os.environ.pop("FILTER_STOCK_DATA_DIR", None)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_watchlist_stocks_data_integrity(self):
        """Assert stocks in watchlist, support values, and self-calculated source integrity."""
        self.assertEqual(len(WATCHLIST_STOCKS), 42)
        self.assertEqual(SOURCE_AUTHOR, "คำนวณเอง")
        self.assertEqual(SOURCE_UPDATED, "2026-11-20")

        groups = {}
        for s in WATCHLIST_STOCKS:
            g = s["group"]
            groups.setdefault(g, []).append(s)
            self.assertGreater(s["support"], 0)
            self.assertTrue(s["ticker"].isupper())

        self.assertEqual(len(groups), 14)
        IMAGE_STOCKS_PER_GROUP = {
            "Space": 3, "Drones": 2, "Nuclear": 1, "Photonics": 2, "CPU Bottleneck": 3,
            "Physical AI": 3, "AI Power": 2, "AI Silicon": 4, "AI Applications": 3,
            "AI Connectivity": 4, "Midterm 2026": 0, "ETF Plan 2026-11": 0, "Bigtech Dip 2026-11": 0,
            "Retail Scale": 0,
        }
        removed = {
            "CIFR", "INTC", "LITE", "OKLO", "VPG", "IREN", "LEU", "ONDS", "UUUU", "ASTS", "MRCY", "AAOI",
            "ON", "NVTS", "QBTS", "RGTI", "INFQ", "IONQ", "DOCN", "SNOW", "FSLR", "DVA", "FIVE"
        }
        self.assertFalse(removed & {s["ticker"] for s in WATCHLIST_STOCKS})
        for g, stocks in groups.items():
            from_image = [x for x in stocks if not x.get("source")]
            expected = IMAGE_STOCKS_PER_GROUP[g]
            self.assertEqual(len(from_image), expected, f"Group {g} should have exactly {expected} image stocks")
        self.assertEqual([x["ticker"] for x in groups["Midterm 2026"]], ["ENSG", "OLLI"])

        # Spot check specific values from shay_fibo_support_2026-10-17.md and additions
        stock_map = {s["ticker"]: s for s in WATCHLIST_STOCKS}
        self.assertEqual(stock_map["RKLB"]["support"], 50.0)
        self.assertEqual(stock_map["COHR"]["support"], 224.0)
        self.assertEqual(stock_map["AEHR"]["support"], 57.0)
        self.assertEqual(stock_map["ADI"]["support"], 363.0)
        self.assertEqual(stock_map["MPWR"]["support"], 1100.0)
        self.assertEqual(stock_map["TXN"]["support"], 262.0)
        self.assertEqual(stock_map["SPCX"]["support"], 115.0)
        self.assertEqual(stock_map["SPCX"]["group"], "Space")
        self.assertEqual(
            [x["ticker"] for x in WATCHLIST_STOCKS if x.get("source")],
            ["SPCX", "ADI", "MPWR", "TXN", "NBIS", "ANT", "ENSG", "OLLI", "QQQM", "SOXQ", "GPIQ", "NFLX", "LRCX", "COST", "WMT"],
        )
        self.assertEqual(stock_map["ENSG"]["support"], 181.68)
        self.assertEqual(
            [(x["ticker"], x["support"]) for x in groups["ETF Plan 2026-11"]],
            [("QQQM", 251.0), ("SOXQ", 63.0), ("GPIQ", 48.0)],
        )
        self.assertEqual(
            [(x["ticker"], x["support"]) for x in groups["Bigtech Dip 2026-11"]],
            [("NFLX", 59.58), ("LRCX", 161.03)],
        )
        self.assertEqual(stock_map["GEV"]["support"], 678.0)
        self.assertEqual(stock_map["ASML"]["support"], 1637.0)
        self.assertEqual(stock_map["NOW"]["support"], 124.0)

    def test_classify_support_distance_exact_values(self):
        """Assert exact classification for -0.7%, +4.5%, +7.4%, boundaries, and None."""
        # 1. Negative diff (-0.7%) -> Group A (ต่ำกว่าแนวรับ)
        code_a, label_a = classify_support_distance(-0.7)
        self.assertEqual(code_a, "A")
        self.assertEqual(label_a, "(ก) ต่ำกว่าแนวรับ")

        # 2. 0 to 5% diff (+4.5%) -> Group B (0-5% เหนือแนวรับ)
        code_b, label_b = classify_support_distance(4.5)
        self.assertEqual(code_b, "B")
        self.assertEqual(label_b, "(ข) 0-5% เหนือแนวรับ")

        # 3. > 5% diff (+7.4%) -> Group C (เกิน 5%)
        code_c, label_c = classify_support_distance(7.4)
        self.assertEqual(code_c, "C")
        self.assertEqual(label_c, "(ค) เกิน 5%")

        # Boundary checks
        self.assertEqual(classify_support_distance(-0.0001)[0], "A")
        self.assertEqual(classify_support_distance(0.0)[0], "B")
        self.assertEqual(classify_support_distance(5.0)[0], "B")
        self.assertEqual(classify_support_distance(5.0001)[0], "C")
        self.assertEqual(classify_support_distance(None)[0], "unknown")

    def test_analyze_watchlist_with_mocked_quotes(self):
        """Assert % diff calculation, status assignment, portfolio tagging, and sorting."""
        # Mock quotes for a few sample stocks
        mock_quotes = {
            # COHR: support 224.0, price 222.43 -> diff -1.57 (-0.7%)
            "COHR": {"close": 222.43, "premarket_close": None, "postmarket_close": None, "exchange": "NYSE", "description": "Coherent Corp"},
            # ADI: support 363.0, price 379.335 -> diff +16.335 (+4.5%)
            "ADI": {"close": 379.335, "premarket_close": None, "postmarket_close": None, "exchange": "NASDAQ", "description": "Analog Devices"},
            # TXN: support 262.0, price 281.388 -> diff +19.388 (+7.4%)
            "TXN": {"close": 281.388, "premarket_close": None, "postmarket_close": None, "exchange": "NASDAQ", "description": "Texas Instruments"},
            # GOOGL: in portfolio
            "GOOGL": {"close": 283.82, "premarket_close": 281.85, "postmarket_close": None, "exchange": "NASDAQ", "description": "Alphabet Inc"},
        }

        result = analyze_watchlist(price_data=mock_quotes, session="premarket")
        self.assertEqual(result["total_count"], 42)
        self.assertEqual(result["portfolio_count"], 2)  # GOOGL and VRT in portfolio.json

        item_map = {it["ticker"]: it for it in result["items"]}

        # Check COHR (-0.7%)
        cohr = item_map["COHR"]
        self.assertEqual(cohr["status_code"], "A")
        self.assertAlmostEqual(cohr["pct_diff"], -0.7, places=1)

        # Check ADI (+4.5%)
        adi_item = item_map["ADI"]
        self.assertEqual(adi_item["status_code"], "B")
        self.assertAlmostEqual(adi_item["pct_diff"], 4.5, places=1)

        # Check TXN (+7.4%)
        txn_item = item_map["TXN"]
        self.assertEqual(txn_item["status_code"], "C")
        self.assertAlmostEqual(txn_item["pct_diff"], 7.4, places=1)

        # Check GOOGL (in portfolio and premarket priority)
        googl = item_map["GOOGL"]
        self.assertTrue(googl["in_portfolio"])
        self.assertEqual(googl["effective_price"], 281.85)
        self.assertEqual(googl["price_type"], "Premarket")

        # Check sorting: lowest pct_diff comes first
        valid_items = [it for it in result["items"] if it["pct_diff"] is not None]
        for i in range(len(valid_items) - 1):
            self.assertLessEqual(valid_items[i]["pct_diff"], valid_items[i + 1]["pct_diff"])

    @patch("urllib.request.urlopen")
    def test_page_generation_when_http_fetch_fails(self, mock_urlopen):
        """When network fetch fails, generate_watchlist_page must succeed and show alert banner."""
        mock_urlopen.side_effect = urllib.error.URLError("Network access blocked in tests")

        reports_temp = Path(self.temp_dir) / "reports"
        reports_temp.mkdir(parents=True, exist_ok=True)

        out_path = generate_watchlist_page(reports_dir=reports_temp)
        self.assertTrue(out_path.exists())
        self.assertTrue(out_path.is_file())

        content = out_path.read_text(encoding="utf-8")
        # Assert alert banner is present
        self.assertIn("ไม่สามารถดึงราคาล่าสุดจาก TradingView Scanner API ได้", content)
        # Assert disclaimer box is present
        self.assertIn("ข้อจำกัดและคำเตือนสำคัญ (Risk Disclaimer)", content)
        self.assertIn("แนวรับ Fibo ยังไม่ผ่าน backtest", content)
        self.assertIn("สภาพคล่องช่วง Premarket ต่ำ", content)
        # Assert nav bar is present
        self.assertIn('aria-label="รายงาน"', content)
        self.assertIn("หุ้นที่สนใจ", content)
        # Assert all 46 tickers are in the generated table
        for s in WATCHLIST_STOCKS:
            self.assertIn(f">{s['ticker']}<", content)

    def test_watchlist_valuation_integration(self):
        """Assert that analyze_watchlist integrates valuation data and renders Fair Value in HTML."""
        mock_quotes = {
            "NVDA": {"close": 150.0, "premarket_close": None, "postmarket_close": None, "exchange": "NASDAQ", "description": "NVIDIA Corp"},
            "GOOGL": {"close": 250.0, "premarket_close": None, "postmarket_close": None, "exchange": "NASDAQ", "description": "Alphabet Inc"},
        }
        res = analyze_watchlist(price_data=mock_quotes)
        item_map = {it["ticker"]: it for it in res["items"]}

        # NVDA fair price is computed by the 3-stage FCFF DCF ($291.28)
        nvda = item_map["NVDA"]
        self.assertIn("valuation", nvda)
        self.assertEqual(nvda["fair_price"], 291.28)
        self.assertEqual(nvda["val_status"], "UNDERVALUED")
        self.assertAlmostEqual(nvda["val_upside"], 94.19, places=1)

        # GOOGL is computed by the revenue-driven DCF ($308.23 fair price)
        googl = item_map["GOOGL"]
        self.assertEqual(googl["fair_price"], 308.23)
        self.assertEqual(googl["val_status"], "UNDERVALUED")

        # HTML generation includes valuation elements
        html = generate_watchlist_html(res, reports_dir=Path(self.temp_dir) / "reports")
        self.assertIn("card-val-box", html)
        self.assertIn("Intrinsic Fair Value", html)
        self.assertIn("มูลค่าเหมาะสม (Fair Value)", html)
        self.assertIn("pill-undervalued", html)
        self.assertIn("data-val-status", html)

    def test_session_determination(self):
        """Test get_us_market_session across various days and times in US Eastern Time."""
        ny_tz = zoneinfo.ZoneInfo("America/New_York")
        # Friday 03:59 ET -> closed
        self.assertEqual(get_us_market_session(datetime(2026, 11, 20, 3, 59, tzinfo=ny_tz)), "closed")
        # Friday 04:00 ET -> premarket
        self.assertEqual(get_us_market_session(datetime(2026, 11, 20, 4, 0, tzinfo=ny_tz)), "premarket")
        # Friday 09:29 ET -> premarket
        self.assertEqual(get_us_market_session(datetime(2026, 11, 20, 9, 29, tzinfo=ny_tz)), "premarket")
        # Friday 09:30 ET -> regular
        self.assertEqual(get_us_market_session(datetime(2026, 11, 20, 9, 30, tzinfo=ny_tz)), "regular")
        # Friday 15:59 ET -> regular
        self.assertEqual(get_us_market_session(datetime(2026, 11, 20, 15, 59, tzinfo=ny_tz)), "regular")
        # Friday 16:00 ET -> postmarket
        self.assertEqual(get_us_market_session(datetime(2026, 11, 20, 16, 0, tzinfo=ny_tz)), "postmarket")
        # Friday 19:59 ET -> postmarket
        self.assertEqual(get_us_market_session(datetime(2026, 11, 20, 19, 59, tzinfo=ny_tz)), "postmarket")
        # Friday 20:00 ET -> closed
        self.assertEqual(get_us_market_session(datetime(2026, 11, 20, 20, 0, tzinfo=ny_tz)), "closed")
        # Saturday -> closed
        self.assertEqual(get_us_market_session(datetime(2026, 11, 21, 12, 0, tzinfo=ny_tz)), "closed")
        # Sunday -> closed
        self.assertEqual(get_us_market_session(datetime(2026, 11, 22, 12, 0, tzinfo=ny_tz)), "closed")

    def test_analyze_watchlist_sessions(self):
        """Assert session-specific price selection and badge formatting."""
        mock_quotes = {
            "NVDA": {
                "close": 145.98,
                "change": -3.30,
                "premarket_close": 152.91,
                "premarket_change": 1.29,
                "postmarket_close": 144.67,
                "postmarket_change": -0.90,
                "exchange": "NASDAQ",
                "description": "NVIDIA Corp",
            },
            "ANT": {
                "close": 97.17,
                "change": None,
                "premarket_close": None,
                "premarket_change": None,
                "postmarket_close": 92.60,
                "postmarket_change": -4.70,
                "exchange": "NASDAQ",
                "description": "Anthropic",
            },
        }

        # 1. Closed session: must pick close price 145.98, NOT stale premarket 152.91
        res_closed = analyze_watchlist(price_data=mock_quotes, session="closed")
        item_map_closed = {it["ticker"]: it for it in res_closed["items"]}
        nvda_closed = item_map_closed["NVDA"]
        self.assertEqual(nvda_closed["effective_price"], 145.98)
        self.assertEqual(nvda_closed["price_type"], "ราคาปิด (Close)")
        self.assertEqual(nvda_closed["card_lbl"], "ราคาปิดล่าสุด")
        self.assertIn("Close", nvda_closed["price_sub"])
        self.assertIn("Post", nvda_closed["price_sub"])
        self.assertIn("144.67", nvda_closed["price_sub"])

        # 2. Regular session: must pick live/regular close
        res_reg = analyze_watchlist(price_data=mock_quotes, session="regular")
        item_map_reg = {it["ticker"]: it for it in res_reg["items"]}
        nvda_reg = item_map_reg["NVDA"]
        self.assertEqual(nvda_reg["effective_price"], 145.98)
        self.assertEqual(nvda_reg["price_type"], "ตลาดสด (Live)")
        self.assertEqual(nvda_reg["card_lbl"], "ราคาตลาดสด")
        self.assertIn("Live", nvda_reg["price_sub"])

        # 3. Premarket session: NVDA has premarket 152.91 (+1.29%)
        res_pre = analyze_watchlist(price_data=mock_quotes, session="premarket")
        item_map_pre = {it["ticker"]: it for it in res_pre["items"]}
        nvda_pre = item_map_pre["NVDA"]
        self.assertEqual(nvda_pre["effective_price"], 152.91)
        self.assertEqual(nvda_pre["price_type"], "Premarket")
        self.assertEqual(nvda_pre["card_lbl"], "ราคา Premarket")
        self.assertIn("+1.29%", nvda_pre["price_sub"])
        self.assertIn("ปิด $145.98", nvda_pre["price_sub"])

        # ANT has no premarket: cleanly falls back to close 97.17
        ant_pre = item_map_pre["ANT"]
        self.assertEqual(ant_pre["effective_price"], 97.17)
        self.assertEqual(ant_pre["price_type"], "ราคาปิด (Close)")
        self.assertEqual(ant_pre["card_lbl"], "ราคาปิดล่าสุด")
        self.assertIn("Close", ant_pre["price_sub"])
        self.assertIn("รอ Pre", ant_pre["price_sub"])

        # 4. Postmarket session: NVDA has postmarket 144.67 (-0.90%)
        res_post = analyze_watchlist(price_data=mock_quotes, session="postmarket")
        item_map_post = {it["ticker"]: it for it in res_post["items"]}
        nvda_post = item_map_post["NVDA"]
        self.assertEqual(nvda_post["effective_price"], 144.67)
        self.assertEqual(nvda_post["price_type"], "Postmarket")
        self.assertEqual(nvda_post["card_lbl"], "ราคา Postmarket")
        self.assertIn("-0.90%", nvda_post["price_sub"])


if __name__ == "__main__":
    unittest.main()
