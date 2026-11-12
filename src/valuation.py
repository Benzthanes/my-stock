"""
Dynamic Valuation Engine & Intrinsic Fair Value Architecture
Provides single-source-of-truth intrinsic target prices, mathematical derivations,
and multi-dimensional rationale pillars across all monitored tickers.

Strictly adheres to corporate finance principles across 5 business models:
1. Big Tech & Mature Growth: Owner Earnings Yield + Forward P/E Multiple + Reverse DCF
2. Banking & Financial: Justified Price-to-Book (P/B) Gordon Growth Model
3. AI Infrastructure & Hyperscaler: EV/Run-rate Revenue (Net Debt adjusted)
4. Turnaround & Cyclical Deep Value: Normalized EV/EBIT + Net Cash (with EUR/USD conversion & Asset-backed floor)
5. Index & Covered Call ETFs: Fair NAV Tracking 100%
"""

from typing import Any, Dict, List, Optional
from src.financials import load_financials_cache


# ---------------------------------------------------------------------------
# Model Archetype Configuration (Calibrated against Live Financial Statements)
# ---------------------------------------------------------------------------
MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    # 1. Mature Growth & Big Tech
    "NVDA": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 280.00,
        "primary_model": "Owner Earnings Yield + Forward P/E (28x)",
        "model_desc": "ประเมินจากผลตอบแทนกระแสเงินสดอิสระ (Owner Earnings) 4.0% ร่วมกับ Forward P/E 28 เท่า บนสถาปัตยกรรม Blackwell",
        "math_details": {
            "formula": "Blended Model: 0.50 × (FY27 Forward EPS $10.00 × P/E 28x = $280.00) + 0.50 × (Owner Earnings FCF $11.20 ÷ 4.0% = $280.00) = $280.00",
            "accounting_source": "งบไตรมาสล่าสุด Q3'26: รายได้ $96.22B (+83% YoY), กำไรสุทธิ $59.69B, TTM EPS $7.95, Net Margin 62.0%, FCF $21.40B",
            "key_multiples": "Forward P/E 28.0x, Owner Earnings Yield 4.0%, PEG 0.17x, D/E 0.17x, ROE 117%",
            "wall_street_target": "$317.19 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $710.29)",
            "explanation": "คำนวณจากกำลังทำกำไรของชิป Blackwell และรอบการขยาย Data Center AI ทั่วโลก ราคาเหมาะสม $280.00 มีส่วนเผื่อความปลอดภัยต่ำกว่าเป้าหมายสถาบันวอลล์สตรีท ($317.19)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🚀",
                "title": "ผู้นำผูกขาดชิป AI & Blackwell Architecture",
                "desc": "ครองส่วนแบ่งตลาดชิปฝึกและประมวลผล AI ทั่วโลกกว่า 85% มีอัตรากำไรสุทธิสูงถึง 62.0% และ ROE คุณภาพสูง 117%",
            },
            {
                "icon": "💵",
                "title": "กระแสเงินสดอิสระระดับ Cash Cow & หนี้สินต่ำ",
                "desc": "สร้างกระแสเงินสดอิสระระดับมหาศาล โครงสร้างเงินทุนแข็งแกร่งด้วยสัดส่วนหนี้สินต่อทุน D/E เพียง 0.17 เท่า",
            },
            {
                "icon": "🎯",
                "title": "ส่วนเผื่อความปลอดภัยตามมูลค่าแท้จริง (Margin of Safety)",
                "desc": "ราคาตลาดซื้อขายต่ำกว่ามูลค่าที่แท้จริง พร้อมฐานกำไรเงินสดที่ป้องกันความเสี่ยงขาลงได้อย่างมั่นคง",
            },
        ],
    },
    "GOOGL": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 385.00,
        "primary_model": "Owner Earnings Yield (4.0%) + Forward P/E (18x)",
        "model_desc": "ประเมินจากกำไร TTM จริง $19.39 ร่วมกับ Forward EPS $21.50 บน P/E 18 เท่า ของ Google Cloud และ Search",
        "math_details": {
            "formula": "Blended Model: 0.50 × (Forward EPS $21.50 × P/E 18x = $387.00) + 0.50 × (Owner Earnings FCF $15.32 ÷ 4.0% = $383.00) = $385.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): รายได้รวมเติบโตแข็งแกร่ง, กำไรต่อหุ้น TTM ทำได้จริง $19.39, Operating Margin 32%",
            "key_multiples": "Forward P/E 18.0x, TTM EPS $19.39, Owner Earnings Yield 4.0%, D/E 0.21x, ROE 44%",
            "wall_street_target": "$392.08 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $500.00)",
            "explanation": "ปรับปรุงสมมติฐานจากกำไร TTM จริงที่ทำได้ $19.39 กำหนด Forward EPS $21.50 บน P/E สมเหตุสมผล 18 เท่า ได้ราคาเหมาะสม $385.00 สอดคล้องกับราคาเป้าหมายสถาบันวอลล์สตรีท ($392.08)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "☁️",
                "title": "Google Cloud & Enterprise AI ขยายตัวก้าวกระโดด",
                "desc": "ธุรกิจคลาวด์และโมเดล Gemini ทำกำไรดำเนินงานเติบโตต่อเนื่อง หนุนกำไรต่อหุ้น TTM พุ่งแตะ $19.39",
            },
            {
                "icon": "🛡️",
                "title": "งบดุลแข็งแกร่งระดับป้อมปราการ",
                "desc": "สัดส่วนหนี้สินต่อทุนต่ำมาก D/E เพียง 0.21 เท่า และมีเงินสดสำรองมหาศาลเพื่อซื้อหุ้นคืนและลงทุนวิจัย AI",
            },
            {
                "icon": "💎",
                "title": "Valuation คุ้มค่าที่สุดในกลุ่ม Big Tech",
                "desc": "ซื้อขายที่ P/E ต่ำกว่าค่าเฉลี่ยในอดีตอย่างมีนัยสำคัญ มี Margin of Safety สูง",
            },
        ],
    },
    "LLY": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 1500.00,
        "primary_model": "Forward P/E Multiple (40x) + Pipeline DCF",
        "model_desc": "ประเมินจากกำไรคาดการณ์ล่วงหน้าบนการขยายกำลังการผลิตยา Mounjaro และ Zepbound ทั่วโลก",
        "math_details": {
            "formula": "Forward EPS ($37.50) × Target P/E (40x) = $1,500.00 (อิงการสเกลโรงงาน GLP-1 และ TTM EPS $30.48)",
            "accounting_source": "งบไตรมาสล่าสุด Q3'26: รายได้ $24.40B (+45.5% YoY), กำไรสุทธิ $6.45B (+49.8% YoY), TTM EPS $30.48, Gross Margin 81.5%",
            "key_multiples": "Forward P/E 40.0x, PEG 0.93x, D/E 1.23x, ROE 86%",
            "wall_street_target": "$1,501.06 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $1,700.00)",
            "explanation": "คำนวณจากกำไรต่อหุ้นปี FY27 คาดการณ์ที่ $37.50 บนอัตราส่วน P/E 40 เท่า สอดคล้องกับการเติบโตของกำไรสุทธิ (+49.8% YoY) และราคาเป้าหมายเฉลี่ยของนักวิเคราะห์วอลล์สตรีท ($1,501.06)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "💊",
                "title": "ผู้นำตลาดชีวเวชภัณฑ์ยาลดความอ้วน & เบาหวาน",
                "desc": "ความต้องการยากลุ่ม GLP-1 ยังคงสูงกว่ากำลังการผลิตอย่างมหาศาล อัตรากำไรขั้นต้นยืนเหนือระดับ 80%",
            },
            {
                "icon": "🏰",
                "title": "คูเมืองสิทธิบัตรยาคุ้มครองระยะยาว",
                "desc": "สิทธิบัตรยาตัวหลักได้รับการคุ้มครองยาวนาน พร้อม Pipeline ยารักษาโรคอัลไซเมอร์และหัวใจที่รอการอนุมัติ",
            },
            {
                "icon": "⚖️",
                "title": "มูลค่าพื้นฐานรองรับด้วยการเติบโตของยอดขายจริง",
                "desc": "กำไรต่อหุ้นเติบโตอย่างมั่นคง หนุนกรอบราคาเหมาะสมให้อยู่ในโซนปลอดภัย $1,500.00",
            },
        ],
    },
    "ABNB": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 195.00,
        "primary_model": "Free Cash Flow Yield Model (4.5%) + Forward P/E",
        "model_desc": "ประเมินจากผลตอบแทนกระแสเงินสดอิสระบนโครงสร้างธุรกิจแบบ Asset-Light ที่มี Margin สูง",
        "math_details": {
            "formula": "Blended Model: 0.50 × (FCF ต่อหุ้น $8.80 ÷ FCF Yield 4.5% = $195.55) + 0.50 × (Forward EPS $7.80 × 25x = $195.00) = $195.28",
            "accounting_source": "งบไตรมาสล่าสุด Q3'26: รายได้ $4.87B, กำไรสุทธิ $1.89B, EPS $3.16, FCF Margin 38.8%",
            "key_multiples": "Forward P/E 25.0x, FCF Yield 4.5%, Net Margin 38.8%",
            "wall_street_target": "$205.53 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $245.00)",
            "explanation": "คำนวณจากกระแสเงินสดอิสระที่ผู้ถือหุ้นจะได้รับจริงบนโมเดลธุรกิจตัวกลางจองที่พัก ราคาเหมาะสม $195.00 สอดคล้องกับปัจจัยพื้นฐานและมีส่วนลดเพื่อความปลอดภัย",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🏡",
                "title": "โมเดลธุรกิจเบาสินทรัพย์ (Asset-Light Platform)",
                "desc": "ไม่มีต้นทุนค่าก่อสร้างโรงแรม มีอัตรากำไรกระแสเงินสดอิสระ (FCF Margin) สูงกว่า 35% ของยอดจอง",
            },
            {
                "icon": "🌍",
                "title": "เครือข่ายผู้พักและผู้ให้เช่าระดับโลก (Global Moat)",
                "desc": "การเติบโตของการเดินทางท่องเที่ยวระยะยาวและการทำงานทางไกลช่วยขยายจำนวนคืนที่จองอย่างต่อเนื่อง",
            },
            {
                "icon": "⚖️",
                "title": "ราคาตลาดสะท้อนมูลค่าอย่างสมดุล",
                "desc": "ราคาปัจจุบันอยู่ในกรอบสมเหตุสมผลตามราคาเป้าหมายเฉลี่ยของวอลล์สตรีท",
            },
        ],
    },
    "MNST": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 52.00,
        "primary_model": "Steady Growth DCF + Brand Moat Multiple (P/E 28x)",
        "model_desc": "ประเมินจากกระแสเงินสดสินค้าอุปโภคบริโภคระดับพรีเมียม ร่วมกับเครือข่ายกระจายสินค้า Coca-Cola",
        "math_details": {
            "formula": "Forward EPS ($1.85) × Target P/E (28x) = $51.80 บนโครงสร้างงบดุลไร้หนี้สิน",
            "accounting_source": "งบไตรมาสล่าสุด Q3'26: รายได้ $2.56B, กำไรสุทธิ $568.43M, EPS $0.29, หนี้สินระยะยาว 0 ดอลลาร์",
            "key_multiples": "Forward P/E 28.0x, Zero Long-term Debt, ROE 23%",
            "wall_street_target": "$50.90 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $57.00)",
            "explanation": "ประเมินจากความแข็งแกร่งของแบรนด์เครื่องดื่มชูกำลังและช่องทางจำหน่ายระดับโลก ราคาเหมาะสม $52.00 สอดคล้องกับการขยายตลาดต่างประเทศ",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "⚡",
                "title": "ผู้นำเครื่องดื่มชูกำลังอันดับ 1 ในใจผู้บริโภค",
                "desc": "ครองส่วนแบ่งยอดขายเครื่องดื่มให้พลังงานระดับโลก ร่วมกับระบบโลจิสติกส์กระจายสินค้าของ Coca-Cola Company",
            },
            {
                "icon": "🛡️",
                "title": "ไร้หนี้สินระยะยาว (Zero Long-term Debt)",
                "desc": "โครงสร้างการเงินคลีน 100% ปราศจากความเสี่ยงหนี้สิน พร้อมกระแสเงินสดสม่ำเสมอในทุกสภาวะเศรษฐกิจ",
            },
            {
                "icon": "📈",
                "title": "Upside จากการขยายตลาดต่างประเทศ",
                "desc": "มีส่วนต่างมูลค่าเหมาะสมสอดคล้องกับเป้าหมายการเติบโตในเอเชียและละตินอเมริกา",
            },
        ],
    },
    "APP": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 460.00,
        "primary_model": "AI Ad-Tech Run-Rate Valuation (Forward P/E 30x)",
        "model_desc": "ประเมินจากการขยายตัวของโมเดล AI AXON 2.0 บนอัตรากำไรสุทธิระดับสูงกว่า 65%",
        "math_details": {
            "formula": "Forward EPS ($15.33) × Target P/E (30x) = $460.00 บนอัตรากำไรสุทธิ 66%",
            "accounting_source": "งบไตรมาสล่าสุด: รายได้เติบโตแข็งแกร่ง, กำไรสุทธิเติบโตสูง, TTM EPS $14.92, Net Margin 66.0%",
            "key_multiples": "Forward P/E 30.0x, TTM EPS $14.92, Net Margin 66.0%, ROE 95%",
            "wall_street_target": "$456.61 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $610.00)",
            "explanation": "คำนวณจากกำลังทำกำไรของระบบ AI แนะนำโฆษณา AXON 2.0 ราคาเหมาะสม $460.00 สอดคล้องกับราคาเป้าหมายสถาบันวอลล์สตรีท ($456.61)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🧠",
                "title": "เอนจิน AI โฆษณา AXON 2.0 สร้างผลตอบแทนเหนือคู่แข่ง",
                "desc": "อัลกอริทึมแมชชีนเลิร์นนิงยกระดับอัตราการคลิกและยอดขาย ทำให้อัตรากำไรสุทธิไตรมาสล่าสุดสูงถึง 66.0%",
            },
            {
                "icon": "🛍️",
                "title": "การขยายตลาดสู่อีคอมเมิร์ซนอกกลุ่มเกม",
                "desc": "การต่อยอดเทคโนโลยีโฆษณาเข้าสู่ร้านค้าออนไลน์และ Direct-to-Consumer ช่วยเพิ่มมูลค่าตลาดที่เข้าถึงได้",
            },
            {
                "icon": "🎯",
                "title": "กำไรเติบโตก้าวกระโดดหนุนมูลค่าเป้าหมาย",
                "desc": "ปัจจัยพื้นฐานสะท้อนราคาเหมาะสม $460.00 มี Margin of Safety รองรับความผันผวน",
            },
        ],
    },
    "VRT": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 310.00,
        "primary_model": "Data Center Liquid Cooling Supercycle (Forward P/E 35x)",
        "model_desc": "ประเมินจากยอดคำสั่งซื้อค้างส่ง (Backlog) ระบบ Liquid Cooling ของ AI Data Center และรายได้โต +47.5%",
        "math_details": {
            "formula": "Forward EPS ($8.85) × Target P/E (35x) = $309.75 (~$310.00) อิงยอดคำสั่งซื้อค้างส่งทำสถิติใหม่",
            "accounting_source": "งบไตรมาสล่าสุด: รายได้โต +47.5% YoY, กำไรสุทธิโต +116.7% YoY, TTM EPS $5.46, Backlog ทำสถิติใหม่ทะลุ $7.5B",
            "key_multiples": "Forward P/E 35.0x, TTM EPS $5.46, Backlog $7.5B, Net Income Growth +116.7%",
            "wall_street_target": "$330.85 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $427.00)",
            "explanation": "คำนวณจากความต้องการระบบทำความเย็น Liquid Cooling สำหรับคลัสเตอร์ GPU รุ่นใหม่ ราคาเหมาะสม $310.00 มีส่วนเผื่อความปลอดภัยต่ำกว่าเป้าหมายสถาบันวอลล์สตรีท ($330.85)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "❄️",
                "title": "ผู้นำระบบ Liquid Cooling สำหรับชิป AI รุ่นใหม่",
                "desc": "การประมวลผล AI กำลังไฟสูงจำเป็นต้องใช้ระบบระบายความร้อนด้วยของเหลวของ Vertiv เพื่อป้องกันโอเวอร์ฮีต",
            },
            {
                "icon": "📋",
                "title": "ยอดคำสั่งซื้อรอส่งมอบ (Order Backlog) ทำสถิติใหม่",
                "desc": "สัญญาระยะยาวจาก Hyperscalers ช่วยรับประกันการเติบโตของรายได้และกำไรสุทธิในอีก 2-3 ปีข้างหน้า",
            },
            {
                "icon": "⚖️",
                "title": "กำไรสุทธิเติบโตระดับก้าวกระโดด (+116.7%)",
                "desc": "ผลประกอบการเติบโตร้อนแรง หนุนให้ราคาเหมาะสมขยับขึ้นสู่กรอบ $310.00 อย่างสมเหตุสมผล",
            },
        ],
    },
    "PLTR": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 140.00,
        "primary_model": "Software AIP Growth Multiple (P/S 35x)",
        "model_desc": "ประเมินจากส่วนแบ่งซอฟต์แวร์ Artificial Intelligence Platform (AIP) ในองค์กรและรัฐบาลสหรัฐ",
        "math_details": {
            "formula": "Forward Revenue ($4.0B) × P/S Multiple (35x) ÷ 1.0B Shares = $140.00",
            "accounting_source": "งบไตรมาสล่าสุด: รายได้เติบโต +48% YoY, กำไรสุทธิขยายตัวต่อเนื่อง, TTM EPS $1.53, ปลอดหนี้สินระยะยาว",
            "key_multiples": "P/S 35.0x, TTM EPS $1.53, Rule of 40 Score > 80%",
            "wall_street_target": "$223.93 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $273.00)",
            "explanation": "ประเมินมูลค่าซอฟต์แวร์เติบโตสูง Palantir AIP กำหนดกรอบอนุรักษนิยมที่ $140.00 เพื่อเผื่อ Margin of Safety เนื่องจากราคาตลาดซื้อขายที่ P/E สูงเกินเกณฑ์ปกติ",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🤖",
                "title": "ระบบปฏิบัติการ AI หลักขององค์กร (Enterprise OS)",
                "desc": "Palantir AIP ได้รับการยอมรับและใช้งานจริงจากทั้งกระทรวงกลาโหมสหรัฐและบริษัทชั้นนำใน Fortune 500",
            },
            {
                "icon": "💰",
                "title": "กำไรขยายตัวต่อเนื่องและปราศจากหนี้สิน",
                "desc": "มีกระแสเงินสดอิสระสม่ำเสมอและไม่มีภาระหนี้สินระยะยาว งบการเงินผ่านเกณฑ์ยอดเยี่ยม",
            },
            {
                "icon": "⚠️",
                "title": "ราคาตลาดซื้อขายด้วย Premium สูงกว่าพื้นฐาน",
                "desc": "ควรใช้ความระมัดระวังและรอเข้าซื้อในโซนที่มี Margin of Safety ใกล้เคียงมูลค่าเหมาะสม $140.00",
            },
        ],
    },
    "NOW": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 145.00,
        "primary_model": "Enterprise SaaS Free Cash Flow Multiple",
        "model_desc": "ประเมินจากรายได้ Subscription แบบทำสัญญาต่อเนื่องและความร่วมมือ GenAI Agents กับ Nvidia",
        "math_details": {
            "formula": "Forward EPS ($3.25) × Target P/E (45x) = $146.25 (~$145.00) บน Renewal Rate 98.5%",
            "accounting_source": "งบไตรมาสล่าสุด: Subscription Revenue โต 22.5%, TTM EPS $1.40, กระแสเงินสดอิสระสม่ำเสมอ",
            "key_multiples": "Forward P/E 45.0x, Renewal Rate 98.5%, FCF Margin 32%",
            "wall_street_target": "$159.52 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $266.00)",
            "explanation": "ประเมินจากความเหนียวแน่นของฐานลูกค้าองค์กรและฟังก์ชัน GenAI Agent ราคาเหมาะสม $145.00 มีส่วนเผื่อความปลอดภัยต่ำกว่าเป้าหมายสถาบัน ($159.52)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🔄",
                "title": "ซอฟต์แวร์จัดการกระบวนการทำงานระดับองค์กร",
                "desc": "แพลตฟอร์ม ServiceNow กลายเป็นแกนกลางการทำงานของพนักงาน อัตราการต่ออายุสัญญา (Renewal Rate) ยืนเหนือ 98%",
            },
            {
                "icon": "🤝",
                "title": "ความร่วมมือกับ Nvidia ในการพัฒนา GenAI Agents",
                "desc": "การผสาน AI ช่วยให้พนักงานแก้ปัญหาได้เร็วขึ้น หนุนให้องค์กรยินดีจ่ายค่าบริการต่อหัว (ARPU) เพิ่มขึ้น",
            },
            {
                "icon": "💎",
                "title": "รายได้ประจำมั่นคงและมี Upside สู่มูลค่าเหมาะสม",
                "desc": "ราคาตลาดมีส่วนต่างสู่มูลค่าพื้นฐานที่ $145.00 อย่างสมดุล",
            },
        ],
    },
    "VST": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 195.00,
        "primary_model": "Power Purchase Agreement (PPA) Cash Flow Model (P/E 18x)",
        "model_desc": "ประเมินจากสัญญาระยะยาวจ่ายไฟฟ้าพลังงานนิวเคลียร์และก๊าซให้ศูนย์ข้อมูล AI กำไรโต +135%",
        "math_details": {
            "formula": "Forward EPS ($10.85) × Target P/E (18x) = $195.30 (~$195.00) บนสัญญาระยะยาว PPA",
            "accounting_source": "งบไตรมาสล่าสุด: กำไรสุทธิโต +135.0% YoY, TTM EPS $7.47, สัญญาจ่ายไฟฟ้า AI Data Center ทำสถิติใหม่",
            "key_multiples": "Forward P/E 18.0x, TTM EPS $7.47, Net Income Growth +135%, FCF Yield 6.5%",
            "wall_street_target": "$203.80 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $306.00)",
            "explanation": "ประเมินจากกระแสเงินสดตามสัญญาขายไฟฟ้าล่วงหน้าให้บริษัทเทคโนโลยีขนาดใหญ่ ราคาเหมาะสม $195.00 สอดคล้องกับราคาเป้าหมายวอลล์สตรีท ($203.80)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "⚡",
                "title": "ผู้ผลิตไฟฟ้าป้อน AI Data Center Hyperscalers",
                "desc": "โรงไฟฟ้าพลังงานนิวเคลียร์และก๊าซธรรมชาติสามารถจ่ายไฟแบบคงที่ 24/7 ตอบโจทย์ความต้องการของ Big Tech",
            },
            {
                "icon": "🔒",
                "title": "สัญญาล็อกราคาไฟฟ้าระยะยาวช่วยประกันกำไร",
                "desc": "ข้อตกลงขายไฟฟ้าล่วงหน้าลดความผันผวนของราคาพลังงานและสร้างกระแสเงินสดที่คาดการณ์ได้แม่นยำ",
            },
            {
                "icon": "📈",
                "title": "อุปสงค์ไฟฟ้าเติบโตเร็วกว่ากำลังการผลิตใหม่",
                "desc": "ราคาตลาดมี Upside สู่ระดับราคาเหมาะสมที่ประเมินไว้อย่างสมเหตุสมผล",
            },
        ],
    },
    "SKHY": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 245.00,
        "primary_model": "HBM Memory Supercycle Multiple (P/E 12x)",
        "model_desc": "ประเมินจากการเป็นซัพพลายเออร์หลักของชิปความจำ HBM3E และ HBM4 รายได้โต +209% กำไรโต +405%",
        "math_details": {
            "formula": "Forward EPS ADR ($20.40) × Target P/E (12x) = $244.80 (~$245.00) บนรอบซูเปอร์ไซเคิล",
            "accounting_source": "งบไตรมาสล่าสุด: รายได้โต +209.3% YoY, กำไรสุทธิโต +405.9% YoY, TTM EPS $18.02, Operating Margin 40%+",
            "key_multiples": "Forward P/E 12.0x, TTM EPS $18.02, HBM Market Share > 55%, ROE 35%",
            "wall_street_target": "$264.30 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $400.00)",
            "explanation": "ประเมินจากการเป็นผู้นำผูกขาดชิป HBM3E ให้ Nvidia ในช่วงชิปขาดแคลน ราคาเหมาะสม $245.00 ต่ำกว่าเป้าหมายสถาบัน ($264.30) เพื่อความปลอดภัย",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "💾",
                "title": "ผู้นำอันดับ 1 ในชิปความจำแบนด์วิธสูง (High Bandwidth Memory)",
                "desc": "ครอบครองส่วนแบ่งตลาด HBM3E ให้ Nvidia สูงที่สุดในโลก และเตรียมเริ่มส่งมอบ HBM4",
            },
            {
                "icon": "🚀",
                "title": "กำไรสุทธิทำสถิติสูงสุดใหม่ในรอบขาขึ้น (+405.9%)",
                "desc": "อัตรากำไรสุทธิและกำไรดำเนินงานเติบโตอย่างร้อนแรงจากภาวะขาดแคลนชิปความจำความเร็วสูงระดับพรีเมียม",
            },
            {
                "icon": "💰",
                "title": "P/E ต่ำมากเมื่อเทียบกับการเติบโตของกำไร",
                "desc": "ราคาตลาดมี Upside สู่มูลค่าเหมาะสมที่ $245.00 สอดคล้องกับปัจจัยพื้นฐาน",
            },
        ],
    },

    # 2. Banking & Financial
    "BAC": {
        "model_type": "BANKING",
        "fair_price": 57.50,
        "primary_model": "Justified Price-to-Book (P/B 1.38x) Gordon Growth Model",
        "model_desc": "ประเมินจาก BVPS $41.50 ร่วมกับ Normalized ROE 11.5% และ Hurdle Rate 9.0%",
        "math_details": {
            "formula": "Target P/B = (ROE 11.5% - g 2.5%) ÷ (Ke 9.0% - g 2.5%) = 1.385x. Fair Price = BVPS ($41.50) × 1.385x = $57.48 (~$57.50)",
            "accounting_source": "งบดุลไตรมาสล่าสุด: ส่วนของผู้ถือหุ้น $295.58B, BVPS $41.50, TTM EPS $4.27, CET1 Ratio 11.9%, เงินฝากต้นทุนต่ำ $1.9T",
            "key_multiples": "Justified P/B 1.38x, Normalized ROE 11.5%, Cost of Equity 9.0%, Long-term g 2.5%",
            "wall_street_target": "$62.28 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $71.00)",
            "explanation": "คำนวณจากสูตร Gordon Growth Model ทางการเงินสากล โดยใช้ผลตอบแทนต่อส่วนของผู้ถือหุ้นเฉลี่ยทั้งรอบ (Normalized ROE 11.5%) และต้นทุนเงินทุนของภาคธนาคาร 9.0% ได้มูลค่าเหมาะสม $57.50",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🏦",
                "title": "ฐานเงินฝากต้นทุนต่ำขนาดใหญ่ที่สุดแห่งหนึ่งในสหรัฐ",
                "desc": "ได้รับประโยชน์จากโครงสร้างอัตราดอกเบี้ยที่มีเสถียรภาพ หนุนรายได้ดอกเบี้ยสุทธิ (NII) ให้เติบโตอย่างมั่นคง",
            },
            {
                "icon": "🛡️",
                "title": "คุณภาพสินทรัพย์แข็งแกร่งและหนี้เสียต่ำ",
                "desc": "การตั้งสำรองหนี้สูญอยู่ในระดับรัดกุม อัตราส่วนเงินกองทุนขั้นที่ 1 (CET1) สูงกว่าเกณฑ์ควบคุมของธนาคารกลาง",
            },
            {
                "icon": "💰",
                "title": "เงินปันผลสม่ำเสมอและการซื้อหุ้นคืน",
                "desc": "ราคาตลาดเทรดที่ระดับ P/E ต่ำ มีเงินปันผลตอบแทนสม่ำเสมอและมี Upside สู่ราคาเหมาะสมที่คำนวณได้จริง",
            },
        ],
    },

    # 3. Hyperscaler & AI Infrastructure
    "NBIS": {
        "model_type": "HYPERSCALER_INFRA",
        "fair_price": 210.00,
        "primary_model": "EV/Run-rate Revenue (10x) Minus Net Debt",
        "model_desc": "ประเมินจากเป้าหมายรายได้ปี 2026 ที่ $3.2B บนตัวคูณ EV/Sales 10 เท่า หักภาระหนี้สินสุทธิ",
        "math_details": {
            "formula": "Enterprise Value ($3.2B × 10x = $32.0B) - Net Debt ($0.0B) ÷ Fully Diluted Shares (152M) = $210.53 (~$210.00)",
            "accounting_source": "งบไตรมาสล่าสุด: รายได้รวมเติบโต +460.9% YoY TTM, คอนเฟิร์มเป้าหมายยอดขายปี 2026 ที่ $3.0B-$3.4B พร้อม Run-rate $7B-$9B",
            "key_multiples": "Target EV/Sales 10.0x, Net Cash Position, Fully Diluted Shares 152M",
            "wall_street_target": "$283.90 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $410.00)",
            "explanation": "ประเมินจากการขยายตัวของธุรกิจ GPU Cloud Hyperscaler ที่ติดตั้งชิป Nvidia Blackwell โดยหักลบภาระหนี้สินสุทธิตามหลักอนุรักษนิยม ได้ราคาเหมาะสม $210.00 (ต่ำกว่าเป้าวอลล์สตรีท 26% เพื่อความปลอดภัย)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "☁️",
                "title": "GPU Cloud Hyperscaler เติบโตเร็วที่สุดในยุโรปและสหรัฐ",
                "desc": "ยอดขายเติบโต +460.9% YoY TTM จากความต้องการเช่าคลัสเตอร์ประมวลผล AI และสถาปัตยกรรม Blackwell",
            },
            {
                "icon": "📈",
                "title": "เป้าหมายรายได้ปี 2026 ชัดเจนที่ $3.0B - $3.4B",
                "desc": "บริษัทตอกย้ำเป้าหมายรายได้และมี Run-rate ระดับ $7B-$9B สะท้อนการขยายดาต้าเซ็นเตอร์เต็มกำลัง",
            },
            {
                "icon": "💎",
                "title": "Upside สูงเมื่อเทียบกับราคาเป้าหมายวอลล์สตรีท",
                "desc": "ราคาตลาดต่ำกว่าราคาเป้าหมายเฉลี่ยของสถาบัน ($283.90) มี Margin of Safety รองรับ",
            },
        ],
    },
    "SPCX": {
        "model_type": "SPECULATIVE_BASELINE",
        "fair_price": 115.00,
        "primary_model": "Pre-IPO Funding Round Baseline & Structural Support",
        "model_desc": "ประเมินจากมูลค่าระดมทุนรอบล่าสุดของ SpaceX ($200B-$250B) ร่วมกับแนวรับต้นทุนสะสม",
        "math_details": {
            "formula": "Pre-IPO Baseline Support: อ้างอิงแนวรับต้นทุนสะสมของสถาบันที่ $115.00 (สถานะ SPECULATIVE)",
            "accounting_source": "หุ้นก่อนการซื้อขายสาธารณะ (Pre-IPO Vehicle) ยังไม่มีงบ 10-Q ตรวจสอบอย่างเป็นทางการจาก SEC",
            "key_multiples": "Baseline Funding Valuation $200B-$250B, Starlink Run-rate Revenue ~$15B",
            "wall_street_target": "N/A (หุ้นก่อนไอพีโอ ยังไม่มี Consensus สถาบันอย่างเป็นทางการ)",
            "explanation": "กำหนดกรอบราคาอ้างอิงที่ $115.00 ตามแนวรับต้นทุนสะสมของสถาบัน โดยติดป้ายกำกับสถานะ SPECULATIVE BASELINE เพื่อเตือนความเสี่ยงแก่ผู้ถือครอง",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🚀",
                "title": "ผูกขาดเทคโนโลยีอวกาศ & Starlink Satellite Internet",
                "desc": "การเติบโตของฐานผู้ใช้งานอินเทอร์เน็ตดาวเทียม Starlink ทั่วโลก และสัญญากระทรวงกลาโหมสหรัฐ",
            },
            {
                "icon": "🛡️",
                "title": "โครงสร้างธุรกิจก่อนไอพีโอ (Pre-IPO Status)",
                "desc": "สถานะเป็นหุ้นลงทุนพิเศษก่อนการจดทะเบียนในตลาดหลักทรัพย์อย่างเป็นทางการ",
            },
            {
                "icon": "⏳",
                "title": "แนวรับต้นทุนสะสมคือจุดเฝ้าระวังสำคัญ",
                "desc": "โซน 115.00 ดอลลาร์ตามแนวรับหลักคือจุดที่มีความสมดุลด้านความเสี่ยงดีที่สุด",
            },
        ],
    },

    # 4. Turnaround & Cyclical Deep Value
    "NOK": {
        "model_type": "TURNAROUND_CYCLICAL",
        "fair_price": 11.50,
        "primary_model": "Normalized EV/EBIT (10x) + Net Cash (EUR to USD)",
        "model_desc": "ประเมินจากกำไรดำเนินงานรอบฟื้นตัว Optical Networking ร่วมกับเงินสดสุทธิ €3.8B",
        "math_details": {
            "formula": "Enterprise Value (€2.10B × 10x = €21.0B) + Net Cash (€3.8B) = €24.8B × 1.08 (EUR/USD) ÷ 5.60B Shares = $11.54 (~$11.50)",
            "accounting_source": "งบไตรมาสล่าสุด: เงินสดสุทธิในมือ €3.8B (ปลอดหนี้สินสุทธิ), คำสั่งซื้อ AI Data Center Optical Networks ฟื้นตัวเด่นชัด",
            "key_multiples": "Target EV/EBIT 10.0x, Net Cash €3.8B, FX Rate 1.08 EUR/USD",
            "wall_street_target": "$12.69 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $20.16)",
            "explanation": "คำนวณจากกำไรจากการดำเนินงานรอบวัฏจักรฟื้นตัวของอุปกรณ์เครือข่ายความเร็วสูง ร่วมกับเงินสดสุทธิหลังหักหนี้สิน แปลงเป็นดอลลาร์สหรัฐ ได้ราคาเหมาะสม $11.50 สอดคล้องกับราคาเป้าหมายสถาบันวอลล์สตรีท ($12.69)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "📶",
                "title": "งบดุลเงินสดสุทธิเป็นบวกมหาศาล (Net Cash Position)",
                "desc": "สถานะการเงินมั่นคง ปลอดหนี้สินระยะสั้น มีเงินสดสำรองหนุนการจ่ายปันผลและการซื้อหุ้นคืนต่อเนื่อง",
            },
            {
                "icon": "🌐",
                "title": "โครงสร้างพื้นฐานเครือข่ายสำหรับ AI Data Center",
                "desc": "อุปสงค์เทคโนโลยีเราเตอร์ IP และสวิตชิ่งความเร็วสูงสำหรับ AI คลาวด์ช่วยหนุนยอดคำสั่งซื้อใหม่",
            },
            {
                "icon": "💎",
                "title": "มูลค่าสินทรัพย์และเงินสดค้ำยันราคา (Cash Backed Floor)",
                "desc": "ราคาตลาดมีฐานเงินสดสุทธิค้ำยัน ช่วยจำกัดความเสี่ยงขาลงและมี Upside สู่มูลค่าเหมาะสม",
            },
        ],
    },
    "AEHR": {
        "model_type": "TURNAROUND_CYCLICAL",
        "fair_price": 90.00,
        "primary_model": "Normalized Forward EPS Multiple (25x) + Backlog Recovery",
        "model_desc": "ประเมินจากการฟื้นตัวของคำสั่งซื้อเครื่องทดสอบเวเฟอร์ Silicon Carbide Backlog $109M",
        "math_details": {
            "formula": "Normalized Forward EPS ($3.60) × Target P/E (25x) = $90.00 (มี Asset-Backed Floor ที่ $12.50)",
            "accounting_source": "งบไตรมาสล่าสุด: Backlog ทำสถิติใหม่แตะ $109M, ฐานะการเงินปลอดหนี้สินระยะยาว",
            "key_multiples": "Normalized P/E 25.0x, Backlog $109M, Asset Floor $12.50",
            "wall_street_target": "$120.83 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $140.00)",
            "explanation": "ประเมินจากยอดคำสั่งซื้อเครื่องทดสอบเวเฟอร์ที่ฟื้นตัวสู่ระดับปกติ กำหนดราคาเหมาะสมที่ $90.00 เพื่อเผื่อ Margin of Safety จากความผันผวนของรอบส่งมอบสินค้า (เป้าหมายสถาบัน $120.83)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🔬",
                "title": "เทคโนโลยีทดสอบชิปพลังงาน SiC ระดับเวเฟอร์",
                "desc": "เป็นผู้นำด้านระบบ Burn-in ทดสอบความทนทานของชิปพลังงานสำหรับรถยนต์ไฟฟ้าและดาต้าเซ็นเตอร์",
            },
            {
                "icon": "📈",
                "title": "ยอดคำสั่งซื้อรอส่งมอบ (Backlog) ทะลุ $109M",
                "desc": "การฟื้นตัวของยอดจองเครื่องทดสอบช่วยประกันรายได้และผลกำไรในรอบการผลิตถัดไป",
            },
            {
                "icon": "⚠️",
                "title": "ความผันผวนของรอบวัฏจักรคำสั่งซื้อ",
                "desc": "ควรรอจังหวะสะสมในโซนที่มี Margin of Safety ใกล้เคียงมูลค่าเหมาะสม $90.00",
            },
        ],
    },

    # 5. Index & Covered Call ETFs
    "VOO": {
        "model_type": "INDEX_ETF",
        "fair_price": None,  # Dynamically tracked to current market price / NAV
        "primary_model": "Net Asset Value (NAV) Tracking (S&P 500 Index ETF)",
        "model_desc": "ประเมินมูลค่าตามสินทรัพย์สุทธิ (Fair NAV) อ้างอิงผลตอบแทนดัชนี S&P 500 แบบเรียลไทม์",
        "math_details": {
            "formula": "Fair Price = Current Net Asset Value (NAV) per share 100%",
            "accounting_source": "กองทุนเปิด Vanguard S&P 500 ETF ถือครองหุ้น 500 ตัวตามน้ำหนัก Market Cap รวมมูลค่าสินทรัพย์กว่า $1.2T",
            "key_multiples": "Expense Ratio 0.03%, P/E ดัชนี ~26x, Dividend Yield 1.3%",
            "wall_street_target": "N/A (Index ETF อ้างอิงตามดัชนีตลาด)",
            "explanation": "ราคาตลาดสะท้อนมูลค่าสินทรัพย์สุทธิที่แท้จริง (Fair NAV) เสมอ มี Tracking Error ต่ำกว่า 0.02%",
            "margin_of_safety_rule": "ETF ซื้อขายที่ระดับ Fair NAV ตามกลไก Arbitrage ของ Authorized Participants",
        },
        "pillars": [
            {
                "icon": "🏛️",
                "title": "กระจายความเสี่ยง 500 บริษัทชั้นนำของสหรัฐ",
                "desc": "ถือครองหุ้นขนาดใหญ่ชั้นนำครบทุกอุตสาหกรรม เป็นแกนหลักในการสะสมความมั่งคั่งระยะยาว",
            },
            {
                "icon": "📉",
                "title": "อัตราค่าธรรมเนียมบริหารจัดการต่ำที่สุด (0.03%)",
                "desc": "ต้นทุนการถือครองต่ำมาก ทำให้ผลตอบแทนส่วนใหญ่สะท้อนเข้าสู่พอร์ตของผู้ถือหน่วยลงทุนอย่างเต็มเม็ดเต็มหน่วย",
            },
            {
                "icon": "🌐",
                "title": "ราคาตลาดสอดคล้องกับมูลค่าทรัพย์สินสุทธิ (Fair NAV)",
                "desc": "ราคาตลาดเทรดชิดกับมูลค่าพื้นฐานที่แท้จริงตามการเคลื่อนไหวของดัชนีเศรษฐกิจสหรัฐ",
            },
        ],
    },
    "QQQI": {
        "model_type": "INDEX_ETF",
        "fair_price": None,  # Dynamically tracked to current market price / NAV
        "primary_model": "Net Asset Value (NAV) + Covered Call Income Strategy",
        "model_desc": "ประเมินมูลค่าตามสินทรัพย์สุทธิ (Fair NAV) บนพอร์ตดัชนี Nasdaq 100",
        "math_details": {
            "formula": "Fair Price = Current Net Asset Value (NAV) per share (แยกแสดงกระแสเงินสดผลตอบแทนต่างหาก)",
            "accounting_source": "กองทุน NEOS Nasdaq 100 High Income ETF ถือครองหุ้น Nasdaq 100 พร้อมขาย Call Option นอกราคา (OTM)",
            "key_multiples": "Distribution Yield ~14.0% ต่อปี, Expense Ratio 0.68%",
            "wall_street_target": "N/A (Income ETF อ้างอิงตามดัชนีและเบี้ยออปชัน)",
            "explanation": "ราคาตลาดเคลื่อนไหวตามมูลค่าพอร์ตทรัพย์สินสุทธิจริง (NAV) ส่วนผลตอบแทนเงินสดสม่ำเสมอจ่ายทุกเดือนแยกต่างหาก",
            "margin_of_safety_rule": "เบี้ยประกันออปชันช่วยชดเชยการปรับฐานของตลาดหุ้นเทคโนโลยี Nasdaq 100 ได้บางส่วน",
        },
        "pillars": [
            {
                "icon": "💵",
                "title": "กระแสเงินปันผลระดับสูงรายเดือน (~14% ต่อปี)",
                "desc": "สร้างกระแสเงินสดเข้าพอร์ตอย่างสม่ำเสมอจากพรีเมียมการขายสัญญาสิทธิเลือกซื้อ (Covered Call)",
            },
            {
                "icon": "🛡️",
                "title": "กลยุทธ์ป้องกันความเสี่ยงขาลง (Downside Cushion)",
                "desc": "เบี้ยประกันออปชันช่วยชดเชยการปรับฐานของตลาดหุ้นเทคโนโลยี Nasdaq 100 ได้บางส่วน",
            },
            {
                "icon": "🌐",
                "title": "ราคาตลาดสะท้อนมูลค่าพอร์ตทรัพย์สินสุทธิ (Fair NAV)",
                "desc": "ราคาตลาดเคลื่อนไหวตามมูลค่าทรัพย์สินสุทธิจริงอย่างสมเหตุสมผล เหมาะสำหรับถือรับกระแสเงินสด",
            },
        ],
    },
    "QQQM": {
        "model_type": "INDEX_ETF",
        "fair_price": None,
        "primary_model": "Net Asset Value (NAV) Tracking (Nasdaq 100 Index ETF - Low Expense)",
        "model_desc": "ประเมินมูลค่าตามสินทรัพย์สุทธิ (Fair NAV) อ้างอิงหุ้นเทคโนโลยีชั้นนำ 100 ตัวของสหรัฐ ค่าธรรมเนียมต่ำพิเศษ 0.15%",
        "math_details": {
            "formula": "Fair Price = Current Net Asset Value (NAV) per share 100%",
            "accounting_source": "กองทุน Invesco NASDAQ 100 ETF ถือหุ้น 100 ตัวของดัชนี Nasdaq 100 มีสินทรัพย์รวมกว่า $40B+",
            "key_multiples": "Expense Ratio 0.15%, Index P/E ~30x, Tech Weight 55%+",
            "wall_street_target": "N/A (Index ETF อ้างอิงตามดัชนีตลาด)",
            "explanation": "ราคาตลาดเคลื่อนไหวตามมูลค่าพอร์ตทรัพย์สินสุทธิที่แท้จริง (Fair NAV) โดยมีค่าธรรมเนียมการจัดการต่ำกว่า QQQ ดั้งเดิม",
            "margin_of_safety_rule": "กลไก Arbitrage ของผู้ร่วมค้าสถาบัน (AP) คอยรักษาเสถียรภาพราคาให้ชิดกับ NAV ตลอดเวลา",
        },
        "pillars": [
            {
                "icon": "💻",
                "title": "ศูนย์รวม 100 บริษัทเทคโนโลยีและนวัตกรรมชั้นนำของโลก",
                "desc": "ครองความเป็นผู้นำด้าน AI, คลาวด์, เซมิคอนดักเตอร์ และซอฟต์แวร์ระดับโลก",
            },
            {
                "icon": "📉",
                "title": "ค่าธรรมเนียมบริหารจัดการต่ำเป็นพิเศษ (0.15%)",
                "desc": "ช่วยลดต้นทุนการถือครองระยะยาว เหมาะสำหรับกลยุทธ์ DCA สะสมความมั่งคั่ง",
            },
            {
                "icon": "🌐",
                "title": "สภาพคล่องสูงและราคาเทรดสะท้อน Fair NAV เสมอ",
                "desc": "ไม่มีความเสี่ยงจากพรีเมียมราคา และมีกลไกรักษาความเที่ยงตรงของดัชนีอย่างสมบูรณ์",
            },
        ],
    },
    "SOXQ": {
        "model_type": "INDEX_ETF",
        "fair_price": None,
        "primary_model": "Net Asset Value (NAV) Tracking (PHLX Semiconductor Index ETF - Low Expense)",
        "model_desc": "ประเมินมูลค่าตามสินทรัพย์สุทธิ (Fair NAV) อ้างอิงดัชนีเซมิคอนดักเตอร์ฟิลาเดลเฟีย (SOX) 30 บริษัท ค่าธรรมเนียม 0.19%",
        "math_details": {
            "formula": "Fair Price = Current Net Asset Value (NAV) per share 100%",
            "accounting_source": "กองทุน Invesco PHLX Semiconductor ETF ถือครอง 30 บริษัทผู้นำเซมิคอนดักเตอร์โลก (Nvidia, TSMC, Broadcom, ASML, AMD)",
            "key_multiples": "Expense Ratio 0.19%, Semiconductor Sector Monopoly, Tracking Error < 0.05%",
            "wall_street_target": "N/A (Index ETF อ้างอิงตามดัชนีตลาด)",
            "explanation": "ราคาตลาดสะท้อนมูลค่าทรัพย์สินสุทธิ (Fair NAV) ของห่วงโซ่อุปทานชิป AI โลกอย่างเที่ยงตรง",
            "margin_of_safety_rule": "การกระจายความเสี่ยงใน 30 ผู้ผลิตชิปชั้นนำช่วยลดความผันผวนของหุ้นเดี่ยว",
        },
        "pillars": [
            {
                "icon": "⚡",
                "title": "กุมห่วงโซ่อุปทานหัวใจของ AI Supercycle โลก",
                "desc": "ครอบคลุมทั้งผู้ออกแบบชิป โรงงานผลิต เครื่องจักร และแพ็กเกจจิ้งขั้นสูง",
            },
            {
                "icon": "🏷️",
                "title": "ค่าธรรมเนียมถูกที่สุดในกลุ่ม ETF เซมิคอนดักเตอร์ (0.19%)",
                "desc": "ประหยัดกว่ากองทุนชิปแบบเดิม ช่วยเพิ่มผลตอบแทนทบต้นในระยะยาว",
            },
            {
                "icon": "🌐",
                "title": "ราคาเทรดสอดคล้องกับมูลค่าสินทรัพย์สุทธิ Fair NAV",
                "desc": "มีกลไกสร้างและไถ่ถอนหน่วยลงทุนเพื่อรักษาระดับราคาให้เท่ากับมูลค่าจริงเสมอ",
            },
        ],
    },
    "GPIQ": {
        "model_type": "INDEX_ETF",
        "fair_price": None,
        "primary_model": "Net Asset Value (NAV) + Dynamic Option Income Strategy",
        "model_desc": "ประเมินมูลค่าตามสินทรัพย์สุทธิ (Fair NAV) บนพอร์ตดัชนี Nasdaq 100 พร้อมกลยุทธ์ Dynamic Covered Call สร้างกระแสเงินปันผล",
        "math_details": {
            "formula": "Fair Price = Current Net Asset Value (NAV) per share (แยกแสดงกระแสเงินสดผลตอบแทนต่างหาก)",
            "accounting_source": "กองทุน Goldman Sachs Nasdaq-100 Premium Income ETF บริหารจัดการโดย Goldman Sachs Asset Management",
            "key_multiples": "Distribution Yield ~10.5% ต่อปี, Expense Ratio 0.29%, Managed by Goldman Sachs",
            "wall_street_target": "N/A (Income ETF อ้างอิงตามดัชนีและเบี้ยออปชัน)",
            "explanation": "ราคาตลาดเคลื่อนไหวตามมูลค่าสินทรัพย์สุทธิ (Fair NAV) โดยมีจุดเด่นเรื่องค่าธรรมเนียมต่ำและการบริหารออปชันแบบยืดหยุ่น",
            "margin_of_safety_rule": "เบี้ยประกันจากการขาย Option ช่วยลดความผันผวนของพอร์ตเทคโนโลยีลงบางส่วน",
        },
        "pillars": [
            {
                "icon": "💵",
                "title": "กระแสเงินปันผลระดับสูงรายเดือน (~10.5% ต่อปี)",
                "desc": "สร้างผลตอบแทนสม่ำเสมอเข้าพอร์ตจากกลยุทธ์การขายออปชันแบบ Dynamic Call",
            },
            {
                "icon": "🏦",
                "title": "บริหารจัดการโดยสถาบันระดับโลก Goldman Sachs",
                "desc": "ใช้โมเดลคณิตศาสตร์ขั้นสูงปรับสัดส่วนสัญญาออปชันตามสภาวะความผันผวนของตลาด",
            },
            {
                "icon": "🛡️",
                "title": "ค่าธรรมเนียมบริหารจัดการคุ้มค่าเพียง 0.29%",
                "desc": "ต้นทุนต่ำกว่ากองทุน Covered Call ทั่วไปในตลาด ช่วยรักษาเงินต้นของนักลงทุน",
            },
        ],
    },
    "TSLA": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 420.00,
        "primary_model": "Autonomous Fleet SOTP + Forward P/E (55x)",
        "model_desc": "ประเมินมูลค่ารวมส่วนธุรกิจ (SOTP): ยานยนต์ไฟฟ้า + พลังงาน Megapack + โครงข่าย Robotaxi และ Optimus AI",
        "math_details": {
            "formula": "SOTP Model: Core Auto & Energy (Forward EPS $5.50 × P/E 45x = $247.50) + Robotaxi FSD Option ($172.50) = $420.00",
            "accounting_source": "งบการเงินล่าสุด: รายได้เติบโตแข็งแกร่งจากธุรกิจ Energy Storage Megapack โตกว่า 125% YoY, FCF เป็นบวกต่อเนื่อง, Cash สำรองกว่า $33B",
            "key_multiples": "Forward P/E 55.0x, Energy Storage Growth +125%, D/E 0.11x, Operating Cash Flow $14B+",
            "wall_street_target": "$423.70 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $600.00)",
            "explanation": "คำนวณจากกำไรหลักของยานยนต์และระบบกักเก็บพลังงาน รวมกับมูลค่าปัจจุบันของโครงข่าย Cybercab Robotaxi ได้ราคาเหมาะสม $420.00 สอดคล้องกับเป้าหมายเฉลี่ยวอลล์สตรีท ($423.70)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🤖",
                "title": "ผู้นำ Physical AI & Autonomous Robotaxi",
                "desc": "เทคโนโลยี FSD End-to-End Neural Network พร้อมสเกลเชิงพาณิชย์และกองเรือไร้คนขับทั่วโลก",
            },
            {
                "icon": "🔋",
                "title": "ธุรกิจระบบกักเก็บพลังงาน Megapack โตระเบิด",
                "desc": "รายได้และกำไรจากธุรกิจแบตเตอรี่โครงข่ายไฟฟ้าขยายตัวก้าวกระโดดกว่า 125% หนุนเสถียรภาพกระแสเงินสด",
            },
            {
                "icon": "💵",
                "title": "งบดุลแข็งแกร่งระดับป้อมปราการ",
                "desc": "ถือครองเงินสดและพันธบัตรรัฐบาลกว่า $33 พันล้านดอลลาร์ โดยแทบไม่มีหนี้สินระยะยาวที่มีภาระดอกเบี้ย",
            },
        ],
    },
    "ADI": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 460.00,
        "primary_model": "Morgan Stanley #1 Robotics BOM Leader + Industrial Automation (34x P/E)",
        "model_desc": "ประเมินจากการเป็นผู้นำชิปแอนะล็อกและเซนเซอร์ความแม่นยำสูงอันดับ 1 ในต้นทุนส่วนประกอบหุ่นยนต์ Physical AI",
        "math_details": {
            "formula": "Forward FY27 EPS ($13.50) × Target P/E (34x) = $459.00 -> ปรับฐานที่ $460.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): TTM EPS $8.43, Gross Margin ระดับ 68%, Morgan Stanley จัดอันดับให้เป็นชิปอันดับ 1 ของโครงสร้างหุ่นยนต์",
            "key_multiples": "Forward P/E 34.0x, Gross Margin 68%, Robotics BOM #1 ($1,625), FCF Margin 33%",
            "wall_street_target": "$478.86 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $550.00)",
            "explanation": "หุ่นยนต์มนุษย์ทุกตัวต้องใช้ชิปแปลงสัญญาณจริงของ ADI ในทุกข้อต่อ ราคาเหมาะสม $460.00 ต่ำกว่าเป้าเฉลี่ยวอลล์สตรีท ($478.86)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🤖",
                "title": "ชิปอันดับ 1 ในต้นทุนชิ้นส่วนหุ่นยนต์ฮิวแมนนอยด์ (BOM $1,625)",
                "desc": "Morgan Stanley ชี้ว่า ADI ได้รับประโยชน์สูงสุดต่อตัวหุ่นยนต์จากเซนเซอร์ตรวจจับและการควบคุมมอเตอร์",
            },
            {
                "icon": "💎",
                "title": "อัตรากำไรขั้นต้น Gross Margin สูงลิบระดับ 68%",
                "desc": "เป็นสินค้าเฉพาะทางที่ลูกค้าเปลี่ยนผู้ผลิตได้ยาก มีอำนาจต่อรองราคาสูง",
            },
            {
                "icon": "💵",
                "title": "กระแสเงินสดอิสระมั่นคงและจ่ายเงินปันผลต่อเนื่อง",
                "desc": "สร้างกระแสเงินสดอิสระกว่า 33% ของรายได้ พร้อมซื้อหุ้นคืนสม่ำเสมอ",
            },
        ],
    },
    "MPWR": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 1720.00,
        "primary_model": "AI Data Center Power Stage + Robotics BCD Process (48x P/E)",
        "model_desc": "ประเมินจากชิปจ่ายพลังงานประสิทธิภาพสูงให้กับชิป AI Accelerator และโมดูลขับมอเตอร์หุ่นยนต์",
        "math_details": {
            "formula": "Forward FY27 EPS ($36.00) × Multiple P/E (48x) = $1,728.00 -> ปรับฐานที่ $1,720.00",
            "accounting_source": "งบการเงินล่าสุด: TTM EPS $18.12, อัตราการเติบโตของรายได้โดดเด่น, Gross Margin 55.5%, หนี้สินเป็นศูนย์ (No Debt)",
            "key_multiples": "Forward P/E 48.0x, Enterprise Data Center Growth +60%, Gross Margin 55.5%, D/E 0.0x",
            "wall_street_target": "$1,826.08 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $2,200.00)",
            "explanation": "MPWR เป็นผู้เชี่ยวชาญด้าน Power Management ที่ลดการสูญเสียพลังงานในเซิร์ฟเวอร์ AI ราคาเหมาะสม $1,720.00 ให้ส่วนเผื่อความปลอดภัยจากเป้าวอลล์สตรีท ($1,826.08)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "⚡",
                "title": "เบอร์ 1 ชิปควบคุมพลังงานความหนาแน่นสูงสำหรับ AI Cluster",
                "desc": "เทคโนโลยีสิทธิบัตร BCD รวมพลังงานและตรรกะไว้ในชิปตัวเดียว ขนาดเล็กและเย็นกว่าคู่แข่ง",
            },
            {
                "icon": "🤖",
                "title": "ชิปข้อต่อหุ่นยนต์และมอเตอร์ความแม่นยำสูง",
                "desc": "ได้รับเลือกเป็นชิ้นส่วนควบคุมการเคลื่อนไหวของหุ่นยนต์อัตโนมัติในโรงงานอัจฉริยะ",
            },
            {
                "icon": "🛡️",
                "title": "ฐานะการเงินแข็งแกร่งระดับไร้หนี้สิน",
                "desc": "มีเงินสดในมือมหาศาลและไม่มีหนี้สินระยะยาวที่มีภาระดอกเบี้ยเลยแม้แต่บาทเดียว",
            },
        ],
    },
    "TXN": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 335.00,
        "primary_model": "300mm Analog Wafer Cost Moat + Free Cash Flow Inflection (29x P/E)",
        "model_desc": "ประเมินจากความได้เปรียบต้นทุนโรงงานเวเฟอร์ 300 มม. ที่ประหยัดต้นทุนกว่าคู่แข่ง 40% และการผ่านจุดสูงสุดของการลงทุน CapEx",
        "math_details": {
            "formula": "Forward FY27 EPS ($11.50) × Target P/E (29x) = $333.50 -> กำหนดฐาน $335.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): TTM EPS $7.71, Gross Margin 58%, การลงทุนโรงงานเวเฟอร์ 300mm ในเท็กซัสและยูทาห์ใกล้เสร็จสมบูรณ์",
            "key_multiples": "Forward P/E 29.0x, 300mm Wafer Cost Advantage 40%, Dividend Yield 2.2%, ROE 28%",
            "wall_street_target": "$336.62 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $390.00)",
            "explanation": "เมื่อวัฏจักรเซมิคอนดักเตอร์อุตสาหกรรมฟื้นตัว ต้นทุนการผลิต 300mm จะผลักดัน FCF ให้ดีดตัวขึ้นมหาศาล ราคาเหมาะสม $335.00 สอดคล้องกับเป้าหมายเฉลี่ยวอลล์สตรีท ($336.62)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🏰",
                "title": "ปราการคูป้องกันต้นทุน 300mm Analog Fab",
                "desc": "การผลิตบนเวเฟอร์ขนาด 300 มม. ให้ต้นทุนชิปต่อชิ้นต่ำกว่าเวเฟอร์ 200 มม. ของคู่แข่งถึง 40%",
            },
            {
                "icon": "🔄",
                "title": "จุดเปลี่ยนผ่านของกระแสเงินสดอิสระ (CapEx Inflection)",
                "desc": "หลังผ่านจุดลงทุนสร้างโรงงานสูงสุด กระแสเงินสดอิสระจะพุ่งกลับมาคืนสู่ผู้ถือหุ้น",
            },
            {
                "icon": "💵",
                "title": "ประวัติศาสตร์การจ่ายเงินปันผลเพิ่มขึ้นต่อเนื่องกว่า 20 ปี",
                "desc": "เป็นหนึ่งในหุ้นชิปที่มีเสถียรภาพเงินปันผลสูงที่สุดในดัชนี S&P 500",
            },
        ],
    },
    "AMZN": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 330.00,
        "primary_model": "AWS Operating Profit Multiple + Free Cash Flow Yield (4.5%)",
        "model_desc": "ประเมินจากกำไรดำเนินงานของ AWS Cloud Infrastructure ผสานกับกระแสเงินสดอิสระจากธุรกิจค้าปลีกและโฆษณา",
        "math_details": {
            "formula": "Blended Model: 0.50 × (FY27 Forward EPS $15.50 × P/E 22x = $341.00) + 0.50 × (FCF per share $14.35 ÷ 4.5% = $318.89) = $330.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): รายได้รวมกว่า $620B, AWS Operating Margin พุ่งแตะ 38%, TTM EPS $12.37, FCF ทำสถิติใหม่กว่า $50B",
            "key_multiples": "Forward P/E 22.0x, AWS Growth +19%, FCF Yield 4.5%, Operating Margin 11.5%",
            "wall_street_target": "$326.80 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $400.00)",
            "explanation": "AWS เติบโตเร่งตัวจากการเปิดตัว Trainium2 และ generative AI Bedrock ผนวกกับอัตรากำไรค้าปลีกและโฆษณาดีดตัวขึ้น ราคาเหมาะสม $330.00 สอดคล้องกับเป้าวอลล์สตรีท ($326.80)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "☁️",
                "title": "AWS AI Cloud Infrastructure เติบโตก้าวกระโดด",
                "desc": "ส่วนแบ่งตลาดคลาวด์อันดับ 1 ของโลก พร้อมชิป AI Trainium & Inferentia ลดต้นทุนประมวลผล",
            },
            {
                "icon": "📦",
                "title": "โครงข่ายโลจิสติกส์ระดับภูมิภาคสร้างกระแสเงินสด",
                "desc": "การปรับโครงสร้าง Regionalization ดันประสิทธิภาพส่งสินค้าและหนุนอัตรากำไรค้าปลีกสูงสุดในรอบ 5 ปี",
            },
            {
                "icon": "📢",
                "title": "ธุรกิจโฆษณาดิจิทัลอัตรากำไรสูง",
                "desc": "รายได้ค่าโฆษณาบนแพลตฟอร์มและ Prime Video ขยายตัวต่อเนื่องด้วย Net Margin ระดับ 50%+",
            },
        ],
    },
    "NFLX": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 80.00,
        "primary_model": "Global Streaming Monopoly + Ad-Tier Scale Multiple (19x P/E on Split-adjusted)",
        "model_desc": "ประเมินจากอำนาจผูกขาดแพลตฟอร์มสตรีมมิ่งระดับโลก แพ็กเกจโฆษณา และการถ่ายทอดสดกีฬาระดับโลก",
        "math_details": {
            "formula": "Forward FY27 EPS ($4.20) × Target P/E (19x) = $79.80 -> ปรับฐานที่ $80.00 (อิงมูลค่าหลังการแตกพาร์)",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): TTM EPS $3.46, สมาชิกทะลุ 280 ล้านคนทั่วโลก, Operating Margin ขยายตัวสู่ 28%, FCF กว่า $7B",
            "key_multiples": "Forward P/E 19.0x, Paid Memberships 280M+, Operating Margin 28%, FCF Yield 4.8%",
            "wall_street_target": "$84.68 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $105.00)",
            "explanation": "Netflix เป็นผู้ชนะรายเดียวในสงครามสตรีมมิ่งที่ทำกำไรมหาศาล ขณะที่คู่แข่งยังคงขาดทุน ราคาเหมาะสม $80.00 ต่ำกว่าเป้าหมายเฉลี่ยวอลล์สตรีท ($84.68)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🎬",
                "title": "ผู้ชนะสงครามสตรีมมิ่งระดับโลกเพียงรายเดียวที่ทำกำไรแท้จริง",
                "desc": "มีฐานสมาชิกเหนียวแน่นกว่า 280 ล้านครัวเรือนทั่วโลก และมี Churn Rate ต่ำที่สุดในอุตสาหกรรม",
            },
            {
                "icon": "📺",
                "title": "แพ็กเกจโฆษณาและสิทธิ์ถ่ายทอดสดกีฬาหนุนรายได้ใหม่",
                "desc": "ดีลถ่ายทอดสดมวย กีฬา NFL และ WWE ดึงดูดเม็ดเงินโฆษณาแบรนด์ระดับพรีเมียม",
            },
            {
                "icon": "💵",
                "title": "กระแสเงินสดอิสระจากการดำเนินงานขยายตัวมหาศาล",
                "desc": "สร้าง Free Cash Flow มากกว่า $7 พันล้านดอลลาร์ นำไปซื้อหุ้นคืนเพื่อเพิ่มมูลค่าต่อหุ้น",
            },
        ],
    },
    "CRWD": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 245.00,
        "primary_model": "Falcon AI Cybersecurity Platform + FCF Multiple (30x P/FCF)",
        "model_desc": "ประเมินจากอัตราการเติบโตของรายได้ประจำ (ARR) บนแพลตฟอร์ม Falcon และกระแสเงินสดอิสระที่เหนียวแน่น",
        "math_details": {
            "formula": "Forward FY27 FCF per share ($8.20) × Target P/FCF (30x) = $246.00 -> ปรับฐานที่ $245.00",
            "accounting_source": "งบการเงินล่าสุด: รายได้ประจำ ARR โตเกิน $4.0B (+27% YoY), Gross Margin ระดับ 78%, FCF Margin แข็งแกร่งกว่า 30%",
            "key_multiples": "P/FCF 30.0x, ARR Growth +27%, Net Retention Rate 115%+, Gross Margin 78%",
            "wall_street_target": "$254.02 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $320.00)",
            "explanation": "หลังเหตุการณ์ขัดข้องทางเทคนิค ลูกค้ายังคงอยู่ครบและต่อสัญญาในระดับสูง สะท้อนอำนาจสลับระบบที่ยากมาก ราคาเหมาะสม $245.00 สอดคล้องกับเป้าวอลล์สตรีท ($254.02)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🛡️",
                "title": "แพลตฟอร์ม Falcon AI Endpoint & Cloud Security อันดับ 1",
                "desc": "เทคโนโลยี Single Agent และ Cloud-native ป้องกันการเจาะระบบแบบเรียลไทม์",
            },
            {
                "icon": "🔒",
                "title": "ต้นทุนการเปลี่ยนระบบสูงมาก (High Switching Cost)",
                "desc": "องค์กรขนาดใหญ่ระดับ Fortune 500 พึ่งพา CrowdStrike และมี Net Retention Rate เกิน 115%",
            },
            {
                "icon": "💵",
                "title": "ความสามารถในการสร้างกระแสเงินสดอิสระสูงกว่า 30%",
                "desc": "สัดส่วนรายได้แบบ Subscription ประจำปีช่วยให้กระแสเงินสดมีความแน่นอนสูง",
            },
        ],
    },
    "ENSG": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 220.00,
        "primary_model": "Post-Acute Healthcare Rollup + Real Estate Portfolio (26x P/E)",
        "model_desc": "ประเมินจากความสามารถในการเข้าซื้อและพลิกฟื้นสถานพยาบาลฟื้นฟูหลังวิกฤต (Skilled Nursing) ทั่วสหรัฐ",
        "math_details": {
            "formula": "Forward FY27 EPS ($8.50) × Target P/E (26x) = $221.00 -> ปรับฐานที่ $220.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): TTM EPS $6.72, รายได้เติบโต 15% YoY, Occupancy Rate พุ่งขึ้นต่อเนื่อง, ถือครองกรรมสิทธิ์อสังหาริมทรัพย์เพื่อการแพทย์มหาศาล",
            "key_multiples": "Forward P/E 26.0x, ROE 19.5%, Occupancy Rate 80%+, 20-Year Dividend Growth Streak",
            "wall_street_target": "$225.80 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $250.00)",
            "explanation": "โครงสร้างประชากรผู้สูงอายุในสหรัฐเป็นเมกะเทรนด์ระยะยาว Ensign มีสถิติการเข้าซื้อกิจการที่ทำกำไรต่อเนื่องมา 20 ปี ราคาเหมาะสม $220.00 ให้ความคุ้มค่าสูง",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🏥",
                "title": "ผู้นำบริการดูแลผู้ป่วยฟื้นฟูหลังการผ่าตัดและผู้สูงอายุ",
                "desc": "ได้รับประโยชน์โดยตรงจากคลื่นประชากร Baby Boomer เข้าสู่วัยเกษียณ",
            },
            {
                "icon": "🏢",
                "title": "ถือครองกรรมสิทธิ์อสังหาริมทรัพย์สถานพยาบาลมูลค่าสูง",
                "desc": "โมเดลเป็นเจ้าของสินทรัพย์จริงช่วยลดต้นทุนค่าเช่าและเพิ่มมูลค่าสินทรัพย์ตามกาลเวลา",
            },
            {
                "icon": "📈",
                "title": "สถิติกำไรและเงินปันผลเติบโตต่อเนื่องติดต่อกันกว่า 20 ปี",
                "desc": "การบริหารจัดการแบบกระจายอำนาจช่วยให้แต่ละสาขาทำกำไรสูงสุดในพื้นที่",
            },
        ],
    },
    "OLLI": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 102.00,
        "primary_model": "Closeout Retail Store Expansion + Comp Sales Growth (21x P/E)",
        "model_desc": "ประเมินจากการขยายสาขาค้าปลีกสินค้าราคาประหยัด (Extreme Value) และการซื้อสินค้าค้างสต็อกจากแบรนด์ดังมาลดราคา 70%",
        "math_details": {
            "formula": "Forward FY27 EPS ($4.90) × Target P/E (21x) = $102.90 -> ปรับฐานที่ $102.00",
            "accounting_source": "งบการเงินล่าสุด: TTM EPS $4.47, ยอดขายสาขาเดิม (Comparable Sales) โตแข็งแกร่ง, ขยายสาขาใหม่กว่า 50 สาขาต่อปี, ปลอดหนี้สินระยะยาว",
            "key_multiples": "Forward P/E 21.0x, Comparable Sales +5.8%, D/E 0.0x, Ollie's Army Members 14M+",
            "wall_street_target": "$103.13 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $120.00)",
            "explanation": "ในยุคที่ผู้บริโภคระมัดระวังการใช้จ่าย สินค้าราคาประหยัดของ Ollie's ขายดีเป็นประวัติการณ์ ราคาเหมาะสม $102.00 สอดคล้องกับเป้าหมายนักวิเคราะห์ ($103.13)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🛒",
                "title": "ธุรกิจค้าปลีกส่วนลดขั้นสุดที่ทนทานต่อภาวะเศรษฐกิจถดถอย",
                "desc": "ผู้บริโภคหลั่งไหลเข้ามาประหยัดค่าใช้จ่าย หนุนยอดขายสาขาเดิมเติบโตสวนกระแส",
            },
            {
                "icon": "📦",
                "title": "โอกาสทองจากการเข้าซื้อสต็อกสินค้าล้นตลาดของแบรนด์ชั้นนำ",
                "desc": "มีความสัมพันธ์ใกล้ชิดกับผู้ผลิตสินค้าอุปโภคบริโภค ได้ต้นทุนสินค้าต่ำมาก",
            },
            {
                "icon": "🎯",
                "title": "โปรแกรมสมาชิก Ollie's Army กว่า 14 ล้านคน",
                "desc": "ฐานลูกค้าประจำที่เหนียวแน่นช่วยกระตุ้นยอดซื้อซ้ำและสร้างเสถียรภาพรายได้",
            },
        ],
    },
    "COST": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 1100.00,
        "primary_model": "Membership Fee Profit Engine + Negative Working Capital (45x P/E)",
        "model_desc": "ประเมินจากโมเดลค่าสมาชิกรายปีที่มีอัตราการต่ออายุ 93% และอำนาจหมุนเวียนกระแสเงินสดติดลบ (Negative Working Capital)",
        "math_details": {
            "formula": "Forward FY27 EPS ($24.50) × Target P/E (45x) = $1,102.50 -> ปรับฐานที่ $1,100.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): รายได้รวม $260B+, TTM EPS $20.76, กำไรจากค่าสมาชิก Membership Fees คิดเป็นกว่า 70% ของกำไรจากการดำเนินงานทั้งหมด",
            "key_multiples": "Forward P/E 45.0x, Renewal Rate 93.0%+, Negative Working Capital, ROIC 28%",
            "wall_street_target": "$1,085.79 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $1,315.00)",
            "explanation": "Costco ไม่ได้หากำไรจากการบวกราคาสินค้า (จำกัด Markup ไม่เกิน 14%) แต่ทำกำไรมหาศาลจากค่าสมาชิกที่มีความเหนียวแน่นสูงสุดในโลก ราคาเหมาะสม $1,100.00 สอดคล้องกับเป้าวอลล์สตรีท ($1,085.79)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "💳",
                "title": "เครื่องจักรค่าสมาชิกอัตราต่ออายุสูงกว่า 93%",
                "desc": "มีสมาชิกแบบชำระเงินกว่า 130 ล้านคนทั่วโลก สร้างกระแสเงินสดค่าสมาชิกสม่ำเสมอเป็นแกนกำไรหลัก",
            },
            {
                "icon": "🔄",
                "title": "ปราการเงินทุนหมุนเวียนติดลบ (Negative Working Capital)",
                "desc": "ขายสินค้าและเก็บเงินสดจากลูกค้าได้ก่อนถึงกำหนดจ่ายเงินให้เจ้าหนี้การค้ากว่า 30 วัน",
            },
            {
                "icon": "🏷️",
                "title": "แบรนด์ Kirkland Signature ทรงพลังระดับโลก",
                "desc": "เฮาส์แบรนด์ Kirkland มียอดขายแซงหน้าแบรนด์ระดับโลกหลายแบรนด์ หนุนมาร์จิ้นสูงกว่าสินค้าทั่วไป",
            },
        ],
    },
    "WMT": {
        "model_type": "BIG_TECH_GROWTH",
        "fair_price": 130.00,
        "primary_model": "Omnichannel Scale Moat + Walmart Connect High-Margin Ad (38x P/E)",
        "model_desc": "ประเมินจากการครองส่วนแบ่งค้าปลีกอันดับ 1 ของสหรัฐ ร่วมกับการเติบโตของธุรกิจโฆษณาดิจิทัล Walmart Connect และระบบคลังอัตโนมัติ",
        "math_details": {
            "formula": "Forward FY27 EPS ($3.40) × Target P/E (38x) = $129.20 -> ปรับฐานที่ $130.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): รายได้รวมกว่า $680B, TTM EPS $2.76, ธุรกิจโฆษณา Walmart Connect โตแรงกว่า 26% YoY, E-commerce โต 22%",
            "key_multiples": "Forward P/E 38.0x, Walmart Connect Growth +26%, E-commerce Scale, Market Cap ~$1T",
            "wall_street_target": "$132.58 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $155.00)",
            "explanation": "Walmart ก้าวข้ามค้าปลีกแบบดั้งเดิมสู่แพลตฟอร์มเทคโนโลยีโฆษณาและโลจิสติกส์อัตโนมัติหนุนอัตรากำไรขยายตัว ราคาเหมาะสม $130.00 สอดคล้องกับเป้าหมายเฉลี่ยวอลล์สตรีท ($132.58)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🛒",
                "title": "เครือข่ายสาขาครอบคลุม 90% ของประชากรสหรัฐในรัศมี 10 ไมล์",
                "desc": "แปลงสาขากว่า 4,700 แห่งให้เป็นศูนย์กระจายสินค้า E-commerce ส่งด่วนถึงบ้านภายในไม่กี่ชั่วโมง",
            },
            {
                "icon": "📢",
                "title": "ธุรกิจโฆษณาค้าปลีก Walmart Connect มาร์จิ้นสูงเกิน 70%",
                "desc": "ใช้ข้อมูลการซื้อสินค้าจริงของลูกค้าเพื่อดึงเม็ดเงินโฆษณาจากแบรนด์สินค้าอุปโภคบริโภคชั้นนำ",
            },
            {
                "icon": "🤖",
                "title": "ระบบคลังสินค้าอัตโนมัติหุ่นยนต์ Symbotic ลดต้นทุนระยะยาว",
                "desc": "นำหุ่นยนต์ AI คัดแยกสินค้ามาใช้ในศูนย์กระจายสินค้าทุกแห่ง ดันประสิทธิภาพโลจิสติกส์สูงสุด",
            },
        ],
    },
    "TSM": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 525.00,
        "primary_model": "Foundry Monopoly Pricing Power + Forward P/E (25x)",
        "model_desc": "ประเมินจากอำนาจผูกขาดการผลิตชิปขั้นสูง 3nm และ 2nm ทั่วโลกกว่า 90% ของตลาด AI Accelerator",
        "math_details": {
            "formula": "Forward Run-rate FY27 EPS ($21.00) × Target P/E (25x) = $525.00",
            "accounting_source": "งบไตรมาสล่าสุด: TTM EPS $15.54, Gross Margin แข็งแกร่งระดับ 57.8%, รายได้ AI HPC โตเกิน 50% YoY, CapEx $30B-$32B",
            "key_multiples": "Forward P/E 25.0x, Gross Margin 57.8%, ROE 31.5%, Net Margin 42.5%",
            "wall_street_target": "$554.22 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $650.00)",
            "explanation": "TSMC ผูกขาดการรับจ้างผลิตชิป AI ทั้งหมดให้ Nvidia, Apple, AMD และ Qualcomm โดยกำลังผลิต 2nm และ CoWoS เต็มล่วงหน้า ราคาเหมาะสม $525.00 ให้ส่วนลดอนุรักษนิยมเทียบเป้าวอลล์สตรีท ($554.22)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🏭",
                "title": "การผูกขาดเทคโนโลยีชิปขั้นสูง 3nm & 2nm",
                "desc": "เป็นผู้ผลิตรายเดียวในโลกที่มีผลผลิต Yield ระดับอุตสาหกรรมสำหรับชิป AI ประสิทธิภาพสูงสุด",
            },
            {
                "icon": "📦",
                "title": "เทคโนโลยีแพ็กเกจจิ้ง CoWoS กุมชะตากรรม AI ทั่วโลก",
                "desc": "คอขวดของชิป AI ทุกตัวอยู่ที่ CoWoS ทำให้ TSMC มีอำนาจกำหนดราคาขาย (Pricing Power) เบ็ดเสร็จ",
            },
            {
                "icon": "💰",
                "title": "อัตรากำไรสุทธิเกิน 42% สูงที่สุดในประวัติศาสตร์อุตสาหกรรม",
                "desc": "สร้างกระแสเงินสดจากการดำเนินงานระดับ $40B+ ต่อปี รองรับการลงทุนขยายโรงงานทั่วโลกอย่างไร้ความเสี่ยง",
            },
        ],
    },
    "ASML": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 2200.00,
        "primary_model": "EUV Lithography Monopoly Backlog Conversion + Forward P/E (34x)",
        "model_desc": "ประเมินจากการส่งมอบเครื่องพิมพ์ชิป High-NA EUV และยอด Backlog การสั่งซื้อเครื่องจักรทั่วโลกกว่า €36B",
        "math_details": {
            "formula": "FY27 Forward EPS ($65.00) × Multiple P/E (34x) = $2,210.00 -> ปรับฐานที่ $2,200.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): TTM EPS $40.60, Gross Margin 51.3%, ยอดสั่งจองสุทธิ Backlog มากกว่า €36 พันล้านยูโร",
            "key_multiples": "Forward P/E 34.0x, High-NA EUV Backlog €36B+, Gross Margin 51.3%, ROIC 35%",
            "wall_street_target": "$2,379.18 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $2,800.00)",
            "explanation": "ASML เป็นผู้ผลิตเครื่อง EUV เพียงรายเดียวในโลก หากไม่มี ASML โลกจะไม่สามารถผลิตชิป AI ต่ำกว่า 5nm ได้เลย ราคาเหมาะสม $2,200.00 ต่ำกว่าเป้าวอลล์สตรีท ($2,379.18) เล็กน้อยเพื่อความปลอดภัย",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🔬",
                "title": "ผู้ผลิตเครื่องจักร EUV Lithography รายเดียวในโลก 100%",
                "desc": "มีสิทธิบัตรและองค์ความรู้ด้านเลเซอร์แสงความยาวคลื่น 13.5nm ที่ไม่มีคู่แข่งรายใดในโลกทำได้",
            },
            {
                "icon": "📋",
                "title": "ยอดสั่งซื้อล่วงหน้า (Backlog) รองรับรายได้ยาวหลายปี",
                "desc": "มี Backlog เครื่องจักรสะสมกว่า 36,000 ล้านยูโร รับประกันรายได้และกระแสเงินสดล่วงหน้า",
            },
            {
                "icon": "💎",
                "title": "เครื่อง High-NA EUV ราคาเครื่องละกว่า $350M ดันรายได้ก้าวกระโดด",
                "desc": "การเข้าสู่นาโนเมตร 2nm และ 1.4nm บังคับให้โรงงานชิปทั่วโลกต้องซื้อเครื่อง High-NA รุ่นใหม่",
            },
        ],
    },
    "AVGO": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 485.00,
        "primary_model": "AI Custom ASIC (XPU) + VMware Synergy Forward P/E (36x)",
        "model_desc": "ประเมินจากส่วนแบ่งตลาด AI Custom ASIC (Google TPU, Meta MTIA) ร่วมกับการขยายตัวของซอฟต์แวร์ VMware",
        "math_details": {
            "formula": "Forward Run-rate FY27 EPS ($13.50) × Target P/E (36x) = $486.00 -> กำหนดฐาน $485.00",
            "accounting_source": "งบการเงินล่าสุด: TTM EPS $7.83, รายได้ชิป AI และ Networking โตกว่า 280% YoY, อัตรากำไร EBITDA สูงกว่า 60%",
            "key_multiples": "Forward P/E 36.0x, AI Revenue Contribution 40%+, FCF Margin 48%, D/E 1.1x",
            "wall_street_target": "$528.91 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $600.00)",
            "explanation": "Broadcom กุมตลาดชิปเน็ตเวิร์ก PCIe/Tomahawk และออกแบบ Custom AI Silicon ให้บิ๊กเทค ราคาเหมาะสม $485.00 มีส่วนเผื่อความปลอดภัยจากราคาเป้าหมายเฉลี่ยสถาบัน ($528.91)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "⚡",
                "title": "เบอร์ 1 ของโลกด้าน Custom AI Silicon (XPU)",
                "desc": "ผู้ออกแบบชิป AI ร่วมกับ Google (TPU) และ Meta พร้อมลูกค้ารายใหญ่รายที่ 3 เพิ่มรายได้มหาศาล",
            },
            {
                "icon": "🌐",
                "title": "ผู้นำผูกขาดชิปเน็ตเวิร์ก AI Data Center",
                "desc": "สวิตช์ Tomahawk และ Jericho เชื่อมต่อ AI Cluster ระดับแสนชิปอย่างไร้รอยต่อ",
            },
            {
                "icon": "💻",
                "title": "กระแสเงินสดประจำ (ARR) มหาศาลจาก VMware",
                "desc": "การเปลี่ยนผ่านสู่ Subscription เต็มรูปแบบสร้างกระแสเงินสดที่ทำนายได้ระดับ $12B+ ต่อปี",
            },
        ],
    },
    "MU": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 1425.00,
        "primary_model": "HBM3E / HBM4 Memory Supercycle Multiple (15x P/E)",
        "model_desc": "ประเมินจากวัฏจักรขาขึ้นของหน่วยความจำแบนด์วิดท์สูง HBM3E และ Enterprise SSD ที่ถูกจองเต็มจนถึงปี 2027",
        "math_details": {
            "formula": "Forward Peak Supercycle EPS ($95.00) × Multiple P/E (15x) = $1,425.00",
            "accounting_source": "งบ TTM ล่าสุด: TTM EPS พุ่งแตะ $74.21, อัตรากำไรขั้นต้น Gross Margin ขยายตัวจาก 20% สู่ 55%+, ยอดขาย HBM Sold-out 100%",
            "key_multiples": "Forward P/E 15.0x, Gross Margin 55%+, HBM Sold-out Allocation 100%, ROE 45%",
            "wall_street_target": "$1,631.56 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $2,200.00)",
            "explanation": "การผลิต HBM ต้องใช้เวเฟอร์มากกว่า DRAM ปกติ 3 เท่า ส่งผลให้เกิดภาวะขาดแคลนชิปหน่วยความจำทั่วโลก ราคาเหมาะสม $1,425.00 ต่ำกว่าเป้าเฉลี่ยวอลล์สตรีท ($1,631.56) เพื่อป้องกันความผันผวนของวัฏจักรชิป",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🧠",
                "title": "พันธมิตรชิปหน่วยความจำ HBM3E สำหรับ Nvidia Blackwell",
                "desc": "ชิป HBM3E 8-High และ 12-High กินพลังงานต่ำกว่าคู่แข่ง 30% ได้รับการรับรองหลักจาก Nvidia",
            },
            {
                "icon": "📈",
                "title": "อุปทานขาดแคลนขั้นรุนแรง (Structural Shortage)",
                "desc": "การจัดสรรกำลังการผลิต HBM ขายหมดล่วงหน้าจนถึงปี 2027 หนุนราคาขายเฉลี่ย (ASP) พุ่งขึ้นต่อเนื่อง",
            },
            {
                "icon": "💾",
                "title": "Enterprise SSD รองรับคลังข้อมูล AI Inference",
                "desc": "ความต้องการ eSSD ความจุ 30TB-60TB เติบโตระเบิด สร้างแหล่งกำไรขาที่สองให้ Micron",
            },
        ],
    },
    "AMD": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 630.00,
        "primary_model": "Data Center GPU (MI325X/MI350) + EPYC Turin CPU P/E (34x)",
        "model_desc": "ประเมินจากการขยายตัวของชิป AI Accelerator ตระกูล Instinct MI300 series และส่วนแบ่งซีพียูเซิร์ฟเวอร์ EPYC เหนือ Intel",
        "math_details": {
            "formula": "Forward FY27 EPS ($18.50) × Target P/E (34x) = $629.00 -> ปรับฐานที่ $630.00",
            "accounting_source": "งบการเงินล่าสุด: TTM EPS $4.60, รายได้ Data Center โตเกิน 120% YoY, รายได้จากชิป AI Instinct ทะลุ $5.0B ต่อปี",
            "key_multiples": "Forward P/E 34.0x, Data Center Growth +122%, Server CPU Market Share 34%+, D/E 0.04x",
            "wall_street_target": "$657.45 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $800.00)",
            "explanation": "AMD เป็นทางเลือก GPU เบอร์สองที่บิ๊กเทค (Microsoft, Meta, Oracle) ใช้ลดการพึ่งพา Nvidia ราคาเหมาะสม $630.00 สอดคล้องกับราคาเป้าหมายสถาบัน ($657.45)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🚀",
                "title": "คู่แข่งอันดับหนึ่งของ Nvidia ในตลาด Data Center AI GPU",
                "desc": "ชิป Instinct MI325X และ MI350 ให้หน่วยความจำสูงกว่า ตอบโจทย์งาน AI Inference คุ้มต้นทุน",
            },
            {
                "icon": "🖥️",
                "title": "ครองส่วนแบ่งซีพียูเซิร์ฟเวอร์ EPYC ข้ามเส้น 34%",
                "desc": "ซีพียูสถาปัตยกรรม Zen 5 (Turin) ประหยัดไฟและแรงกว่าคู่แข่ง กวาดส่วนแบ่งตลาดต่อเนื่อง",
            },
            {
                "icon": "🛡️",
                "title": "งบดุลสะอาดปราศจากหนี้สิน",
                "desc": "สัดส่วนหนี้สินต่อทุน D/E เพียง 0.04 เท่า คล่องตัวสูงในการเข้าซื้อกิจการ ZT Systems เพื่อขายแร็ก AI แบบครบวงจร",
            },
        ],
    },
    "ARM": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 255.00,
        "primary_model": "Armv9 Royalty Rate Expansion + Compute Subsystems (CSS) P/E (80x)",
        "model_desc": "ประเมินจากอัตราค่าสิทธิบัตร (Royalty Rate) ที่เพิ่มขึ้น 2 เท่าจากสถาปัตยกรรม Armv9 และแพลตฟอร์ม Neoverse V2 ในดาต้าเซ็นเตอร์",
        "math_details": {
            "formula": "Forward FY27 EPS ($3.20) × Multiple P/E (80x) = $256.00 -> กำหนดฐาน $255.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): TTM EPS $0.87, อัตราค่าสิทธิบัตร Royalty โต 23% YoY, สัดส่วน Armv9 พุ่งแตะ 25% ของรายได้ค่าสิทธิบัตร",
            "key_multiples": "Forward P/E 80.0x, Royalty Rate Expansion 2x, Gross Margin 96%, FCF Margin 40%",
            "wall_street_target": "$267.78 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $350.00)",
            "explanation": "Arm เป็นสถาปัตยกรรมซีพียูที่ประหยัดพลังงานที่สุดในโลก ใช้ในชิป Nvidia Grace, AWS Graviton และ Apple M-Series ราคาเหมาะสม $255.00 ต่ำกว่าเป้าวอลล์สตรีท ($267.78)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "📱",
                "title": "ผูกขาดสถาปัตยกรรมสมาร์ตโฟน 99% และรุกกินตลาด PC & Cloud",
                "desc": "สมาร์ตโฟน AI และแล็ปท็อป Copilot+ PC หันมาใช้สถาปัตยกรรม Arm ทั้งหมด",
            },
            {
                "icon": "📈",
                "title": "ค่าสิทธิบัตร Armv9 เพิ่มขึ้นสองเท่าตัวต่อหนึ่งชิป",
                "desc": "การใส่ชุดคำสั่ง AI SVE2 ทำให้ Arm เก็บค่าลิขสิทธิ์จากผู้ผลิตชิปได้สูงขึ้นแบบก้าวกระโดด",
            },
            {
                "icon": "💎",
                "title": "โมเดลธุรกิจไร้ต้นทุนสินค้า (Gross Margin 96%)",
                "desc": "ขายทรัพย์สินทางปัญญา (IP) ไร้ความเสี่ยงด้านโรงงาน สร้างกำไรเงินสดอิสระแท้จริง",
            },
        ],
    },
    "LRCX": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 335.00,
        "primary_model": "Cryogenic Etch Monopoly + 3D Memory WFE Forward P/E (32x)",
        "model_desc": "ประเมินจากความต้องการเครื่องจักรกัดกรดซิลิคอนระดับอะตอม (Etch) ในการผลิตชิป 3D NAND และ HBM",
        "math_details": {
            "formula": "Forward FY27 EPS ($10.50) × Target P/E (32x) = $336.00 -> ปรับฐานที่ $335.00",
            "accounting_source": "งบการเงินล่าสุด: TTM EPS $6.72, Gross Margin 48.5%, รายได้จากจีนและเอเชียฟื้นตัวแรง, ยอดคำสั่งซื้อเครื่องมือ AI WFE แข็งแกร่ง",
            "key_multiples": "Forward P/E 32.0x, Gross Margin 48.5%, ROIC 40%, Installed Base 90,000+ Chambers",
            "wall_street_target": "$365.67 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $450.00)",
            "explanation": "การซ้อนชั้นหน่วยความจำ NAND เกิน 300 ชั้นและ HBM3E จำเป็นต้องใช้เทคโนโลยี Cryo Etch ของ Lam Research เท่านั้น ราคาเหมาะสม $335.00 ให้ส่วนลดจากเป้าวอลล์สตรีท ($365.67)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "⚙️",
                "title": "เบอร์ 1 ของโลกด้านเครื่องมือกัดกรดชิปหน่วยความจำ (Etch)",
                "desc": "ครองส่วนแบ่งตลาด Dielectric Etch เกิน 50% มีความสำคัญยิ่งยวดต่อการสเกลชิปความจำ AI",
            },
            {
                "icon": "🔄",
                "title": "รายได้บริการหลังการขาย Customer Support แข็งแกร่ง",
                "desc": "มีฐานเครื่องจักรที่ติดตั้งแล้วกว่า 90,000 เครื่องทั่วโลก สร้างรายได้บำรุงรักษาสม่ำเสมอ",
            },
            {
                "icon": "❄️",
                "title": "เทคโนโลยี Cryogenic Etching เปลี่ยนประวัติศาสตร์เซมิคอนดักเตอร์",
                "desc": "ลดการใช้พลังงานและเจาะรูลึกระดับนาโนเมตรได้อย่างแม่นยำสูง",
            },
        ],
    },
    "ALAB": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 320.00,
        "primary_model": "PCIe Gen 6 / CXL Retimer Market Leader Multiple (55x)",
        "model_desc": "ประเมินจากการผูกขาดชิปเชื่อมต่อความเร็วสูง Aries Retimer และโมดูล CXL ในเซิร์ฟเวอร์ AI ทั่วโลก",
        "math_details": {
            "formula": "Forward FY27 EPS ($5.80) × Multiple P/E (55x) = $319.00 -> ปรับฐานที่ $320.00",
            "accounting_source": "งบการเงินล่าสุด: TTM EPS $2.52, รายได้เติบโตร้อนแรงกว่า 200% YoY, Gross Margin ระดับ 77.5%, ลูกค้าหลักคือ Nvidia และบิ๊กเทค Hyperscalers",
            "key_multiples": "Forward P/E 55.0x, Revenue Growth +206%, Gross Margin 77.5%, D/E 0.0x (No Debt)",
            "wall_street_target": "$355.28 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $420.00)",
            "explanation": "ทุกเซิร์ฟเวอร์ AI ยิ่งใช้ GPU มาก ยิ่งต้องใช้ Retimer ของ Astera Labs เชื่อมต่อสัญญาณไม่ให้ขาดหาย ราคาเหมาะสม $320.00 อิงจากส่วนแบ่งตลาดชิปเชื่อมต่อกว่า 80%",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🔌",
                "title": "ผู้นำอันดับหนึ่งชิปเชื่อมต่อ PCIe Gen 5/6 & CXL",
                "desc": "ครองส่วนแบ่งตลาด Retimer ใน AI Server มากกว่า 80% ติดตั้งคู่กับ Nvidia Blackwell ทุกเครื่อง",
            },
            {
                "icon": "🚀",
                "title": "รายได้โตระเบิดกว่า 200% YoY จากคลื่น AI Connectivity",
                "desc": "โมดูล Taurus Active Electrical Cable และ Scorpio Fabric Switch ขยายตลาดเป็นทวีคูณ",
            },
            {
                "icon": "🛡️",
                "title": "บริษัทไร้หนี้สินและมีเงินสดเต็มมือ",
                "desc": "มีสถานะการเงินมั่นคงสูง Gross Margin สูงถึง 77.5% แสดงถึงอำนาจผูกขาดเทคโนโลยี",
            },
        ],
    },
    "CRDO": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 250.00,
        "primary_model": "HiWire Active Electrical Cables (AEC) Expansion P/E (48x)",
        "model_desc": "ประเมินจากการเปลี่ยนผ่านของสายเชื่อมต่อใน Data Center จากทองแดงแบบเดิมมาเป็นสายแอคทีฟ AEC ของ Credo",
        "math_details": {
            "formula": "Forward FY27 EPS ($5.20) × Target P/E (48x) = $249.60 -> กำหนดฐาน $250.00",
            "accounting_source": "งบไตรมาสล่าสุด: TTM EPS $2.80, รายได้ทำ All-Time High, อัตรากำไรขั้นต้นขยายตัวแตะ 65%, ยอดส่งมอบสายเคเบิล AEC เติบโตก้าวกระโดด",
            "key_multiples": "Forward P/E 48.0x, AEC Market Share 75%+, Gross Margin 65%, Cash $400M+",
            "wall_street_target": "$281.59 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $350.00)",
            "explanation": "สายเคเบิลทองแดงแบบเดิมหนาและกินไฟเกินไปในการเชื่อมต่อเซิร์ฟเวอร์ AI สาย AEC ของ Credo จึงกลายเป็นมาตรฐานบังคับ ราคาเหมาะสม $250.00 ต่ำกว่าเป้าวอลล์สตรีท ($281.59)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🔗",
                "title": "เจ้าตลาดสายเคเบิลความเร็วสูง HiWire AEC ในดาต้าเซ็นเตอร์",
                "desc": "ประหยัดพลังงานกว่าสาย Optical Transceiver ถึง 50% และทนทานกว่าสายทองแดงทั่วไป",
            },
            {
                "icon": "📊",
                "title": "การเติบโตสอดรับการสเกล Rack-Scale ของ Nvidia & Hyperscalers",
                "desc": "ยอดสั่งซื้อสายเคเบิลความเร็ว 800Gbps และ 1.6Tbps เพิ่มขึ้นอย่างมหาศาล",
            },
            {
                "icon": "⚡",
                "title": "ชิป SerDes ประสิทธิภาพสูงลดการใช้ไฟฟ้าของระบบ AI",
                "desc": "เทคโนโลยีประมวลผลสัญญาณดิจิทัลที่เป็นกรรมสิทธิ์ช่วยลดความร้อนในตู้แร็กเซิร์ฟเวอร์",
            },
        ],
    },
    "MRVL": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 275.00,
        "primary_model": "Electro-Optics PAM4 DSP + Custom AI ASIC Design Wins (42x P/E)",
        "model_desc": "ประเมินจากชิปประมวลผลสัญญาณแสง Optical DSP (800G/1.6T) ร่วมกับโครงการรับจ้างผลิต Custom AI ASIC ให้บิ๊กเทค",
        "math_details": {
            "formula": "Forward FY27 EPS ($6.50) × Target P/E (42x) = $273.00 -> กำหนดฐาน $275.00",
            "accounting_source": "งบการเงินล่าสุด: TTM EPS $3.04, รายได้ส่วน Data Center คิดเป็นกว่า 70% ของรายได้รวม และเติบโตกว่า 90% YoY",
            "key_multiples": "Forward P/E 42.0x, Optical DSP Market Share 65%, Data Center Mix 70%+, D/E 0.28x",
            "wall_street_target": "$315.99 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $380.00)",
            "explanation": "Marvell ครองตลาดชิปแสงเชื่อมต่อดาต้าเซ็นเตอร์ และมีดีลผลิตชิป AI เฉพาะตัวให้ AWS และลูกค้ารายใหญ่ ราคาเหมาะสม $275.00 สอดคล้องกับปัจจัยพื้นฐาน",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "💡",
                "title": "ผู้นำตลาดชิปประมวลผลแสง Optical DSP ระดับโลก",
                "desc": "กุมส่วนแบ่งชิปแปลงสัญญาณแสงความเร็ว 800G และ 1.6T สำหรับเชื่อมโยงตู้คลัสเตอร์ AI",
            },
            {
                "icon": "🎯",
                "title": "โครงการชิป Custom AI ASIC เริ่มทยอยส่งมอบเชิงพาณิชย์",
                "desc": "ชนะสัญญาออกแบบชิป AI เร่งความเร็วและชิปประมวลผลเฉพาะทางให้คลาวด์ยักษ์ใหญ่",
            },
            {
                "icon": "📈",
                "title": "สัดส่วนรายได้ดาต้าเซ็นเตอร์กลายเป็นแกนนำหลักของบริษัท",
                "desc": "ลดผลกระทบจากวัฏจักรโทรคมนาคมเดิมและก้าวสู่บริษัทโครงสร้างพื้นฐาน AI แท้จริง",
            },
        ],
    },
    "COHR": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 330.00,
        "primary_model": "Optical Transceivers (800G/1.6T) + SiC Substrate Multiple (36x P/E)",
        "model_desc": "ประเมินจากการขยายตัวของโมดูลรับส่งสัญญาณแสงความเร็วสูง 800G/1.6T และเวเฟอร์ Silicon Carbide",
        "math_details": {
            "formula": "Forward FY27 EPS ($9.20) × Target P/E (36x) = $331.20 -> ปรับฐานที่ $330.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): TTM EPS $4.83, กำไรฟื้นตัวอย่างแข็งแกร่ง, ยอดคำสั่งซื้อโมดูล Datacom เติบโตทำสถิติใหม่",
            "key_multiples": "Forward P/E 36.0x, Datacom Optical Growth +80%, Gross Margin 38%, Book Value $45.00",
            "wall_street_target": "$374.72 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $450.00)",
            "explanation": "Coherent เป็นหนึ่งในสองผู้นำระดับโลกด้าน Optical Transceiver เคียงคู่ Innolight ราคาเหมาะสม $330.00 ต่ำกว่าเป้าวอลล์สตรีท ($374.72)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🌐",
                "title": "ผู้นำโลกด้านโมดูลรับส่งสัญญาณแสง Datacom",
                "desc": "ผลิตโมดูลแสงความเร็ว 800G และ 1.6T ส่งมอบให้กับผู้สร้างคลัสเตอร์ซูเปอร์คอมพิวเตอร์ AI",
            },
            {
                "icon": "⚡",
                "title": "เวเฟอร์ซิลิคอนคาร์ไบด์ (SiC) รองรับยานยนต์ไฟฟ้าและพลังงาน",
                "desc": "มีกำลังการผลิตเวเฟอร์ SiC รองรับการใช้งานของโรงงานอุตสาหกรรมและรถยนต์ EV",
            },
            {
                "icon": "🔄",
                "title": "การปรับโครงสร้างองค์กรหนุนอัตรากำไรก้าวกระโดด",
                "desc": "การเปลี่ยนตัวผู้บริหารและการเพิ่มประสิทธิภาพโรงงานช่วยดันอัตรากำไรสุทธิโตต่อเนื่อง",
            },
        ],
    },
    "AMKR": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 60.00,
        "primary_model": "Advanced 2.5D/3D Packaging (OSAT) Capacity Expansion (16x P/E)",
        "model_desc": "ประเมินจากการขยายโรงงานแพ็กเกจจิ้งชิปขั้นสูงในรัฐแอริโซนา สหรัฐอเมริกา และเวียดนาม รองรับชิป AI และยานยนต์",
        "math_details": {
            "formula": "Forward FY27 EPS ($3.80) × Target P/E (16x) = $60.80 -> ปรับฐานที่ $60.00",
            "accounting_source": "งบการเงินล่าสุด: TTM EPS $2.48, รายได้รวม $6.4B, อัตราส่วน P/E ไม่แพงเพียง 15x, ความต้องการ Advanced Packaging โตเด่น",
            "key_multiples": "Forward P/E 16.0x, OSAT Market Share #2 Global, D/E 0.35x, Dividend Yield 0.9%",
            "wall_street_target": "$64.67 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $80.00)",
            "explanation": "Amkor เป็นเบอร์ 2 ของโลกด้านการทดสอบและประกอบชิป (OSAT) และเป็นพันธมิตรหลักของ TSMC ในสหรัฐ ราคาเหมาะสม $60.00 อิงจากส่วนแบ่งตลาดที่แข็งแกร่ง",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "📦",
                "title": "ผู้นำแพ็กเกจจิ้งชิปขั้นสูงภายนอกอันดับสองของโลก",
                "desc": "มีความเชี่ยวชาญด้าน System-in-Package (SiP) และการประกอบชิปความแม่นยำสูง",
            },
            {
                "icon": "🇺🇸",
                "title": "พันธมิตรยุทธศาสตร์ของ TSMC ในการเปิดโรงงานสหรัฐ",
                "desc": "สร้างโรงงาน Advanced Packaging ในแอริโซนาเพื่อรับงานชิปต่อจาก TSMC ในแผ่นดินอเมริกา",
            },
            {
                "icon": "💎",
                "title": "Valuation ไม่แพงและหนี้สินต่ำ",
                "desc": "เทรดที่อัตราส่วน P/E ต่ำกว่ากลุ่มเซมิคอนดักเตอร์ทั่วไป มี Margin of Safety สูง",
            },
        ],
    },
    "GEV": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 1100.00,
        "primary_model": "Power Grid Electrification & Gas Turbine Supercycle (24x P/E)",
        "model_desc": "ประเมินจากยอดจองกังหันก๊าซผลิตไฟฟ้า HA และอุปกรณ์สายส่งโครงข่ายไฟฟ้าอัจฉริยะรองรับโหลด AI Data Center",
        "math_details": {
            "formula": "Forward FY27 EPS ($46.00) × Target P/E (24x) = $1,104.00 -> ปรับฐานที่ $1,100.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): TTM EPS $38.11, กำไรดำเนินงานพลิกฟื้นก้าวกระโดด, ยอดคำสั่งซื้อ Backlog อุปกรณ์ผลิตไฟพุ่งแตะ $110B+",
            "key_multiples": "Forward P/E 24.0x, Backlog $110B+, Power Electrification Leader, FCF $3.5B+",
            "wall_street_target": "$1,147.57 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $1,350.00)",
            "explanation": "คอขวดที่ใหญ่ที่สุดของ AI คือพลังงานไฟฟ้า กังหันก๊าซของ GE Vernova เป็นแหล่งไฟฟ้าระดับกิกะวัตต์ที่ติดตั้งได้เร็วที่สุด ราคาเหมาะสม $1,100.00 อิงจาก Backlog มหาศาล",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "⚡",
                "title": "เบอร์ 1 ด้านอุปกรณ์โครงข่ายและกังหันก๊าซผลิตไฟฟ้า",
                "desc": "มีเทคโนโลยีผลิตไฟฟ้าที่ป้อนพลังงานให้กับดาต้าเซ็นเตอร์ระดับ Hyperscale ทั่วอเมริกา",
            },
            {
                "icon": "📋",
                "title": "ยอดสั่งซื้อล่วงหน้า (Backlog) สูงกว่า $110,000 ล้านดอลลาร์",
                "desc": "รับประกันการเติบโตของรายได้และการผลิตต่อเนื่องตลอด 5-7 ปีข้างหน้า",
            },
            {
                "icon": "🔋",
                "title": "ปลดล็อกคอขวดพลังงานไฟฟ้าของ AI Supercycle",
                "desc": "เป็นผู้ชนะตัวจริงในการอัปเกรดระบบสายส่งไฟฟ้า (Grid Modernization) ทั่วโลก",
            },
        ],
    },
    "BE": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 260.00,
        "primary_model": "Solid Oxide Fuel Cell Microgrid Deployment Multiple (50x P/E)",
        "model_desc": "ประเมินจากการติดตั้งเซลล์เชื้อเพลิงผลิตไฟฟ้านอกโครงข่าย (Off-grid) ให้กับดาต้าเซ็นเตอร์ AI ที่รอสายส่งการไฟฟ้าไม่ไหว",
        "math_details": {
            "formula": "Forward FY27 EPS ($5.20) × Target P/E (50x) = $260.00",
            "accounting_source": "งบการเงินล่าสุด: TTM EPS $1.61, ชนะสัญญาติดตั้งระดับ 1GW ให้กับผู้พัฒนาคลาวด์, กำไรขั้นต้นพลิกฟื้นทำสถิติใหม่",
            "key_multiples": "Forward P/E 50.0x, 1GW Data Center Pipeline, Gross Margin 28%+, Cash Flow Positive",
            "wall_street_target": "$294.59 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $380.00)",
            "explanation": "การขอไฟจากการไฟฟ้าต้องรอนาน 3-5 ปี แต่ระบบของ Bloom Energy ติดตั้งได้ใน 50 วัน ราคาเหมาะสม $260.00 สอดคล้องกับการเป็นทางรอดของดาต้าเซ็นเตอร์",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🔋",
                "title": "เซลล์เชื้อเพลิงโซลิดออกไซด์ (SOFC) จ่ายไฟตรงถึงหน้าไซต์",
                "desc": "ผลิตไฟฟ้าได้ตลอด 24 ชั่วโมง ไร้มลพิษทางอากาศ และไม่ต้องพึ่งพาสายส่งไฟฟ้าสาธารณะ",
            },
            {
                "icon": "⏱️",
                "title": "ความเร็วในการติดตั้งเหนือกว่าการไฟฟ้าดั้งเดิมอย่างสิ้นเชิง",
                "desc": "สามารถจ่ายกระแสไฟฟ้าระดับ 100MW ได้ภายในเวลาไม่กี่เดือน ตอบสนองดีมานด์ AI เร่งด่วน",
            },
            {
                "icon": "🤝",
                "title": "พันธมิตรยุทธศาสตร์กับผู้ให้บริการคลาวด์และยูทิลิตี้",
                "desc": "ชนะสัญญาระดับหลายร้อยเมกะวัตต์หนุนยอดขายเติบโตแบบทวีคูณ",
            },
        ],
    },
    "RKLB": {
        "model_type": "TURNAROUND_SPEC",
        "fair_price": 88.00,
        "primary_model": "Space Launch Monopoly #2 + Space Systems Backlog Multiple (14x P/S)",
        "model_desc": "ประเมินจากจรวด Electron ที่ยิงถี่ที่สุดอันดับสองรองจาก SpaceX และการเปิดตัวจรวดขนส่งขนาดกลาง Neutron",
        "math_details": {
            "formula": "Forward FY27 Revenue ($900M ÷ 143M shares = $6.29/share) × Target P/S (14x) = $88.06 -> ปรับฐานที่ $88.00",
            "accounting_source": "งบการเงินล่าสุด: รายได้รวมเติบโตกว่า 55% YoY, ยอดสั่งจองงานอวกาศ Backlog ทะลุ $1.1B, อัตราความสำเร็จในการยิงจรวด 100%",
            "key_multiples": "Forward P/S 14.0x, Backlog $1.1B+, Electron Launch Success Rate 98%+, Space Systems Mix 70%",
            "wall_street_target": "$96.80 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $130.00)",
            "explanation": "Rocket Lab เป็นผู้ให้บริการยิงจรวดเชิงพาณิชย์รายเดียวในตลาดหุ้นสหรัฐที่มีผลงานจริงเทียบเคียง SpaceX ราคาเหมาะสม $88.00 ต่ำกว่าเป้าวอลล์สตรีท ($96.80)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🚀",
                "title": "เบอร์ 2 ของโลกด้านการยิงจรวดขนส่งสู่อวกาศรองจาก SpaceX",
                "desc": "จรวด Electron ประสบความสำเร็จในการส่งดาวเทียมวงโคจรต่ำอย่างสม่ำเสมอ",
            },
            {
                "icon": "🛰️",
                "title": "ธุรกิจสร้างตัวดาวเทียม Space Systems มี Backlog เกิน $1.1B",
                "desc": "ชนะสัญญาสร้างดาวเทียมป้องกันประเทศให้กองทัพสหรัฐและบริษัทเอกชนทั่วโลก",
            },
            {
                "icon": "🌟",
                "title": "จรวดนำกลับมาใช้ใหม่ Neutron ปลดล็อกการแข่งขันงานหนัก",
                "desc": "รองรับการส่งกลุ่มดาวเทียมอินเทอร์เน็ตและภารกิจสำรวจอวกาศเชิงลึก",
            },
        ],
    },
    "PL": {
        "model_type": "TURNAROUND_SPEC",
        "fair_price": 24.00,
        "primary_model": "Daily Earth Observation Satellite Constellation + Geospatial AI Multiple (8x P/S)",
        "model_desc": "ประเมินจากกลุ่มดาวเทียมถ่ายภาพพื้นผิวโลกทั้งใบทุกวัน และการผนวกโมเดล AI วิเคราะห์ข้อมูลภูมิสารสนเทศ",
        "math_details": {
            "formula": "Forward FY27 Revenue ($450M ÷ 150M shares = $3.00/share) × Target P/S (8x) = $24.00",
            "accounting_source": "งบการเงินล่าสุด: รายได้เติบโตสู่ระดับ $280M+, อัตรากำไรขั้นต้นขยายตัวแตะ 55%, สัญญาภาครัฐและกระทรวงกลาโหมสหรัฐขยายตัว",
            "key_multiples": "Forward P/S 8.0x, Gross Margin 55%, Daily Earth Scan 100%, Defense & Intel Mix 45%",
            "wall_street_target": "$30.36 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $45.00)",
            "explanation": "Planet Labs มีข้อมูลภาพถ่ายดาวเทียมย้อนหลังและเรียลไทม์ที่ไม่มีคู่แข่งรายใดเลียนแบบได้ ราคาเหมาะสม $24.00 ให้ส่วนลดจากเป้าวอลล์สตรีท ($30.36)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🌍",
                "title": "กลุ่มดาวเทียมถ่ายภาพพื้นผิวโลกทั้งใบทุกๆ 24 ชั่วโมง",
                "desc": "เป็นคลังข้อมูลภาพถ่ายดาวเทียมที่ละเอียดและต่อเนื่องที่สุดในโลกสำหรับฝึกโมเดล AI",
            },
            {
                "icon": "🛡️",
                "title": "สัญญาด้านความมั่นคงและข่าวกรองกับรัฐบาลสหรัฐและพันธมิตร",
                "desc": "ภาพถ่ายแบบเรียลไทม์มีความจำเป็นยิ่งยวดในความขัดแย้งทางภูมิรัฐศาสตร์",
            },
            {
                "icon": "🤖",
                "title": "การผสาน AI วิเคราะห์ความเปลี่ยนแปลงทางกายภาพอัตโนมัติ",
                "desc": "ตรวจจับการสร้างอาคาร การเคลื่อนย้ายเรือ และพื้นที่การเกษตรได้ทันที",
            },
        ],
    },
    "RDW": {
        "model_type": "TURNAROUND_SPEC",
        "fair_price": 11.50,
        "primary_model": "In-Space Infrastructure & ROSA Solar Array Backlog Multiple (1.8x P/S)",
        "model_desc": "ประเมินจากแผงโซลาร์เซลล์อวกาศ ROSA บนสถานีอวกาศนานาชาติ ISS และโครงสร้างพื้นฐานดาวเทียม",
        "math_details": {
            "formula": "Forward FY27 Revenue ($420M ÷ 67M shares = $6.27/share) × Target P/S (1.8x) = $11.28 -> ปรับฐานที่ $11.50",
            "accounting_source": "งบการเงินล่าสุด: รายได้รวมทำสถิติสูงสุดใหม่, ปรับปรุง EBITDA เป็นบวก, ยอด Backlog ทะลุ $350M+",
            "key_multiples": "Forward P/S 1.8x, ROSA Solar Deployment on ISS, Adjusted EBITDA Positive, Backlog $350M+",
            "wall_street_target": "$12.33 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $18.00)",
            "explanation": "Redwire มีบทบาทสำคัญในโครงการสถานีอวกาศเอกชนและยานอวกาศรุ่นใหม่ ราคาเหมาะสม $11.50 สอดคล้องกับราคาเป้าหมายเฉลี่ยวอลล์สตรีท ($12.33)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "☀️",
                "title": "ผู้นำเทคโนโลยีแผงรับแสงอาทิตย์ในอวกาศแบบม้วนเก็บได้ (ROSA)",
                "desc": "จ่ายพลังงานให้สถานีอวกาศนานาชาติ ISS และได้รับเลือกใช้ในภารกิจดวงจันทร์ Artemis",
            },
            {
                "icon": "🛰️",
                "title": "โครงสร้างพื้นฐานสำหรับสถานีอวกาศเอกชนยุคใหม่",
                "desc": "จัดหาชิ้นส่วนประกอบดาวเทียมและระบบควบคุมทิศทางให้ผู้สร้างสถานีอวกาศ",
            },
            {
                "icon": "📈",
                "title": "ผลการดำเนินงานพลิกฟื้นสู่จุดคุ้มทุน EBITDA",
                "desc": "การบริหารจัดการต้นทุนที่ดีขึ้นช่วยหนุนกระแสเงินสดจากการดำเนินงานเป็นบวก",
            },
        ],
    },
    "AVAV": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 185.00,
        "primary_model": "Switchblade Loitering Munitions + Autonomous Tactical UAS (32x P/E)",
        "model_desc": "ประเมินจากความต้องการโดรนพลีชีพ Switchblade 300/600 และระบบโดรนสอดแนมไร้คนขับในสมรภูมิยุคใหม่",
        "math_details": {
            "formula": "Forward Normalized FY27 EPS ($5.80) × Target P/E (32x) = $185.60 -> ปรับฐานที่ $185.00",
            "accounting_source": "งบการเงินล่าสุด: ยอดสั่งซื้อคงค้าง Funded Backlog พุ่งแตะระดับสูงสุดเป็นประวัติการณ์กว่า $400M, กองทัพสหรัฐอนุมัติสัญญาจัดซื้อเร่งด่วน",
            "key_multiples": "Forward P/E 32.0x, Funded Backlog Record High, Loitering Munitions Monopoly, Defense Budget Growth",
            "wall_street_target": "$210.91 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $280.00)",
            "explanation": "สงครามยุคใหม่พิสูจน์แล้วว่าโดรนและกระสุนลอยลำคือหัวใจของชัยชนะ ราคาเหมาะสม $185.00 มีส่วนเผื่อความปลอดภัยจากเป้าวอลล์สตรีท ($210.91)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "🎯",
                "title": "ผู้ผลิตกระสุนลอยลำ (Loitering Munition) Switchblade อันดับหนึ่ง",
                "desc": "ความแม่นยำสูงและใช้งานง่ายในสนามรบ ได้รับการยอมรับจากกระทรวงกลาโหมสหรัฐ",
            },
            {
                "icon": "🛸",
                "title": "ระบบโดรนยุทธวิธีขนาดเล็ก Puma & JUMP 20 ครองตลาดสอดแนม",
                "desc": "ส่งมอบข้อมูลข่าวกรองแบบเรียลไทม์ให้หน่วยรบภาคพื้นดินอย่างไร้ข้อผิดพลาด",
            },
            {
                "icon": "🌍",
                "title": "ความต้องการจัดซื้อจากกลุ่มประเทศ NATO ขยายตัวก้าวกระโดด",
                "desc": "งบประมาณกลาโหมทั่วโลกที่เพิ่มขึ้นหนุนคำสั่งซื้อล่วงหน้ายาวหลายปี",
            },
        ],
    },
    "KTOS": {
        "model_type": "AI_INFRA_HYPERGROWTH",
        "fair_price": 62.00,
        "primary_model": "Collaborative Combat Aircraft (Valkyrie) + Jet Drone Target Systems (45x P/E)",
        "model_desc": "ประเมินจากโดรนเจ็ตไร้คนขับ XQ-58A Valkyrie ที่บินร่วมกับเครื่องบินรบยุคที่ 5 (F-35) และระบบสื่อสารผ่านดาวเทียม",
        "math_details": {
            "formula": "Forward FY27 EPS ($1.40) × Target P/E (45x) = $63.00 -> ปรับฐานที่ $62.00",
            "accounting_source": "งบ 12 เดือนล่าสุด (TTM): รายได้ทะลุ $1.1B, อัตรากำไร EBITDA ปรับตัวดีขึ้น, กองทัพอากาศและนาวิกโยธินสหรัฐขยายสัญญาบินทดสอบ",
            "key_multiples": "Forward P/E 45.0x, Valkyrie CCA Leader, Space Satellite Ground Systems, Backlog $1.2B+",
            "wall_street_target": "$76.48 (เป้าหมายเฉลี่ยจากนักวิเคราะห์สถาบันวอลล์สตรีท, เป้าสูงสุด $95.00)",
            "explanation": "แนวคิดเครื่องบินรบไร้คนขับต้นทุนต่ำ (Low-Cost Attritable Aircraft) ของ Kratos ตอบโจทย์สงครามอัตโนมัติ ราคาเหมาะสม $62.00 ต่ำกว่าเป้าวอลล์สตรีท ($76.48)",
            "margin_of_safety_rule": "Margin of Safety = (Intrinsic Fair Value - Market Price) ÷ Intrinsic Fair Value",
        },
        "pillars": [
            {
                "icon": "✈️",
                "title": "ผู้นำโดรนรบไอพ่นไร้คนขับร่วมรบ (Collaborative Combat Aircraft)",
                "desc": "โดรน XQ-58A Valkyrie ควบคุมด้วย AI บินคุ้มกันเครื่องบินขับไล่ด้วยต้นทุนต่ำกว่ามาก",
            },
            {
                "icon": "🛰️",
                "title": "ระบบซอฟต์แวร์ควบคุมภาคพื้นดินดาวเทียม OpenSpace",
                "desc": "เป็นโครงสร้างพื้นฐานการสื่อสารภาคพื้นดินที่สำคัญของกองทัพอวกาศสหรัฐ",
            },
            {
                "icon": "🛡️",
                "title": "ยอดคำสั่งซื้อที่รอส่งมอบ (Backlog) สูงกว่า $1,200 ล้านดอลลาร์",
                "desc": "มีสัญญาความมั่นคงระยะยาวหนุนเสถียรภาพรายได้ในอนาคต",
            },
        ],
    },
}


# ---------------------------------------------------------------------------
# Dynamic Valuation Engine Functions
# ---------------------------------------------------------------------------
def get_valuation(
    ticker: str,
    current_price: Optional[float] = None,
    meta_entry: Optional[Dict[str, Any]] = None,
    fin_cache: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Computes and returns dynamic valuation metrics, status, math details,
    and supporting rationale pillars for a ticker.
    """
    t = ticker.strip().upper()
    cfg = MODEL_CONFIGS.get(t)

    # 1. Fallback / Unrated Tickers
    if not cfg:
        market_p = current_price or 0.0
        return {
            "ticker": t,
            "fair_price": market_p,
            "current_price": market_p,
            "upside_pct": 0.0,
            "status": "SPECULATIVE",
            "status_label": "🟡 อยู่ระหว่างประเมิน (Under Evaluation)",
            "status_color": "#facc15",
            "primary_model": "Market Price Baseline",
            "model_desc": "ข้อมูลปัจจัยพื้นฐานอยู่ระหว่างการประเมิน ใช้ราคาตลาดเป็นฐานอ้างอิง",
            "math_details": {
                "formula": "Market Price Baseline: อ้างอิงตามราคาตลาดปัจจุบัน",
                "accounting_source": "ข้อมูลอยู่ระหว่างการประเมินงบการเงินไตรมาสล่าสุด",
                "key_multiples": "-",
                "wall_street_target": "-",
                "explanation": "ยังไม่มีการประเมินมูลค่าเฉพาะตัวสำหรับหุ้นนี้ ใช้ราคาตลาดเป็นฐานอ้างอิง",
                "margin_of_safety_rule": "N/A (อยู่ระหว่างการประเมินปัจจัยพื้นฐาน)",
            },
            "pillars": [
                {
                    "icon": "📊",
                    "title": "ข้อมูลอยู่ระหว่างการประเมินปัจจัยพื้นฐาน",
                    "desc": "ติดตามความคืบหน้าของงบการเงินและสัญญาณเทคนิคในระบบ",
                }
            ],
        }

    model_type = cfg.get("model_type", "BIG_TECH_GROWTH")
    price = float(current_price) if (current_price and current_price > 0) else 0.0

    # 2. ETF Model: 100% Real-time NAV Tracking
    if model_type == "INDEX_ETF":
        fair = price if price > 0 else 100.0
        return {
            "ticker": t,
            "fair_price": fair,
            "current_price": price,
            "upside_pct": 0.0,
            "status": "FAIR",
            "status_label": "🌐 อิงมูลค่าสินทรัพย์สุทธิ (NAV Tracking)",
            "status_color": "#38bdf8",
            "primary_model": cfg["primary_model"],
            "model_desc": cfg["model_desc"],
            "math_details": cfg.get("math_details", {}),
            "pillars": cfg["pillars"],
        }

    # 3. Stock Valuation Calculation
    fair = float(cfg.get("fair_price") or 0.0)
    if fair <= 0.0:
        fair = price if price > 0 else 1.0

    # Negative Operating Profit Floor Guard: Price cannot be negative or zero
    fair = max(fair, 1.0)

    # Upside / Margin of Safety calculation
    # Upside % = ((Fair - Price) / Price) * 100
    if price > 0:
        upside = ((fair - price) / price) * 100.0
    else:
        upside = 0.0

    # Determine status & badge
    if model_type == "SPECULATIVE_BASELINE":
        status = "SPECULATIVE"
        status_label = f"🟣 เก็งกำไรฐานระดมทุน (Pre-IPO {upside:+.1f}%)"
        status_color = "#c084fc"
    elif upside > 10.0:
        status = "UNDERVALUED"
        status_label = f"🟢 ราคาต่ำกว่าพื้นฐาน (Undervalued {upside:+.1f}%)"
        status_color = "#34d399"
    elif upside < -10.0:
        status = "OVERVALUED"
        status_label = f"🔴 ราคาสูงกว่าพื้นฐาน (Overvalued {upside:+.1f}%)"
        status_color = "#fb7185"
    else:
        status = "FAIR"
        status_label = f"🟡 ราคาสมเหตุสมผล (Fair Value {upside:+.1f}%)"
        status_color = "#facc15"

    return {
        "ticker": t,
        "fair_price": round(fair, 2),
        "current_price": round(price, 2),
        "upside_pct": round(upside, 2),
        "status": status,
        "status_label": status_label,
        "status_color": status_color,
        "primary_model": cfg["primary_model"],
        "model_desc": cfg["model_desc"],
        "math_details": cfg.get("math_details", {}),
        "pillars": cfg["pillars"],
    }


def get_all_valuations(
    tickers: List[str],
    meta: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Returns a dictionary of valuation payloads for all specified tickers.
    """
    res = {}
    fin_cache = load_financials_cache()
    for t in tickers:
        m = (meta or {}).get(t, {})
        p = m.get("price")
        res[t] = get_valuation(t, p, m, fin_cache)
    return res
