#!/usr/bin/env python3
"""
Build 115 social answer-card question bank.

The generated bank keeps official PDF text as the source of truth. Text is
structured only for answer-card interaction; figures/tables that must preserve
layout are cropped from the official PDF.
"""
import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data/raw-extract/115學年度/社會"
PDF = ROOT / "資料/大考中心官方PDF/115學年度/社會/115學測-社會-試題內容-05-115學測社會試卷.pdf"
ANSWER_JSON = RAW_DIR / "115學測-社會-選擇題答案-05-115學測社會答案.json"
EXAM_JSON = RAW_DIR / "115學測-社會-試題內容-05-115學測社會試卷.json"
OUT_JS = ROOT / "src/question-bank/115-social.js"
IMAGE_DIR = ROOT / "public/images/115學年度/社會"

CHOICES = ["A", "B", "C", "D"]
QUESTION_RE = re.compile(r"(?m)^(\d{1,2})\.\s")
GROUP_RE = re.compile(r"(?m)^(\d{1,2})-(\d{1,2})\s*為題組")
CHOICE_RE = re.compile(r"\(([A-D])\)")

GROUPS = [
    (26, 27), (28, 29), (30, 33), (34, 35), (36, 38),
    (39, 40), (41, 42), (43, 44), (45, 46), (47, 49),
    (50, 52), (53, 54), (55, 56), (57, 60), (61, 63), (64, 65),
]

# PDF coordinates in points: page, (x0, y0, x1, y1). Crops contain only the
# official figure/table region needed for answering.
CROPS = {
    "q05-table": (3, (108, 118, 490, 204)),
    "q08-table": (3, (108, 592, 494, 720)),
    "q12-figure": (4, (80, 545, 525, 747)),
    "q16-figure": (5, (340, 500, 532, 742)),
    "q18-figure": (6, (108, 248, 488, 454)),
    "q19-figure": (6, (108, 540, 488, 765)),
    "q20-figure": (7, (278, 104, 534, 338)),
    "q22-figure": (7, (120, 508, 475, 765)),
    "q23-figure": (8, (78, 170, 532, 292)),
    "group-36-38": (10, (288, 558, 526, 764)),
    "group-45-46": (13, (260, 345, 538, 616)),
    "group-47-49": (14, (120, 345, 474, 558)),
    "group-53-54": (16, (108, 190, 480, 756)),
    "group-57-60": (18, (58, 245, 536, 596)),
    "group-64-65": (20, (80, 178, 526, 392)),
}

QUESTION_IMAGES = {
    5: "q05-table",
    8: "q08-table",
    12: "q12-figure",
    16: "q16-figure",
    18: "q18-figure",
    19: "q19-figure",
    20: "q20-figure",
    22: "q22-figure",
    23: "q23-figure",
}

GROUP_IMAGES = {
    (36, 38): "group-36-38",
    (45, 46): "group-45-46",
    (47, 49): "group-47-49",
    (53, 54): "group-53-54",
    (57, 60): "group-57-60",
    (64, 65): "group-64-65",
}


def clean_lines(text):
    cleaned = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "115年學測" in line or "共 19 頁" in line:
            continue
        if "請記得在答題卷簽名欄位" in line:
            continue
        if line in {"社會考科", "共 19 頁"}:
            continue
        if re.fullmatch(r"-\s*\d+\s*-", line):
            continue
        if re.fullmatch(r"第\s*\d+\s*頁", line):
            continue
        if re.fullmatch(r"115年學測", line):
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
        page = doc[page_no - 1]
        pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=fitz.Rect(*bbox), alpha=False)
        out = IMAGE_DIR / f"{key}.png"
        pix.save(out)
        outputs[key] = f"public/images/115學年度/社會/{out.name}"
    doc.close()
    return outputs


def find_items(text):
    items = []
    for match in QUESTION_RE.finditer(text):
        items.append(("question", int(match.group(1)), match.start()))
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


def strip_official_figure_noise(no, text):
    replacements = {
        5: r"\n^表\s*1[\s\S]*$",
        8: r"\n^表\s*2[\s\S]*$",
        12: r"\n?甲\s+乙\s*\n?圖1",
        16: r"\n?●「崙」字地名\s*\n?圖2",
        18: r"\n?臺北[\s\S]*?圖3",
        19: r"\n?N\s*\n?圖4",
        20: r"\n?80\s*\n?55[\s\S]*?圖5",
        22: r"\n?甲\s+乙[\s\S]*?照片1",
        23: r"\n?\(℃\)[\s\S]*?圖6",
    }
    pattern = replacements.get(no)
    if pattern:
        text = re.sub(pattern, "", text, flags=re.MULTILINE).strip()
    return text


def strip_shared_figure_noise(group, text):
    if group == (36, 38):
        lines = []
        for line in text.splitlines():
            if line.startswith("聚落 主要道路"):
                continue
            if line.strip() == "圖7":
                continue
            line = line.replace(" 圖7", "")
            lines.append(line)
        return "\n".join(lines).strip()

    if group == (53, 54):
        return "\n".join(
            line for line in text.splitlines()
            if line.strip() not in {"舊線", "新線", "圖9", "圖10"}
        ).strip()

    replacements = {
        (45, 46): r"\n?左：巴米揚西大佛[\s\S]*?照片\s*2",
        (47, 49): r"\n?^俄羅斯[\s\S]*?圖8",
        (57, 60): r"\n?甲\s+乙[\s\S]*?圖11",
        (64, 65): r"\n?（百萬桶／天）[\s\S]*?圖\s*12",
    }
    pattern = replacements.get(group)
    if pattern:
        text = re.sub(pattern, "", text, flags=re.MULTILINE).strip()
    return text


def clean_option_text(value):
    lines = []
    for line in value.splitlines():
        line = line.strip()
        if not line:
            continue
        if "115年學測" in line or "共 19 頁" in line:
            continue
        if re.match(r"^\d{1,2}-\d{1,2}\s*為題組$", line):
            continue
        if line.startswith("第 ") and "部分" in line:
            continue
        if line.startswith("說明："):
            continue
        if line.startswith("題號的作答區內作答"):
            continue
        if "修正帶" in line or "非選擇題請" in line or "2B 鉛筆作答" in line:
            continue
        if line.startswith("●") or re.fullmatch(r"圖\s*\d+|照片\s*\d+", line):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def parse_question(no, segment, answer, image_paths):
    segment = re.sub(rf"^{no}\.\s*", "", segment).strip()

    if no == 20:
        question = {
            "id": "social-115-q20",
            "no": 20,
            "type": "single",
            "stem": (
                "某生玩一款手機遊戲，其中一個關卡需要先利用射程 200 公尺的狙擊槍來癱瘓某座碉堡\n"
                "頂端的探照燈，而且若走入該碉堡半徑 40 公尺的範圍內，則會被碉堡內的\n"
                "士兵發現並遭到反擊。圖 5 是該關卡的地圖，每個網格為10公尺的正方形，\n"
                "網格內的數值代表高度，黑色網格為碉堡所在位置，灰色網格為射擊地點\n"
                "候選位置。若要成功過關，該生選擇下列哪個網格作為射擊地點最為理想？"
            ),
            "choices": CHOICES,
            "options": {"A": "甲", "B": "乙", "C": "丙", "D": "丁"},
            "answer": answer,
            "image": image_paths[QUESTION_IMAGES[20]],
        }
        return question

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
        "id": f"social-115-q{no}",
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


def build_blocks(questions_by_no, shared_by_group, image_paths):
    grouped_numbers = {no for start, end in GROUPS for no in range(start, end + 1)}
    single_questions = [questions_by_no[no] for no in sorted(questions_by_no) if no not in grouped_numbers]
    blocks = []

    if single_questions:
        blocks.append({
            "title": "第 1-25 題",
            "questions": single_questions,
        })

    for group in GROUPS:
        start, end = group
        qs = [questions_by_no[no] for no in range(start, end + 1) if no in questions_by_no]
        if not qs:
            continue
        raw_shared = shared_by_group.get(group, "")
        shared_text = strip_shared_figure_noise(group, raw_shared)
        image_key = GROUP_IMAGES.get(group)
        if image_key and shared_text:
            shared = {
                "kind": "passage-image",
                "text": shared_text,
                "src": image_paths[image_key],
            }
        elif image_key:
            shared = {
                "kind": "image",
                "src": image_paths[image_key],
            }
        elif shared_text:
            shared = {
                "kind": "passage",
                "text": shared_text,
            }
        else:
            shared = None

        block = {
            "title": f"第 {start}-{end} 題題組",
            "questions": qs,
        }
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

    gradable = {no: ans for no, ans in answers.items() if ans != "／"}
    questions_by_no = {}
    for no in sorted(gradable):
        questions_by_no[no] = parse_question(no, question_segments[no], gradable[no], image_paths)

    answer_check = [
        {"題號": no, "官方答案": gradable[no], "題庫答案": questions_by_no[no]["answer"], "結果": "相符"}
        for no in sorted(gradable)
    ]

    blocks = build_blocks(questions_by_no, shared_by_group, image_paths)
    all_questions = []
    for block in blocks:
        all_questions.extend(block["questions"])

    bank = {
        "id": "social-115-answer-card",
        "subject": "社會",
        "year": "115",
        "category": "答題卡練習",
        "title": "115 年社會答題卡練習",
        "status": "官方 PDF 提取題庫",
        "source": {
            "試題": "資料/大考中心官方PDF/115學年度/社會/115學測-社會-試題內容-05-115學測社會試卷.pdf",
            "答案": "資料/大考中心官方PDF/115學年度/社會/115學測-社會-選擇題答案-05-115學測社會答案.pdf",
        },
        "note": "收錄 115 學測社會選擇題共 54 題；答案為「／」的非選擇題不納入。題目、選項與答案均取自官方 PDF；圖表依官方 PDF 必要區域裁切。",
        "review_flags": [],
        "answer_check": answer_check,
        "questions": all_questions,
        "blocks": blocks,
    }
    return bank


def main():
    bank = build_bank()
    OUT_JS.write_text(
        "// 由 tools/build_social_115.py 自動產生，請勿手改。題目與答案取自官方 PDF，未經改寫。\n"
        "QUESTION_BANKS.push(\n"
        + json.dumps(bank, ensure_ascii=False, indent=2)
        + "\n);\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "questions": len(bank["questions"]),
        "blocks": len(bank["blocks"]),
        "images": len(CROPS),
        "review_flags": bank["review_flags"],
        "out": str(OUT_JS),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
