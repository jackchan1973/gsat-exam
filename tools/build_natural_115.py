#!/usr/bin/env python3
"""
build_natural_115.py — 115 自然題庫（官方圖像題組＋答題卡）。

自然科包含大量公式、圖表、化學式與跨頁題組；為避免文字化造成誤植，
本版以官方 PDF 區域裁切呈現題面，互動區只負責答題卡與官方答案核對。
答案為「／」的非選擇題不納入互動作答。
"""
import json
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "資料/大考中心官方PDF/115學年度/自然/115學測-自然-試題內容-06-115學測自然試卷.pdf"
OUT_JS = ROOT / "src/question-bank/115-natural.js"
IMAGE_DIR = ROOT / "public/images/115學年度/自然"
IMAGE_PREFIX = "public/images/115學年度/自然"
CHOICES = ["A", "B", "C", "D", "E"]

ANSWERS = {
    1: "C", 2: "C", 3: "D", 4: "A", 5: "D", 6: "A",
    7: "AE", 8: "BD", 9: "AC", 10: "C", 11: "DE", 12: "BE",
    13: "E", 14: "C", 15: "B", 16: "B", 17: "E", 18: "E",
    19: "D", 20: "A", 21: "E", 22: "C", 23: "AE", 24: "B",
    25: "CD", 26: "ABC", 27: "ABE", 28: "A", 29: "E", 30: "E",
    31: "AC", 32: "CD", 33: "B", 34: "A", 35: "DE", 36: "A",
    37: "BDE", 39: "AD", 40: "E", 43: "E", 44: "AB", 45: "ABC",
    47: "B", 48: "AD", 51: "B", 52: "DE", 55: "B", 56: "B",
}

NON_CHOICE = [38, 41, 42, 46, 49, 50, 53, 54]

# PDF coordinates: page_no, (x0, y0, x1, y1). Keep enough original context for
# formulas, charts, tables and shared materials to stay faithful.
CROPS = [
    {"id": "nature-115-p02-q01-04", "label": "第 1-4 題", "questionNos": [1, 2, 3, 4],
     "images": [(2, (48, 74, 548, 792))]},
    {"id": "nature-115-p03-q05-06", "label": "第 5-6 題", "questionNos": [5, 6],
     "images": [(3, (48, 74, 548, 792))]},
    {"id": "nature-115-p04-q07-09", "label": "第 7-9 題", "questionNos": [7, 8, 9],
     "images": [(4, (48, 74, 548, 792))]},
    {"id": "nature-115-p05-q10-12", "label": "第 10-12 題", "questionNos": [10, 11, 12],
     "images": [(5, (48, 74, 548, 792))]},
    {"id": "nature-115-p06-q13-16", "label": "第 13-16 題", "questionNos": [13, 14, 15, 16],
     "images": [(6, (48, 74, 548, 792))]},
    {"id": "nature-115-p07-q17-20", "label": "第 17-20 題", "questionNos": [17, 18, 19, 20],
     "images": [(7, (48, 74, 548, 792))]},
    {"id": "nature-115-p08-q21-23", "label": "第 21-23 題", "questionNos": [21, 22, 23],
     "images": [(8, (48, 74, 548, 792))]},
    {"id": "nature-115-p09-q24", "label": "第 24 題", "questionNos": [24],
     "images": [(9, (48, 74, 548, 248))]},
    {"id": "nature-115-p09-p10-q25-27", "label": "第 25-27 題", "questionNos": [25, 26, 27],
     "images": [(9, (48, 224, 548, 792)), (10, (48, 74, 548, 382))]},
    {"id": "nature-115-p10-q28-30", "label": "第 28-30 題", "questionNos": [28, 29, 30],
     "images": [(10, (48, 360, 548, 792))]},
    {"id": "nature-115-p11-q31-34", "label": "第 31-34 題", "questionNos": [31, 32, 33, 34],
     "images": [(11, (48, 74, 548, 792))]},
    {"id": "nature-115-p12-q35-37", "label": "第 35-37 題", "questionNos": [35, 36, 37],
     "images": [(12, (48, 74, 548, 792))]},
    {"id": "nature-115-p13-q39", "label": "第 39 題（含題組材料）", "questionNos": [39],
     "images": [(13, (48, 74, 548, 792))]},
    {"id": "nature-115-p14-p15-q40-43", "label": "第 40-43 題（只作答選擇題）", "questionNos": [40, 43],
     "images": [(14, (48, 74, 548, 792)), (15, (48, 74, 548, 456))]},
    {"id": "nature-115-p16-q44-45", "label": "第 44-45 題", "questionNos": [44, 45],
     "images": [(16, (48, 74, 548, 792))]},
    {"id": "nature-115-p17-q47-48", "label": "第 47-48 題", "questionNos": [47, 48],
     "images": [(17, (48, 74, 548, 792))]},
    {"id": "nature-115-p18-p19-q51-52", "label": "第 51-52 題", "questionNos": [51, 52],
     "images": [(18, (48, 74, 548, 792)), (19, (48, 74, 548, 572))]},
    {"id": "nature-115-p20-q55-56", "label": "第 55-56 題", "questionNos": [55, 56],
     "images": [(20, (48, 74, 548, 792))]},
]


def answer_value(raw):
    return list(raw) if len(raw) > 1 else raw


def question_type(raw):
    return "multiple" if len(raw) > 1 else "single"


def qid(no):
    return f"natural-115-q{no}"


def build_questions():
    questions = []
    for no in sorted(ANSWERS):
        raw = ANSWERS[no]
        questions.append({
            "id": qid(no),
            "no": no,
            "type": question_type(raw),
            "choices": CHOICES,
            "answer": answer_value(raw),
        })
    return questions


def crop_images():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    display_groups = []
    for group in CROPS:
        image_paths = []
        for index, (page_no, bbox) in enumerate(group["images"], start=1):
            page = doc[page_no - 1]
            out = IMAGE_DIR / f"{group['id']}-{index}.png"
            pix = page.get_pixmap(matrix=fitz.Matrix(2.8, 2.8), clip=fitz.Rect(*bbox), alpha=False)
            pix.save(out)
            image_paths.append(f"{IMAGE_PREFIX}/{out.name}")
        display_groups.append({
            "id": group["id"],
            "label": group["label"],
            "questionNos": group["questionNos"],
            "images": image_paths,
        })
    doc.close()
    return display_groups


def build_answer_check(questions):
    rows = []
    for question in questions:
        official = ANSWERS[question["no"]]
        bank = "".join(question["answer"]) if isinstance(question["answer"], list) else question["answer"]
        rows.append({
            "題號": question["no"],
            "官方答案": official,
            "題庫答案": bank,
            "結果": "相符" if official == bank else "不相符",
        })
    return rows


def main():
    questions = build_questions()
    display_groups = crop_images()
    covered = sorted(no for group in display_groups for no in group["questionNos"])
    expected = sorted(ANSWERS)
    if covered != expected:
        raise SystemExit(f"題號覆蓋不一致：covered={covered}, expected={expected}")

    bank = {
        "id": "natural-115-answer-card",
        "subject": "自然",
        "year": "115",
        "category": "答題卡練習",
        "title": "115 年自然答題卡練習",
        "status": "官方 PDF 提取題庫",
        "source": {
            "試題": "資料/大考中心官方PDF/115學年度/自然/115學測-自然-試題內容-06-115學測自然試卷.pdf",
            "答案": "資料/大考中心官方PDF/115學年度/自然/115學測-自然-選擇題答案-06-115學測自然答案.pdf",
        },
        "note": (
            "收錄 115 學測自然選擇題共 48 題；答案為「／」的非選擇題 "
            f"{'、'.join(map(str, NON_CHOICE))} 不納入。"
            "自然科公式、圖表與跨頁題組較多，本版以官方 PDF 裁切區域呈現題面，答案卡獨立互動。"
        ),
        "review_flags": [],
        "answer_check": build_answer_check(questions),
        "presentation": "image-answer-card",
        "questions": questions,
        "displayGroups": display_groups,
    }
    OUT_JS.parent.mkdir(parents=True, exist_ok=True)
    header = "// 由 tools/build_natural_115.py 自動產生，請勿手改。題目與答案取自官方 PDF，未經改寫。\n"
    OUT_JS.write_text(
        header + "QUESTION_BANKS.push(\n" + json.dumps(bank, ensure_ascii=False, indent=2) + "\n);\n",
        encoding="utf-8",
    )
    print(f"已輸出：{OUT_JS.relative_to(ROOT)}")
    print(f"題數：{len(questions)}；裁切題組：{len(display_groups)}；圖片：{sum(len(g['images']) for g in display_groups)}")
    print("排除非選擇題：", "、".join(map(str, NON_CHOICE)))


if __name__ == "__main__":
    main()
