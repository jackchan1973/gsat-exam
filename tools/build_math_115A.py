#!/usr/bin/env python3
"""
build_math_115A.py — 115 數學A 題庫（圖片題型）。

數學公式無法可靠文字化，依規範每一題（題幹＋選項）裁成官方圖片呈現，
答題卡另放作答輸入：單選/多選點 ①–⑤；選填題填數字格。答案取自官方選擇(填)題答案。

題型（依官方）：
- Q1–6   單選（選 ①–⑤ 之一）
- Q7–12  多選（①–⑤ 複選）
- Q13–17 選填（數字格，各格 0–9）
- Q18    單選（18–20 題組的選擇題，圖含共用圖形）
- Q19–20 非選擇題 → 排除
輸出：src/question-bank/115-matha.js（QUESTION_BANKS.push）。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "question-bank" / "115-matha.js"
IMG = "public/images/115學年度/數學A"

# 官方答案（選擇(填)題答案 PDF）
SINGLE = {1: "2", 2: "1", 3: "1", 4: "3", 5: "5", 6: "2", 18: "3"}
MULTI = {7: ["3", "4"], 8: ["2", "5"], 9: ["1", "2", "4"], 10: ["1", "5"], 11: ["2", "4"], 12: ["2", "4"]}
FILL = {
    13: (["13-1", "13-2", "13-3"], ["9", "1", "0"]),
    14: (["14-1", "14-2"], ["1", "4"]),
    15: (["15-1", "15-2"], ["3", "2"]),
    16: (["16-1", "16-2", "16-3"], ["3", "5", "2"]),
    17: (["17-1", "17-2", "17-3"], ["3", "1", "1"]),
}


def img(n):
    return "%s/q%02d.png" % (IMG, n)


def qid(n):
    return "matha-115-q%d" % n


def build():
    flat, blocks = [], []

    def add(q):
        flat.append(q)
        return q

    def single_q(n):
        return add({"id": qid(n), "no": n, "type": "single", "image": img(n),
                    "choices": ["1", "2", "3", "4", "5"], "answer": SINGLE[n]})

    # 一、單選題 1-6
    blocks.append({"type": "group", "title": "一、單選題（第 1–6 題）", "shared": None,
                   "questions": [single_q(n) for n in range(1, 7)]})
    # 二、多選題 7-12
    blocks.append({"type": "group", "title": "二、多選題（第 7–12 題）", "shared": None,
                   "questions": [add({"id": qid(n), "no": n, "type": "multiple", "image": img(n),
                                      "choices": ["1", "2", "3", "4", "5"], "answer": MULTI[n]})
                                 for n in range(7, 13)]})
    # 三、選填題 13-17
    fillqs = []
    for n in range(13, 18):
        boxes, ans = FILL[n]
        fillqs.append(add({"id": qid(n), "no": n, "type": "fill", "image": img(n),
                           "boxes": boxes, "answer": ans}))
    blocks.append({"type": "group", "title": "三、選填題（第 13–17 題）· 填數字格", "shared": None,
                   "questions": fillqs})
    # 第貳部分 題組 18-20（18 單選；19、20 手寫題僅列出，不作答）
    hw = [add({"id": qid(n), "no": n, "type": "handwritten", "image": img(n)}) for n in (19, 20)]
    blocks.append({"type": "group", "title": "第貳部分 題組（第 18–20 題；18 單選，19–20 手寫題）", "shared": None,
                   "questions": [single_q(18)] + hw})

    bank = {
        "id": "matha-115-answer-card", "subject": "數學", "sourceSubject": "數學A", "year": "115",
        "category": "數學A 答題卡練習", "title": "115 年數學A 答題卡練習",
        "status": "官方 PDF 提取題庫",
        "source": {
            "試題": "資料/大考中心官方PDF/115學年度/數學A/115學測-數學A-試題內容-03-115學測數學a試卷.pdf",
            "答案": "資料/大考中心官方PDF/115學年度/數學A/115學測-數學A-選擇(填)題答案-03-115學測數學a答案.pdf",
        },
        "note": "收錄 115 數學A：可作答 18 題（單選6＋多選6＋選填5＋題組單選1）＋手寫題 2 題（第19、20題，僅列出不作答）。"
                "每題為官方 PDF 裁圖，公式原樣呈現；答案取自官方選擇(填)題答案。",
        "questions": flat, "blocks": blocks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    header = "// 由 tools/build_math_115A.py 自動產生，請勿手改。題目與答案取自官方 PDF，未經改寫。\n"
    OUT.write_text(header + "QUESTION_BANKS.push(\n" + json.dumps(bank, ensure_ascii=False, indent=2) + "\n);\n",
                   encoding="utf-8")
    print("已輸出：", OUT.relative_to(ROOT))
    print("題數：%d（單選 %d + 多選 %d + 選填 %d + 題組單選 1）" % (
        len(flat), len(SINGLE) - 1, len(MULTI), len(FILL)))


if __name__ == "__main__":
    build()
