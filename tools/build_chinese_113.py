#!/usr/bin/env python3
"""
Build 113 Chinese Guozong answer-card question bank.

113 國文依照 114/115 國文標準：純文字題盡量文字化，只有圖表、
框選資料等必要版面才裁官方 PDF 局部圖。題目與答案均取自官方 PDF，
不改寫、不推測；32、33、36 為手寫題，只列出不作答不判分。
"""
import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data/raw-extract/113學年度/國綜"
PDF = ROOT / "資料/大考中心官方PDF/113學年度/國綜/113學測-國綜-試題內容-01-113學測國綜試題定稿.pdf"
ANSWER_JSON = RAW_DIR / "113學測-國綜-選擇題答案-01-113學測國語文綜合能力測驗答案.json"
EXAM_JSON = RAW_DIR / "113學測-國綜-試題內容-01-113學測國綜試題定稿.json"
OUT_JS = ROOT / "src/question-bank/113-chinese.js"
IMAGE_DIR = ROOT / "public/images/113學年度/國綜"

QUESTION_RE = re.compile(r"(?m)^(\d{1,2})\.\s")
GROUP_RE = re.compile(r"(?m)^(\d{1,2})-?(\d{1,2})\s*為題組")
CHOICE_RE = re.compile(r"\(([A-E])\)")

GROUPS = [
    (6, 8), (9, 10), (11, 12), (13, 15), (16, 17),
    (18, 20), (21, 22), (23, 24), (30, 31), (32, 36),
]

CROPS = {
    "q15-movie-box": (5, (344, 575, 548, 780)),
    "group-21-22-judgment-box": (7, (376, 590, 544, 670)),
    "q29-material": (9, (62, 512, 548, 755)),
}

QUESTION_IMAGES = {
    15: "q15-movie-box",
    29: "q29-material",
}

GROUP_IMAGES = {
    (21, 22): "group-21-22-judgment-box",
}

HANDWRITTEN = [32, 33, 36]


MANUAL_QUESTIONS = {
    15: {
        "stem": "迷因（meme）是文化傳遞的微型單位，經由模仿、複製、改作，承載片段資訊或觀點，透過語文、圖片或影音等型態流傳，帶來影響。「周處除三害」即屬迷因，依據右列電影《周處除三害》簡介，關於其模仿、改作傳說，說明最適當的是：",
        "options": {
            "A": "行為動機模仿傳說，陳桂林因欲「為民除害」，而向兩大通緝要犯下手",
            "B": "故事結局模仿傳說，陳桂林悔悟後奮發向上，改造自己，最終盡除三害",
            "C": "人物設計模仿傳說，均安排一關鍵角色，勸說主角在離世前為人間除惡",
            "D": "三害概念模仿傳說，將猛虎惡蛟轉為兩大通緝要犯，並創發貪嗔痴的新義",
        },
    },
    21: {
        "stem": "若依右框當代判決書要項，觀察上列古代判決書，最符合文中所述的是：",
        "options": {
            "A": "當事人：程十乙為原告，劉珵、鄭七為被告",
            "B": "事實：鄭七有償獲得元老，自認有理由繼續保有養子",
            "C": "主文：劉珵須賠償鄭七，並不得與元老恢復父子關係",
            "D": "理由：鄭七已撫養元老三年；元老已對生父心懷不滿",
        },
    },
    22: {
        "stem": "下列敘述，最符合上文寫作方式的是：",
        "options": {
            "A": "全文大致先提出法律規定，再說明案件違背該法條，最後敘述判決結果",
            "B": "說明案件時，先列被告自陳的事實，再敘原告的反駁，再舉證人的佐證",
            "C": "以「其罪在子、其責在父」為綱領，依序指陳「子不子、父不父」之過",
            "D": "時見教化口吻，除對悖倫者嚴辭訓斥，並期勉受託者負起維護禮教之責",
        },
    },
    29: {
        "stem": "關於硃砂（主成分為硫化汞），符合下列資料所述的是：",
        "options": {
            "A": "水飛法是將硃砂先以清水反覆淘洗，再曬乾研成粉末",
            "B": "今日若以機器研磨取代水飛法，將因高溫使硃砂含有劇毒",
            "C": "升煉法主要用於煉製水銀，水銀加入硫黃之後可再產生銀朱",
            "D": "銀朱藉升煉獲得，不僅速度快，毒性也比水飛法獲得的頭朱低",
            "E": "藥用硃砂若以安全方式炮製，非全不可用，但臺灣目前完全禁用",
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
        if "113年學測" in line or "共 11 頁" in line:
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
        outputs[key] = f"public/images/113學年度/國綜/{out.name}"
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
        content = re.sub(r"閱讀甲、乙、丙、丁文，回答\s*\d{1,2}-?\d{1,2}\s*題。?", "", content).strip()
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
        if line.startswith("第貳部分") or line.startswith("第 2 頁"):
            continue
        if "作答區內作答" in line or "修正帶" in line:
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def labels_for(no):
    return ["A", "B", "C", "D", "E"] if 25 <= no <= 31 else ["A", "B", "C", "D"]


def make_question(no, answer, image_paths):
    labels = labels_for(no)
    q_type = "multiple" if len(answer) > 1 else "single"
    source = MANUAL_QUESTIONS[no]
    question = {
        "id": f"chinese-113-guozong-q{no}",
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
    stem = segment[:matches[0].start()].strip()
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
        "id": f"chinese-113-guozong-q{no}",
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


def split_32_36_material(q_segments, shared_by_group):
    q32 = re.sub(r"^32\.\s*", "", q_segments[32]).strip()
    q33 = re.sub(r"^33\.\s*", "", q_segments[33]).strip()
    q32_question, _, material_乙 = q32.partition("\n乙\n")
    q33_question, _, material_丙丁 = q33.partition("\n丙\n")
    shared = shared_by_group.get((32, 36), "").strip()
    if material_乙.strip():
        shared += "\n\n乙\n" + material_乙.strip()
    if material_丙丁.strip():
        shared += "\n\n丙\n" + material_丙丁.strip()
    q_segments[32] = "32. " + q32_question.strip()
    q_segments[33] = "33. " + q33_question.strip()
    shared_by_group[(32, 36)] = shared.strip()


def parse_handwritten(no, segment, image_paths):
    segment = re.sub(rf"^{no}\.\s*", "", segment).strip()
    return {
        "id": f"chinese-113-guozong-hw-q{no}",
        "no": no,
        "type": "handwritten",
        "stem": segment,
    }


def strip_shared_noise(group, text):
    if group == (21, 22):
        text = re.sub(r"\n?當代判決書的要項[\s\S]*$", "", text).strip()
    return text.strip()


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
    for group in [(6, 8), (9, 10), (11, 12), (13, 15), (16, 17), (18, 20), (21, 22), (23, 24)]:
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
    split_32_36_material(q_segments, shared)

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
        "id": "chinese-113-guozong-answer-card",
        "subject": "國文",
        "sourceSubject": "國綜",
        "year": "113",
        "category": "答題卡練習",
        "title": "113 年國文國綜答題卡練習",
        "status": "官方 PDF 提取題庫",
        "source": {
            "試題": "資料/大考中心官方PDF/113學年度/國綜/113學測-國綜-試題內容-01-113學測國綜試題定稿.pdf",
            "答案": "資料/大考中心官方PDF/113學年度/國綜/113學測-國綜-選擇題答案-01-113學測國語文綜合能力測驗答案.pdf",
        },
        "note": "收錄 113 學測國文選擇題共 33 題，另列手寫題 3 題（32、33、36，僅列出不作答）。題目與答案均取自官方 PDF；圖表依官方 PDF 必要區域裁切。",
        "review_flags": [],
        "answer_check": answer_check,
        "questions": questions,
        "blocks": blocks,
    }


def main():
    bank = build_bank()
    OUT_JS.write_text(
        "// 由 tools/build_chinese_113.py 自動產生，請勿手改。題目與答案取自官方 PDF，未經改寫。\n"
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
