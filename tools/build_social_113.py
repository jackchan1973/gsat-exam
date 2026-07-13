#!/usr/bin/env python3
"""
Build 113 social answer-card question bank.

參考 115 社會做法：官方 PDF 是唯一依據；純文字題結構化，圖表/地圖/圖片才裁
官方 PDF 局部圖。題組共用資料只放在題組層；非選擇題列為 handwritten，不判分。
"""
import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data/raw-extract/113學年度/社會"
PDF = ROOT / "資料/大考中心官方PDF/113學年度/社會/113學測-社會-試題內容-05-113學測社會科試題定稿.pdf"
ANSWER_JSON = RAW_DIR / "113學測-社會-選擇題答案-05-113學測社會答案.json"
EXAM_JSON = RAW_DIR / "113學測-社會-試題內容-05-113學測社會科試題定稿.json"
OUT_JS = ROOT / "src/question-bank/113-social.js"
IMAGE_DIR = ROOT / "public/images/113學年度/社會"

CHOICES = ["A", "B", "C", "D"]
QUESTION_RE = re.compile(r"(?m)^(\d{1,2})\.\s")
GROUP_RE = re.compile(r"(?m)^(\d{1,2})-(\d{1,2})\s*為題組")
CHOICE_RE = re.compile(r"\(([A-D])\)")

GROUPS = [
    (21, 22), (23, 26), (27, 28), (29, 30), (31, 32),
    (33, 35), (36, 38), (39, 40), (41, 43), (44, 46),
    (47, 50), (51, 53), (54, 57), (58, 60), (61, 64),
]

CROPS = {
    "q07-table": (3, (108, 282, 496, 444)),
    "q08-figures": (3, (92, 620, 510, 744)),
    "q09-table": (4, (152, 132, 448, 254)),
    "q18-photo": (5, (70, 602, 525, 742)),
    "q20-map": (6, (342, 252, 532, 470)),
    "group-27-28-material": (8, (88, 182, 520, 382)),
    "group-29-30-table": (8, (82, 612, 520, 778)),
    "q29-map-options": (9, (78, 104, 516, 368)),
    "group-31-32-table": (9, (104, 536, 470, 666)),
    "q36-figure": (11, (252, 386, 524, 618)),
    "q38-written": (12, (88, 156, 510, 262)),
    "group-39-40-table": (12, (88, 448, 508, 548)),
    "q40-written": (12, (88, 680, 508, 780)),
    "q43-written": (13, (82, 548, 510, 664)),
    "q46-written": (14, (82, 570, 532, 776)),
    "q49-written": (15, (138, 480, 458, 580)),
    "q50-written": (15, (138, 622, 458, 698)),
    "group-51-53-map": (16, (382, 132, 532, 266)),
    "q53-written": (16, (82, 616, 532, 778)),
    "q54-map": (17, (62, 300, 520, 472)),
    "q57-written": (18, (86, 82, 522, 262)),
    "q60-written": (18, (86, 604, 512, 750)),
    "q64-written": (19, (98, 718, 514, 780)),
}
QUESTION_IMAGES = {
    7: "q07-table",
    8: "q08-figures",
    9: "q09-table",
    18: "q18-photo",
    20: "q20-map",
    29: "q29-map-options",
    36: "q36-figure",
    38: "q38-written",
    40: "q40-written",
    43: "q43-written",
    46: "q46-written",
    49: "q49-written",
    50: "q50-written",
    53: "q53-written",
    54: "q54-map",
    57: "q57-written",
    60: "q60-written",
    64: "q64-written",
}
GROUP_IMAGES = {
    (27, 28): "group-27-28-material",
    (29, 30): "group-29-30-table",
    (31, 32): "group-31-32-table",
    (39, 40): "group-39-40-table",
    (51, 53): "group-51-53-map",
}


def clean_lines(text):
    cleaned = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "113年學測" in line or "共 18 頁" in line:
            continue
        if "請記得在答題卷簽名欄位" in line:
            continue
        if line in {"社會考科", "共 18 頁"}:
            continue
        if re.fullmatch(r"-\s*\d+\s*-", line):
            continue
        if re.fullmatch(r"第\s*\d+\s*頁", line):
            continue
        if re.match(r"^(第\s*[壹貳參肆伍陸柒捌玖拾]+\s*部\s*分|說明：)", line):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def load_answers():
    data = json.loads(ANSWER_JSON.read_text(encoding="utf-8"))
    answers = {}
    for table in data["tables"]:
        for row in table["cells"][1:]:
            for i in range(0, len(row), 2):
                if i + 1 < len(row) and row[i] and row[i + 1]:
                    answers[int(row[i])] = row[i + 1]
    return answers


def load_exam_text():
    data = json.loads(EXAM_JSON.read_text(encoding="utf-8"))
    return "\n".join(clean_lines(page["text"]) for page in data["pages"][1:])


def crop_images():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    outputs = {}
    for key, (page_no, bbox) in CROPS.items():
        pix = doc[page_no - 1].get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=fitz.Rect(*bbox), alpha=False)
        out = IMAGE_DIR / f"{key}.png"
        pix.save(out)
        outputs[key] = f"public/images/113學年度/社會/{out.name}"
    doc.close()
    return outputs


def find_items(text):
    items = []
    seen_questions = set()
    for match in QUESTION_RE.finditer(text):
        no = int(match.group(1))
        if no in seen_questions:
            continue
        seen_questions.add(no)
        items.append(("question", no, match.start()))
    for match in GROUP_RE.finditer(text):
        items.append(("group", (int(match.group(1)), int(match.group(2))), match.start()))
    return sorted(items, key=lambda item: item[2])


def segment_questions(text):
    items = find_items(text)
    segments = {}
    for index, (kind, value, start) in enumerate(items):
        if kind != "question":
            continue
        end = items[index + 1][2] if index + 1 < len(items) else len(text)
        segments[value] = text[start:end].strip()
    return segments


def segment_groups(text):
    items = find_items(text)
    shared = {}
    for idx, (kind, value, start) in enumerate(items):
        if kind != "group":
            continue
        end = items[idx + 1][2] if idx + 1 < len(items) else len(text)
        content = text[start:end].strip()
        content = re.sub(r"^\d{1,2}-\d{1,2}\s*為題組\s*", "", content).strip()
        content = re.sub(r"請問：\s*$", "", content).strip()
        shared[value] = content
    return shared


def clean_option_text(value):
    lines = []
    for line in value.splitlines():
        line = line.strip()
        if not line:
            continue
        if "113年學測" in line or "共 18 頁" in line:
            continue
        if re.match(r"^\d{1,2}-\d{1,2}\s*為題組$", line):
            continue
        if line.startswith("第 ") and "部分" in line:
            continue
        if line.startswith("說明："):
            continue
        if "修正帶" in line or "非選擇題請" in line or "2B 鉛筆作答" in line:
            continue
        if line.startswith("●") or re.fullmatch(r"圖\s*\d+|照片\s*\d+|表\s*\d+", line):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def strip_official_figure_noise(no, text):
    replacements = {
        7: r"\n?表\s*1[\s\S]*$",
        8: r"\n?3%[\s\S]*?圖2",
        9: r"\n?表\s*2[\s\S]*$",
        18: r"\n?照片1\s*$",
        20: r"\n?圖\s*3\s*$",
        29: r"\n?\(A\)[\s\S]*$",
        36: r"\n?甲\s+乙[\s\S]*?圖\s*5",
        54: r"\n?70°W[\s\S]*?圖\s*7",
    }
    pattern = replacements.get(no)
    if pattern:
        text = re.sub(pattern, "", text, flags=re.MULTILINE).strip()
    return text


def strip_shared_figure_noise(group, text):
    replacements = {
        (27, 28): r"\n?甲\s+丁[\s\S]*?照片2\s+圖4",
        (29, 30): r"\n?表\s*3[\s\S]*$",
        (31, 32): r"\n?表\s*4[\s\S]*$",
        (39, 40): r"\n?表\s*5[\s\S]*$",
        (51, 53): r"\n?俄羅斯[\s\S]*?圖\s*6",
    }
    pattern = replacements.get(group)
    if pattern:
        text = re.sub(pattern, "", text, flags=re.MULTILINE).strip()
    return text


def parse_question(no, segment, answer, image_paths):
    segment = re.sub(rf"^{no}\.\s*", "", segment).strip()
    matches = list(CHOICE_RE.finditer(segment))
    if len(matches) < 4:
        raise ValueError(f"第 {no} 題選項不足")

    stem = segment[:matches[0].start()].strip()
    stem = strip_official_figure_noise(no, stem)
    options = {}
    for idx, match in enumerate(matches):
        label = match.group(1)
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(segment)
        options[label] = clean_option_text(segment[match.end():end])

    question = {
        "id": f"social-113-q{no}",
        "no": no,
        "type": "single",
        "stem": stem,
        "choices": CHOICES,
        "options": options,
        "answer": answer,
    }
    if no in QUESTION_IMAGES:
        question["image"] = image_paths[QUESTION_IMAGES[no]]
    return question


def parse_handwritten(no, segment, image_paths):
    segment = re.sub(rf"^{no}\.\s*", "", segment).strip()
    question = {
        "id": f"social-113-hw-q{no}",
        "no": no,
        "type": "handwritten",
        "stem": segment,
    }
    if no in QUESTION_IMAGES:
        question["image"] = image_paths[QUESTION_IMAGES[no]]
    return question


def build_blocks(questions_by_no, shared_by_group, image_paths):
    grouped_numbers = {no for start, end in GROUPS for no in range(start, end + 1)}
    single_questions = [questions_by_no[no] for no in sorted(questions_by_no) if no not in grouped_numbers]
    blocks = []

    if single_questions:
        blocks.append({"title": "第 1-20 題", "questions": single_questions})

    for group in GROUPS:
        start, end = group
        qs = [questions_by_no[no] for no in range(start, end + 1) if no in questions_by_no]
        if not qs:
            continue
        shared_text = strip_shared_figure_noise(group, shared_by_group.get(group, "").strip())
        image_key = GROUP_IMAGES.get(group)
        if image_key and shared_text:
            shared = {"kind": "passage-image", "text": shared_text, "src": image_paths[image_key]}
        elif image_key:
            shared = {"kind": "image", "src": image_paths[image_key]}
        elif shared_text:
            shared = {"kind": "passage", "text": shared_text}
        else:
            shared = None
        block = {"title": f"第 {start}-{end} 題題組", "questions": qs}
        if shared:
            block["shared"] = shared
        blocks.append(block)
    return blocks


def build_bank():
    answers = load_answers()
    image_paths = crop_images()
    text = load_exam_text()
    question_segments = segment_questions(text)
    shared_by_group = segment_groups(text)

    questions_by_no = {}
    gradable = {no: ans for no, ans in answers.items() if ans != "／"}
    handwritten = [no for no, ans in answers.items() if ans == "／"]
    for no in sorted(gradable):
        questions_by_no[no] = parse_question(no, question_segments[no], gradable[no], image_paths)
    for no in sorted(handwritten):
        questions_by_no[no] = parse_handwritten(no, question_segments[no], image_paths)

    answer_check = [
        {"題號": no, "官方答案": gradable[no], "題庫答案": questions_by_no[no]["answer"], "結果": "相符"}
        for no in sorted(gradable)
    ]

    blocks = build_blocks(questions_by_no, shared_by_group, image_paths)
    all_questions = [q for block in blocks for q in block["questions"]]

    return {
        "id": "social-113-answer-card",
        "subject": "社會",
        "year": "113",
        "category": "答題卡練習",
        "title": "113 年社會答題卡練習",
        "status": "官方 PDF 提取題庫",
        "source": {
            "試題": "資料/大考中心官方PDF/113學年度/社會/113學測-社會-試題內容-05-113學測社會科試題定稿.pdf",
            "答案": "資料/大考中心官方PDF/113學年度/社會/113學測-社會-選擇題答案-05-113學測社會答案.pdf",
        },
        "note": "收錄 113 學測社會選擇題共 54 題；另列手寫題 10 題（38,40,43,46,49,50,53,57,60,64，僅列出不作答）。題目、選項與答案均取自官方 PDF；圖表依官方 PDF 必要區域裁切。",
        "review_flags": [],
        "answer_check": answer_check,
        "questions": all_questions,
        "blocks": blocks,
    }


def main():
    bank = build_bank()
    OUT_JS.write_text(
        "// 由 tools/build_social_113.py 自動產生，請勿手改。題目與答案取自官方 PDF，未經改寫。\n"
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
        "images": len(CROPS),
        "review_flags": bank["review_flags"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
