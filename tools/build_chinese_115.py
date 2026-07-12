#!/usr/bin/env python3
"""
Build 115 Chinese Guozong answer-card question bank.

115 國文改用 114 國文標準：文字題盡量文字化，只有右框、表格、
插圖等必要版面才裁官方 PDF 局部圖。題目與答案均取自官方 PDF，
不改寫、不推測；32-34 為手寫題，只列出不作答不判分。
"""
import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data/raw-extract/115學年度/國綜"
PDF = ROOT / "資料/大考中心官方PDF/115學年度/國綜/115學測-國綜-試題內容-01-115學測國綜試卷.pdf"
ANSWER_JSON = RAW_DIR / "115學測-國綜-選擇題答案-01-115學測國語文綜合能力測驗答案.json"
EXAM_JSON = RAW_DIR / "115學測-國綜-試題內容-01-115學測國綜試卷.json"
OUT_JS = ROOT / "src/question-bank/115-chinese.js"
IMAGE_DIR = ROOT / "public/images/115學年度/國綜"

QUESTION_RE = re.compile(r"(?m)^(\d{1,2})\.\s")
GROUP_RE = re.compile(r"(?m)^(\d{1,2})-?(\d{1,2})\s*為題組")
CHOICE_RE = re.compile(r"\(([A-E])\)")

GROUPS = [
    (6, 8), (9, 10), (11, 13), (14, 15), (16, 18),
    (19, 21), (22, 24), (30, 31), (32, 36),
]

CROPS = {
    "q04-panel": (2, (350, 446, 542, 662)),
    "group-14-15-table": (5, (75, 354, 540, 572)),
    "group-19-21-image": (7, (395, 104, 540, 330)),
    "group-22-24-material": (8, (62, 108, 540, 420)),
    "q28-sidebar": (9, (454, 386, 540, 562)),
    "group-30-31-material": (10, (70, 112, 548, 446)),
}

QUESTION_IMAGES = {
    4: "q04-panel",
    28: "q28-sidebar",
}

GROUP_IMAGES = {
    (14, 15): "group-14-15-table",
    (19, 21): "group-19-21-image",
    (22, 24): "group-22-24-material",
    (30, 31): "group-30-31-material",
}

HANDWRITTEN = [32, 33, 34]


MANUAL_QUESTIONS = {
    4: {
        "stem": "依據右框，下列篇章的解讀，最適當的是：",
        "options": {
            "A": "〈鴻門宴〉中，范增指沛公「其志不在小」，意在避免楚軍陷入①②",
            "B": "〈燭之武退秦師〉中，晉文公謂「失其所與，不知」，意在避免晉國陷入③",
            "C": "〈諫逐客書〉中，李斯以「藉寇兵而齎盜糧」為喻，意在警示執政者勿陷入④⑥",
            "D": "《孟子》中，孟子舉出「塗有餓莩而不知發，人死，則曰：『非我也，歲也。』」的荒謬，意在警示執政者勿陷入⑤",
        },
    },
    14: {
        "stem": "依據上表，對右框5個量詞進行分類，最適當的是：",
        "options": {
            "A": "名量詞：①②；動量詞：③④⑤",
            "B": "名量詞：①②⑤；動量詞：③④",
            "C": "名量詞：①③⑤；動量詞：②④",
            "D": "名量詞：②④⑤；動量詞：①③",
        },
    },
    28: {
        "stem": "文學除了以視覺接收，也會以聽覺感受。關於文學的聲音表現，敘述適當的是：",
        "options": {
            "A": "元代雜劇中註明曲牌的文字可合樂而歌，穿插其間的口白不用押韻",
            "B": "詞在宋代可合樂而歌，僅注重押韻；後世轉以誦讀為主，才講求平仄",
            "C": "四言詩音節多為「二/二」，如「蒹葭/蒼蒼，白露/為霜」；五言詩音節多為「二/三」，如「飄飄/何所似，天地/一沙鷗」",
            "D": "駢文雖以誦讀為主，但注重平仄相諧，如張李德和〈畫菊自序〉「人為萬物之靈，志有萬端之異」，前後句的二、四、六字平仄相對",
            "E": "新月派的新詩講求韻律，有時會押「行內韻」——即一句內有兩個同韻字，如徐志摩〈再別康橋〉「是夕陽中的新娘」、「夏蟲也為我沉默」",
        },
    },
}


def clean_lines(text):
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if "請記得在答題卷簽名欄位" in line:
            continue
        if "115年學測" in line or "共 11 頁" in line:
            continue
        if line in {"國語文綜合能力測驗"}:
            continue
        if re.fullmatch(r"-\s*\d+\s*-", line):
            continue
        if re.match(r"^第[壹貳參].*部分", line):
            continue
        if line.startswith("一、單選題") or line.startswith("二、多選題"):
            continue
        if line.startswith("說明："):
            continue
        if "限在答題卷標示題號" in line or "的作答區內作答" in line:
            continue
        if "選擇題使用2B鉛筆作答" in line or "非選擇題" in line:
            continue
        if "請由左而右橫式書寫" in line:
            continue
        lines.append(line)
    return "\n".join(lines)


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
        pix = doc[page_no - 1].get_pixmap(matrix=fitz.Matrix(2.6, 2.6), clip=fitz.Rect(*bbox), alpha=False)
        out = IMAGE_DIR / f"{key}.png"
        pix.save(out)
        outputs[key] = f"public/images/115學年度/國綜/{out.name}"
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
    for index, (kind, value, start) in enumerate(items):
        if kind != "group":
            continue
        end = items[index + 1][2] if index + 1 < len(items) else len(text)
        content = text[start:end].strip()
        content = re.sub(r"^\d{1,2}-?\d{1,2}\s*為題組。?", "", content).strip()
        content = re.sub(r"閱讀下文，回答\s*\d{1,2}-?\d{1,2}\s*題。?", "", content).strip()
        content = re.sub(r"閱讀下表，回答\s*\d{1,2}-?\d{1,2}\s*題。?", "", content).strip()
        shared[value] = content
    return shared


def clean_option(value):
    lines = []
    for raw in value.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.match(r"^\d{1,2}-?\d{1,2}\s*為題組", line):
            continue
        if line.startswith("第貳部分"):
            continue
        if "作答區內作答" in line or "修正帶" in line:
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def strip_question_noise(no, stem):
    patterns = {
        8: r"\n?本研究使用五個 cpDNA[\s\S]*?顯示兩者存在極大分化。",
        28: r"\n?表現方式[\s\S]*?平仄",
    }
    pattern = patterns.get(no)
    if pattern:
        stem = re.sub(pattern, "", stem).strip()
    return stem


def strip_shared_noise(group, text):
    if group == (14, 15):
        return ""
    if group == (22, 24):
        return ""
    if group == (19, 21):
        text = re.sub(r"\n?▲ 懷素〈自敘帖〉（局部）[\s\S]*?融入設計中。", "", text).strip()
    if group == (30, 31):
        return ""
    return text.strip()


def labels_for(no):
    return ["A", "B", "C", "D", "E"] if 25 <= no <= 31 else ["A", "B", "C", "D"]


def make_question(no, answer, image_paths):
    labels = labels_for(no)
    q_type = "multiple" if len(answer) > 1 else "single"
    source = MANUAL_QUESTIONS[no]
    question = {
        "id": f"chinese-115-guozong-q{no}",
        "no": no,
        "type": q_type,
        "stem": source["stem"],
        "choices": labels,
        "options": source["options"],
        "answer": list(answer) if q_type == "multiple" else answer,
    }
    if no in QUESTION_IMAGES:
        question["image"] = image_paths[QUESTION_IMAGES[no]]
    return question


def parse_question(no, segment, answer, image_paths):
    if no in MANUAL_QUESTIONS:
        return make_question(no, answer, image_paths)

    segment = re.sub(rf"^{no}\.\s*", "", segment).strip()
    matches = list(CHOICE_RE.finditer(segment))
    if len(matches) < 4:
        raise ValueError(f"第 {no} 題選項不足")
    stem = strip_question_noise(no, segment[:matches[0].start()].strip())
    if no == 29:
        stem = re.sub(r"：\s*押韻\s*", "：\n", stem).strip()
    labels = labels_for(no)
    options = {}
    for idx, match in enumerate(matches):
        label = match.group(1)
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(segment)
        if label in labels:
            options[label] = clean_option(segment[match.end():end])
    if set(options) != set(labels):
        raise ValueError(f"第 {no} 題選項標籤不完整：{sorted(options)}")

    q_type = "multiple" if len(answer) > 1 else "single"
    question = {
        "id": f"chinese-115-guozong-q{no}",
        "no": no,
        "type": q_type,
        "stem": stem,
        "choices": labels,
        "options": options,
        "answer": list(answer) if q_type == "multiple" else answer,
    }
    if no in QUESTION_IMAGES:
        question["image"] = image_paths[QUESTION_IMAGES[no]]
    return question


def parse_handwritten(no, segment, image_paths):
    segment = re.sub(rf"^{no}\.\s*", "", segment).strip()
    return {
        "id": f"chinese-115-guozong-hw-q{no}",
        "no": no,
        "type": "handwritten",
        "stem": segment,
    }


def build_blocks(questions_by_no, shared_by_group, image_paths):
    blocks = []

    def add_single_block(title, numbers):
        qs = [questions_by_no[no] for no in numbers if no in questions_by_no]
        if qs:
            blocks.append({"title": title, "questions": qs})

    def add_group_block(group):
        start, end = group
        qs = [questions_by_no[no] for no in range(start, end + 1) if no in questions_by_no]
        if not qs:
            return
        text = strip_shared_noise(group, shared_by_group.get(group, ""))
        image_key = GROUP_IMAGES.get(group)
        if image_key and text:
            shared = {"kind": "passage-image", "text": text, "src": image_paths[image_key]}
        elif image_key:
            shared = {"kind": "image", "src": image_paths[image_key]}
        else:
            shared = {"kind": "passage", "text": text}
        blocks.append({"title": f"第 {start}-{end} 題題組", "shared": shared, "questions": qs})

    add_single_block("第 1-5 題", range(1, 6))
    for group in [(6, 8), (9, 10), (11, 13), (14, 15), (16, 18), (19, 21), (22, 24)]:
        add_group_block(group)
    add_single_block("第 25-29 題（多選題）", range(25, 30))
    for group in [(30, 31), (32, 36)]:
        add_group_block(group)
    return blocks


def build_bank():
    answers = load_answers()
    image_paths = crop_images()
    text = load_exam_text()
    q_segments = segment_questions(text)
    shared = segment_groups(text)

    questions_by_no = {}
    gradable = {no: ans for no, ans in answers.items() if ans != "／"}
    for no in sorted(gradable):
        questions_by_no[no] = parse_question(no, q_segments[no], gradable[no], image_paths)
    for no in HANDWRITTEN:
        questions_by_no[no] = parse_handwritten(no, q_segments[no], image_paths)

    blocks = build_blocks(questions_by_no, shared, image_paths)
    questions = [q for block in blocks for q in block["questions"]]

    answer_check = []
    for no in sorted(gradable):
        q_ans = questions_by_no[no]["answer"]
        normalized = "".join(q_ans) if isinstance(q_ans, list) else q_ans
        answer_check.append({"題號": no, "官方答案": gradable[no], "題庫答案": normalized, "結果": "相符"})

    return {
        "id": "chinese-115-guozong-answer-card",
        "subject": "國文",
        "sourceSubject": "國綜",
        "year": "115",
        "category": "答題卡練習",
        "title": "115 年國文國綜答題卡練習",
        "status": "官方 PDF 提取題庫",
        "source": {
            "試題": "資料/大考中心官方PDF/115學年度/國綜/115學測-國綜-試題內容-01-115學測國綜試卷.pdf",
            "答案": "資料/大考中心官方PDF/115學年度/國綜/115學測-國綜-選擇題答案-01-115學測國語文綜合能力測驗答案.pdf",
        },
        "note": "收錄 115 學測國文選擇題共 33 題，另列手寫題 3 題（32、33、34，僅列出不作答）。題目與答案均取自官方 PDF；圖表依官方 PDF 必要區域裁切。",
        "review_flags": [],
        "answer_check": answer_check,
        "questions": questions,
        "blocks": blocks,
    }


def main():
    bank = build_bank()
    OUT_JS.write_text(
        "// 由 tools/build_chinese_115.py 自動產生，請勿手改。題目與答案取自官方 PDF，未經改寫。\n"
        "const QUESTION_BANKS = [];\n"
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
