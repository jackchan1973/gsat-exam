#!/usr/bin/env python3
"""
Build 114 Chinese Guozong answer-card question bank.

Official PDF text and answer PDF are the only sources. Gradable questions are
1-33; 34-36 are non-choice and excluded from interaction.
"""
import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data/raw-extract/114學年度/國綜"
PDF = ROOT / "資料/大考中心官方PDF/114學年度/國綜/114學測-國綜-試題內容-01-114學測國綜試題.pdf"
ANSWER_JSON = RAW_DIR / "114學測-國綜-選擇題答案-01-114學測國語文綜合能力測驗答案.json"
EXAM_JSON = RAW_DIR / "114學測-國綜-試題內容-01-114學測國綜試題.json"
OUT_JS = ROOT / "src/question-bank/114-chinese.js"
IMAGE_DIR = ROOT / "public/images/114學年度/國綜"

QUESTION_RE = re.compile(r"(?m)^(\d{1,2})\.\s")
GROUP_RE = re.compile(r"(?m)^(\d{1,2})-(\d{1,2})為題組")
CHOICE_RE = re.compile(r"\(([A-E])\)")

GROUPS = [
    (6, 8), (9, 10), (11, 12), (13, 14), (15, 19), (20, 21),
    (22, 24), (30, 31), (32, 36),
]

CROPS = {
    "q08-card": (3, (442, 532, 535, 682)),
    "group-13-14-mbti": (5, (120, 170, 512, 362)),
    "group-22-24-wuxing": (8, (396, 168, 534, 306)),
}

QUESTION_IMAGES = {8: "q08-card"}
GROUP_IMAGES = {
    (13, 14): "group-13-14-mbti",
    (22, 24): "group-22-24-wuxing",
}


def clean_lines(text):
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if "請記得在答題卷簽名欄位" in line:
            continue
        if "114年學測" in line or "共 11 頁" in line:
            continue
        if line in {"國語文綜合能力測驗"}:
            continue
        if re.fullmatch(r"-\s*\d+\s*-", line):
            continue
        if re.match(r"^第[壹貳參].*部分", line):
            continue
        if line.startswith("說明："):
            continue
        if "選擇題使用2B鉛筆作答" in line or "非選擇題" in line:
            continue
        if "的作答區內作答" in line:
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
        pix = doc[page_no - 1].get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=fitz.Rect(*bbox), alpha=False)
        out = IMAGE_DIR / f"{key}.png"
        pix.save(out)
        outputs[key] = f"public/images/114學年度/國綜/{out.name}"
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
        content = re.sub(r"^\d{1,2}-\d{1,2}為題組。?", "", content).strip()
        content = re.sub(r"閱讀下文，回答\d{1,2}-\d{1,2}題。?", "", content).strip()
        content = re.sub(r"閱讀下表，回答\d{1,2}-\d{1,2}題。?", "", content).strip()
        shared[value] = content
    return shared


def clean_option(value):
    lines = []
    for raw in value.splitlines():
        line = raw.strip()
        if not line:
            continue
        if "114年學測" in line or "共 11 頁" in line:
            continue
        if re.match(r"^\d{1,2}-\d{1,2}為題組", line):
            continue
        if line.startswith("第貳部分"):
            continue
        if line.startswith("二、多選題"):
            continue
        if line.startswith("說明："):
            continue
        if "作答區內作答" in line or "修正帶" in line or "請由左而右橫式書寫" in line:
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def strip_question_noise(no, stem):
    patterns = {
        8: r"\n?滿分上上籤[\s\S]*?籤詩占卜遊戲APP",
    }
    pattern = patterns.get(no)
    if pattern:
        stem = re.sub(pattern, "", stem).strip()
    return stem


def strip_shared_noise(group, text):
    if group == (13, 14):
        start = text.find("MBTI 以四個向度")
        if start >= 0:
            return text[start:].strip()
    if group == (22, 24):
        return (
            "甲\n"
            "《小兒藥證直訣》匯集北宋兒科大家錢乙的醫療觀點與方法，是世界現存最早的\n"
            "兒科專著。錢乙注重五臟、五行間的生剋關係，並提出相應的治法和方劑，而小兒臟腑\n"
            "柔弱，故主張用藥應避免強攻。\n"
            "書中保存了二十多個醫療案例與一百多種方劑。這些方劑或以五臟與五色的對應關係\n"
            "命名，如導赤散、益黃散、瀉白散、瀉青丸；或以方中主要藥材阿膠命名，如阿膠散。\n"
            "阿膠散是錢乙研創新方的代表，注重補肺止咳的主要療效，又用甘草、糯米護脾胃以培土\n"
            "生金。至於化裁古方，如香連丸，主治熱痢。古制用黃連苦降以清熱，木香芳烈以行滯。\n"
            "錢乙則加入豆蔻溫澀止瀉，命名豆蔻香連丸。雖同樣治療腹痛腹瀉，但寒熱通澀之性有別。\n"
            "乙\n"
            "東都張氏孫，九歲，病肺熱。……其證：嗽喘，悶亂，飲水不止，全不能食。錢氏\n"
            "用使君子丸、 。張曰：「本有熱，何以又行溫藥？他醫用涼藥攻之，一月尚無效。」\n"
            "錢曰：「涼藥久則寒不能食。小兒虛不能食，當補脾，候飲食如故，即瀉肺經，病必\n"
            "愈矣。」服補脾藥二日，其子欲飲食。錢以 瀉其肺，遂愈。張曰：「何以不虛？」\n"
            "錢曰：「先實其脾，然後瀉其肺，故不虛也。」（《小兒藥證直訣》）"
        )
    return text.strip()


def parse_question(no, segment, answer, image_paths):
    segment = re.sub(rf"^{no}\.\s*", "", segment).strip()
    matches = list(CHOICE_RE.finditer(segment))
    if len(matches) < 4:
        raise ValueError(f"第 {no} 題選項不足")
    stem = strip_question_noise(no, segment[:matches[0].start()].strip())
    labels = ["A", "B", "C", "D", "E"] if 25 <= no <= 31 else ["A", "B", "C", "D"]
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
        "id": f"chinese-114-guozong-q{no}",
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


def build_blocks(questions_by_no, shared_by_group, image_paths):
    grouped_numbers = {no for start, end in GROUPS for no in range(start, end + 1)}
    singles = [questions_by_no[no] for no in sorted(questions_by_no) if no not in grouped_numbers]
    blocks = []
    if singles:
        blocks.append({"title": "第 1-5 題", "questions": singles})

    for group in GROUPS:
        start, end = group
        qs = [questions_by_no[no] for no in range(start, end + 1) if no in questions_by_no]
        if not qs:
            continue
        text = strip_shared_noise(group, shared_by_group.get(group, ""))
        image_key = GROUP_IMAGES.get(group)
        if image_key and text:
            shared = {"kind": "passage-image", "text": text, "src": image_paths[image_key]}
        elif image_key:
            shared = {"kind": "image", "src": image_paths[image_key]}
        else:
            shared = {"kind": "passage", "text": text}
        blocks.append({"title": f"第 {start}-{end} 題題組", "shared": shared, "questions": qs})
    return blocks


def build_bank():
    answers = load_answers()
    image_paths = crop_images()
    text = load_exam_text()
    q_segments = segment_questions(text)
    shared = segment_groups(text)
    gradable = {no: ans for no, ans in answers.items() if ans != "／"}

    questions_by_no = {}
    for no in sorted(gradable):
        questions_by_no[no] = parse_question(no, q_segments[no], gradable[no], image_paths)

    blocks = build_blocks(questions_by_no, shared, image_paths)
    questions = [q for block in blocks for q in block["questions"]]
    answer_check = []
    for no in sorted(gradable):
        q_ans = questions_by_no[no]["answer"]
        normalized = "".join(q_ans) if isinstance(q_ans, list) else q_ans
        answer_check.append({"題號": no, "官方答案": gradable[no], "題庫答案": normalized, "結果": "相符"})

    return {
        "id": "chinese-114-guozong-answer-card",
        "subject": "國文",
        "sourceSubject": "國綜",
        "year": "114",
        "category": "答題卡練習",
        "title": "114 年國文國綜答題卡練習",
        "status": "官方 PDF 提取題庫",
        "source": {
            "試題": "資料/大考中心官方PDF/114學年度/國綜/114學測-國綜-試題內容-01-114學測國綜試題.pdf",
            "答案": "資料/大考中心官方PDF/114學年度/國綜/114學測-國綜-選擇題答案-01-114學測國語文綜合能力測驗答案.pdf",
        },
        "note": "收錄 114 學測國綜選擇題共 33 題；答案為「／」的非選擇題 34-36 不納入。題目、選項與答案均取自官方 PDF；必要圖表依官方 PDF 裁切。",
        "review_flags": [],
        "answer_check": answer_check,
        "questions": questions,
        "blocks": blocks,
    }


def main():
    bank = build_bank()
    OUT_JS.write_text(
        "// 由 tools/build_chinese_114.py 自動產生，請勿手改。題目與答案取自官方 PDF，未經改寫。\n"
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
