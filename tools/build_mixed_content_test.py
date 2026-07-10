#!/usr/bin/env python3
import html
import json
import re
from pathlib import Path

import fitz
import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "資料/大考中心官方PDF/115學年度/國綜/115學測-國綜-試題內容-01-115學測國綜試卷.pdf"
OUTPUT_DIR = ROOT / "data/mixed-content-test/L03"
IMAGE_DIR = ROOT / "public/images/mixed-content-test"
LESSON = "L03"


def question_block(page_text, number, next_number):
    pattern = rf"(?ms)^{number}\.\s*(.*?)(?=^{next_number}\.\s)"
    match = re.search(pattern, page_text)
    if not match:
        raise ValueError(f"找不到第 {number} 題文字")
    return match.group(1).strip()


def final_question_block(page_text, number):
    pattern = rf"(?ms)^{number}\.\s*(.*?)(?=^\s*-\s*\d+\s*-\s*$|\Z)"
    match = re.search(pattern, page_text)
    if not match:
        raise ValueError(f"找不到第 {number} 題文字")
    return match.group(1).strip()


def detect_question_groups(page_text):
    ranges = set()
    patterns = [
        r"(\d+)\s*[-–]\s*(\d+)\s*為題組",
        r"回答\s*(\d+)\s*[-–]\s*(\d+)\s*題",
    ]
    for pattern in patterns:
        for start, end in re.findall(pattern, page_text):
            ranges.add((int(start), int(end)))
    return sorted(ranges)


def split_choices(block):
    matches = list(re.finditer(r"\(([A-D])\)", block))
    if len(matches) != 4:
        raise ValueError(f"選項數量不是 4：{block[:80]}")
    stem = block[: matches[0].start()].strip()
    choices = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        choices[match.group(1)] = " ".join(block[match.end() : end].split())
    return " ".join(stem.split()), choices


def lines_in_region(page, x0, top, x1, bottom, tolerance=3):
    words = [
        word
        for word in page.extract_words(x_tolerance=2, y_tolerance=3)
        if word["x0"] >= x0
        and word["x1"] <= x1
        and word["top"] >= top
        and word["bottom"] <= bottom
    ]
    rows = []
    for word in sorted(words, key=lambda item: (item["top"], item["x0"])):
        row = next((item for item in rows if abs(item["top"] - word["top"]) <= tolerance), None)
        if row is None:
            row = {"top": word["top"], "words": []}
            rows.append(row)
        row["words"].append(word)
    return [
        "".join(word["text"] for word in sorted(row["words"], key=lambda item: item["x0"]))
        for row in sorted(rows, key=lambda item: item["top"])
    ]


def extract_spatial_choices(lines):
    choices = {}
    active = None
    for line in lines:
        match = re.match(r"\(([A-D])\)(.*)", line)
        if match:
            active = match.group(1)
            choices[active] = match.group(2).strip()
        elif active:
            choices[active] += line.strip()
    if set(choices) != {"A", "B", "C", "D"}:
        raise ValueError(f"空間選項提取失敗：{choices}")
    return choices


def flatten_quantity_table(raw_table):
    rows = []
    category = ""
    kind = ""
    for index, raw_row in enumerate(raw_table[1:], start=1):
        col0, col1, col2, examples = [(cell or "").strip() for cell in raw_row]
        if col0:
            category = col0
        if col1:
            kind = col1
        if index == 7:
            category = "動量詞表示動作次數的單位"
        rows.append(
            {
                "量詞類別": category,
                "分類": kind,
                "細類": col2,
                "例子": examples,
            }
        )
    return rows


def table_html(headers, rows):
    head = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body = "".join(
        "<tr>"
        + "".join(
            f"<td>{html.escape(row[header]).replace(chr(10), '<br>')}</td>"
            for header in headers
        )
        + "</tr>"
        for row in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def quantity_table_html(raw_table):
    def cell(value):
        return html.escape((value or "").strip()).replace("\n", "<br>")

    header = raw_table[0]
    name_rows = raw_table[1:6]
    name_borrowed = raw_table[6]
    verb_dedicated = raw_table[7]
    verb_borrowed = raw_table[8]

    rows = [
        (
            f'<td rowspan="6">{cell(name_rows[0][0])}</td>'
            f'<td rowspan="5">{cell(name_rows[0][1])}</td>'
            f"<td>{cell(name_rows[0][2])}</td>"
            f"<td>{cell(name_rows[0][3])}</td>"
        )
    ]
    rows.extend(
        f"<td>{cell(row[2])}</td><td>{cell(row[3])}</td>"
        for row in name_rows[1:]
    )
    rows.append(
        f'<td colspan="2">{cell(name_borrowed[1])}</td>'
        f"<td>{cell(name_borrowed[3])}</td>"
    )
    rows.append(
        f'<td rowspan="2">{cell(verb_dedicated[0])}</td>'
        f'<td colspan="2">{cell(verb_dedicated[1])}</td>'
        f"<td>{cell(verb_dedicated[3])}</td>"
    )
    rows.append(
        f'<td colspan="2">{cell(verb_borrowed[1])}</td>'
        f"<td>{cell(verb_borrowed[3])}</td>"
    )

    body = "".join(f"<tr>{row}</tr>" for row in rows)
    return (
        "<table class=\"quantity-table\">"
        "<thead><tr>"
        f'<th colspan="3">{cell(header[0])}</th>'
        f"<th>{cell(header[3])}</th>"
        "</tr></thead>"
        f"<tbody>{body}</tbody></table>"
    )


def extract_portrait(document, page_number):
    page = document[page_number - 1]
    candidates = []
    for image in page.get_images(full=True):
        xref, width, height = image[0], image[2], image[3]
        ratio = width / height
        rects = page.get_image_rects(xref)
        if 0.8 <= ratio <= 1.2 and width * height < 20000 and rects:
            candidates.append((width * height, xref))
    if not candidates:
        raise ValueError("找不到第 4 題人物插圖")
    _, xref = max(candidates)
    image = document.extract_image(xref)
    output_path = IMAGE_DIR / f"{LESSON}_q4.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image["image"])
    return f"images/mixed-content-test/{output_path.name}"


def build():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    with pdfplumber.open(PDF_PATH) as pdf:
        page2 = pdf.pages[1]
        page5 = pdf.pages[4]
        page2_text = page2.extract_text(x_tolerance=2, y_tolerance=3) or ""
        page5_text = page5.extract_text(x_tolerance=2, y_tolerance=3) or ""

        q1_stem, q1_choices = split_choices(question_block(page2_text, 1, 2))
        q2_stem, q2_choices = split_choices(question_block(page2_text, 2, 3))

        q4_stem_lines = lines_in_region(page2, 80, 450, 340, 471)
        q4_option_lines = lines_in_region(page2, 80, 470, 340, 620)
        q4_reference_lines = lines_in_region(page2, 340, 450, 535, 620)
        q4_stem = "\n".join(q4_stem_lines + q4_reference_lines)
        q4_choices = extract_spatial_choices(q4_option_lines)

        tables = page5.find_tables()
        if len(tables) < 2:
            raise ValueError("第 14 題表格提取失敗")
        raw_quantity_table = tables[0].extract()
        quantity_rows = flatten_quantity_table(raw_quantity_table)
        headers = ["量詞類別", "分類", "細類", "例子"]
        q14_table = {
            "格式": "html+rows",
            "欄位": headers,
            "資料": quantity_rows,
            "HTML": quantity_table_html(raw_quantity_table),
            "來源頁面": 5,
            "來源座標": [round(value, 2) for value in tables[0].bbox],
            "處理方式": "pdfplumber.extract_tables() 後展平合併儲存格",
        }

        q14_stem_lines = lines_in_region(page5, 80, 570, 530, 592)
        q14_statements = lines_in_region(page5, 300, 590, 535, 690)
        q14_stem = "\n".join(q14_stem_lines + q14_statements)
        option_table = tables[1].extract()
        q14_choices = {
            row[0].strip("()"): f"名量詞：{row[1]}；動量詞：{row[2]}"
            for row in option_table[1:]
        }
        q15_stem, q15_choices = split_choices(final_question_block(page5_text, 15))

        group_ranges = detect_question_groups(page5_text)
        if (14, 15) not in group_ranges:
            raise ValueError("未辨識到 14-15 題組標記")

    document = fitz.open(PDF_PATH)
    q4_image = extract_portrait(document, 2)
    document.close()

    single_questions = [
        {
            "題號": 1,
            "課次": LESSON,
            "題型": "text",
            "題幹文字": q1_stem,
            "附表": None,
            "附圖": None,
            "選項": q1_choices,
        },
        {
            "題號": 2,
            "課次": LESSON,
            "題型": "text",
            "題幹文字": q2_stem,
            "附表": None,
            "附圖": None,
            "選項": q2_choices,
        },
        {
            "題號": 4,
            "課次": LESSON,
            "題型": "image",
            "題幹文字": q4_stem,
            "附表": None,
            "附圖": q4_image,
            "選項": q4_choices,
        },
    ]

    result = {
        "題組": [
            {
                "題組ID": f"{LESSON}-Q14-Q15",
                "課次": LESSON,
                "題號範圍": [14, 15],
                "共用資料": {
                    "類型": "table",
                    "內容": q14_table,
                },
                "題目": [
                    {
                        "題號": 14,
                        "題幹文字": q14_stem,
                        "選項": q14_choices,
                    },
                    {
                        "題號": 15,
                        "題幹文字": q15_stem,
                        "選項": q15_choices,
                    },
                ],
            }
        ],
        "單題": single_questions,
    }

    output_path = OUTPUT_DIR / "questions.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output_path)
    print(IMAGE_DIR / f"{LESSON}_q4.png")


if __name__ == "__main__":
    build()
