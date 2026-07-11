#!/usr/bin/env python3
"""
add_handwritten_natural_115.py — 補 115 自然非選擇題（手寫題）。

依規則：手寫題放進題庫、列出題目，但不作答、不判分。
自然科手寫題多含圖表/公式，故由官方 PDF 裁出必要題面與共用材料區。
可重複執行：先移除舊 handwritten 與手寫題 displayGroups，再重建。
"""
import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "src/question-bank/115-natural.js"
PDF = ROOT / "資料/大考中心官方PDF/115學年度/自然/115學測-自然-試題內容-06-115學測自然試卷.pdf"
IMAGE_DIR = ROOT / "public/images/115學年度/自然"
PREFIX = "public/images/115學年度/自然"

HW_NOS = [38, 41, 42, 46, 49, 50, 53, 54]

# 每列：輸出檔名, PDF頁碼, (x0, y0, x1, y1)
CROPS = [
    ("nature-115-hw-q38-shared.png", 12, (48, 518, 548, 665)),
    ("nature-115-hw-q38.png", 13, (58, 84, 540, 286)),
    ("nature-115-hw-q41-q42-shared.png", 14, (58, 84, 540, 790)),
    ("nature-115-hw-q41.png", 15, (58, 196, 540, 360)),
    ("nature-115-hw-q42.png", 15, (58, 356, 540, 398)),
    ("nature-115-hw-q46-shared.png", 16, (58, 84, 540, 535)),
    ("nature-115-hw-q46.png", 17, (58, 82, 540, 166)),
    ("nature-115-hw-q49-shared.png", 17, (58, 170, 540, 535)),
    ("nature-115-hw-q49.png", 17, (58, 624, 540, 785)),
    ("nature-115-hw-q50.png", 18, (58, 86, 540, 708)),
    ("nature-115-hw-q53.png", 19, (58, 264, 540, 670)),
    ("nature-115-hw-q54.png", 20, (58, 86, 540, 421)),
]

GROUPS = [
    (38, "第 38 題（手寫題）", ["nature-115-hw-q38-shared.png", "nature-115-hw-q38.png"]),
    (41, "第 41 題（手寫題）", ["nature-115-hw-q41-q42-shared.png", "nature-115-hw-q41.png"]),
    (42, "第 42 題（手寫題）", ["nature-115-hw-q41-q42-shared.png", "nature-115-hw-q42.png"]),
    (46, "第 46 題（手寫題）", ["nature-115-hw-q46-shared.png", "nature-115-hw-q46.png"]),
    (49, "第 49 題（手寫題）", ["nature-115-hw-q49-shared.png", "nature-115-hw-q49.png"]),
    (50, "第 50 題（手寫題）", ["nature-115-hw-q50.png"]),
    (53, "第 53 題（手寫題）", ["nature-115-hw-q53.png"]),
    (54, "第 54 題（手寫題）", ["nature-115-hw-q54.png"]),
]


def load_bank():
    text = BANK.read_text(encoding="utf-8")
    match = re.search(r"QUESTION_BANKS\.push\(\s*(\{.*\})\s*\);", text, re.S)
    if not match:
        raise RuntimeError("找不到 QUESTION_BANKS.push JSON")
    return text[:match.start()], json.loads(match.group(1))


def write_bank(header, bank):
    BANK.write_text(
        header + "QUESTION_BANKS.push(\n" + json.dumps(bank, ensure_ascii=False, indent=2) + "\n);\n",
        encoding="utf-8",
    )


def crop_images():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    for filename, page_no, bbox in CROPS:
        pix = doc[page_no - 1].get_pixmap(matrix=fitz.Matrix(2.8, 2.8), clip=fitz.Rect(*bbox), alpha=False)
        pix.save(IMAGE_DIR / filename)
    doc.close()


def image_path(filename):
    return f"{PREFIX}/{filename}"


def main():
    crop_images()
    header, bank = load_bank()

    bank["questions"] = [q for q in bank["questions"] if q.get("type") != "handwritten"]
    bank["displayGroups"] = [
        g for g in bank["displayGroups"]
        if not str(g.get("id", "")).startswith("nature-115-hw-q")
    ]

    for no, label, filenames in GROUPS:
        bank["questions"].append({
            "id": f"natural-115-hw-q{no}",
            "no": no,
            "type": "handwritten",
            "image": image_path(f"nature-115-hw-q{no}.png"),
        })
        bank["displayGroups"].append({
            "id": f"nature-115-hw-q{no}",
            "label": label,
            "questionNos": [no],
            "images": [image_path(name) for name in filenames],
        })

    bank["questions"].sort(key=lambda q: q["no"])
    bank["displayGroups"].sort(key=lambda g: min(g["questionNos"]))

    bank["note"] = (
        "收錄 115 學測自然選擇題共 48 題，另列手寫題 8 題"
        "（38、41、42、46、49、50、53、54，僅列出不作答）。"
        "自然科公式、圖表與跨頁題組較多，本版以官方 PDF 裁切區域呈現題面，答案卡獨立互動。"
    )
    bank["review_flags"] = bank.get("review_flags") or []

    write_bank(header, bank)
    print("已補 115 自然手寫題：", HW_NOS)
    print("裁圖張數：", len(CROPS))
    print("總題目數（含手寫）：", len(bank["questions"]))


if __name__ == "__main__":
    main()
