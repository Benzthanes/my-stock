"""
Watchlist Engine & Report Generator (หุ้นที่สนใจ)
Tracks 44 tickers across 15 high-growth sectors with Fibonacci / structural supports:
- Physical AI & Robotics Leaders: ADI (#1 BOM $1,625), MPWR (#2 Monolithic BCD), TXN (#3 300mm Low-Cost), TSLA, AMZN, GOOGL.
- Photonics & AI Wafer Burn-in: COHR, AEHR (Super Turnaround Q1 FY2027 Backlog $109M).
- Space, Drones, Nuclear, AI Power, AI Silicon, AI Applications, AI Connectivity, Midterm 2026, ETF Plans, and Bigtech Dips.
- Culled on 2026-11-07: ON (SiC price war / margin drop), NVTS (OM -272%), QBTS, RGTI, INFQ (Quantum cash burn).
- Features Dual View Mode (Grid Cards vs Pro Table), Market Radar Ribbon, Interactive Theme Pills, and Direct Chart Links.
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
    # 2) Quantum (Cull QBTS, RGTI, INFQ due to severe cash burn OM < -200%; keep only commercial leader IONQ)
    {"group": "Quantum", "ticker": "IONQ", "support": 30.0},
    # 3) Drones
    {"group": "Drones", "ticker": "AVAV", "support": 102.0},
    {"group": "Drones", "ticker": "KTOS", "support": 39.0},
    # 4) Nuclear
    {"group": "Nuclear", "ticker": "GEV", "support": 678.0},
    # 5) Photonics (COHR & AEHR - AI Wafer Burn-in & Optical Transceiver Turnaround)
    {"group": "Photonics", "ticker": "COHR", "support": 224.0},
    {"group": "Photonics", "ticker": "AEHR", "support": 57.0},
    # 6) CPU Bottleneck
    {"group": "CPU Bottleneck", "ticker": "AMD", "support": 479.0},
    {"group": "CPU Bottleneck", "ticker": "ARM", "support": 225.0},
    {"group": "CPU Bottleneck", "ticker": "AMKR", "support": 38.0},
    # 7) Physical AI & Robotics (Added Morgan Stanley BOM leaders: ADI, MPWR, TXN)
    {"group": "Physical AI", "ticker": "TSLA", "support": 353.0},
    {"group": "Physical AI", "ticker": "AMZN", "support": 231.0},
    {"group": "Physical AI", "ticker": "GOOGL", "support": 307.0},
    {"group": "Physical AI", "ticker": "ADI", "support": 363.0, "source": "ชิปหุ่นยนต์ Morgan Stanley #1 ($1,625) แนวรับ EMA200"},
    {"group": "Physical AI", "ticker": "MPWR", "support": 1100.0, "source": "ชิปข้อต่อหุ่นยนต์ & Power Stage แนวรับจิตวิทยา"},
    {"group": "Physical AI", "ticker": "TXN", "support": 262.0, "source": "ชิปแอนะล็อกโรงงาน 300mm แนวรับ EMA200"},
    # 8) AI Utilities
    {"group": "AI Utilities", "ticker": "DOCN", "support": 90.0},
    # 9) AI Power (Cull ON due to SiC price war/margin drop, NVTS due to OM -272%)
    {"group": "AI Power", "ticker": "BE", "support": 192.0},
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

CATALYSTS: Dict[str, str] = {
    # Space
    "RKLB": "🚀 จรวด Neutron & ดาวเทียมป้องกันประเทศ",
    "PL": "🛰️ ภาพถ่ายดาวเทียม & AI Geospatial Analytics",
    "RDW": "🛰️ แผงโซลาร์อวกาศ & โครงสร้างพื้นฐานวงโคจร",
    "SPCX": "🚀 ยาน Starship & ดาวเทียม Starlink ผูกขาด",
    # Quantum
    "IONQ": "⚛️ ผู้นำควอนตัม Trapped-ion เชิงพาณิชย์",
    # Drones
    "AVAV": "🛩️ โดรนพลีชีพ Switchblade & ยุทธวิธีไร้คนขับ",
    "KTOS": "🛩️ โดรนเป้าซ้อมรบ & โดรนรบร่วม Valkyrie",
    # Nuclear
    "GEV": "⚡ โรงไฟฟ้านิวเคลียร์ SMR & กังหันพลังงานสะอาด",
    # Photonics
    "COHR": "💡 Optical Transceiver 800G/1.6T สำหรับ AI",
    "AEHR": "✨ Q1 Turnaround สถิติ Backlog $109M Wafer Burn-in",
    # CPU Bottleneck
    "AMD": "🖥️ ชิปเร่งความเร็ว AI MI300/MI350 & ซีพียู EPYC",
    "ARM": "📱 สถาปัตยกรรมชิปประหยัดพลังงาน v9 ในเซิร์ฟเวอร์",
    "AMKR": "📦 แพ็กเกจจิ้งชิปขั้นสูง 2.5D/3D สำหรับ AI",
    # Physical AI
    "TSLA": "🤖 หุ่นยนต์ Optimus & ระบบขับเคลื่อนไร้คนขับ FSD",
    "AMZN": "📦 หุ่นยนต์อัตโนมัติในคลังสินค้า & ชิป Trainium",
    "GOOGL": "🤖 สมองกล Physical AI Gemini & ชิป TPU v6",
    "ADI": "👑 ชิปหุ่นยนต์อันดับ 1 (BOM $1,625) มาร์จิ้น 67%",
    "MPWR": "🚀 Monolithic BCD ชิปจัดการพลังงานข้อต่อหุ่นยนต์",
    "TXN": "🛡️ โรงงาน 300mm ชิปแอนะล็อกต้นทุนต่ำ R:R 1:5.1",
    # AI Utilities
    "DOCN": "☁️ คลาวด์สำหรับนักพัฒนาโมเดล AI ขนาดเล็ก/กลาง",
    # AI Power
    "BE": "⚡ เซลล์เชื้อเพลิงผลิตไฟฟ้านอกสายส่งป้อน Datacenter",
    "VRT": "❄️ ระบบระบายความร้อนด้วยของเหลวสำหรับ GPU คลัสเตอร์",
    # AI Silicon
    "NVDA": "🧠 เจ้าตลาดชิป AI ผูกขาดสถาปัตยกรรม Blackwell Ultra",
    "TSM": "🏭 ผู้ผลิตชิปผูกขาดระดับโลก N3/N2 Foundry",
    "ASML": "🔬 เครื่องพิมพ์ชิป EUV High-NA หนึ่งเดียวในโลก",
    "MU": "💾 ชิปหน่วยความจำ HBM3E สำหรับเซิร์ฟเวอร์ AI",
    # AI Applications
    "PLTR": "🛡️ แพลตฟอร์มซอฟต์แวร์ AIP กองทัพและองค์กร",
    "NOW": "💼 ระบบจัดการงานอัตโนมัติ Workflow AI",
    "CRWD": "🔒 ระบบความปลอดภัยไซเบอร์ Falcon AI Cloud",
    "SNOW": "📊 คลังข้อมูล Data Cloud ผนวก Cortex AI",
    # AI Connectivity
    "AVGO": "🌐 ชิปเน็ตเวิร์ก Ethernet 800G & Custom ASIC",
    "ALAB": "🔌 ชิปเชื่อมต่อ PCIe Gen 6/CXL สำหรับ AI",
    "CRDO": "⚡ สายเคเบิลความเร็วสูง AEC & DSP ประหยัดไฟ",
    "MRVL": "📡 ชิปเครือข่ายความเร็วสูง Optical DSP & AI",
    # Midterm 2026
    "ENSG": "🏥 ธุรกิจดูแลผู้ป่วยระยะยาว นโยบายหนุน",
    "FSLR": "☀️ แผงโซลาร์สหรัฐฯ รับอานิสงส์กฎหมายพลังงานสะอาด",
    "DVA": "🏥 ศูนย์ฟอกไตทั่วสหรัฐฯ ประกันสุขภาพคุ้มครอง",
    "OLLI": "🛒 ค้าปลีกสินค้าราคาประหยัด ชนะเงินเฟ้อ",
    "FIVE": "🛍️ สินค้าวัยรุ่นราคาประหยัด ขยายสาขาเติบโตเร็ว",
    # ETF Plan 2026-11
    "QQQM": "📈 ดัชนี Nasdaq 100 ค่าธรรมเนียมต่ำ ไม้ 2",
    "SOXQ": "📈 กองทุนดัชนีเซมิคอนดักเตอร์ SOX ไม้ 2",
    "GPIQ": "💵 ETF ปันผลรายเดือนจากดัชนี Nasdaq 100 ไม้ 2",
    # Bigtech Dip 2026-11
    "NFLX": "🎬 ผู้นำสตรีมมิงระดับโลก ย่อตัวลึกจากจุดสูงสุด",
    "LRCX": "⚙️ เครื่องจักรผลิตชิป Etching ย่อตัวลึก 1.5 ATR",
}


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

        catalyst = CATALYSTS.get(tk, "")

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
            "catalyst": catalyst,
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


STATUS_SECTIONS = [
    {
        "code": "B", "icon": "🎯", "title": "อยู่ในโซนซื้อ", "range": "ราคาอยู่เหนือแนวรับ 0-5%",
        "action": "ใกล้จุดซื้อแล้ว ตั้ง Limit Order ที่แนวรับได้", "color": "emerald",
    },
    {
        "code": "A", "icon": "🔻", "title": "หลุดแนวรับแล้ว", "range": "ราคาต่ำกว่าแนวรับ",
        "action": "แนวรับเดิมแตกแล้ว รอราคายืนกลับเหนือแนวรับก่อน ห้ามรับมีด", "color": "rose",
    },
    {
        "code": "C", "icon": "⏳", "title": "ยังไกลจากแนวรับ", "range": "ราคาอยู่เหนือแนวรับเกิน 5%",
        "action": "ยังไม่ถึงจุดซื้อ รอราคาย่อตัวลงมาทดสอบ", "color": "slate",
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
        '<div class="gauge" title="เส้นกลาง = แนวรับ (0%), แถบเขียว = โซนซื้อ 0-5%">'
        f'<span class="gauge-zone" style="left:{zone_left:.1f}%;width:{zone_width:.1f}%"></span>'
        '<span class="gauge-mid"></span>'
        f'<span class="gauge-dot dot-{color} {overflow}" style="left:{pos:.1f}%"></span>'
        '</div>'
    )


def generate_watchlist_html(
    analyzed: Optional[Dict[str, Any]] = None,
    reports_dir: Optional[Path] = None,
) -> str:
    """Generate modern, high-converting Watchlist report with Dual View, Radar Ribbon, and Pills."""
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

    # Identify tickers in buy zone for spotlight
    buy_zone_tickers = [it["ticker"] for it in items if it["status_code"] == "B"]
    buy_zone_preview = ", ".join(buy_zone_tickers[:6]) if buy_zone_tickers else "ยังไม่มีหุ้นในโซน 0-5%"
    if len(buy_zone_tickers) > 6:
        buy_zone_preview += f" และอีก {len(buy_zone_tickers) - 6} ตัว"

    # Compute Watchlist Health percentages
    cnt_b = counts.get("B", 0)
    cnt_a = counts.get("A", 0)
    cnt_c = counts.get("C", 0)
    denom = max(1, total)
    pct_b = (cnt_b / denom) * 100.0
    pct_a = (cnt_a / denom) * 100.0
    pct_c = (cnt_c / denom) * 100.0

    all_groups = sorted({it["group"] for it in items})

    # Group Icons mapping for pills
    GROUP_ICONS = {
        "Physical AI": "🤖",
        "Photonics": "💡",
        "Space": "🚀",
        "Quantum": "⚛️",
        "Drones": "🛩️",
        "Nuclear": "⚡",
        "CPU Bottleneck": "🖥️",
        "AI Utilities": "☁️",
        "AI Power": "🔋",
        "AI Silicon": "🧠",
        "AI Applications": "💼",
        "AI Connectivity": "🌐",
        "Midterm 2026": "🗳️",
        "ETF Plan 2026-11": "📈",
        "Bigtech Dip 2026-11": "💎",
    }

    # Build Interactive Filter Pills
    pills_html = [
        f'<button class="pill-btn active" id="pill-all" onclick="filterByPill(\'all\')">🌟 ทั้งหมด ({total})</button>',
        f'<button class="pill-btn pill-buy" id="pill-buy" onclick="filterByPill(\'buy\')">🎯 โซนซื้อ 0-5% ({cnt_b})</button>',
        f'<button class="pill-btn pill-port" id="pill-port" onclick="filterByPill(\'port\')">⭐ ในพอร์ต ({port_count})</button>',
    ]
    for g in all_groups:
        g_count = sum(1 for it in items if it["group"] == g)
        icon = GROUP_ICONS.get(g, "📁")
        pills_html.append(
            f'<button class="pill-btn" data-group="{escape(g)}" onclick="filterByPill(\'{escape(g)}\')">'
            f'{icon} {escape(g)} ({g_count})</button>'
        )

    # Build Grid Cards HTML
    grid_cards_html = []
    # Build Pro Table Rows HTML
    table_rows_html = []

    for it in items:
        tk = it["ticker"]
        grp = it["group"]
        supp = it["support"]
        eff = it["effective_price"]
        close = it["close"]
        pct = it["pct_diff"]
        code = it["status_code"]
        sec_color = "emerald" if code == "B" else ("rose" if code == "A" else "slate")
        status_badge_txt = "🎯 โซนซื้อ 0-5%" if code == "B" else ("🔻 หลุดแนวรับ" if code == "A" else ("⏳ ยังไกล" if code == "C" else "⚪ รอราคา"))
        catalyst = it.get("catalyst", "")
        source = it.get("source")
        src_line = f"แนวรับจาก {escape(source)}" if source else f"แนวรับ Fibo {SOURCE_AUTHOR}"

        if pct is None:
            dist_txt = "-"
            dist_val = 999999.0
        elif pct < 0:
            dist_txt = f"-{abs(pct):.1f}%"
            dist_val = pct
        else:
            dist_txt = f"+{pct:.1f}%"
            dist_val = pct

        if it["price_type"] in ("Premarket", "Postmarket") and close:
            chg = (eff - close) / close * 100.0
            chg_cls = "up" if chg >= 0 else "down"
            tag = "Pre" if it["price_type"] == "Premarket" else "Post"
            price_sub = f'<span class="ptag">{tag}</span> <span class="{chg_cls}">{chg:+.1f}%</span>'
        elif eff is not None:
            price_sub = '<span class="ptag-close">Close</span>'
        else:
            price_sub = '<span class="ptag-wait">รอราคา</span>'

        port_badge = '<span class="port-star" title="มีในพอร์ตจริง">⭐</span>' if it["in_portfolio"] else ""

        # 1. Grid Card
        grid_cards_html.append(f"""
        <div class="stock-card card-{sec_color}" data-group="{escape(grp)}" data-status="{code}"
             data-portfolio="{'true' if it['in_portfolio'] else 'false'}" data-ticker="{escape(tk)}"
             data-pct="{dist_val}">
            <div class="card-head">
                <div class="card-tk-box">
                    <span class="tk">{tk}</span>{port_badge}
                    <span class="card-grp">{escape(grp)}</span>
                </div>
                <span class="status-pill status-{sec_color}">{status_badge_txt}</span>
            </div>
            <div class="card-name" title="{escape(it['name'])}">{escape(it['name'])}</div>
            <div class="card-catalyst">{escape(catalyst)}</div>
            <div class="card-price-grid">
                <div>
                    <div class="card-lbl">ราคาตอนนี้</div>
                    <div class="card-val">{_fmt_money(eff)}</div>
                    <div class="card-sub">{price_sub}</div>
                </div>
                <div>
                    <div class="card-lbl">แนวรับ</div>
                    <div class="card-val gold">{_fmt_support(supp)}</div>
                    <div class="card-sub">{src_line}</div>
                </div>
                <div style="text-align:right;">
                    <div class="card-lbl">ระยะห่าง</div>
                    <div class="card-val dist-{sec_color}">{dist_txt}</div>
                    <div class="card-sub">เทียบแนวรับ</div>
                </div>
            </div>
            <div class="card-gauge-box">
                {_gauge_html(pct, sec_color)}
            </div>
            <div class="card-actions">
                <a href="chart.html?ticker={escape(tk)}" class="btn-chart-link" title="เปิดหน้ากราฟแท่งเทียน & อินดิเคเตอร์">
                    <span>📈</span> ดูกราฟ
                </a>
                <span class="card-src-tag">{src_line}</span>
            </div>
        </div>
        """)

        # 2. Table Row
        table_rows_html.append(f"""
        <tr class="table-row row-{sec_color}" data-group="{escape(grp)}" data-status="{code}"
            data-portfolio="{'true' if it['in_portfolio'] else 'false'}" data-ticker="{escape(tk)}"
            data-pct="{dist_val}">
            <td>
                <div class="table-tk-box">
                    <span class="tk">{tk}</span>{port_badge}
                    <span class="table-company">{escape(it['name'])}</span>
                </div>
            </td>
            <td><span class="table-grp-pill">{escape(grp)}</span></td>
            <td><div class="table-catalyst">{escape(catalyst)}</div></td>
            <td>
                <div class="table-price">{_fmt_money(eff)}</div>
                <div class="table-sub">{price_sub}</div>
            </td>
            <td><div class="table-supp gold">{_fmt_support(supp)}</div></td>
            <td><div class="table-dist dist-{sec_color}">{dist_txt}</div></td>
            <td style="min-width:110px;">{_gauge_html(pct, sec_color)}</td>
            <td><span class="status-pill status-{sec_color}">{status_badge_txt}</span></td>
            <td>
                <a href="chart.html?ticker={escape(tk)}" class="table-chart-btn" title="ดูกราฟ">📈 กราฟ</a>
            </td>
        </tr>
        """)

    return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>หุ้นที่สนใจ (Watchlist) - Filter Stock</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
    --bg: #070d19; --card: #0f172a; --card2: #142038; --line: rgba(255,255,255,0.08);
    --line-bright: rgba(255,255,255,0.16); --text: #f1f5f9; --text2: #94a3b8; --muted: #64748b;
    --emerald: #10b981; --emerald-glow: rgba(16,185,129,0.3); --rose: #f43f5e; --rose-glow: rgba(244,63,94,0.3);
    --gold: #fbbf24; --gold-glow: rgba(251,191,36,0.3); --blue: #60a5fa; --blue-glow: rgba(96,165,250,0.3);
    --purple: #c084fc; --slate: #94a3b8;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ overflow-x: hidden; }}
body {{
    font-family: 'Prompt', 'Inter', -apple-system, sans-serif;
    background: var(--bg); color: var(--text);
    line-height: 1.55; padding: 24px; min-height: 100vh;
    background-image:
        radial-gradient(at 0% 0%, rgba(59,130,246,0.08) 0, transparent 45%),
        radial-gradient(at 100% 0%, rgba(168,85,247,0.07) 0, transparent 45%),
        radial-gradient(at 50% 100%, rgba(16,185,129,0.05) 0, transparent 40%);
}}
.container {{ max-width: 1200px; margin: 0 auto; min-width: 0; }}

/* Top Header */
.top-header {{ margin-bottom: 20px; }}
h1 {{ font-size: 1.75rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 10px; }}
.lead {{ color: var(--text2); font-size: 0.95rem; margin-top: 4px; }}
.meta {{ color: var(--muted); font-size: 0.82rem; margin-top: 6px; display: flex; gap: 16px; flex-wrap: wrap; align-items: center; }}
.meta strong {{ color: var(--text2); font-weight: 600; }}
.meta-chip {{ background: rgba(255,255,255,0.05); padding: 2px 8px; border-radius: 6px; border: 1px solid var(--line); }}

.alert {{ display: flex; gap: 10px; margin: 16px 0; padding: 12px 16px; border-radius: 12px; font-size: 0.88rem;
    background: rgba(244,63,94,0.08); border: 1px solid rgba(244,63,94,0.3); color: #fecdd3; }}

/* Main Navigation Tabs */
.main-tabs {{ display: flex; gap: 10px; margin: 20px 0 24px; border-bottom: 1px solid var(--line); padding-bottom: 14px; }}
.main-tab-btn {{
    font-family: inherit; font-size: 0.95rem; font-weight: 600; color: var(--text2);
    background: var(--card); border: 1px solid var(--line); border-radius: 12px;
    padding: 10px 20px; cursor: pointer; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex; align-items: center; gap: 8px;
}}
.main-tab-btn:hover {{ background: var(--card2); color: #fff; transform: translateY(-1px); }}
.main-tab-btn.active {{
    background: linear-gradient(135deg, rgba(96,165,250,0.18), rgba(59,130,246,0.08));
    border-color: var(--blue); color: #fff; box-shadow: 0 0 16px rgba(96,165,250,0.25);
}}
.tab-badge {{ font-size: 0.7rem; font-weight: 700; background: var(--rose); color: #fff; padding: 2px 7px; border-radius: 6px; }}

/* Pillar 1: Market Radar & Executive Ribbon */
.radar-ribbon {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 14px; margin-bottom: 24px;
}}
.ribbon-card {{
    background: var(--card); border: 1px solid var(--line); border-radius: 16px;
    padding: 16px 18px; position: relative; overflow: hidden; transition: all 0.2s;
    display: flex; flex-direction: column; justify-content: space-between;
}}
.ribbon-card:hover {{ background: var(--card2); border-color: var(--line-bright); }}
.ribbon-card-buy {{ border-top: 4px solid var(--emerald); }}
.ribbon-card-broken {{ border-top: 4px solid var(--rose); }}
.ribbon-card-far {{ border-top: 4px solid var(--slate); }}
.ribbon-card-health {{ border-top: 4px solid var(--gold); }}

.ribbon-top {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.ribbon-title {{ font-size: 0.85rem; font-weight: 600; color: var(--text2); display: flex; align-items: center; gap: 6px; }}
.ribbon-num {{ font-size: 2.1rem; font-weight: 800; font-family: 'Inter', sans-serif; line-height: 1.1; margin: 6px 0 2px; }}
.ribbon-card-buy .ribbon-num {{ color: var(--emerald); text-shadow: 0 0 20px var(--emerald-glow); }}
.ribbon-card-broken .ribbon-num {{ color: var(--rose); text-shadow: 0 0 20px var(--rose-glow); }}
.ribbon-card-far .ribbon-num {{ color: var(--slate); }}
.ribbon-sub {{ font-size: 0.78rem; color: var(--muted); }}
.ribbon-preview {{ font-size: 0.76rem; color: var(--emerald); font-weight: 500; margin-top: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

/* Health Gauge */
.health-bar-container {{ margin: 10px 0 6px; }}
.health-bar {{
    display: flex; height: 10px; border-radius: 5px; overflow: hidden;
    background: rgba(255,255,255,0.06); width: 100%;
}}
.hb-seg {{ height: 100%; transition: width 0.3s; }}
.hb-emerald {{ background: var(--emerald); }}
.hb-slate {{ background: var(--slate); }}
.hb-rose {{ background: var(--rose); }}
.health-legend {{ display: flex; justify-content: space-between; font-size: 0.72rem; color: var(--muted); margin-top: 4px; }}

/* Pillar 3: Theme & Sector Filter Pills */
.pills-container {{
    margin-bottom: 20px; overflow-x: auto; padding-bottom: 6px;
    -webkit-overflow-scrolling: touch; scrollbar-width: none;
}}
.pills-container::-webkit-scrollbar {{ display: none; }}
.pills-bar {{ display: flex; gap: 8px; flex-wrap: nowrap; min-width: max-content; }}
.pill-btn {{
    font-family: inherit; font-size: 0.82rem; font-weight: 500; color: var(--text2);
    background: var(--card); border: 1px solid var(--line); border-radius: 9999px;
    padding: 7px 14px; cursor: pointer; transition: all 0.15s ease; white-space: nowrap;
    display: inline-flex; align-items: center; gap: 6px;
}}
.pill-btn:hover {{ background: var(--card2); color: #fff; border-color: var(--line-bright); }}
.pill-btn.active {{
    background: var(--blue); color: #070d19; font-weight: 700;
    border-color: var(--blue); box-shadow: 0 0 14px var(--blue-glow);
}}
.pill-buy.active {{ background: var(--emerald); color: #070d19; border-color: var(--emerald); box-shadow: 0 0 14px var(--emerald-glow); }}
.pill-port.active {{ background: var(--gold); color: #070d19; border-color: var(--gold); box-shadow: 0 0 14px var(--gold-glow); }}

/* Toolbar & Dual View Toggle */
.toolbar {{
    display: flex; gap: 12px; align-items: center; flex-wrap: wrap;
    background: var(--card); border: 1px solid var(--line); border-radius: 14px;
    padding: 10px 14px; margin-bottom: 22px;
}}
.search-box {{
    flex: 1 1 200px; position: relative; display: flex; align-items: center;
}}
.search-box input {{
    width: 100%; font-family: inherit; font-size: 0.85rem; color: var(--text);
    background: rgba(255,255,255,0.04); border: 1px solid var(--line); border-radius: 10px;
    padding: 8px 12px 8px 34px; outline: none; transition: 0.2s;
}}
.search-box input:focus {{ border-color: var(--blue); background: rgba(255,255,255,0.06); }}
.search-icon {{ position: absolute; left: 10px; color: var(--muted); font-size: 0.85rem; pointer-events: none; }}

.view-toggle-group {{
    display: flex; background: rgba(255,255,255,0.04); border: 1px solid var(--line);
    border-radius: 10px; padding: 2px;
}}
.view-btn {{
    font-family: inherit; font-size: 0.82rem; font-weight: 600; color: var(--text2);
    background: none; border: none; border-radius: 8px; padding: 6px 12px;
    cursor: pointer; display: flex; align-items: center; gap: 6px; transition: 0.15s;
}}
.view-btn.active {{
    background: var(--card2); color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.25);
    border: 1px solid var(--line-bright);
}}
.row-count-chip {{ color: var(--muted); font-size: 0.82rem; margin-left: auto; }}

/* Pillar 2 & 4: Grid Cards View */
.cards-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 16px; margin-bottom: 30px;
}}
.stock-card {{
    background: var(--card); border: 1px solid var(--line); border-radius: 16px;
    padding: 16px 18px; position: relative; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex; flex-direction: column; justify-content: space-between; gap: 12px;
}}
.stock-card:hover {{
    transform: translateY(-2px); border-color: var(--line-bright);
    box-shadow: 0 8px 24px rgba(0,0,0,0.35); background: var(--card2);
}}
.card-emerald {{ border-left: 4px solid var(--emerald); }}
.card-rose {{ border-left: 4px solid var(--rose); }}
.card-slate {{ border-left: 4px solid var(--slate); }}

.card-head {{ display: flex; justify-content: space-between; align-items: center; }}
.card-tk-box {{ display: flex; align-items: center; gap: 8px; }}
.tk {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 1.15rem; letter-spacing: 0.02em; color: #fff; }}
.port-star {{ color: var(--gold); font-size: 0.95rem; }}
.card-grp {{ font-size: 0.76rem; color: var(--text2); background: rgba(255,255,255,0.05); padding: 2px 7px; border-radius: 6px; }}
.card-name {{ font-size: 0.82rem; color: var(--text2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

/* Catalyst Tag */
.card-catalyst {{
    font-size: 0.78rem; color: #93c5fd; background: rgba(96,165,250,0.08);
    border: 1px solid rgba(96,165,250,0.22); border-radius: 8px; padding: 5px 10px;
    line-height: 1.4; display: flex; align-items: center; gap: 6px;
}}

/* Card Price Matrix */
.card-price-grid {{
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;
    background: rgba(255,255,255,0.02); border: 1px solid var(--line);
    border-radius: 12px; padding: 10px 12px;
}}
.card-lbl {{ font-size: 0.7rem; color: var(--muted); }}
.card-val {{ font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.05rem; }}
.gold {{ color: var(--gold); }}
.dist-emerald {{ color: var(--emerald); font-weight: 700; }}
.dist-rose {{ color: var(--rose); font-weight: 700; }}
.dist-slate {{ color: var(--text2); font-weight: 600; }}
.card-sub {{ font-size: 0.72rem; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.ptag {{ color: var(--blue); font-weight: 700; }}
.up {{ color: var(--emerald); font-weight: 600; }} .down {{ color: var(--rose); font-weight: 600; }}

/* Status Pills */
.status-pill {{
    display: inline-flex; align-items: center; gap: 4px; font-size: 0.72rem;
    font-weight: 700; padding: 3px 8px; border-radius: 9999px; white-space: nowrap;
}}
.status-emerald {{ background: rgba(16,185,129,0.15); color: var(--emerald); border: 1px solid rgba(16,185,129,0.35); }}
.status-rose {{ background: rgba(244,63,94,0.15); color: var(--rose); border: 1px solid rgba(244,63,94,0.35); }}
.status-slate {{ background: rgba(148,163,184,0.12); color: var(--text2); border: 1px solid rgba(148,163,184,0.25); }}

/* Visual Proximity Gauge */
.card-gauge-box {{ margin: 4px 0; }}
.gauge {{
    position: relative; height: 8px; border-radius: 4px;
    background: linear-gradient(90deg, rgba(244,63,94,0.3), rgba(244,63,94,0.08) 50%, rgba(148,163,184,0.15) 50%);
}}
.gauge-empty {{ opacity: 0.3; }}
.gauge-zone {{ position: absolute; top: 0; bottom: 0; background: rgba(16,185,129,0.65); }}
.gauge-mid {{ position: absolute; left: 50%; top: -4px; bottom: -4px; width: 2px; background: var(--gold); }}
.gauge-dot {{
    position: absolute; top: 50%; width: 12px; height: 12px; border-radius: 50%;
    transform: translate(-50%, -50%); border: 2px solid var(--bg);
}}
.dot-emerald {{ background: var(--emerald); box-shadow: 0 0 6px var(--emerald); }}
.dot-rose {{ background: var(--rose); box-shadow: 0 0 6px var(--rose); }}
.dot-slate {{ background: #cbd5e1; }}
.gauge-dot-edge {{ box-shadow: 0 0 0 3px rgba(255,255,255,0.2); }}

/* Card Actions */
.card-actions {{
    display: flex; justify-content: space-between; align-items: center;
    border-top: 1px solid var(--line); padding-top: 10px; margin-top: 2px;
}}
.btn-chart-link {{
    font-size: 0.78rem; font-weight: 600; color: var(--blue); text-decoration: none;
    background: rgba(96,165,250,0.1); border: 1px solid rgba(96,165,250,0.3);
    border-radius: 8px; padding: 4px 10px; transition: 0.15s; display: inline-flex; align-items: center; gap: 4px;
}}
.btn-chart-link:hover {{ background: rgba(96,165,250,0.2); color: #fff; transform: translateY(-1px); }}
.card-src-tag {{ font-size: 0.7rem; color: var(--muted); }}

/* Pillar 2: Pro Table View */
.pro-table-wrap {{
    overflow-x: auto; background: var(--card); border: 1px solid var(--line);
    border-radius: 16px; margin-bottom: 30px; display: none;
}}
.pro-table {{ width: 100%; border-collapse: collapse; font-size: 0.84rem; text-align: left; }}
.pro-table th {{
    background: rgba(255,255,255,0.03); color: var(--text2); font-weight: 600;
    padding: 12px 14px; border-bottom: 1px solid var(--line); white-space: nowrap;
    cursor: pointer; user-select: none; transition: 0.15s;
}}
.pro-table th:hover {{ color: #fff; background: rgba(255,255,255,0.06); }}
.pro-table td {{ padding: 12px 14px; border-bottom: 1px solid var(--line); color: var(--text); vertical-align: middle; }}
.pro-table tr:hover {{ background: rgba(255,255,255,0.02); }}
.table-tk-box {{ display: flex; flex-direction: column; gap: 2px; }}
.table-company {{ font-size: 0.74rem; color: var(--muted); white-space: nowrap; max-width: 140px; overflow: hidden; text-overflow: ellipsis; }}
.table-grp-pill {{ font-size: 0.74rem; color: var(--text2); background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; white-space: nowrap; }}
.table-catalyst {{ font-size: 0.78rem; color: #93c5fd; max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.table-price {{ font-family: 'Inter', sans-serif; font-weight: 700; font-size: 0.95rem; }}
.table-supp {{ font-family: 'Inter', sans-serif; font-weight: 700; font-size: 0.95rem; }}
.table-dist {{ font-family: 'Inter', sans-serif; font-weight: 700; font-size: 0.95rem; }}
.table-sub {{ font-size: 0.7rem; color: var(--muted); }}
.table-chart-btn {{
    font-size: 0.75rem; font-weight: 600; color: var(--blue); text-decoration: none;
    background: rgba(96,165,250,0.1); border: 1px solid rgba(96,165,250,0.25);
    border-radius: 6px; padding: 4px 8px; white-space: nowrap;
}}
.table-chart-btn:hover {{ background: rgba(96,165,250,0.2); color: #fff; }}

/* Tab 2: Robotics Deep Analysis */
.robotics-container {{ display: flex; flex-direction: column; gap: 24px; margin-top: 10px; }}
.robotics-hero {{
    background: linear-gradient(135deg, rgba(30,58,138,0.25), rgba(15,23,42,0.95));
    border: 1px solid rgba(96,165,250,0.3); border-radius: 16px; padding: 20px 24px;
}}
.robotics-hero h2 {{ font-size: 1.35rem; color: #fff; margin-bottom: 6px; display: flex; align-items: center; gap: 10px; }}
.robotics-hero p {{ font-size: 0.88rem; color: var(--text2); line-height: 1.6; }}
.hero-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-top: 16px; }}
.hero-stat-card {{ background: rgba(255,255,255,0.04); border: 1px solid var(--line); border-radius: 12px; padding: 12px 16px; }}
.hero-stat-num {{ font-size: 1.4rem; font-weight: 700; font-family: 'Inter', sans-serif; color: var(--gold); }}
.hero-stat-lbl {{ font-size: 0.78rem; color: var(--muted); margin-top: 2px; }}

.deep-table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 14px; background: var(--card); }}
.deep-table {{ width: 100%; border-collapse: collapse; font-size: 0.84rem; text-align: left; }}
.deep-table th {{ background: rgba(255,255,255,0.03); color: var(--text2); font-weight: 600; padding: 12px 14px; border-bottom: 1px solid var(--line); white-space: nowrap; }}
.deep-table td {{ padding: 12px 14px; border-bottom: 1px solid var(--line); color: var(--text); vertical-align: middle; }}
.deep-table tr:hover {{ background: rgba(255,255,255,0.02); }}
.deep-table tr.culled-row {{ opacity: 0.6; background: rgba(244,63,94,0.04); }}
.deep-badge {{ display: inline-block; font-size: 0.72rem; font-weight: 600; padding: 2px 8px; border-radius: 6px; }}
.deep-badge-rank1 {{ background: rgba(251,191,36,0.15); color: var(--gold); border: 1px solid rgba(251,191,36,0.4); }}
.deep-badge-rank2 {{ background: rgba(96,165,250,0.15); color: var(--blue); border: 1px solid rgba(96,165,250,0.4); }}
.deep-badge-rank3 {{ background: rgba(16,185,129,0.15); color: var(--emerald); border: 1px solid rgba(16,185,129,0.4); }}
.deep-badge-culled {{ background: rgba(244,63,94,0.15); color: var(--rose); border: 1px solid rgba(244,63,94,0.4); }}

.strategy-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }}
.strat-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 18px 20px; display: flex; flex-direction: column; gap: 12px; border-top: 4px solid var(--blue); }}
.strat-card-adi {{ border-top-color: var(--gold); }}
.strat-card-mpwr {{ border-top-color: var(--blue); }}
.strat-card-txn {{ border-top-color: var(--emerald); }}
.strat-header {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.strat-title {{ font-size: 1.15rem; font-weight: 700; color: #fff; }}
.strat-sub {{ font-size: 0.8rem; color: var(--text2); }}
.strat-points {{ display: flex; flex-direction: column; gap: 8px; font-size: 0.82rem; color: var(--text2); }}
.strat-points strong {{ color: var(--text); }}
.strat-box {{ background: rgba(255,255,255,0.03); border: 1px solid var(--line); border-radius: 10px; padding: 10px 14px; font-size: 0.8rem; }}
.strat-box-val {{ font-weight: 600; color: var(--emerald); font-family: 'Inter', sans-serif; }}
.strat-box-warn {{ color: var(--rose); font-weight: 600; }}

.cull-table-wrap {{ overflow-x: auto; border: 1px solid rgba(244,63,94,0.25); border-radius: 14px; background: var(--card); }}
.cull-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
.cull-table th {{ background: rgba(244,63,94,0.08); color: #fecdd3; padding: 10px 12px; border-bottom: 1px solid rgba(244,63,94,0.2); }}
.cull-table td {{ padding: 10px 12px; border-bottom: 1px solid var(--line); color: var(--text2); }}

/* Details Modal & Disclaimer */
details.more {{ margin-top: 30px; background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 14px 18px; }}
details.more summary {{ cursor: pointer; font-weight: 600; color: var(--text2); }}
details.more .inner {{ margin-top: 12px; font-size: 0.85rem; color: var(--text2); }}
details.more ul {{ padding-left: 20px; margin: 6px 0 12px; }}
details.more h3 {{ font-size: 0.92rem; color: var(--gold); margin: 12px 0 4px; }}
.thumb {{ display: flex; gap: 14px; align-items: center; flex-wrap: wrap; margin-top: 8px; }}
.thumb img {{ width: 160px; max-width: 100%; border-radius: 8px; cursor: zoom-in; border: 1px solid var(--line); }}
code {{ background: rgba(255,255,255,0.06); padding: 1px 5px; border-radius: 4px; font-size: 0.8rem; }}

.modal-overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 1000; align-items: center; justify-content: center; padding: 20px; }}
.modal-overlay.open {{ display: flex; }}
.modal-content {{ position: relative; max-width: 95vw; max-height: 92vh; overflow: auto; background: var(--card); border-radius: 12px; padding: 10px; }}
.modal-img {{ max-width: 100%; display: block; }}
.modal-close {{ position: absolute; top: 6px; right: 10px; background: none; border: none; color: #fff; font-size: 1.8rem; cursor: pointer; }}

/* Sticky First Column for Pro Table on mobile scroll */
.pro-table th:first-child,
.pro-table td:first-child {{
    position: sticky;
    left: 0;
    z-index: 2;
    background: var(--card);
    box-shadow: 2px 0 8px rgba(0,0,0,0.35);
}}
.pro-table th:first-child {{
    z-index: 3;
    background: #142038;
}}
.pro-table tr:hover td:first-child {{
    background: var(--card2);
}}

/* Tablet Adaptive Breakpoint (769px - 1024px) */
@media (min-width: 769px) and (max-width: 1024px) {{
    .radar-ribbon {{ grid-template-columns: repeat(2, 1fr); gap: 12px; }}
    .cards-grid {{ grid-template-columns: repeat(2, 1fr); gap: 14px; }}
    .strategy-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .toolbar {{ gap: 10px; }}
    .search-box {{ flex: 1 1 180px; }}
}}

/* Desktop Large (> 1025px) */
@media (min-width: 1025px) {{
    .radar-ribbon {{ grid-template-columns: repeat(4, 1fr); }}
    .cards-grid {{ grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); }}
    .strategy-grid {{ grid-template-columns: repeat(3, 1fr); }}
}}

/* Mobile Adaptive Breakpoint (<= 768px) */
@media (max-width: 768px) {{
    body {{ padding: 12px; }}
    h1 {{ font-size: 1.35rem; }}
    .top-header {{ margin-bottom: 14px; }}
    .lead {{ font-size: 0.88rem; }}
    .meta {{ gap: 8px; font-size: 0.78rem; }}

    /* Main Navigation Tabs touch target */
    .main-tabs {{ gap: 6px; margin: 14px 0 18px; }}
    .main-tab-btn {{ font-size: 0.85rem; padding: 10px 14px; min-height: 44px; }}

    /* Pillar 1: Radar Ribbon 2 columns on mobile */
    .radar-ribbon {{ grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 16px; }}
    .ribbon-card {{ padding: 12px 14px; min-height: 120px; }}
    .ribbon-title {{ font-size: 0.75rem; }}
    .ribbon-num {{ font-size: 1.6rem; margin: 4px 0; }}
    .ribbon-sub {{ font-size: 0.7rem; line-height: 1.3; }}
    .ribbon-preview {{ display: none; }}
    .health-legend {{ font-size: 0.68rem; }}

    /* Pillar 3: Theme Pills Touch-friendly Scroll */
    .pills-container {{ margin-bottom: 14px; scroll-padding: 10px; }}
    .pill-btn {{ min-height: 40px; padding: 8px 14px; font-size: 0.8rem; }}

    /* Toolbar & Search Bar on Mobile */
    .toolbar {{ flex-direction: column; align-items: stretch; gap: 10px; padding: 12px; margin-bottom: 16px; }}
    .search-box {{ width: 100%; flex: 1 1 auto; }}
    .search-box input {{ height: 44px; font-size: 0.88rem; }}
    .view-toggle-group {{ width: 100%; display: grid; grid-template-columns: 1fr 1fr; height: 44px; }}
    .view-btn {{ justify-content: center; font-size: 0.88rem; height: 100%; }}
    .row-count-chip {{ width: 100%; text-align: center; margin-left: 0; font-size: 0.78rem; }}

    /* Pillar 2: Cards Grid Single Column on Mobile */
    .cards-grid {{ grid-template-columns: 1fr; gap: 12px; }}
    .stock-card {{ padding: 14px; }}
    .card-price-grid {{ grid-template-columns: 1fr 1fr 1fr; gap: 6px; padding: 8px 10px; }}
    .card-val {{ font-size: 0.95rem; }}
    .btn-chart-link {{ min-height: 40px; padding: 8px 14px; font-size: 0.84rem; }}

    /* Tab 2: Robotics Strategy Grid & Hero on Mobile */
    .robotics-hero {{ padding: 16px 18px; }}
    .robotics-hero h2 {{ font-size: 1.15rem; }}
    .hero-stats {{ grid-template-columns: 1fr; gap: 10px; }}
    .strategy-grid {{ grid-template-columns: 1fr; gap: 12px; }}
    .strat-card {{ padding: 14px 16px; }}
}}

/* Extra Small Mobile (<= 480px) */
@media (max-width: 480px) {{
    .radar-ribbon {{ grid-template-columns: 1fr; gap: 8px; }}
    .card-price-grid {{ grid-template-columns: 1fr 1fr; gap: 8px; }}
    .card-price-grid > div:last-child {{ grid-column: span 2; text-align: left; }}
}}
</style>
</head>
<body>
{nav_html}
<div class="container">
    <div class="top-header">
        <h1>📋 หุ้นที่สนใจ (Watchlist)</h1>
        <p class="lead">เรดาร์ติดตามหุ้นคุณภาพสูง 44 ตัวตามกรอบแนวรับสำคัญ เพื่อจับจังหวะเข้าซื้อในระดับราคาที่ปลอดภัย</p>
        <div class="meta">
            <span class="meta-chip">🕒 ข้อมูลราคา: <strong>{fetch_time}</strong> ({price_note})</span>
            <span class="meta-chip">⭐ ในพอร์ตจริง: <strong>{port_count} ตัว</strong></span>
            <span class="meta-chip">🎯 ในโซนซื้อ 0-5%: <strong>{cnt_b} ตัว</strong></span>
        </div>
    </div>
    {alert_banner}

    <!-- Main Navigation Tabs -->
    <div class="main-tabs">
        <button class="main-tab-btn active" id="tab-btn-watchlist" onclick="switchMainTab('watchlist')">
            📋 เรดาร์หุ้นและแนวรับ ({total} ตัว)
        </button>
        <button class="main-tab-btn" id="tab-btn-robotics" onclick="switchMainTab('robotics')">
            🤖 เจาะลึกชิปหุ่นยนต์ & Physical AI (BOM $7,200) <span class="tab-badge">Hot</span>
        </button>
    </div>

    <!-- Tab 1: Watchlist & Radar View -->
    <div id="view-watchlist">
        <!-- Pillar 1: Market Radar & Executive Metric Ribbon -->
        <div class="radar-ribbon">
            <!-- Card 1: Buy Zone Ready -->
            <div class="ribbon-card ribbon-card-buy" onclick="filterByPill('buy')" style="cursor:pointer;" title="คลิกเพื่อกรองเฉพาะหุ้นในโซนซื้อ">
                <div class="ribbon-top">
                    <span class="ribbon-title"><span>🎯</span> พร้อมเข้าซื้อ (Buy Zone 0-5%)</span>
                    <span class="status-pill status-emerald">จุดซื้อทันที</span>
                </div>
                <div class="ribbon-num">{cnt_b}</div>
                <div class="ribbon-sub">ราคาอยู่เหนือแนวรับ 0-5% พร้อมตั้ง Limit Order</div>
                <div class="ribbon-preview">{buy_zone_preview}</div>
            </div>

            <!-- Card 2: Broken Support -->
            <div class="ribbon-card ribbon-card-broken" onclick="filterByStatus('A')" style="cursor:pointer;" title="คลิกเพื่อกรองหุ้นที่หลุดแนวรับ">
                <div class="ribbon-top">
                    <span class="ribbon-title"><span>🔻</span> หลุดแนวรับแล้ว (&lt; 0%)</span>
                    <span class="status-pill status-rose">ห้ามรับมีด</span>
                </div>
                <div class="ribbon-num">{cnt_a}</div>
                <div class="ribbon-sub">แนวรับเดิมแตกแล้ว รอราคายืนกลับเหนือเส้นเฉลี่ย</div>
            </div>

            <!-- Card 3: Far from Support -->
            <div class="ribbon-card ribbon-card-far" onclick="filterByStatus('C')" style="cursor:pointer;" title="คลิกเพื่อกรองหุ้นที่ยังไกล">
                <div class="ribbon-top">
                    <span class="ribbon-title"><span>⏳</span> ยังไกลจากแนวรับ (&gt; 5%)</span>
                    <span class="status-pill status-slate">รอจังหวะย่อ</span>
                </div>
                <div class="ribbon-num">{cnt_c}</div>
                <div class="ribbon-sub">ยังไม่ถึงจุดเข้าซื้อ อดทนรอราคาย่อตัวลงมาทดสอบ</div>
            </div>

            <!-- Card 4: Health Gauge & Highlights -->
            <div class="ribbon-card ribbon-card-health">
                <div class="ribbon-top">
                    <span class="ribbon-title"><span>📊</span> สัดส่วนสุขภาพ Watchlist</span>
                    <span style="font-size:0.75rem;color:var(--gold);font-weight:700;">{cnt_b}/{total} ตัว</span>
                </div>
                <div class="health-bar-container">
                    <div class="health-bar">
                        <div class="hb-seg hb-emerald" style="width:{pct_b:.1f}%" title="ในจุดซื้อ: {pct_b:.1f}%"></div>
                        <div class="hb-seg hb-slate" style="width:{pct_c:.1f}%" title="ยังไกล: {pct_c:.1f}%"></div>
                        <div class="hb-seg hb-rose" style="width:{pct_a:.1f}%" title="หลุดแนวรับ: {pct_a:.1f}%"></div>
                    </div>
                    <div class="health-legend">
                        <span>🟢 จุดซื้อ {pct_b:.0f}%</span>
                        <span>⚪ รอ {pct_c:.0f}%</span>
                        <span>🔴 หลุด {pct_a:.0f}%</span>
                    </div>
                </div>
                <div style="font-size:0.74rem;color:var(--text2);margin-top:4px;">
                    ✨ <strong>AEHR</strong> Super Turnaround | 👑 <strong>ADI</strong> ชิปหุ่นยนต์ #1
                </div>
            </div>
        </div>

        <!-- Pillar 3: Theme & Sector Filter Pills -->
        <div class="pills-container">
            <div class="pills-bar">
                {''.join(pills_html)}
            </div>
        </div>

        <!-- Toolbar: Search, Portfolio Toggle & Dual View Mode -->
        <div class="toolbar">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="search" id="watchlist-search" placeholder="ค้นหา Ticker, ชื่อบริษัท หรือตัวเร่ง (Catalyst)..." oninput="handleSearch(this.value)">
            </div>

            <!-- Pillar 2: Dual View Switcher -->
            <div class="view-toggle-group">
                <button class="view-btn active" id="btn-view-grid" onclick="setViewMode('grid')">
                    <span>🗂️</span> Grid Cards
                </button>
                <button class="view-btn" id="btn-view-table" onclick="setViewMode('table')">
                    <span>📊</span> Pro Table
                </button>
            </div>

            <div class="row-count-chip" id="row-count-display">แสดง {total} จาก {total} ตัว</div>
        </div>

        <!-- View 1: Grid Cards View -->
        <div id="view-grid" class="cards-grid">
            {''.join(grid_cards_html)}
        </div>

        <!-- View 2: Pro Table View -->
        <div id="view-table" class="pro-table-wrap">
            <table class="pro-table" id="pro-watchlist-table">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Ticker & บริษัท ⬍</th>
                        <th onclick="sortTable(1)">กลุ่ม (Group) ⬍</th>
                        <th>ตัวเร่งทางธุรกิจ (Catalyst)</th>
                        <th onclick="sortTable(3)">ราคาตอนนี้ ⬍</th>
                        <th onclick="sortTable(4)">แนวรับ ⬍</th>
                        <th onclick="sortTable(5)">ระยะห่าง (%) ⬍</th>
                        <th>เรดาร์วัดระยะ</th>
                        <th onclick="sortTable(7)">สถานะ ⬍</th>
                        <th>ดูกราฟ</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(table_rows_html)}
                </tbody>
            </table>
        </div>

        <!-- Details & Methodology -->
        <details class="more">
            <summary>ที่มาของแนวรับ วิธีคำนวณ และข้อจำกัดความเสี่ยง</summary>
            <div class="inner">
                <h3>⚠️ ข้อจำกัดและคำเตือนสำคัญ (Risk Disclaimer)</h3>
                <ul>
                    <li><strong>แนวรับ Fibo จากภาพยังไม่ผ่าน backtest:</strong> เป็นการประเมินโซนราคาทางเทคนิคจากภายนอก ห้ามนำไปใช้เป็นคะแนนในระบบหลัก (Unified Score) และห้ามใช้บล็อกการซื้อขาย</li>
                    <li><strong>สภาพคล่องช่วง Premarket ต่ำ:</strong> ราคาซื้อขายนอกเวลาทำการปกติมีความผันผวนสูงและมี Spread กว้าง โปรดใช้ความระมัดระวัง</li>
                    <li><strong>ไม่ใช่คำแนะนำการลงทุน:</strong> ข้อมูลนี้จัดทำเพื่อการติดตามและศึกษา Risk/Reward เท่านั้น ผู้ลงทุนต้องวิเคราะห์ปัจจัยพื้นฐานและความเสี่ยงด้วยตนเอง</li>
                </ul>
                <h3>วิธีคำนวณระยะห่าง</h3>
                <p>ระยะห่าง = <code>((ราคา - แนวรับ) / แนวรับ) × 100</code>. ราคาที่ใช้คือ Premarket ถ้ามี ต่อด้วย Postmarket แล้วจึงเป็นราคาปิด. แถบแสดงช่วง ±{GAUGE_RANGE_PCT:.0f}% ถ้าเกินนั้นจุดจะอยู่ที่ขอบ.</p>
                <h3>ที่มาของแนวรับ</h3>
                <div class="thumb">
                    <img src="assets/shay_fibo_support_2026-10-17.jpeg" alt="Fibo Support" onclick="openImageModal()">
                    <p>แนวรับ Fibonacci ส่วนใหญ่มาจาก <strong>{SOURCE_AUTHOR}</strong> (อัปเดต {analyzed['source_updated']}).
                    ตัวที่มีบรรทัด "แนวรับจาก ..." ใต้ชื่อเป็นแนวรับที่กำหนดเอง เช่น ชิปหุ่นยนต์จากการดีเบต หรือแผน ETF. คลิกภาพเพื่อขยาย.</p>
                </div>
            </div>
        </details>
    </div>

    <!-- Tab 2: Physical AI & Robotics Deep Analysis -->
    <div id="view-robotics" class="robotics-container" style="display:none;">
        <div class="robotics-hero">
            <h2>🤖 วิเคราะห์เจาะลึกชิป Physical AI & Humanoid Robotics (BOM $7,200)</h2>
            <p>สรุปผลการวิเคราะห์และ Debate ข้ามเทอร์มินัลระหว่าง 2 AI Agents เพื่อคัดสรร 3 หุ้นชิปที่ดีที่สุดตามประมาณการ Bill of Materials (BOM) ชิปแอนะล็อกและพลังงานมูลค่า $7,200 ต่อตัวหุ่นยนต์ของ <strong>Morgan Stanley</strong> ภายในปี 2030 พร้อมแผนกลยุทธ์ราคาเข้าซื้อและจุดตัดขาดทุนจริงในตลาดปัจจุบัน.</p>
            <div class="hero-stats">
                <div class="hero-stat-card">
                    <div class="hero-stat-num">$7,200</div>
                    <div class="hero-stat-lbl">มูลค่าชิป Analog & Power ต่อตัว</div>
                </div>
                <div class="hero-stat-card">
                    <div class="hero-stat-num">22.6%</div>
                    <div class="hero-stat-lbl">สัดส่วนสูงสุดโดย ADI ($1,625)</div>
                </div>
                <div class="hero-stat-card">
                    <div class="hero-stat-num">1 : 5.1</div>
                    <div class="hero-stat-lbl">Risk/Reward สูงสุด (TXN รับ EMA200)</div>
                </div>
            </div>
        </div>

        <div>
            <h3 style="font-size:1.15rem;margin-bottom:12px;color:var(--text);display:flex;align-items:center;gap:8px;">
                <span>📊</span> ตารางเปรียบเทียบชิปหุ่นยนต์ชั้นนำ (The Semiconductor Face-Off)
            </h3>
            <div class="deep-table-wrap">
                <table class="deep-table">
                    <thead>
                        <tr>
                            <th>Ticker</th>
                            <th>บริษัท</th>
                            <th>บทบาทในหุ่นยนต์ (Role)</th>
                            <th>BOM Content ($ & %)</th>
                            <th>Gross Margin</th>
                            <th>Operating Margin</th>
                            <th>D/E Ratio</th>
                            <th>Forward P/E</th>
                            <th>สถานะ & คำตัดสิน Debate</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong style="color:var(--gold);font-size:1rem;">ADI</strong></td>
                            <td>Analog Devices</td>
                            <td>ตัวควบคุมมอเตอร์ความแม่นยำสูง, แอนะล็อกแปลงสัญญาณ, BMS, Magnetic Encoders</td>
                            <td><strong>$1,625</strong> <span style="color:var(--gold);">(22.6%)</span></td>
                            <td>67.3%</td>
                            <td>39.5%</td>
                            <td>0.27</td>
                            <td>~26.0x</td>
                            <td><span class="deep-badge deep-badge-rank1">👑 อันดับ 1 (คุณภาพ & คูเมืองสูงสุด)</span></td>
                        </tr>
                        <tr>
                            <td><strong style="color:var(--blue);font-size:1rem;">MPWR</strong></td>
                            <td>Monolithic Power Systems</td>
                            <td>Monolithic BCD ย่อขนาด Power Stage ในข้อต่อหุ่นยนต์, ไดรเวอร์มอเตอร์ MP65xx</td>
                            <td><strong>$400 - $550</strong> <span style="color:var(--text2);">(~7%)</span></td>
                            <td>55.4%</td>
                            <td>28.2%</td>
                            <td>0.01 (Net Cash)</td>
                            <td>50 - 54x</td>
                            <td><span class="deep-badge deep-badge-rank2">🚀 อันดับ 2 (เติบโตสูงสุดใน AI DC & ข้อต่อ)</span></td>
                        </tr>
                        <tr>
                            <td><strong style="color:var(--emerald);font-size:1rem;">TXN</strong></td>
                            <td>Texas Instruments</td>
                            <td>ชิปแอนะล็อกและพลังงานความจุสูง ผลิตด้วยเวเฟอร์ 300mm ต้นทุนต่ำกว่าคู่แข่ง 40%</td>
                            <td><strong>$600 - $750</strong> <span style="color:var(--text2);">(~10%)</span></td>
                            <td>60.1%</td>
                            <td>38.2%</td>
                            <td>0.58</td>
                            <td>~27.0x (ที่ EMA200)</td>
                            <td><span class="deep-badge deep-badge-rank3">🛡️ อันดับ 3 (ตัวแทนตลาดสหรัฐฯ แกร่งสุด)</span></td>
                        </tr>
                        <tr>
                            <td><strong style="color:#a78bfa;font-size:1rem;">IFX</strong></td>
                            <td>Infineon Technologies</td>
                            <td>เบอร์ 1 ชิปพลังงานโลก (MOSFET/GaN/SiC Modules) ครองหุ่นยนต์โรงงานยุโรป/ญี่ปุ่น</td>
                            <td><strong>$1,094</strong> <span style="color:var(--text2);">(15.2%)</span></td>
                            <td>42.5%</td>
                            <td>20.8%</td>
                            <td>0.45</td>
                            <td>~16.0x</td>
                            <td><span class="deep-badge" style="background:rgba(167,139,250,0.15);color:#a78bfa;border:1px solid rgba(167,139,250,0.4);">🌐 อันดับ 3 ร่วม (ตลาดต่างประเทศ / ADR)</span></td>
                        </tr>
                        <tr class="culled-row">
                            <td><strong style="color:var(--rose);font-size:1rem;">ON</strong></td>
                            <td>ON Semiconductor</td>
                            <td>Image Sensors สำหรับสายตาหุ่นยนต์ และชิปกำลัง SiC สำหรับมอเตอร์ข้อต่อ</td>
                            <td><strong>$1,125</strong> <span style="color:var(--rose);">(15.6%)</span></td>
                            <td>36 - 41%</td>
                            <td>19.2%</td>
                            <td>0.62</td>
                            <td>36.8x TTM</td>
                            <td><span class="deep-badge deep-badge-culled">❌ คัดออกจากการดีเบต (มาร์จิ้นทรุด & สงครามราคา SiC)</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div>
            <h3 style="font-size:1.15rem;margin-bottom:12px;color:var(--text);display:flex;align-items:center;gap:8px;">
                <span>🎯</span> แผนกลยุทธ์ราคาเข้าซื้อและจุดตัดขาดทุน (Actionable Entry Strategy)
            </h3>
            <div class="strategy-grid">
                <!-- ADI Card -->
                <div class="strat-card strat-card-adi">
                    <div class="strat-header">
                        <div>
                            <div class="strat-title">ADI — Analog Devices</div>
                            <div class="strat-sub">ราคาปัจจุบัน $363.56 | EMA200 $365.67 | RSI 36.2</div>
                        </div>
                        <span class="deep-badge deep-badge-rank1">อันดับ 1</span>
                    </div>
                    <div class="strat-points">
                        <div>• <strong>พฤติกรรมราคา:</strong> ราคาลงมาทดสอบเส้น EMA200 พอดี และ RSI ใกล้แตะเขต Oversold (&lt;35).</div>
                        <div>• <strong>กลยุทธ์เข้าซื้อ:</strong> ใช้แผนแบ่งไม้ 2 ไม้ เพื่อแก้ปัญหาตกรถและคุมความเสี่ยงขาลง.</div>
                        <div class="strat-box">
                            <div><strong>ไม้ที่ 1 (สัดส่วน 30%):</strong> โซน <span class="strat-box-val">$360 - $365</span> เมื่อเกิดสัญญาณแท่งเทียนกลับตัวหรือ RSI Hook ดีดพ้น 38.</div>
                            <div style="margin-top:4px;"><strong>ไม้ที่ 2 (สัดส่วน 70%):</strong> ตั้งรับที่แนวรับใหญ่ <span class="strat-box-val">$338 - $348</span> (Forward P/E ลดเหลือ 24x).</div>
                            <div style="margin-top:4px;"><strong>จุดตัดขาดทุน (Stop Loss):</strong> หลุดต่ำกว่า <span class="strat-box-warn">$328</span> (-8.5%).</div>
                        </div>
                    </div>
                </div>

                <!-- MPWR Card -->
                <div class="strat-card strat-card-mpwr">
                    <div class="strat-header">
                        <div>
                            <div class="strat-title">MPWR — Monolithic Power</div>
                            <div class="strat-sub">ราคาปัจจุบัน $1,190.44 | EMA200 $1,257.87 | RSI 45.0</div>
                        </div>
                        <span class="deep-badge deep-badge-rank2">อันดับ 2</span>
                    </div>
                    <div class="strat-points">
                        <div>• <strong>พฤติกรรมราคา:</strong> ราคาหลุดใต้เส้น EMA200 และมีความผันผวน ATR สูงถึง $79.68 ต่อวัน.</div>
                        <div>• <strong>กฎเหล็ก:</strong> ห้ามรับมีดเด็ดขาดในขณะที่แท่งราคายังอยู่ใต้เส้นเฉลี่ย EMA200.</div>
                        <div class="strat-box">
                            <div><strong>แผน A (สายดักซื้อของถูก):</strong> ตั้งรับลึกที่แนวรับจิตวิทยา <span class="strat-box-val">$1,050 - $1,100</span> (Forward P/E ลดเหลือ 45x). ตัดขาดทุนหลุด <span class="strat-box-warn">$990</span>.</div>
                            <div style="margin-top:4px;"><strong>แผน B (สายเทรดคอนเฟิร์มกลับตัว):</strong> ซื้อเมื่อราคาปิดวันยืนเหนือ <span class="strat-box-val">$1,260</span> พร้อม RSI เกิน 50. ตัดขาดทุนหลุด <span class="strat-box-warn">$1,190</span>.</div>
                        </div>
                    </div>
                </div>

                <!-- TXN Card -->
                <div class="strat-card strat-card-txn">
                    <div class="strat-header">
                        <div>
                            <div class="strat-title">TXN — Texas Instruments</div>
                            <div class="strat-sub">ราคาปัจจุบัน $277.36 | EMA200 $261.76 | RSI 42.5</div>
                        </div>
                        <span class="deep-badge deep-badge-rank3">อันดับ 3</span>
                    </div>
                    <div class="strat-points">
                        <div>• <strong>พฤติกรรมราคา:</strong> เพิ่งทุบลงมาจาก $311 ใน 2 วัน โดยราคาอยู่ห่างจาก EMA200 เพียง 5.6% (1 วัน ATR).</div>
                        <div>• <strong>กลยุทธ์เข้าซื้อ:</strong> ไม่ไล่ซื้อที่ราคาปัจจุบัน แต่ตั้ง Limit Order รอรับที่ขอบบน EMA200.</div>
                        <div class="strat-box">
                            <div><strong>จุดเข้าซื้อ (Limit Order):</strong> โซน <span class="strat-box-val">$260 - $268</span> (ต้นทุนเฉลี่ยคาดหวัง $262, Forward P/E 27x).</div>
                            <div style="margin-top:4px;"><strong>จุดตัดขาดทุน (Stop Loss):</strong> หลุดต่ำกว่า <span class="strat-box-warn">$248</span> (ความเสี่ยง -5.3%).</div>
                            <div style="margin-top:4px;"><strong>เป้าหมายทำกำไร (Target):</strong> จุดสูงสุดเดิม <span class="strat-box-val">$334</span> (อัปไซด์ +27.5%).</div>
                            <div style="margin-top:4px;color:var(--gold);"><strong>Risk / Reward Ratio:</strong> สูงถึง <span style="font-weight:700;">1 ต่อ 5.1</span> (คุ้มค่าที่สุดในกลุ่ม).</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div>
            <h3 style="font-size:1.15rem;margin-bottom:12px;color:var(--rose);display:flex;align-items:center;gap:8px;">
                <span>🗑️</span> บันทึกการทบทวนและคัดหุ้นออกจาก Watchlist (Cull Log 2026-11-07)
            </h3>
            <div class="cull-table-wrap">
                <table class="cull-table">
                    <thead>
                        <tr>
                            <th>Ticker</th>
                            <th>กลุ่มเดิม</th>
                            <th>แนวรับเดิม</th>
                            <th>ราคาล่าสุด</th>
                            <th>สถานะงบการเงินจริง</th>
                            <th>มติจากการ Debate (เหตุผลที่คัดออก)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong style="color:var(--text);">ON</strong></td>
                            <td>AI Power</td>
                            <td>$72.00</td>
                            <td>$63.31</td>
                            <td>Gross Margin ร่วงเหลือ 36-41%, ขาดทุนต้นปี 2026</td>
                            <td>หลุดแนวรับรุนแรง, ภาระค่าเสื่อมโรงงาน IDM และสงครามราคา SiC จากผู้ผลิตจีนตัดส่วนแบ่ง</td>
                        </tr>
                        <tr>
                            <td><strong style="color:var(--text);">NVTS</strong></td>
                            <td>AI Power</td>
                            <td>$8.00</td>
                            <td>$8.61</td>
                            <td>Operating Margin -222.8%, FCF -$19.2M</td>
                            <td>บริษัทเผาเงินสดหนักต่อเนื่อง ขาดทุนบานปลาย ไม่ผ่านเกณฑ์พื้นฐานสำหรับการลงทุน</td>
                        </tr>
                        <tr>
                            <td><strong style="color:var(--text);">QBTS</strong></td>
                            <td>Quantum</td>
                            <td>$10.00</td>
                            <td>$10.68</td>
                            <td>Operating Margin -1,732.1%, ขาดทุน -$48.0M</td>
                            <td>หุ้นเก็งกำไรขนาดเล็ก อัตราการเผาเงินสดสูงลิบลิ่ว และเทรดต่ำกว่าเส้น SMA200</td>
                        </tr>
                        <tr>
                            <td><strong style="color:var(--text);">RGTI</strong></td>
                            <td>Quantum</td>
                            <td>$11.00</td>
                            <td>$11.75</td>
                            <td>Operating Margin -546.2%, ขาดทุน -$52.6M</td>
                            <td>ผลขาดทุนสุทธิสูงกว่ารายได้เกือบ 10 เท่า ธุรกิจยังไม่สามารถทำกำไรในระดับอุตสาหกรรมได้</td>
                        </tr>
                        <tr>
                            <td><strong style="color:var(--text);">INFQ</strong></td>
                            <td>Quantum</td>
                            <td>$8.00</td>
                            <td>$8.89</td>
                            <td>Operating Margin -220.5%, ขาดทุน -$24.7M</td>
                            <td>มาร์จิ้นติดลบลึก ขาดทุนเรื้อรัง จึงคงเหลือเพียง IONQ ตัวเดียวในกลุ่ม Quantum ที่การเงินแกร่งสุด</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="margin-top:16px;padding:14px 18px;background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);border-radius:10px;font-size:0.875rem;line-height:1.6;color:var(--text);">
                <div style="font-weight:700;color:var(--emerald);display:flex;align-items:center;gap:6px;margin-bottom:4px;">
                    <span>✨</span> บันทึกการทบทวนพิเศษ (AEHR Reinstatement & Turnaround)
                </div>
                ตรวจสอบงบล่าสุดไตรมาส Q1 FY2027 พบผลการดำเนินงานพลิกฟื้นแบบ Super Turnaround: รายได้ทำสถิติสูงสุดใหม่ $33.0M (+200% YoY, +75% QoQ), พลิกมีกำไรสุทธิ GAAP EPS $0.21 (Non-GAAP $0.28 ชนะคาดการณ์เกือบ 3 เท่า), ยอดจอง $46.7M (Book-to-Bill 1.4x) และ Backlog All-Time High $109.3M จากความต้องการทดสอบ AI Wafer Burn-in (FOX-P & Sonoma) จึงมีมติเอกฉันท์ <strong>ดึง AEHR กลับเข้า Watchlist กลุ่ม Photonics</strong> ทันที ที่แนวรับเดิม $57.00 โดยวางจุด Stop Loss ที่ $48.50 และเป้าหมาย Rebound เส้น EMA200 ที่ $72.80 (R:R 1 : 3.8).
            </div>
        </div>
    </div>
</div>

<div class="modal-overlay" id="image-modal" onclick="closeImageModal(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
        <button class="modal-close" onclick="closeImageModal()">&times;</button>
        <img src="assets/shay_fibo_support_2026-10-17.jpeg" alt="Fibo Support Large" class="modal-img">
    </div>
</div>

<script>
let currentStatus = 'all', currentGroup = 'all', currentSearch = '', currentPortOnly = false;
let currentViewMode = localStorage.getItem('watchlist_view_mode') || 'grid';

function setViewMode(mode) {{
    currentViewMode = mode;
    localStorage.setItem('watchlist_view_mode', mode);
    const isGrid = (mode === 'grid');
    document.getElementById('view-grid').style.display = isGrid ? 'grid' : 'none';
    document.getElementById('view-table').style.display = isGrid ? 'none' : 'block';
    document.getElementById('btn-view-grid').classList.toggle('active', isGrid);
    document.getElementById('btn-view-table').classList.toggle('active', !isGrid);
}}

function switchMainTab(tab) {{
    const isWatch = (tab === 'watchlist');
    document.getElementById('view-watchlist').style.display = isWatch ? '' : 'none';
    document.getElementById('view-robotics').style.display = isWatch ? 'none' : '';
    document.getElementById('tab-btn-watchlist').classList.toggle('active', isWatch);
    document.getElementById('tab-btn-robotics').classList.toggle('active', !isWatch);
}}

function applyFilters() {{
    const cards = document.querySelectorAll('.stock-card');
    const tableRows = document.querySelectorAll('.table-row');
    let visible = 0;

    function checkItem(el) {{
        const ok = (currentStatus === 'all' || el.dataset.status === currentStatus)
            && (!currentPortOnly || el.dataset.portfolio === 'true')
            && (currentGroup === 'all' || el.dataset.group === currentGroup)
            && (!currentSearch || el.dataset.ticker.toLowerCase().includes(currentSearch) || el.innerText.toLowerCase().includes(currentSearch));
        el.style.display = ok ? '' : 'none';
        return ok;
    }}

    cards.forEach(card => {{
        if (checkItem(card)) visible++;
    }});

    tableRows.forEach(row => {{
        checkItem(row);
    }});

    document.getElementById('row-count-display').textContent = `แสดง ${{visible}} จาก ${{cards.length}} ตัว`;
}}

function setActivePills() {{
    document.querySelectorAll('.pill-btn').forEach(btn => btn.classList.remove('active'));
    if (currentPortOnly) {{
        document.getElementById('pill-port')?.classList.add('active');
    }} else if (currentStatus === 'B') {{
        document.getElementById('pill-buy')?.classList.add('active');
    }} else if (currentGroup !== 'all') {{
        document.querySelector(`.pill-btn[data-group="${{currentGroup}}"]`)?.classList.add('active');
    }} else {{
        document.getElementById('pill-all')?.classList.add('active');
    }}
}}

function filterByPill(pill) {{
    if (pill === 'all') {{
        currentStatus = 'all'; currentGroup = 'all'; currentPortOnly = false;
    }} else if (pill === 'buy') {{
        currentStatus = 'B'; currentGroup = 'all'; currentPortOnly = false;
    }} else if (pill === 'port') {{
        currentPortOnly = true; currentStatus = 'all'; currentGroup = 'all';
    }} else {{
        currentGroup = pill; currentStatus = 'all'; currentPortOnly = false;
    }}
    setActivePills();
    applyFilters();
}}

function filterByStatus(status) {{
    currentStatus = (status === currentStatus && status !== 'all') ? 'all' : status;
    currentGroup = 'all'; currentPortOnly = false;
    setActivePills();
    applyFilters();
}}

function handleSearch(q) {{
    currentSearch = (q || '').trim().toLowerCase();
    applyFilters();
}}

// Pro Table Sorting
let sortDirections = {{}};
function sortTable(colIndex) {{
    const table = document.getElementById('pro-watchlist-table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isAsc = !sortDirections[colIndex];
    sortDirections[colIndex] = isAsc;

    rows.sort((a, b) => {{
        let valA, valB;
        if (colIndex === 0) {{ // Ticker
            valA = a.dataset.ticker; valB = b.dataset.ticker;
        }} else if (colIndex === 1) {{ // Group
            valA = a.dataset.group; valB = b.dataset.group;
        }} else if (colIndex === 3) {{ // Price
            valA = parseFloat(a.cells[3].innerText.replace(/[^0-9.-]/g, '')) || 0;
            valB = parseFloat(b.cells[3].innerText.replace(/[^0-9.-]/g, '')) || 0;
        }} else if (colIndex === 4) {{ // Support
            valA = parseFloat(a.cells[4].innerText.replace(/[^0-9.-]/g, '')) || 0;
            valB = parseFloat(b.cells[4].innerText.replace(/[^0-9.-]/g, '')) || 0;
        }} else if (colIndex === 5) {{ // Pct Diff
            valA = parseFloat(a.dataset.pct) || 999999;
            valB = parseFloat(b.dataset.pct) || 999999;
        }} else if (colIndex === 7) {{ // Status
            valA = a.dataset.status; valB = b.dataset.status;
        }} else {{
            valA = a.cells[colIndex].innerText.trim();
            valB = b.cells[colIndex].innerText.trim();
        }}
        if (valA < valB) return isAsc ? -1 : 1;
        if (valA > valB) return isAsc ? 1 : -1;
        return 0;
    }});

    rows.forEach(r => tbody.appendChild(r));
}}

function openImageModal() {{ document.getElementById('image-modal').classList.add('open'); }}
function closeImageModal() {{ document.getElementById('image-modal').classList.remove('open'); }}
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeImageModal(); }});

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {{
    setViewMode(currentViewMode);
    setActivePills();
    applyFilters();
}});
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
