"""
Watchlist Engine & Report Generator (หุ้นที่สนใจ)
Tracks 46 tickers: 35 growth stocks from Shay Boloor (Fibonacci supports, updated 2026-10-17), SPCX added by the user,
5 midterm-2026 trend picks (Democratic sweep) whose supports come from the screener (SMA200 / lower Bollinger Band),
3 ETFs from the 2026-11-06 $10k plan whose supports are the tranche-2 buy prices,
and 2 big-tech dip picks (NFLX, LRCX) from the 2026-11-06 screen whose supports come from the screener.

Removed by the user on 2026-11-05 (grade F, losing money or EPS falling, and price already below its support):
CIFR, INTC, LITE, OKLO, VPG, IREN, LEU, ONDS, UUUU, ASTS, NBIS, MRCY, AAOI.
Fetches live close, premarket, and postmarket prices from TradingView Scanner API.
"""

import json
import os
import shutil
import sys
import urllib.request
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.nav import nav_bar_html
from src.trades import data_path
from src.universe import resolve_custom_tickers

SOURCE_AUTHOR = "Shay Boloor"
SOURCE_UPDATED = "2026-10-17"

WATCHLIST_STOCKS: List[Dict[str, Any]] = [
    # 1) Space
    {"group": "Space", "ticker": "RKLB", "support": 50.0},
    {"group": "Space", "ticker": "PL", "support": 10.0},
    {"group": "Space", "ticker": "RDW", "support": 7.0},
    # Not in Shay Boloor's image: support set by the user on 2026-10-30.
    {"group": "Space", "ticker": "SPCX", "support": 115.0, "source": "ผู้ใช้กำหนดเอง 2026-10-30"},
    # 2) Quantum
    {"group": "Quantum", "ticker": "IONQ", "support": 30.0},
    {"group": "Quantum", "ticker": "RGTI", "support": 11.0},
    {"group": "Quantum", "ticker": "QBTS", "support": 10.0},
    {"group": "Quantum", "ticker": "INFQ", "support": 8.0},
    # 3) Drones
    {"group": "Drones", "ticker": "AVAV", "support": 102.0},
    {"group": "Drones", "ticker": "KTOS", "support": 39.0},
    # 4) Nuclear
    {"group": "Nuclear", "ticker": "GEV", "support": 678.0},
    # 5) Photonics
    {"group": "Photonics", "ticker": "COHR", "support": 224.0},
    {"group": "Photonics", "ticker": "AEHR", "support": 57.0},
    # 6) CPU Bottleneck
    {"group": "CPU Bottleneck", "ticker": "AMD", "support": 479.0},
    {"group": "CPU Bottleneck", "ticker": "ARM", "support": 225.0},
    {"group": "CPU Bottleneck", "ticker": "AMKR", "support": 38.0},
    # 7) Physical AI
    {"group": "Physical AI", "ticker": "TSLA", "support": 353.0},
    {"group": "Physical AI", "ticker": "AMZN", "support": 231.0},
    {"group": "Physical AI", "ticker": "GOOGL", "support": 307.0},
    # 8) AI Utilities
    {"group": "AI Utilities", "ticker": "DOCN", "support": 90.0},
    # 9) AI Power
    {"group": "AI Power", "ticker": "ON", "support": 72.0},
    {"group": "AI Power", "ticker": "BE", "support": 192.0},
    {"group": "AI Power", "ticker": "NVTS", "support": 8.0},
    {"group": "AI Power", "ticker": "VRT", "support": 195.0},
    # 10) AI Silicon
    {"group": "AI Silicon", "ticker": "NVDA", "support": 210.0},
    {"group": "AI Silicon", "ticker": "TSM", "support": 398.0},
    {"group": "AI Silicon", "ticker": "ASML", "support": 1637.0},
    {"group": "AI Silicon", "ticker": "MU", "support": 849.0},
    # 11) AI Applications
    {"group": "AI Applications", "ticker": "PLTR", "support": 172.0},
    {"group": "AI Applications", "ticker": "NOW", "support": 124.0},
    {"group": "AI Applications", "ticker": "CRWD", "support": 210.0},
    {"group": "AI Applications", "ticker": "SNOW", "support": 283.0},
    # 12) AI Connectivity
    {"group": "AI Connectivity", "ticker": "AVGO", "support": 324.0},
    {"group": "AI Connectivity", "ticker": "ALAB", "support": 251.0},
    {"group": "AI Connectivity", "ticker": "CRDO", "support": 167.0},
    {"group": "AI Connectivity", "ticker": "MRVL", "support": 222.0},
    # 13) Midterm 2026 trend picks. Not from Shay Boloor's image. Picked with the user on 2026-11-05
    # after the Democratic sweep (all rose more than SPY on 2026-11-04). Supports are the screener's
    # key_support on 2026-11-05. Snapshot and reasons: docs/watchlist_midterm_2026-11-05.md
    {"group": "Midterm 2026", "ticker": "ENSG", "support": 181.68, "source": "เทรนเลือกตั้ง 2026-11-05 แนวรับ SMA200"},
    {"group": "Midterm 2026", "ticker": "FSLR", "support": 165.61, "source": "เทรนเลือกตั้ง 2026-11-05 แนวรับ BB ล่าง"},
    {"group": "Midterm 2026", "ticker": "DVA", "support": 178.24, "source": "เทรนเลือกตั้ง 2026-11-05 แนวรับ SMA200"},
    {"group": "Midterm 2026", "ticker": "OLLI", "support": 86.69, "source": "เทรนเลือกตั้ง 2026-11-05 แนวรับ SMA200"},
    {"group": "Midterm 2026", "ticker": "FIVE", "support": 205.42, "source": "เทรนเลือกตั้ง 2026-11-05 แนวรับ BB ล่าง"},
    # 14) ETF plan $10k agreed with Antigravity on 2026-11-06 (QQQM 65 / SOXQ 25 / GPIQ 10).
    # Support is the tranche-2 buy price of the ladder. Tranche 1 is bought near the 2026-11-05 close.
    {"group": "ETF Plan 2026-11", "ticker": "QQQM", "support": 251.0, "source": "แผน ETF $10k 2026-11-06 ไม้ 2"},
    {"group": "ETF Plan 2026-11", "ticker": "SOXQ", "support": 63.0, "source": "แผน ETF $10k 2026-11-06 ไม้ 2"},
    {"group": "ETF Plan 2026-11", "ticker": "GPIQ", "support": 48.0, "source": "แผน ETF $10k 2026-11-06 ไม้ 2"},
    # 15) Big-tech dip screen on 2026-11-06 (market cap >= $100B, fundamentals >= 93/100, >= 25% off the
    # 52-week high). Only the names not already in the watchlist. Supports are the screener's key_support that day.
    {"group": "Bigtech Dip 2026-11", "ticker": "NFLX", "support": 59.58, "source": "Bigtech ลงหนัก 2026-11-06 แนวรับ BB ล่าง"},
    {"group": "Bigtech Dip 2026-11", "ticker": "LRCX", "support": 161.03, "source": "Bigtech ลงหนัก 2026-11-06 แนวรับ 1.5 ATR"},
]


def classify_support_distance(pct_diff: Optional[float]) -> Tuple[str, str]:
    """
    Classify based on distance percentage from Fibonacci support:
    - (ก) ต่ำกว่าแนวรับ: pct_diff < 0.0
    - (ข) 0-5% เหนือแนวรับ: 0.0 <= pct_diff <= 5.0
    - (ค) เกิน 5%: pct_diff > 5.0
    Returns tuple of (code, thai_label).
    """
    if pct_diff is None:
        return ("unknown", "รอข้อมูลราคา")
    if pct_diff < 0.0:
        return ("A", "(ก) ต่ำกว่าแนวรับ")
    elif pct_diff <= 5.0:
        return ("B", "(ข) 0-5% เหนือแนวรับ")
    else:
        return ("C", "(ค) เกิน 5%")


def fetch_watchlist_prices(timeout: int = 15) -> Dict[str, Dict[str, Any]]:
    """
    Fetch market quotes (close, premarket_close, postmarket_close) for all watchlist tickers.
    Returns mapping of {ticker: {column: val}}.
    """
    tickers = [s["ticker"] for s in WATCHLIST_STOCKS]
    symbols = resolve_custom_tickers(tickers)

    url = "https://scanner.tradingview.com/america/scan"
    columns = [
        "name",
        "description",
        "close",
        "premarket_close",
        "premarket_change",
        "postmarket_close",
        "postmarket_change",
    ]
    payload = {
        "symbols": {"tickers": symbols, "query": {"types": []}},
        "columns": columns,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        print(f"⚠️ [watchlist] Failed to fetch prices from TradingView: {exc}")
        return {}

    results: Dict[str, Dict[str, Any]] = {}
    for item in data.get("data", []):
        sym_full = item.get("s", "")
        parts = sym_full.split(":", 1)
        ex = parts[0] if len(parts) > 1 else ""
        tk = parts[1] if len(parts) > 1 else sym_full
        d_vals = item.get("d", [])
        row = {"exchange": ex, "symbol_full": sym_full}
        for col_name, val in zip(columns, d_vals):
            row[col_name] = val
        results[tk] = row

    return results


def load_portfolio_holdings_tickers() -> set:
    """Read holdings in data/portfolio.json (read-only) honoring FILTER_STOCK_DATA_DIR."""
    path = data_path("portfolio.json")
    if not path.exists():
        return set()
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
        return {h["ticker"] for h in content.get("holdings", []) if "ticker" in h}
    except Exception as exc:
        print(f"⚠️ [watchlist] Error loading portfolio holdings: {exc}")
        return set()


def analyze_watchlist(
    price_data: Optional[Dict[str, Dict[str, Any]]] = None,
    portfolio_tickers: Optional[set] = None,
) -> Dict[str, Any]:
    """
    Analyze every watchlist stock against Fibonacci support levels.
    Sorts ascending by percentage distance (%ห่างจากแนวรับ ต่ำสุดไปสูงสุด).
    """
    if price_data is None:
        price_data = fetch_watchlist_prices()
    if portfolio_tickers is None:
        portfolio_tickers = load_portfolio_holdings_tickers()

    fetch_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    has_prices = bool(price_data)

    items = []
    group_counts = {"A": 0, "B": 0, "C": 0, "unknown": 0}

    for stock in WATCHLIST_STOCKS:
        tk = stock["ticker"]
        grp = stock["group"]
        supp = stock["support"]
        in_port = tk in portfolio_tickers

        p_info = price_data.get(tk, {}) if price_data else {}
        close = p_info.get("close")
        pm_close = p_info.get("premarket_close")
        post_close = p_info.get("postmarket_close")
        ex = p_info.get("exchange", "")
        desc = p_info.get("description", tk)

        # Pick effective price: premarket > postmarket > close
        price_type = "รอราคา"
        eff_price = None

        if pm_close is not None:
            eff_price = pm_close
            price_type = "Premarket"
        elif post_close is not None:
            eff_price = post_close
            price_type = "Postmarket"
        elif close is not None:
            eff_price = close
            price_type = "ราคาปิด (Close)"

        diff = (eff_price - supp) if eff_price is not None else None
        pct_diff = ((diff / supp) * 100.0) if diff is not None else None

        code, label = classify_support_distance(pct_diff)
        group_counts[code] = group_counts.get(code, 0) + 1

        items.append({
            "ticker": tk,
            "group": grp,
            "name": desc,
            "exchange": ex,
            "support": supp,
            "close": close,
            "premarket_close": pm_close,
            "postmarket_close": post_close,
            "effective_price": eff_price,
            "price_type": price_type,
            "diff": diff,
            "pct_diff": pct_diff,
            "status_code": code,
            "status_label": label,
            "in_portfolio": in_port,
            "source": stock.get("source"),
        })

    # Sort ascending by pct_diff (None goes to the bottom)
    items.sort(key=lambda x: (x["pct_diff"] is None, x["pct_diff"] if x["pct_diff"] is not None else 999999))

    return {
        "fetch_time": fetch_time_str,
        "has_prices": has_prices,
        "source_author": SOURCE_AUTHOR,
        "source_updated": SOURCE_UPDATED,
        "group_counts": group_counts,
        "portfolio_count": sum(1 for it in items if it["in_portfolio"]),
        "total_count": len(items),
        "items": items,
    }


def copy_watchlist_assets(reports_dir: Path) -> Path:
    """Copy shay_fibo_support_2026-10-17.jpeg to reports/assets/."""
    src_img = Path("docs/assets/shay_fibo_support_2026-10-17.jpeg")
    dst_dir = reports_dir / "assets"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_img = dst_dir / "shay_fibo_support_2026-10-17.jpeg"
    if src_img.exists() and (not dst_img.exists() or dst_img.stat().st_size != src_img.stat().st_size):
        shutil.copy2(src_img, dst_img)
    return dst_img


def _fmt_money(v: Optional[float]) -> str:
    """$1,356.65 style. Keeps cents so a support like 181.68 is not shown as 182."""
    if v is None:
        return "-"
    return f"${v:,.2f}"


def _fmt_support(v: float) -> str:
    return f"${v:,.0f}" if float(v).is_integer() else f"${v:,.2f}"


# Plain-language meaning of each support status, in the order the page shows them.
# The order is what a reader acts on first: in the buy zone, then broken support, then still far away.
STATUS_SECTIONS = [
    {
        "code": "B", "icon": "🎯", "title": "อยู่ในโซนซื้อ", "range": "ราคาอยู่เหนือแนวรับ 0-5%",
        "action": "ใกล้จุดซื้อแล้ว ตั้ง Limit ที่แนวรับได้", "color": "emerald",
    },
    {
        "code": "A", "icon": "🔻", "title": "หลุดแนวรับแล้ว", "range": "ราคาต่ำกว่าแนวรับ",
        "action": "แนวรับเดิมแตกแล้ว รอราคายืนกลับเหนือแนวรับก่อน อย่ารีบรับมีด", "color": "rose",
    },
    {
        "code": "C", "icon": "⏳", "title": "ยังไกลจากแนวรับ", "range": "ราคาอยู่เหนือแนวรับเกิน 5%",
        "action": "ยังไม่ถึงจุดซื้อ รอราคาย่อลงมา", "color": "slate",
    },
    {
        "code": "unknown", "icon": "⚪", "title": "รอราคา", "range": "ดึงราคาไม่ได้",
        "action": "ยังเทียบกับแนวรับไม่ได้", "color": "slate",
    },
]

GAUGE_RANGE_PCT = 25.0  # the bar spans -25% .. +25% around the support line


def _gauge_html(pct: Optional[float], color: str) -> str:
    """A bar with the support line in the middle and a dot for where the price is now."""
    if pct is None:
        return '<div class="gauge gauge-empty"></div>'
    clamped = max(-GAUGE_RANGE_PCT, min(GAUGE_RANGE_PCT, pct))
    pos = (clamped + GAUGE_RANGE_PCT) / (2 * GAUGE_RANGE_PCT) * 100.0
    zone_left = 50.0
    zone_width = 5.0 / (2 * GAUGE_RANGE_PCT) * 100.0
    overflow = "gauge-dot-edge" if abs(pct) > GAUGE_RANGE_PCT else ""
    return (
        '<div class="gauge" title="เส้นกลาง = แนวรับ, แถบเขียว = โซนซื้อ 0-5%">'
        f'<span class="gauge-zone" style="left:{zone_left:.1f}%;width:{zone_width:.1f}%"></span>'
        '<span class="gauge-mid"></span>'
        f'<span class="gauge-dot dot-{color} {overflow}" style="left:{pos:.1f}%"></span>'
        '</div>'
    )


def generate_watchlist_html(
    analyzed: Optional[Dict[str, Any]] = None,
    reports_dir: Optional[Path] = None,
) -> str:
    """Watchlist page grouped by what to do next: in the buy zone, broken support, still far."""
    if analyzed is None:
        analyzed = analyze_watchlist()
    if reports_dir is None:
        reports_dir = Path("reports")

    copy_watchlist_assets(reports_dir)

    fetch_time = analyzed["fetch_time"]
    has_prices = analyzed["has_prices"]
    items = analyzed["items"]
    counts = analyzed["group_counts"]
    port_count = analyzed["portfolio_count"]
    total = analyzed["total_count"]

    nav_html = nav_bar_html("watchlist")

    alert_banner = ""
    if not has_prices:
        alert_banner = """
        <div class="alert">
            <span>⚠️</span>
            <div><strong>ไม่สามารถดึงราคาล่าสุดจาก TradingView Scanner API ได้:</strong>
            ระบบกำลังแสดงเฉพาะแนวรับ Fibonacci อ้างอิงตามตาราง (รอการเชื่อมต่อเพื่ออัปเดตราคา)</div>
        </div>
        """

    price_types = {it["price_type"] for it in items if it["effective_price"] is not None}
    if "Premarket" in price_types:
        price_note = "ใช้ราคา Premarket ถ้ามี ไม่มีจึงใช้ราคาปิด"
    elif "Postmarket" in price_types:
        price_note = "ใช้ราคา Postmarket ถ้ามี ไม่มีจึงใช้ราคาปิด"
    else:
        price_note = "ใช้ราคาปิดล่าสุด"

    all_groups = sorted({it["group"] for it in items})
    group_options = "".join(f'<option value="{escape(g)}">{escape(g)}</option>' for g in all_groups)

    # Summary cards double as status filters.
    summary_cards = []
    for sec in STATUS_SECTIONS:
        n = counts.get(sec["code"], 0)
        if sec["code"] == "unknown" and n == 0:
            continue
        summary_cards.append(f"""
        <button class="sum-card sum-{sec['color']}" id="card-{sec['code']}" onclick="filterByStatus('{sec['code']}')">
            <div class="sum-top"><span class="sum-icon">{sec['icon']}</span><span class="sum-num">{n}</span></div>
            <div class="sum-title">{sec['title']}</div>
            <div class="sum-range">{sec['range']}</div>
        </button>""")

    sections_html = []
    for sec in STATUS_SECTIONS:
        sec_items = [it for it in items if it["status_code"] == sec["code"]]
        if not sec_items:
            continue
        # Closest to the support line first inside each section.
        sec_items.sort(key=lambda it: abs(it["pct_diff"]) if it["pct_diff"] is not None else 1e9)
        rows = []
        for it in sec_items:
            tk = it["ticker"]
            pct = it["pct_diff"]
            eff = it["effective_price"]
            close = it["close"]
            if pct is None:
                dist_txt = "-"
            elif pct < 0:
                dist_txt = f"ต่ำกว่าแนวรับ {abs(pct):.1f}%"
            else:
                dist_txt = f"เหนือแนวรับ {pct:.1f}%"

            if it["price_type"] in ("Premarket", "Postmarket") and close:
                chg = (eff - close) / close * 100.0
                chg_cls = "up" if chg >= 0 else "down"
                tag = "Pre" if it["price_type"] == "Premarket" else "Post"
                price_sub = (f'<span class="ptag">{tag}</span> '
                             f'<span class="{chg_cls}">{chg:+.1f}%</span> จากปิด {_fmt_money(close)}')
            elif eff is not None:
                price_sub = "ราคาปิด"
            else:
                price_sub = "รอราคา"

            port_badge = '<span class="port-badge" title="มีหุ้นนี้ในพอร์ตจริง (data/portfolio.json)">⭐ มีในพอร์ต</span>' if it["in_portfolio"] else ""
            source = it.get("source")
            src_line = (f'<div class="src" title="แนวรับไม่ได้มาจากภาพ {SOURCE_AUTHOR}">แนวรับจาก {escape(source)}</div>'
                        if source else f'<div class="src">แนวรับ Fibo จาก {SOURCE_AUTHOR}</div>')

            rows.append(f"""
            <div class="row stock-row" data-group="{escape(it['group'])}" data-status="{it['status_code']}"
                 data-portfolio="{'true' if it['in_portfolio'] else 'false'}" data-ticker="{escape(tk)}">
                <div class="col-name">
                    <div class="name-line"><span class="tk">{tk}</span>{port_badge}</div>
                    <div class="grp">{escape(it['group'])}</div>
                    {src_line}
                </div>
                <div class="col-price">
                    <div class="lbl">ราคาตอนนี้</div>
                    <div class="big">{_fmt_money(eff)}</div>
                    <div class="sub">{price_sub}</div>
                </div>
                <div class="col-supp">
                    <div class="lbl">แนวรับ</div>
                    <div class="big gold">{_fmt_support(it['support'])}</div>
                </div>
                <div class="col-dist">
                    <div class="dist dist-{sec['color']}">{dist_txt}</div>
                    {_gauge_html(pct, sec['color'])}
                </div>
            </div>""")
        sections_html.append(f"""
        <section class="sec sec-{sec['color']}" data-section="{sec['code']}">
            <div class="sec-head">
                <h2>{sec['icon']} {sec['title']} <span class="sec-count">{len(sec_items)} ตัว</span></h2>
                <p>{sec['range']}. <strong>ควรทำ:</strong> {sec['action']}.</p>
            </div>
            <div class="rows">{''.join(rows)}</div>
        </section>""")

    return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>หุ้นที่สนใจ (Watchlist) - Filter Stock</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
    --bg: #080d1a; --card: #0f172a; --card2: #131c31; --line: rgba(255,255,255,0.08);
    --text: #f1f5f9; --text2: #94a3b8; --muted: #64748b;
    --emerald: #10b981; --rose: #f43f5e; --amber: #f59e0b; --gold: #fbbf24; --blue: #60a5fa; --slate: #94a3b8;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ overflow-x: hidden; }}
body {{ font-family: 'Prompt', 'Inter', -apple-system, sans-serif; background: var(--bg); color: var(--text);
    line-height: 1.55; padding: 24px; min-height: 100vh;
    background-image: radial-gradient(at 0% 0%, rgba(59,130,246,0.07) 0, transparent 50%),
                      radial-gradient(at 100% 0%, rgba(168,85,247,0.06) 0, transparent 50%); }}
.container {{ max-width: 1100px; margin: 0 auto; min-width: 0; }}
h1 {{ font-size: 1.6rem; font-weight: 700; margin: 18px 0 4px; }}
.lead {{ color: var(--text2); font-size: 0.95rem; }}
.meta {{ color: var(--muted); font-size: 0.8rem; margin-top: 6px; }}
.meta strong {{ color: var(--text2); font-weight: 500; }}
.alert {{ display: flex; gap: 10px; margin: 16px 0; padding: 12px 16px; border-radius: 12px; font-size: 0.88rem;
    background: rgba(244,63,94,0.08); border: 1px solid rgba(244,63,94,0.3); color: #fecdd3; }}

.howto {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 18px 0; }}
.howto div {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 12px 14px;
    font-size: 0.84rem; color: var(--text2); }}
.howto b {{ color: var(--text); display: block; font-size: 0.9rem; margin-bottom: 2px; }}

.sums {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 8px 0 16px; }}
.sum-card {{ text-align: left; cursor: pointer; font-family: inherit; color: var(--text); background: var(--card);
    border: 1px solid var(--line); border-radius: 14px; padding: 14px 16px; transition: 0.15s; border-top: 3px solid var(--slate); }}
.sum-card:hover {{ background: var(--card2); }}
.sum-card.active {{ outline: 2px solid var(--blue); }}
.sum-emerald {{ border-top-color: var(--emerald); }} .sum-rose {{ border-top-color: var(--rose); }}
.sum-top {{ display: flex; justify-content: space-between; align-items: center; }}
.sum-icon {{ font-size: 1.3rem; }}
.sum-num {{ font-size: 1.9rem; font-weight: 700; font-family: 'Inter', sans-serif; }}
.sum-emerald .sum-num {{ color: var(--emerald); }} .sum-rose .sum-num {{ color: var(--rose); }}
.sum-title {{ font-weight: 600; }}
.sum-range {{ font-size: 0.78rem; color: var(--muted); }}

.toolbar {{ display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 18px; }}
.toolbar button, .toolbar select, .toolbar input {{ font-family: inherit; font-size: 0.85rem; color: var(--text);
    background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; min-width: 0; }}
.toolbar button {{ cursor: pointer; }}
.toolbar button.active {{ border-color: var(--blue); color: var(--blue); }}
.toolbar input {{ flex: 1 1 160px; }}
.toolbar .count {{ margin-left: auto; color: var(--muted); font-size: 0.8rem; }}

.sec {{ margin-bottom: 26px; }}
.sec-head {{ margin-bottom: 10px; padding-left: 12px; border-left: 4px solid var(--slate); }}
.sec-emerald .sec-head {{ border-left-color: var(--emerald); }} .sec-rose .sec-head {{ border-left-color: var(--rose); }}
.sec-head h2 {{ font-size: 1.15rem; font-weight: 600; }}
.sec-count {{ font-size: 0.8rem; color: var(--muted); font-weight: 400; margin-left: 6px; }}
.sec-head p {{ font-size: 0.85rem; color: var(--text2); }}
.sec-head p strong {{ color: var(--text); font-weight: 600; }}

.rows {{ display: flex; flex-direction: column; gap: 8px; }}
.row {{ display: grid; grid-template-columns: 1.5fr 1.2fr 0.8fr 1.6fr; gap: 16px; align-items: center;
    background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 12px 16px; min-width: 0; }}
.row > div {{ min-width: 0; }}
.sec-emerald .row {{ background: linear-gradient(90deg, rgba(16,185,129,0.08), var(--card) 40%); border-color: rgba(16,185,129,0.25); }}
.name-line {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
.tk {{ font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.05rem; letter-spacing: 0.02em; }}
.port-badge {{ font-size: 0.7rem; color: var(--gold); background: rgba(251,191,36,0.1);
    border: 1px solid rgba(251,191,36,0.3); border-radius: 6px; padding: 1px 6px; }}
.grp {{ font-size: 0.8rem; color: var(--text2); }}
.src {{ font-size: 0.7rem; color: var(--muted); }}
.lbl {{ font-size: 0.7rem; color: var(--muted); }}
.big {{ font-family: 'Inter', sans-serif; font-weight: 600; font-size: 1.02rem; }}
.gold {{ color: var(--gold); }}
.sub {{ font-size: 0.74rem; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.ptag {{ color: var(--blue); font-weight: 600; }}
.up {{ color: var(--emerald); }} .down {{ color: var(--rose); }}
.dist {{ font-weight: 600; font-size: 0.92rem; margin-bottom: 6px; }}
.dist-emerald {{ color: var(--emerald); }} .dist-rose {{ color: var(--rose); }} .dist-slate {{ color: var(--text2); }}

.gauge {{ position: relative; height: 8px; border-radius: 4px;
    background: linear-gradient(90deg, rgba(244,63,94,0.35), rgba(244,63,94,0.08) 50%, rgba(148,163,184,0.15) 50%); }}
.gauge-empty {{ opacity: 0.3; }}
.gauge-zone {{ position: absolute; top: 0; bottom: 0; background: rgba(16,185,129,0.6); }}
.gauge-mid {{ position: absolute; left: 50%; top: -4px; bottom: -4px; width: 2px; background: var(--gold); }}
.gauge-dot {{ position: absolute; top: 50%; width: 12px; height: 12px; border-radius: 50%;
    transform: translate(-50%, -50%); border: 2px solid var(--bg); }}
.dot-emerald {{ background: var(--emerald); }} .dot-rose {{ background: var(--rose); }} .dot-slate {{ background: #cbd5e1; }}
.gauge-dot-edge {{ box-shadow: 0 0 0 3px rgba(255,255,255,0.15); }}

details.more {{ margin-top: 30px; background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 12px 16px; }}
details.more summary {{ cursor: pointer; font-weight: 600; color: var(--text2); }}
details.more .inner {{ margin-top: 12px; font-size: 0.85rem; color: var(--text2); }}
details.more ul {{ padding-left: 20px; margin: 6px 0 12px; }}
details.more h3 {{ font-size: 0.92rem; color: var(--amber); margin: 10px 0 4px; }}
.thumb {{ display: flex; gap: 14px; align-items: center; flex-wrap: wrap; }}
.thumb img {{ width: 160px; max-width: 100%; border-radius: 8px; cursor: zoom-in; border: 1px solid var(--line); }}
code {{ background: rgba(255,255,255,0.06); padding: 1px 5px; border-radius: 4px; font-size: 0.8rem; }}

.modal-overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 1000;
    align-items: center; justify-content: center; padding: 20px; }}
.modal-overlay.open {{ display: flex; }}
.modal-content {{ position: relative; max-width: 95vw; max-height: 92vh; overflow: auto; background: var(--card);
    border-radius: 12px; padding: 10px; }}
.modal-img {{ max-width: 100%; display: block; }}
.modal-close {{ position: absolute; top: 6px; right: 10px; background: none; border: none; color: #fff; font-size: 1.8rem; cursor: pointer; }}

@media (max-width: 760px) {{
    body {{ padding: 14px; }}
    h1 {{ font-size: 1.3rem; }}
    .howto {{ grid-template-columns: 1fr; }}
    .sums {{ grid-template-columns: repeat(3, 1fr); gap: 8px; }}
    .sum-card {{ padding: 10px; }}
    .sum-num {{ font-size: 1.5rem; }}
    .sum-title {{ font-size: 0.82rem; }}
    .sum-range {{ display: none; }}
    .row {{ grid-template-columns: 1fr 1fr; gap: 10px 12px; padding: 12px; }}
    .col-name {{ grid-column: 1 / -1; }}
    .col-dist {{ grid-column: 1 / -1; }}
    .col-supp {{ text-align: right; }}
    .toolbar .count {{ width: 100%; margin-left: 0; }}
}}
</style>
</head>
<body>
{nav_html}
<div class="container">
    <h1>📋 หุ้นที่สนใจ</h1>
    <p class="lead">หุ้นที่รอซื้อ {total} ตัว. หน้านี้บอกว่าแต่ละตัวอยู่ใกล้ "แนวรับ" (ราคาที่ตั้งใจรอซื้อ) แค่ไหน.</p>
    <p class="meta">ราคาเมื่อ <strong>{fetch_time}</strong>. {price_note}. มีในพอร์ตจริง {port_count} ตัว.</p>
    {alert_banner}

    <div class="howto">
        <div><b>1. ดูกลุ่มเขียวก่อน</b>ราคาอยู่เหนือแนวรับไม่เกิน 5%. เป็นกลุ่มที่ใกล้จุดซื้อที่สุด.</div>
        <div><b>2. แถบแต่ละแถว</b>เส้นเหลืองตรงกลางคือแนวรับ. จุดคือราคาตอนนี้. แถบเขียวคือโซนซื้อ.</div>
        <div><b>3. กลุ่มแดงยังไม่ต้องรีบ</b>ราคาหลุดแนวรับแล้ว. แนวรับนั้นใช้ไม่ได้จนกว่าราคาจะยืนกลับ.</div>
    </div>

    <div class="sums">{''.join(summary_cards)}</div>

    <div class="toolbar">
        <button class="filter-btn active" id="btn-filter-all" onclick="filterByStatus('all')">ทั้งหมด ({total})</button>
        <button class="filter-btn" id="btn-filter-port" onclick="filterByPortfolio()">⭐ เฉพาะที่มีในพอร์ต ({port_count})</button>
        <select onchange="filterByGroup(this.value)" aria-label="กลุ่ม">
            <option value="all">ทุกกลุ่ม ({len(all_groups)})</option>
            {group_options}
        </select>
        <input type="search" placeholder="ค้นหา Ticker" oninput="handleSearch(this.value)" aria-label="ค้นหา Ticker">
        <span class="count" id="row-count-display">แสดง {total} จาก {total} ตัว</span>
    </div>

    {''.join(sections_html)}

    <details class="more">
        <summary>ที่มาของแนวรับ วิธีคำนวณ และข้อจำกัด</summary>
        <div class="inner">
            <h3>⚠️ ข้อจำกัดและคำเตือนสำคัญ (Risk Disclaimer)</h3>
            <ul>
                <li><strong>แนวรับ Fibo จากภาพยังไม่ผ่าน backtest:</strong> เป็นการประเมินโซนราคาทางเทคนิคจากภายนอก ห้ามนำไปใช้เป็นคะแนนในระบบหลัก (Unified Score) และห้ามใช้บล็อกการซื้อขาย</li>
                <li><strong>สภาพคล่องช่วง Premarket ต่ำ:</strong> ราคาซื้อขายนอกเวลาทำการปกติมีความผันผวนสูงและมี Spread กว้าง โปรดใช้ความระมัดระวัง</li>
                <li><strong>ไม่ใช่คำแนะนำการลงทุน:</strong> ข้อมูลนี้จัดทำเพื่อการติดตามและศึกษา Risk/Reward เท่านั้น ผู้ลงทุนต้องวิเคราะห์ปัจจัยพื้นฐานและความเสี่ยงด้วยตนเอง</li>
            </ul>
            <h3>วิธีคำนวณ</h3>
            <p>ระยะห่าง = <code>((ราคา - แนวรับ) / แนวรับ) × 100</code>. ราคาที่ใช้คือ Premarket ถ้ามี ต่อด้วย Postmarket แล้วจึงเป็นราคาปิด. แถบแสดงช่วง ±{GAUGE_RANGE_PCT:.0f}% ถ้าเกินนั้นจุดจะอยู่ที่ขอบ.</p>
            <h3>ที่มาของแนวรับ</h3>
            <div class="thumb">
                <img src="assets/shay_fibo_support_2026-10-17.jpeg" alt="Fibo Support" onclick="openImageModal()">
                <p>แนวรับ Fibonacci ส่วนใหญ่มาจาก <strong>{SOURCE_AUTHOR}</strong> (อัปเดต {analyzed['source_updated']}).
                ตัวที่มีบรรทัด "แนวรับจาก ..." ใต้ชื่อเป็นแนวรับที่กำหนดเอง เช่น จาก screener หรือจากแผน ETF. คลิกภาพเพื่อขยาย.</p>
            </div>
        </div>
    </details>
</div>

<div class="modal-overlay" id="image-modal" onclick="closeImageModal(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
        <button class="modal-close" onclick="closeImageModal()">&times;</button>
        <img src="assets/shay_fibo_support_2026-10-17.jpeg" alt="Fibo Support Large" class="modal-img">
    </div>
</div>

<script>
let currentStatus = 'all', currentGroup = 'all', currentSearch = '', currentPortOnly = false;

function applyFilters() {{
    const rows = document.querySelectorAll('.stock-row');
    let visible = 0;
    rows.forEach(row => {{
        const ok = (currentStatus === 'all' || row.dataset.status === currentStatus)
            && (!currentPortOnly || row.dataset.portfolio === 'true')
            && (currentGroup === 'all' || row.dataset.group === currentGroup)
            && (!currentSearch || row.dataset.ticker.toLowerCase().includes(currentSearch));
        row.style.display = ok ? '' : 'none';
        if (ok) visible++;
    }});
    document.querySelectorAll('.sec').forEach(sec => {{
        const any = Array.from(sec.querySelectorAll('.stock-row')).some(r => r.style.display !== 'none');
        sec.style.display = any ? '' : 'none';
    }});
    document.getElementById('row-count-display').textContent = `แสดง ${{visible}} จาก ${{rows.length}} ตัว`;
}}

function setActive() {{
    document.querySelectorAll('.filter-btn, .sum-card').forEach(el => el.classList.remove('active'));
    if (currentPortOnly) document.getElementById('btn-filter-port')?.classList.add('active');
    else if (currentStatus === 'all') document.getElementById('btn-filter-all')?.classList.add('active');
    else document.getElementById('card-' + currentStatus)?.classList.add('active');
}}

function filterByStatus(status) {{
    currentStatus = (status === currentStatus && status !== 'all') ? 'all' : status;
    currentPortOnly = false;
    setActive(); applyFilters();
}}

function filterByPortfolio() {{
    currentPortOnly = !currentPortOnly;
    currentStatus = 'all';
    setActive(); applyFilters();
}}

function filterByGroup(group) {{ currentGroup = group; applyFilters(); }}
function handleSearch(q) {{ currentSearch = (q || '').trim().toLowerCase(); applyFilters(); }}
function openImageModal() {{ document.getElementById('image-modal').classList.add('open'); }}
function closeImageModal() {{ document.getElementById('image-modal').classList.remove('open'); }}
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeImageModal(); }});
</script>
</body>
</html>
"""




def generate_watchlist_page(reports_dir: Optional[Path] = None) -> Path:
    """Generate reports/watchlist.html. Returns the Path to the written file."""
    if reports_dir is None:
        reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    analyzed = analyze_watchlist()
    html_content = generate_watchlist_html(analyzed, reports_dir=reports_dir)
    out_file = reports_dir / "watchlist.html"
    out_file.write_text(html_content, encoding="utf-8")
    return out_file


if __name__ == "__main__":
    out = generate_watchlist_page()
    print(f"Generated {out}")
