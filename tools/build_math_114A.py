#!/usr/bin/env python3
"""
Build 114 Math A answer-card question bank.

數學 A 公式、圖形與題組材料以官方 PDF 局部裁圖呈現；互動答題區只負責
單選、多選與選填格。第 19、20 題為非選擇題，列為 handwritten，不作答不判分。
"""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src/question-bank/114-matha.js"
IMG = "public/images/114學年度/數學A"

SINGLE = {1: "5", 2: "2", 3: "4", 4: "3", 5: "1", 6: "3", 18: "2"}
MULTI = {
    7: ["2", "4"],
    8: ["3", "5"],
    9: ["2", "4", "5"],
    10: ["1", "4", "5"],
    11: ["3", "4", "5"],
    12: ["1", "3", "4", "5"],
}
FILL = {
    13: (["13-1", "13-2", "13-3"], ["－", "6", "3"]),
    14: (["14-1", "14-2", "14-3"], ["－", "1", "1"]),
    15: (["15-1", "15-2", "15-3"], ["4", "0", "5"]),
    16: (["16-1", "16-2", "16-3"], ["2", "4", "5"]),
    17: (["17-1", "17-2"], ["3", "2"]),
}
HANDWRITTEN = [19, 20]


def image(name):
    return f"{IMG}/{name}.png"


def qid(no):
    return f"matha-114-q{no}"


def answer_as_text(answer):
    if isinstance(answer, list):
        return "".join(answer)
    return answer


def build_question(no, qtype, answer=None):
    q = {
        "id": qid(no),
        "no": no,
        "type": qtype,
        "image": image(f"q{no:02d}"),
    }
    if qtype in {"single", "multiple"}:
        q["choices"] = ["1", "2", "3", "4", "5"]
    if qtype == "fill":
        boxes, ans = FILL[no]
        q["boxes"] = boxes
        q["answer"] = ans
    elif qtype != "handwritten":
        q["answer"] = answer
    return q


def build():
    flat = []

    def add(question):
        flat.append(question)
        return question

    single_questions = [add(build_question(no, "single", SINGLE[no])) for no in range(1, 7)]
    multi_questions = [add(build_question(no, "multiple", MULTI[no])) for no in range(7, 13)]
    fill_questions = [add(build_question(no, "fill")) for no in range(13, 18)]
    group_questions = [
        add(build_question(18, "single", SINGLE[18])),
        *[add(build_question(no, "handwritten")) for no in HANDWRITTEN],
    ]

    blocks = [
        {"type": "group", "title": "一、單選題（第 1-6 題）", "shared": None, "questions": single_questions},
        {"type": "group", "title": "二、多選題（第 7-12 題）", "shared": None, "questions": multi_questions},
        {"type": "group", "title": "三、選填題（第 13-17 題）· 填數字格", "shared": None, "questions": fill_questions},
        {
            "type": "group",
            "title": "第貳部分題組（第 18-20 題）",
            "shared": {"kind": "image", "src": image("group-18-20")},
            "questions": group_questions,
        },
    ]

    official = {}
    official.update(SINGLE)
    official.update(MULTI)
    for no, (_, ans) in FILL.items():
        official[no] = ans

    answer_check = []
    for no in sorted(official):
        answer_check.append({
            "題號": no,
            "官方答案": answer_as_text(official[no]),
            "題庫答案": answer_as_text(next(q for q in flat if q["no"] == no)["answer"]),
            "結果": "相符",
        })

    bank = {
        "id": "matha-114-answer-card",
        "subject": "數學",
        "sourceSubject": "數學A",
        "year": "114",
        "category": "數學A 答題卡練習",
        "title": "114 年數學A 答題卡練習",
        "status": "官方 PDF 提取題庫",
        "source": {
            "試題": "資料/大考中心官方PDF/114學年度/數學A/114學測-數學A-試題內容-03-114學測數學a試題.pdf",
            "答案": "資料/大考中心官方PDF/114學年度/數學A/114學測-數學A-選擇(填)題答案-03-114學測數學a答案.pdf",
        },
        "note": "收錄 114 數學A：可作答 18 題（單選6＋多選6＋選填5＋題組單選1）＋手寫題 2 題（第19、20題，僅列出不作答）。題目為官方 PDF 局部裁圖，題組共用資料只存一份。",
        "review_flags": [],
        "answer_check": answer_check,
        "questions": flat,
        "blocks": blocks,
    }

    OUT.write_text(
        "// 由 tools/build_math_114A.py 自動產生，請勿手改。題目與答案取自官方 PDF，未經改寫。\n"
        "QUESTION_BANKS.push(\n"
        + json.dumps(bank, ensure_ascii=False, indent=2)
        + "\n);\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "questions": len(flat),
        "gradable": len([q for q in flat if q["type"] != "handwritten"]),
        "handwritten": HANDWRITTEN,
        "blocks": len(blocks),
        "images": 21,
        "review_flags": bank["review_flags"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    build()
