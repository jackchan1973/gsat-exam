#!/usr/bin/env python3
"""
Build 113 natural answer-card question bank.

自然科公式、圖表、化學式與跨頁題組多；正式題面以官方 PDF 局部圖呈現，
互動區只提供答題卡。答案一律由官方答案 JSON 讀取，答案為「／」者列為
handwritten，不作答不判分。
"""
import json
from pathlib import Path

import fitz
from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data/raw-extract/113學年度/自然"
PDF = ROOT / "資料/大考中心官方PDF/113學年度/自然/113學測-自然-試題內容-06-113學測自然試題定稿.pdf"
ANSWER_JSON = RAW_DIR / "113學測-自然-選擇題答案-06-113學測自然答案.json"
OUT_JS = ROOT / "src/question-bank/113-natural.js"
IMAGE_DIR = ROOT / "public/images/113學年度/自然"
IMAGE_PREFIX = "public/images/113學年度/自然"

CHOICES = ["A", "B", "C", "D", "E"]
FULL = (48, 74, 548, 792)


BLOCK_SPECS = [
    {"id": "nature-113-p02-q01-03", "title": "第 1-3 題", "questionNos": [1, 2, 3],
     "crops": [(2, FULL)]},
    {"id": "nature-113-p03-q04-07", "title": "第 4-7 題", "questionNos": [4, 5, 6, 7],
     "crops": [(3, FULL)]},
    {"id": "nature-113-p04-q08-11", "title": "第 8-11 題", "questionNos": [8, 9, 10, 11],
     "crops": [(4, FULL)]},
    {"id": "nature-113-p05-q12-14", "title": "第 12-14 題", "questionNos": [12, 13, 14],
     "crops": [(5, FULL)]},
    {"id": "nature-113-p06-q15-17", "title": "第 15-17 題", "questionNos": [15, 16, 17],
     "crops": [(6, FULL)]},
    {"id": "nature-113-p07-q18-21", "title": "第 18-21 題", "questionNos": [18, 19, 20, 21],
     "crops": [(7, FULL)]},
    {"id": "nature-113-p08-q22-23", "title": "第 22-23 題", "questionNos": [22, 23],
     "crops": [(8, FULL)]},
    {"id": "nature-113-p09-q24-27", "title": "第 24-27 題", "questionNos": [24, 25, 26, 27],
     "crops": [(9, FULL)]},
    {"id": "nature-113-p10-q28-32", "title": "第 28-32 題", "questionNos": [28, 29, 30, 31, 32],
     "crops": [(10, FULL)]},
    {"id": "nature-113-p11-q33-36", "title": "第 33-36 題", "questionNos": [33, 34, 35, 36],
     "crops": [(11, FULL)]},
    {"id": "nature-113-p12-p13-q37-39", "title": "第 37-39 題題組", "questionNos": [37, 38, 39],
     "crops": [(12, FULL), (13, FULL)]},
    {"id": "nature-113-p14-p15-q40-43", "title": "第 40-43 題題組", "questionNos": [40, 41, 42, 43],
     "crops": [(14, FULL), (15, FULL)]},
    {"id": "nature-113-p16-q44-46", "title": "第 44-46 題題組", "questionNos": [44, 45, 46],
     "crops": [(16, FULL)]},
    {"id": "nature-113-p17-q47-49", "title": "第 47-49 題題組", "questionNos": [47, 48, 49],
     "crops": [(17, FULL)]},
    {"id": "nature-113-p18-p19-q50-53", "title": "第 50-53 題題組", "questionNos": [50, 51, 52, 53],
     "crops": [(18, FULL), (19, (48, 74, 548, 260))]},
    {"id": "nature-113-p19-q54-56", "title": "第 54-56 題題組", "questionNos": [54, 55, 56],
     "crops": [(19, (48, 260, 548, 792))]},
]


def load_answers():
    data = json.loads(ANSWER_JSON.read_text(encoding="utf-8"))
    answers = {}
    for table in data["tables"]:
        for row in table["cells"][1:]:
            for index in range(0, len(row), 2):
                if index + 1 < len(row) and row[index] and row[index + 1]:
                    answers[int(row[index])] = row[index + 1]
    return dict(sorted(answers.items()))


def answer_value(raw):
    return list(raw) if len(raw) > 1 else raw


def question_type(raw):
    if raw == "／":
        return "handwritten"
    return "multiple" if len(raw) > 1 else "single"


def build_question(no, raw):
    question = {
        "id": f"natural-113-{'hw-' if raw == '／' else ''}q{no}",
        "no": no,
        "type": question_type(raw),
        "choices": CHOICES,
    }
    if raw == "／":
        question.pop("choices")
        return question
    question["answer"] = answer_value(raw)
    return question


def stitch_images(parts, out):
    width = max(part.width for part in parts)
    height = sum(part.height for part in parts) + 24 * (len(parts) - 1)
    canvas = Image.new("RGB", (width, height), "white")
    y = 0
    for index, part in enumerate(parts):
        canvas.paste(part, ((width - part.width) // 2, y))
        y += part.height
        if index < len(parts) - 1:
            y += 24
    canvas.save(out)


def crop_block_images():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    paths = {}
    for spec in BLOCK_SPECS:
        parts = []
        for page_no, bbox in spec["crops"]:
            page = doc[page_no - 1]
            pix = page.get_pixmap(matrix=fitz.Matrix(2.4, 2.4), clip=fitz.Rect(*bbox), alpha=False)
            parts.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
        out = IMAGE_DIR / f"{spec['id']}.png"
        stitch_images(parts, out)
        paths[spec["id"]] = f"{IMAGE_PREFIX}/{out.name}"
    doc.close()
    return paths


def build_answer_check(questions, answers):
    rows = []
    for question in questions:
        raw = answers[question["no"]]
        if raw == "／":
            continue
        bank = "".join(question["answer"]) if isinstance(question["answer"], list) else question["answer"]
        rows.append({
            "題號": question["no"],
            "官方答案": raw,
            "題庫答案": bank,
            "結果": "相符" if raw == bank else "不相符",
        })
    return rows


def build_bank():
    answers = load_answers()
    expected = list(range(1, 57))
    if sorted(answers) != expected:
        raise SystemExit(f"答案題號不連續：{sorted(answers)}")

    image_paths = crop_block_images()
    questions_by_no = {no: build_question(no, raw) for no, raw in answers.items()}

    blocks = []
    covered = []
    for spec in BLOCK_SPECS:
        nos = spec["questionNos"]
        covered.extend(nos)
        blocks.append({
            "title": spec["title"],
            "shared": {"kind": "image", "src": image_paths[spec["id"]]},
            "questions": [questions_by_no[no] for no in nos],
        })

    if sorted(covered) != expected:
        raise SystemExit(f"區塊題號覆蓋不一致：{sorted(covered)}")

    questions = [questions_by_no[no] for no in expected]
    handwritten = [no for no, raw in answers.items() if raw == "／"]
    gradable = [no for no, raw in answers.items() if raw != "／"]

    return {
        "id": "natural-113-answer-card",
        "subject": "自然",
        "year": "113",
        "category": "答題卡練習",
        "title": "113 年自然答題卡練習",
        "status": "官方 PDF 提取題庫",
        "source": {
            "試題": "資料/大考中心官方PDF/113學年度/自然/113學測-自然-試題內容-06-113學測自然試題定稿.pdf",
            "答案": "資料/大考中心官方PDF/113學年度/自然/113學測-自然-選擇題答案-06-113學測自然答案.pdf",
        },
        "note": (
            f"收錄 113 學測自然選擇題共 {len(gradable)} 題；另列手寫題 {len(handwritten)} 題"
            f"（{'、'.join(map(str, handwritten))}，僅列出不作答）。自然科公式、圖表與跨頁題組較多，"
            "本版以官方 PDF 局部裁圖呈現題面，答案卡獨立互動。"
        ),
        "review_flags": [],
        "answer_check": build_answer_check(questions, answers),
        "questions": questions,
        "blocks": blocks,
    }


def main():
    bank = build_bank()
    OUT_JS.write_text(
        "// 由 tools/build_natural_113.py 自動產生，請勿手改。題目與答案取自官方 PDF，未經改寫。\n"
        "QUESTION_BANKS.push(\n"
        + json.dumps(bank, ensure_ascii=False, indent=2)
        + "\n);\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "questions": len(bank["questions"]),
        "gradable": len([q for q in bank["questions"] if q["type"] != "handwritten"]),
        "handwritten": [q["no"] for q in bank["questions"] if q["type"] == "handwritten"],
        "blocks": len(bank["blocks"]),
        "images": len(BLOCK_SPECS),
        "review_flags": bank["review_flags"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
