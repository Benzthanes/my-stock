#!/usr/bin/env python3
"""
Fetch the reported figures the fair value engine needs and save a reviewed snapshot.

For each ticker it reads the Yahoo Finance fundamentals-timeseries API and keeps
TTM revenue, TTM operating income (EBIT), latest-quarter revenue growth YoY, the
effective tax rate, cash and short-term investments, total debt, invested capital
and share count. Values are in the company's reporting currency, in billions.

The snapshot is written to src/valuation_fundamentals.json so reports and GitHub
Actions use the same reviewed numbers without network access. Rerun this after
each earnings season, review the diff, then commit.

Usage:
    python3 -m scripts.fetch_valuation_fundamentals              # dry run, prints the table
    python3 -m scripts.fetch_valuation_fundamentals --write      # writes the snapshot
    python3 -m scripts.fetch_valuation_fundamentals --tickers AMD,MU --write
"""

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.http import http_get

SNAPSHOT = Path(__file__).resolve().parent.parent / "src" / "valuation_fundamentals.json"
URL = ("https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/"
       "{t}?type={types}&period1={p1}&period2={p2}")
TYPES = [
    "quarterlyTotalRevenue",
    "quarterlyOperatingIncome",
    "trailingTotalRevenue",
    "trailingOperatingIncome",
    "quarterlyTaxRateForCalcs",
    "quarterlyCashCashEquivalentsAndShortTermInvestments",
    "quarterlyTotalDebt",
    "quarterlyInvestedCapital",
    "quarterlyDilutedAverageShares",
    "quarterlyOrdinarySharesNumber",
]
B = 1e9


def _series(raw: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    out: Dict[str, List[Dict[str, Any]]] = {}
    for item in raw.get("timeseries", {}).get("result", []):
        t = item.get("meta", {}).get("type", [None])[0]
        pts = [p for p in item.get(t, []) or [] if p and p.get("reportedValue")]
        out[t] = sorted(pts, key=lambda p: p["asOfDate"])
    return out


def _last(s: Dict[str, List[Dict[str, Any]]], key: str) -> Optional[Dict[str, Any]]:
    pts = s.get(key) or []
    return pts[-1] if pts else None


def _val(p: Optional[Dict[str, Any]]) -> Optional[float]:
    return None if p is None else float(p["reportedValue"]["raw"])


def parse(ticker: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    """Turn a raw timeseries payload into the snapshot record. Pure function."""
    s = _series(raw)
    q_rev = s.get("quarterlyTotalRevenue") or []
    q_op = s.get("quarterlyOperatingIncome") or []

    rev_ttm = _val(_last(s, "trailingTotalRevenue"))
    if rev_ttm is None and len(q_rev) >= 4:
        rev_ttm = sum(_val(p) for p in q_rev[-4:])
    ebit_ttm = _val(_last(s, "trailingOperatingIncome"))
    if ebit_ttm is None and len(q_op) >= 4:
        ebit_ttm = sum(_val(p) for p in q_op[-4:])

    growth = None
    if len(q_rev) >= 5 and _val(q_rev[-5]) and _val(q_rev[-5]) > 0:
        growth = _val(q_rev[-1]) / _val(q_rev[-5]) - 1.0

    diluted = _val(_last(s, "quarterlyDilutedAverageShares"))
    ordinary = _val(_last(s, "quarterlyOrdinarySharesNumber"))
    shares = max(x for x in (diluted, ordinary, 0.0) if x is not None)

    currency = None
    as_of = None
    for key in ("quarterlyTotalRevenue", "trailingTotalRevenue", "quarterlyCashCashEquivalentsAndShortTermInvestments"):
        p = _last(s, key)
        if p:
            currency = currency or p.get("currencyCode")
            as_of = max(as_of or "", p["asOfDate"])

    def b(x: Optional[float]) -> Optional[float]:
        return None if x is None else round(x / B, 6)

    return {
        "currency": currency,
        "as_of": as_of,
        "revenue_ttm": b(rev_ttm),
        "ebit_ttm": b(ebit_ttm),
        "revenue_growth_yoy_q": None if growth is None else round(growth, 4),
        "tax_rate": _val(_last(s, "quarterlyTaxRateForCalcs")),
        "cash": b(_val(_last(s, "quarterlyCashCashEquivalentsAndShortTermInvestments"))) or 0.0,
        "debt": b(_val(_last(s, "quarterlyTotalDebt"))) or 0.0,
        "invested_capital": b(_val(_last(s, "quarterlyInvestedCapital"))),
        "shares": b(shares) if shares else None,
        "shares_diluted_avg": b(diluted),
        "shares_ordinary": b(ordinary),
    }


def fetch(ticker: str) -> Dict[str, Any]:
    now = int(time.time())
    url = URL.format(t=ticker.replace(".", "-"), types=",".join(TYPES), p1=now - 3 * 365 * 86400, p2=now)
    return json.loads(http_get(url, timeout=20).decode("utf-8"))


def default_tickers() -> List[str]:
    from src.valuation import MODEL_CONFIGS
    return [t for t, c in MODEL_CONFIGS.items() if c.get("model_type") != "INDEX_ETF"]


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Fetch reported figures for the fair value engine.")
    ap.add_argument("--tickers", help="Comma-separated tickers. Default is every non-ETF ticker in MODEL_CONFIGS.")
    ap.add_argument("--write", action="store_true", help="Write src/valuation_fundamentals.json.")
    args = ap.parse_args(argv)

    tickers = [t.strip().upper() for t in args.tickers.split(",")] if args.tickers else default_tickers()
    snap = json.loads(SNAPSHOT.read_text(encoding="utf-8")) if SNAPSHOT.exists() else {"tickers": {}}
    failed = []
    print(f"{'TICKER':6} {'CCY':4} {'AS_OF':10} {'REV':>10} {'EBIT':>10} {'G_Q':>7} {'TAX':>6} {'CASH':>9} {'DEBT':>9} {'SHARES':>8}")
    for t in tickers:
        try:
            rec = parse(t, fetch(t))
        except Exception as exc:  # network or payload problem, keep the old record
            print(f"{t:6} fetch failed: {exc}", file=sys.stderr)
            failed.append(t)
            continue
        rec["source"] = f"https://finance.yahoo.com/quote/{t}/financials"
        snap["tickers"][t] = rec

        def f(x, fmt="{:>10.2f}"):
            return fmt.format(x) if isinstance(x, (int, float)) else f"{'-':>{len(fmt.format(0.0))}}"
        print(f"{t:6} {rec['currency'] or '-':4} {rec['as_of'] or '-':10} {f(rec['revenue_ttm'])} {f(rec['ebit_ttm'])} "
              f"{f(rec['revenue_growth_yoy_q'], '{:>7.1%}')} {f(rec['tax_rate'], '{:>6.1%}')} "
              f"{f(rec['cash'], '{:>9.2f}')} {f(rec['debt'], '{:>9.2f}')} {f(rec['shares'], '{:>8.3f}')}")
    snap["fetched_at"] = date.today().isoformat()
    snap["note"] = "Generated by scripts/fetch_valuation_fundamentals.py from Yahoo Finance. Money in billions of the reporting currency."
    if args.write:
        SNAPSHOT.write_text(json.dumps(snap, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {SNAPSHOT}")
    else:
        print("dry run, nothing written. Pass --write to save.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
