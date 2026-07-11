#!/usr/bin/env python3
"""
add_handwritten_chinese_114.py — 補 114 國文非選擇題（手寫題）。

第 34、35 題為純文字，題幹取自官方 PDF 中繼文字；第 36 題含表格，
依規則裁官方 PDF 局部圖。手寫題只列出題目，不作答、不判分。
可重複執行：先移除舊 handwritten 再重插。
"""
import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "src/question-bank/114-chinese.js"
RAW = ROOT / "data/raw-extract/114學年度/國綜/114學測-國綜-試題內容-01-114學測國綜試題.json"
PDF = ROOT / "資料/大考中心官方PDF/114學年度/國綜/114學測-國綜-試題內容-01-114學測國綜試題.pdf"
IMAGE_DIR = ROOT / "public/images/114學年度/國綜"
Q36_IMAGE = "q36-handwritten.png"
Q36_IMAGE_PATH = f"public/images/114學年度/國綜/{Q36_IMAGE}"
HW_NOS = [34, 35, 36]


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


def extract_stems():
    data = json.loads(RAW.read_text(encoding="utf-8"))
    text = "\n".join(page["text"] for page in data["pages"])
    stems = {}
    for no in HW_NOS:
        match = re.search(rf"(?m)^{no}\.\s*(.*?)(?=^\d{{1,2}}\.\s|-\s*11\s*-|\Z)", text, re.S)
        if not match:
            stems[no] = None
            continue
        stems[no] = re.sub(r"\n\s*", "\n", match.group(1).strip())
    return stems


def crop_q36():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    pix = doc[11].get_pixmap(
        matrix=fitz.Matrix(2.8, 2.8),
        clip=fitz.Rect(58, 500, 540, 720),
        alpha=False,
    )
    pix.save(IMAGE_DIR / Q36_IMAGE)
    doc.close()


def main():
    crop_q36()
    stems = extract_stems()
    missing = [no for no in HW_NOS if not stems.get(no)]
    if missing:
        raise RuntimeError(f"找不到手寫題題幹：{missing}")

    header, bank = load_bank()
    bank["questions"] = [q for q in bank["questions"] if q.get("type") != "handwritten"]
    for block in bank["blocks"]:
        block["questions"] = [q for q in block["questions"] if q.get("type") != "handwritten"]

    entries = [
        {"id": "chinese-114-guozong-hw-q34", "no": 34, "type": "handwritten", "stem": stems[34]},
        {"id": "chinese-114-guozong-hw-q35", "no": 35, "type": "handwritten", "stem": stems[35]},
        {"id": "chinese-114-guozong-hw-q36", "no": 36, "type": "handwritten", "image": Q36_IMAGE_PATH},
    ]

    target = None
    for block in bank["blocks"]:
        if block.get("title") == "第 32-36 題題組":
            target = block
            break
    if target is None:
        raise RuntimeError("找不到第 32-36 題題組 block")

    target["questions"].extend(entries)
    target["questions"].sort(key=lambda q: q["no"])
    bank["questions"].extend(entries)
    bank["questions"].sort(key=lambda q: q["no"])

    bank["note"] = (
        "收錄 114 學測國文選擇題共 33 題，另列手寫題 3 題"
        "（34、35、36，僅列出不作答）。題目與答案均取自官方 PDF；圖表依官方 PDF 必要區域裁切。"
    )
    bank["review_flags"] = bank.get("review_flags") or []

    write_bank(header, bank)
    print("已補 114 國文手寫題：", HW_NOS)
    print("裁圖張數：1")
    print("總題目數（含手寫）：", len(bank["questions"]))


if __name__ == "__main__":
    main()
