#!/usr/bin/env python3
"""
add_handwritten_social_115.py — 把 115 社會的非選擇題（手寫題）插入既有題庫。

依規則：手寫題放進題庫、列出題目，但不作答不判分。
題幹取自中繼檔（官方 PDF 抽取結果），不改寫；插入 src/question-bank/115-social.js
對應題組 block（依題號排序），並加進 flat questions 供程式統計。
非選題號（官方答案「／」）：40,42,44,46,49,52,54,56,60,63,65。
可重複執行（已存在的手寫題會先移除再重插）。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "src" / "question-bank" / "115-social.js"
RAW_DIR = ROOT / "data" / "raw-extract" / "115學年度" / "社會"
HW_NOS = [40, 42, 44, 46, 49, 52, 54, 56, 60, 63, 65]
NOISE = ["請記得在答題卷簽名欄位", "背 面 還 有 試 題"]


def clean_lines():
    meta = None
    for f in RAW_DIR.glob("*.json"):
        if "試題內容" in f.name:
            meta = json.loads(f.read_text(encoding="utf-8"))
    lines = []
    for p in meta["pages"][1:]:
        for ln in p["text"].splitlines():
            s = ln.strip()
            if not s or any(n in s for n in NOISE) or "社會考科" in s:
                continue
            if re.fullmatch(r"-\s*\d+\s*-", s):
                continue
            lines.append(ln.rstrip())
    return lines


def extract_stems(lines):
    """回傳 {題號: 題幹文字}。從 'NN.' 起，收到下一個題號/題組標記為止。"""
    starts = {}
    for i, ln in enumerate(lines):
        m = re.match(r"^(\d{1,2})\.\s", ln.strip())
        if m:
            n = int(m.group(1))
            if n not in starts:
                starts[n] = i
    stems = {}
    boundary = re.compile(r"^(\d{1,2})\.\s|為題組|^第\s*[壹貳參]")
    for n in HW_NOS:
        if n not in starts:
            stems[n] = None
            continue
        i = starts[n]
        buf = [re.sub(r"^\d{1,2}\.\s*", "", lines[i].strip())]
        for j in range(i + 1, len(lines)):
            if boundary.search(lines[j].strip()):
                break
            buf.append(lines[j].strip())
        stems[n] = " ".join(buf).strip()
    return stems


def main():
    lines = clean_lines()
    stems = extract_stems(lines)
    missing = [n for n, s in stems.items() if not s]
    if missing:
        print("⚠ 找不到題幹，需人工處理：", missing)

    txt = BANK.read_text(encoding="utf-8")
    m = re.search(r"QUESTION_BANKS\.push\(\s*(\{.*\})\s*\);", txt, re.S)
    bank = json.loads(m.group(1))

    # 移除舊的手寫題（可重跑）
    bank["questions"] = [q for q in bank["questions"] if q.get("type") != "handwritten"]
    for blk in bank["blocks"]:
        blk["questions"] = [q for q in blk["questions"] if q.get("type") != "handwritten"]

    inserted = []
    for n in HW_NOS:
        if not stems[n]:
            continue
        entry = {"id": "social-115-hw-%d" % n, "no": n, "type": "handwritten", "stem": stems[n]}
        # 找涵蓋此題號的題組 block（標題如「第 39-40 題題組」）
        target = None
        for blk in bank["blocks"]:
            mm = re.search(r"第\s*(\d+)-(\d+)\s*題", blk.get("title", ""))
            if mm and int(mm.group(1)) <= n <= int(mm.group(2)):
                target = blk
                break
        if target is None:
            print("⚠ 第 %d 題找不到對應題組 block，跳過" % n)
            continue
        target["questions"].append(entry)
        target["questions"].sort(key=lambda q: q["no"])
        bank["questions"].append(entry)
        inserted.append(n)

    bank["questions"].sort(key=lambda q: q["no"])
    bank["note"] = (bank.get("note") or "").rstrip("。") + \
        "；含手寫題 %d 題（%s，僅列出不作答）。" % (len(inserted), ",".join(map(str, inserted)))

    header = txt[:m.start()]
    BANK.write_text(header + "QUESTION_BANKS.push(\n" +
                    json.dumps(bank, ensure_ascii=False, indent=2) + "\n);\n", encoding="utf-8")
    print("已插入手寫題 %d 題：%s" % (len(inserted), inserted))
    print("總題目數（含手寫）：%d" % len(bank["questions"]))


if __name__ == "__main__":
    main()
