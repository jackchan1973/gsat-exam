#!/usr/bin/env python3
"""
build_english.py — 跨年度英文題庫建置（113/114/115…）

用法：
    python tools/build_english.py 114

把某年度英文中繼檔，依「圖文混合題庫解析規範」組成正式互動題庫，並輸出：
- data/questions/{年}學年度/英文/questions.json（中繼結構）
- src/question-bank/{年}-english.js（主程式 index.html 用的 QUESTION_BANKS）
- public/images/{年}學年度/英文/*.png（看圖題/需裁圖的共用材料）

原則：題目、選項、文章、答案一律取自官方 PDF，不改寫/推測/補完；
抽取異常一律進 review_flags 交人工；各年度差異只寫在 CONFIG，共用結構共用程式。

各年度英文大題結構相同（詞彙10、綜合10、文意選填10、篇章4、閱讀12、混合），
年度差異集中在：看圖題題號與裁圖座標、混合題型態（雙欄裁圖 or 單欄論壇文字）。
"""
import json
import re
import sys
import traceback
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
NOISE = ["請記得在答題卷簽名欄位", "背 面 還 有 試 題"]

# ---- 各年度差異設定（只有這裡跟年度有關）----
CONFIG = {
    "113": {
        "image_q": {"no": 35, "page": 6,
                    "crops": {"A": (68, 106, 289, 261), "B": (289, 106, 508, 261),
                              "C": (68, 261, 289, 428), "D": (289, 261, 508, 428)}},
        "mixed": {"style": "image", "page": 9, "rect": (50, 160, 548, 712)},
    },
    "114": {
        "image_q": {"no": 36, "page": 6,
                    "crops": {"A": (107, 195, 289, 371), "B": (289, 195, 496, 371),
                              "C": (107, 373, 289, 540), "D": (289, 373, 496, 540)}},
        "mixed": {"style": "forum"},
    },
    "115": {
        "image_q": {"no": 38, "page": 6,
                    "crops": {"A": (82, 210, 307, 403), "B": (307, 210, 533, 403),
                              "C": (82, 403, 307, 594), "D": (307, 403, 533, 594)}},
        "mixed": {"style": "shops", "page": 9, "map_rect": (64, 276, 528, 492)},
    },
}

review_flags = []


def clean_lines(meta, page_footer_kw):
    def is_noise(line):
        s = line.strip()
        if not s:
            return True
        if any(n in s for n in NOISE) or page_footer_kw in s:
            return True
        if re.fullmatch(r"-\s*\d+\s*-", s):
            return True
        return False

    lines = []
    for p in meta["pages"][1:]:
        for ln in p["text"].splitlines():
            if not is_noise(ln):
                lines.append(ln.rstrip())
    return lines


def load_answers(raw_dir):
    for f in raw_dir.glob("*.json"):
        if "選擇題答案" in f.name:
            text = json.loads(f.read_text(encoding="utf-8"))["pages"][0]["text"]
            answers = {}
            for m in re.finditer(r"(\d+)\s+([A-J／]+)", text):
                answers[int(m.group(1))] = m.group(2)
            return answers
    raise FileNotFoundError("選擇題答案")


OPT_SPLIT = re.compile(r"\(([A-J])\)")


def parse_options(text):
    parts = OPT_SPLIT.split(text)
    stem = parts[0].strip()
    options = {}
    for i in range(1, len(parts) - 1, 2):
        options[parts[i]] = parts[i + 1].strip()
    return stem, options


def idx(lines, substr, start=0):
    for i in range(start, len(lines)):
        if substr in lines[i]:
            return i
    raise ValueError("找不到標記：" + substr)


def join(lines, a, b):
    return " ".join(x.strip() for x in lines[a:b]).strip()


def collect_explicit_questions(lines, a, b):
    qs, cur, buf = {}, None, []
    for ln in lines[a:b]:
        m = re.match(r"^(\d+)\.\s*(.*)$", ln)
        if m:
            if cur is not None:
                qs[cur] = " ".join(buf).strip()
            cur, buf = int(m.group(1)), [m.group(2)]
        elif cur is not None:
            buf.append(ln.strip())
    if cur is not None:
        qs[cur] = " ".join(buf).strip()
    return qs


def mark_blanks(passage, nums):
    for n in nums:
        new, count = re.subn(r"(?<=\s)" + str(n) + r"(?=\s)", "{{%d}}" % n, passage, count=1)
        if count != 1:
            new, count = re.subn(r"(?<![\d,.])" + str(n) + r"(?![\d,.%])", "{{%d}}" % n, passage, count=1)
            if count != 1:
                review_flags.append({"位置": "文章空格標記", "題號": n,
                                     "原因": "找不到唯一對應空格編號 %d，請人工確認" % n})
        passage = new
    return passage


def crop(pdf_path, img_dir, page_index, rect, out_name):
    img_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    pix = doc[page_index].get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72), clip=fitz.Rect(*rect))
    pix.save(str(img_dir / out_name))
    doc.close()


def build(year):
    cfg = CONFIG[year]
    raw_dir = ROOT / "data" / "raw-extract" / ("%s學年度" % year) / "英文"
    pdf_dir = ROOT / "資料" / "大考中心官方PDF" / ("%s學年度" % year) / "英文"
    question_pdf = next(p for p in pdf_dir.glob("*.pdf") if "試題內容" in p.name)
    answer_pdf = next(p for p in pdf_dir.glob("*.pdf") if "選擇題答案" in p.name or "選擇(填)題答案" in p.name)
    out_json = ROOT / "data" / "questions" / ("%s學年度" % year) / "英文" / "questions.json"
    out_bank = ROOT / "src" / "question-bank" / ("%s-english.js" % year)
    img_dir = ROOT / "public" / "images" / ("%s學年度" % year) / "英文"
    img_web = "images/%s學年度/英文" % year

    meta = None
    for f in raw_dir.glob("*.json"):
        if "試題內容" in f.name:
            meta = json.loads(f.read_text(encoding="utf-8"))
    lines = clean_lines(meta, "%s年學測" % year if False else "英文考科")
    ans = load_answers(raw_dir)

    題組, 單題, 未納入互動 = [], [], []
    img_no = cfg["image_q"]["no"]

    def do_crops():
        names = {}
        for k, rect in cfg["image_q"]["crops"].items():
            fn = "q%d_%s.png" % (img_no, k)
            crop(question_pdf, img_dir, cfg["image_q"]["page"], rect, fn)
            names[k] = "%s/%s" % (img_web, fn)
        return names

    # 一、詞彙題 1-10
    i0 = idx(lines, "1. ")
    i1 = idx(lines, "二 、 綜 合 測 驗")
    vocab = collect_explicit_questions(lines, i0, i1)
    for n in range(1, 11):
        stem, options = parse_options(vocab[n])
        單題.append({"題號": n, "題型": "詞彙題", "作答模式": "單選",
                    "題幹文字": stem, "選項": options, "答案": ans[n]})

    # 二、綜合測驗 11-15 / 16-20
    for lo, hi, pstart, ostart, nextmark in [
        (11, 15, "第11至15題為題組", "11. (A)", "第16至20題為題組"),
        (16, 20, "第16至20題為題組", "16. (A)", "三 、 文 意 選 填"),
    ]:
        ps = idx(lines, pstart) + 1
        pe = idx(lines, ostart)
        passage = mark_blanks(join(lines, ps, pe), list(range(lo, hi + 1)))
        qs = collect_explicit_questions(lines, pe, idx(lines, nextmark))
        題目 = []
        for n in range(lo, hi + 1):
            _, options = parse_options(qs[n])
            題目.append({"題號": n, "作答模式": "單選", "題幹文字": "第 %d 格" % n,
                        "選項": options, "答案": ans[n]})
        題組.append({"題組ID": "%s-英文-%d-%d" % (year, lo, hi), "題型": "綜合測驗",
                    "題號範圍": [lo, hi],
                    "共用資料": {"類型": "passage", "內容": passage, "處理方式": "純文字，空格以 {{題號}} 標記"},
                    "題目": 題目})

    # 三、文意選填 21-30
    ps = idx(lines, "第21至30題為題組") + 1
    bank1 = idx(lines, "(A) ", ps)
    passage = mark_blanks(join(lines, ps, bank1), list(range(21, 31)))
    bank_text = join(lines, bank1, idx(lines, "四 、 篇 章 結 構"))
    _, word_bank = parse_options(bank_text)
    題組.append({"題組ID": "%s-英文-21-30" % year, "題型": "文意選填", "題號範圍": [21, 30],
                "共用資料": {"類型": "passage+wordbank", "文章": passage, "字庫": word_bank,
                           "處理方式": "文章空格以 {{題號}} 標記，字庫為全題組共用選項"},
                "題目": [{"題號": n, "作答模式": "單選(共用字庫)", "題幹文字": "第 %d 格" % n, "答案": ans[n]}
                        for n in range(21, 31)]})

    # 四、篇章結構 31-34
    ps = idx(lines, "第31至34題為題組") + 1
    sent1 = idx(lines, "(A) ", ps)
    passage = mark_blanks(join(lines, ps, sent1), list(range(31, 35)))
    sent_text = join(lines, sent1, idx(lines, "五 、 閱 讀 測 驗"))
    _, sentence_bank = parse_options(sent_text)
    題組.append({"題組ID": "%s-英文-31-34" % year, "題型": "篇章結構", "題號範圍": [31, 34],
                "共用資料": {"類型": "passage+sentencebank", "文章": passage, "句庫": sentence_bank,
                           "處理方式": "文章空格以 {{題號}} 標記，句庫為全題組共用選項"},
                "題目": [{"題號": n, "作答模式": "單選(共用句庫)", "題幹文字": "第 %d 空格" % n, "答案": ans[n]}
                        for n in range(31, 35)]})

    # 五、閱讀測驗 35-38 / 39-42 / 43-46
    reading = [
        (35, 38, "第35至38題為題組", "第39至42題為題組"),
        (39, 42, "第39至42題為題組", "第43至46題為題組"),
        (43, 46, "第43至46題為題組", "第 貳 部 分"),
    ]
    img_crops = None
    for lo, hi, pstart, nextmark in reading:
        ps = idx(lines, pstart) + 1
        pe = idx(lines, "%d. " % lo, ps)
        passage = join(lines, ps, pe)
        qs = collect_explicit_questions(lines, pe, idx(lines, nextmark))
        題目 = []
        for n in range(lo, hi + 1):
            stem, options = parse_options(qs[n])
            q = {"題號": n, "作答模式": "單選", "題幹文字": stem, "選項": options, "答案": ans[n]}
            if n == img_no:
                if img_crops is None:
                    img_crops = do_crops()
                q["選項"] = {k: "" for k in "ABCD"}
                q["選項圖片"] = img_crops
                q["備註"] = "看圖選項，四張圖裁自官方 PDF"
            題目.append(q)
        題組.append({"題組ID": "%s-英文-%d-%d" % (year, lo, hi), "題型": "閱讀測驗",
                    "題號範圍": [lo, hi],
                    "共用資料": {"類型": "passage", "內容": passage}, "題目": 題目})

    # 第貳部分 混合題 47-50（49 互動；47/48、50 為手寫題，列出不作答）
    build_mixed(year, cfg, lines, ans, question_pdf, img_dir, img_web, 題組, 未納入互動)

    # 第參部分 非選擇題（中譯英＋英文作文）：手寫題，列出題目不作答
    build_part3(year, lines, meta, question_pdf, img_dir, img_web, 題組)

    interactive = [q["題號"] for g in 題組 for q in g["題目"] if q.get("作答模式") != "手寫"] + [q["題號"] for q in 單題]
    handwritten = [q.get("標籤") or ("第 %s 題" % q["題號"]) for g in 題組 for q in g["題目"] if q.get("作答模式") == "手寫"]
    for n in interactive:
        if n not in ans:
            review_flags.append({"題號": n, "原因": "找不到官方答案"})

    result = {
        "科目": "英文", "年度": year,
        "來源": {"試題": str(question_pdf.relative_to(ROOT)), "答案": str(answer_pdf.relative_to(ROOT))},
        "說明": "本題庫題目、選項、文章與答案均取自官方 PDF，未改寫或補完。空格以 {{題號}} 標記。",
        "統計": {"互動題數": len(interactive), "題組數": len(題組), "單題數": len(單題),
                "手寫題數": len(handwritten)},
        "手寫題清單": handwritten,
        "題組": 題組, "單題": 單題, "review_flags": review_flags,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    emit_app_bank(year, result, out_bank)

    print("=== %s 英文 ===" % year)
    print("已輸出：", out_json.relative_to(ROOT))
    print("已輸出：", out_bank.relative_to(ROOT))
    print("互動題數 %d（單題 %d + 題組 %d），題組 %d" % (
        len(interactive), len(單題), len(interactive) - len(單題), len(題組)))
    print("手寫題 %d：%s" % (len(handwritten), "、".join(handwritten)))
    print("review_flags：%d 筆" % len(review_flags))
    for f in review_flags:
        print("  -", f)
    return result


def build_mixed(year, cfg, lines, ans, question_pdf, img_dir, img_web, 題組, 未納入互動):
    marker = idx(lines, "第47至50題為題組")
    q49_start = next(i for i in range(marker, len(lines)) if lines[i].strip().startswith("49."))
    q50_start = next(i for i in range(q49_start, len(lines)) if lines[i].strip().startswith("50."))
    q49_stem = re.sub(r"^\d+\.\s*", "", lines[q49_start]).strip()
    ans49 = [c for c in ans[49] if c.isalpha()]

    if cfg["mixed"]["style"] == "image":
        src = crop_mixed_image(cfg, question_pdf, img_dir, img_web)
        review_flags.append({"位置": "第47-50題共用文章", "題號": "47-50",
                             "原因": "官方為左右雙欄版面，文字抽取交錯無法可靠重建；依規範第5點改用官方 PDF 裁圖，請人工複核。"})
        # 113 型：Q49 選項自列於題下（(A)-(F)）
        _, opts = parse_options(join(lines, q49_start + 1, q50_start))
        q49_entry = {"題號": 49, "作答模式": "多選", "題幹文字": q49_stem, "選項": opts, "答案": ans[49],
                    "備註": "多選題"}
        共用 = {"類型": "image", "內容": src, "處理方式": "雙欄版面無法可靠重建，裁官方 PDF 區域為圖"}
    elif cfg["mixed"]["style"] == "forum":
        # 114 型：單欄論壇，共用文章為文字；Q49 從論壇 (A)-(J) 貼文中複選
        forum = join(lines, marker + 1, idx(lines, "47-48", marker))
        choices = sorted(set(re.findall(r"(?m)^([A-J])\.\s", forum)))
        if not choices:
            choices = list("ABCDEFGHIJ")
        q49_entry = {"題號": 49, "作答模式": "多選", "題幹文字": q49_stem, "choices": choices, "答案": ans[49],
                    "備註": "多選題，選項為上方論壇 A–J 各則貼文"}
        共用 = {"類型": "passage", "內容": forum, "處理方式": "單欄論壇，共用文章為文字；Q49 從論壇各則複選"}
    else:
        # 115 型：店家介紹為文字，官方地圖為共用局部圖；Q49 從 A-F 店家複選
        map_src = crop_mixed_map(cfg, question_pdf, img_dir, img_web)
        forum = join(lines, marker + 1, idx(lines, "47-48", marker))
        choices = sorted(set(re.findall(r"(?m)^([A-F])\.\s", forum)))
        if not choices:
            choices = list("ABCDEF")
        q49_entry = {"題號": 49, "作答模式": "多選", "題幹文字": q49_stem, "choices": choices, "答案": ans[49],
                    "備註": "多選題，選項為上方店家 A–F 各則介紹"}
        共用 = {"類型": "passage-image", "文章": forum, "圖片": map_src,
              "處理方式": "店家介紹文字化；官方店家地圖裁為題組共用圖"}

    # 47/48（填充）與 50（簡答）為手寫題：列出題目，不作答
    part3_i = idx(lines, "第 參 部 分")
    t4748 = join(lines, idx(lines, "47-48", marker), q49_start)
    t50 = join(lines, q50_start, part3_i)
    題目 = [
        {"題號": 47, "作答模式": "手寫", "標籤": "第 47–48 題（填充）", "題幹文字": t4748},
        q49_entry,
        {"題號": 50, "作答模式": "手寫", "標籤": "第 50 題（簡答）", "題幹文字": t50},
    ]

    題組.append({"題組ID": "%s-英文-47-50" % year, "題型": "混合題", "題號範圍": [47, 50],
                "共用資料": 共用, "題目": 題目})


def build_part3(year, lines, meta, question_pdf, img_dir, img_web, 題組):
    """第參部分：中譯英＋英文作文，做成手寫題（列出題目，不作答）。"""
    p3 = idx(lines, "第 參 部 分")
    trans_i = idx(lines, "中 譯 英", p3)
    essay_i = idx(lines, "英 文 作 文", p3)
    trans_text = join(lines, trans_i, essay_i)
    essay_text = join(lines, essay_i, len(lines))

    題目 = [
        {"題號": 51, "作答模式": "手寫", "標籤": "一、中譯英（第 1–2 題）", "題幹文字": trans_text},
    ]
    essay = {"題號": 52, "作答模式": "手寫", "標籤": "二、英文作文", "題幹文字": essay_text}

    # 作文若有附圖（如 113 的三張情境圖），把最後一頁圖片區域裁下來一併列出
    last_page = meta["meta"]["pageCount"]
    imgs = [im for im in meta["images"] if im["page"] == last_page]
    if imgs:
        x0 = min(im["bbox"][0] for im in imgs) - 8
        y0 = min(im["bbox"][1] for im in imgs) - 8
        x1 = max(im["bbox"][2] for im in imgs) + 8
        y1 = max(im["bbox"][3] for im in imgs) + 28  # 含圖下方文字標題
        fn = "part3_essay_figures.png"
        crop(question_pdf, img_dir, last_page - 1, (x0, y0, x1, y1), fn)
        essay["圖片"] = "%s/%s" % (img_web, fn)
    題目.append(essay)

    題組.append({"題組ID": "%s-英文-第參部分" % year, "題型": "非選擇題(手寫)",
                "題號範圍": [51, 52], "共用資料": None, "題目": 題目})


def crop_mixed_image(cfg, question_pdf, img_dir, img_web):
    fn = "group_47_50_passage.png"
    crop(question_pdf, img_dir, cfg["mixed"]["page"], cfg["mixed"]["rect"], fn)
    return "%s/%s" % (img_web, fn)


def crop_mixed_map(cfg, question_pdf, img_dir, img_web):
    fn = "group_47_50_map.png"
    crop(question_pdf, img_dir, cfg["mixed"]["page"], cfg["mixed"]["map_rect"], fn)
    return "%s/%s" % (img_web, fn)


def emit_app_bank(year, result, out_bank):
    def web_img(p):
        return "public/" + p if not p.startswith("public/") else p

    def qid(no):
        return "english-%s-q%d" % (year, no)

    blocks, flat = [], []

    def add(q):
        flat.append(q)
        return q

    vocab_qs = []
    for item in result["單題"]:
        no = item["題號"]
        vocab_qs.append(add({"id": qid(no), "no": no, "type": "single", "stem": item["題幹文字"],
                             "choices": sorted(item["選項"].keys()), "options": item["選項"], "answer": item["答案"]}))
    blocks.append({"type": "group", "title": "一、詞彙題（第 1–10 題）", "shared": None, "questions": vocab_qs})

    seq = {"綜合測驗": "二", "文意選填": "三", "篇章結構": "四", "閱讀測驗": "五", "混合題": "第貳部分"}
    for g in result["題組"]:
        lo, hi = g["題號範圍"]
        gtype, s = g["題型"], g["共用資料"]
        shared = None
        if s is None:
            pass
        elif s["類型"] == "passage":
            shared = {"kind": "passage", "text": s["內容"]}
        elif s["類型"] == "passage+wordbank":
            shared = {"kind": "passage-bank", "text": s["文章"], "bankLabel": "字庫", "bank": s["字庫"]}
        elif s["類型"] == "passage+sentencebank":
            shared = {"kind": "passage-bank", "text": s["文章"], "bankLabel": "句庫", "bank": s["句庫"]}
        elif s["類型"] == "image":
            shared = {"kind": "image", "src": web_img(s["內容"])}
        elif s["類型"] == "passage-image":
            shared = {"kind": "passage-image", "text": s["文章"], "src": web_img(s["圖片"])}

        qs = []
        for q in g["題目"]:
            no = q["題號"]
            if q.get("作答模式") == "手寫":
                entry = {"id": "english-%s-hw-%s" % (year, no), "no": no, "type": "handwritten",
                         "label": q.get("標籤"), "stem": q.get("題幹文字", "")}
                if q.get("圖片"):
                    entry["image"] = web_img(q["圖片"])
                qs.append(add(entry))
                continue
            multi = q.get("作答模式") == "多選"
            entry = {"id": qid(no), "no": no, "type": "multiple" if multi else "single", "stem": q["題幹文字"]}
            if q.get("選項圖片"):
                entry["choices"] = sorted(q["選項圖片"].keys())
                entry["optionImages"] = {k: web_img(v) for k, v in q["選項圖片"].items()}
            elif ("選項" not in q) and ("choices" in q):
                entry["choices"] = q["choices"]   # 選項內容在共用文章（如論壇），只存字母
            elif ("選項" not in q) and shared and shared["kind"] == "passage-bank":
                entry["choices"] = sorted(shared["bank"].keys())
                entry["useBank"] = True
            else:
                entry["choices"] = sorted(q["選項"].keys())
                entry["options"] = q["選項"]
            entry["answer"] = [c for c in q["答案"] if c.isalpha()] if multi else q["答案"]
            qs.append(add(entry))

        if gtype == "非選擇題(手寫)":
            title = "第參部分 非選擇題（手寫題・不需作答）"
        elif gtype == "混合題":
            title = "第貳部分 混合題（第 %d–%d 題；47/48、50 為手寫題）" % (lo, hi)
        else:
            prefix = seq.get(gtype, "")
            title = ("%s、%s（第 %d–%d 題）" % (prefix, gtype, lo, hi)) if prefix in ("二", "三", "四", "五") \
                else ("%s %s（第 %d–%d 題）" % (prefix, gtype, lo, hi))
        blocks.append({"type": "group", "title": title, "shared": shared, "questions": qs})

    bank = {"id": "english-%s-answer-card" % year, "subject": "英文", "year": year,
            "category": "答題卡練習", "title": "%s 年英文答題卡練習" % year, "status": "官方 PDF 提取題庫",
            "source": result["來源"],
            "note": "收錄 %s 學測英文：可作答選擇題 %d 題＋手寫題 %d 題（填充、簡答、中譯英、作文，僅列出不作答）。題目/選項/文章/答案均取自官方 PDF。" % (
                year, result["統計"]["互動題數"], result["統計"]["手寫題數"]),
            "questions": flat, "blocks": blocks}

    out_bank.parent.mkdir(parents=True, exist_ok=True)
    header = "// 由 tools/build_english.py 自動產生，請勿手改。題目與答案取自官方 PDF，未經改寫。\n"
    out_bank.write_text(header + "QUESTION_BANKS.push(\n" + json.dumps(bank, ensure_ascii=False, indent=2) + "\n);\n",
                        encoding="utf-8")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CONFIG:
        print("用法：python tools/build_english.py <年度>，目前支援：", ", ".join(CONFIG))
        sys.exit(1)
    global review_flags
    review_flags = []
    build(sys.argv[1])


if __name__ == "__main__":
    main()
