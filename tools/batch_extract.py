#!/usr/bin/env python3
"""
batch_extract.py — 純腳本階段：把大考中心官方 PDF 批次轉成輕量「中繼檔」。

原則（見 docs/圖文混合題庫解析規範.md）：
- 不做任何 AI 判斷、不做題目拆解，只忠實抽取版面資料。
- 純文字（依頁分段）：pdfplumber
- 表格結構 + 座標：pdfplumber find_tables / extract
- 圖片座標清單：PyMuPDF（只記座標，不裁圖）
- 國寫科目：只抽純文字（供瀏覽），不做表格/圖片分析
- 任何讀取失敗或內容異常記到 extract-errors.json，不猜測、不默默跳過。

用法：
    # 只跑某年度某科目（小範圍測試）
    python tools/batch_extract.py --year 113 --subject 英文

    # 跑全部
    python tools/batch_extract.py --all
"""
import argparse
import json
import re
import traceback
from datetime import datetime
from pathlib import Path

import pdfplumber
import fitz  # PyMuPDF

EXTRACTOR_VERSION = "batch_extract.py v1"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_ROOT = PROJECT_ROOT / "資料" / "大考中心官方PDF"
OUT_ROOT = PROJECT_ROOT / "data" / "raw-extract"
ERROR_FILE = OUT_ROOT / "extract-errors.json"

# 只抽純文字、不做表格/圖片分析的科目
TEXT_ONLY_SUBJECTS = {"國寫"}

# 檔名類型關鍵字（順序有意義，先比對較長的字串）
FILE_TYPE_KEYWORDS = [
    "非選擇題評分原則",
    "選擇(填)題答案",
    "選擇題答案",
    "試題內容",
    "答題卷",
]


def detect_file_type(file_name: str) -> str:
    for kw in FILE_TYPE_KEYWORDS:
        if kw in file_name:
            return kw
    return "其他"


def round_bbox(values):
    return [round(v, 3) for v in values]


def looks_garbled(text: str) -> bool:
    """粗略偵測亂碼：出現 Unicode 取代字元，或幾乎沒有可見字元。"""
    if not text:
        return False
    if "�" in text:
        return True
    return False


def extract_text_pages(pdf):
    """依頁抽取純文字，回傳 (pages, warnings)。"""
    pages = []
    warnings = []
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        pages.append({
            "page": i,
            "width": round(page.width, 3),
            "height": round(page.height, 3),
            "text": text,
            "charCount": len(text),
        })
        if not text:
            warnings.append(f"第 {i} 頁抽取到空白文字（可能是純圖片頁或掃描頁）")
        elif looks_garbled(text):
            warnings.append(f"第 {i} 頁疑似亂碼（含取代字元 \\ufffd）")
    return pages, warnings


def extract_tables(pdf):
    """依頁抽取表格結構與座標，回傳 (tables, warnings)。"""
    tables = []
    warnings = []
    for i, page in enumerate(pdf.pages, start=1):
        try:
            found = page.find_tables()
        except Exception as exc:  # pragma: no cover - 防禦性
            warnings.append(f"第 {i} 頁表格辨識失敗：{exc}")
            continue
        for t_index, table in enumerate(found):
            try:
                cells = table.extract()
            except Exception as exc:  # pragma: no cover
                warnings.append(f"第 {i} 頁第 {t_index} 個表格內容抽取失敗：{exc}")
                cells = None
            row_count = len(cells) if cells else 0
            col_count = max((len(r) for r in cells), default=0) if cells else 0
            tables.append({
                "page": i,
                "tableIndex": t_index,
                "bbox": round_bbox(table.bbox),
                "rowCount": row_count,
                "colCount": col_count,
                "cells": cells,
            })
            if cells is None:
                warnings.append(f"第 {i} 頁第 {t_index} 個表格辨識到框線但抽不到內容，需人工檢查")
    return tables, warnings


def extract_image_coords(pdf_path: Path):
    """用 PyMuPDF 抽取每頁圖片座標清單（只記座標，不裁圖）。"""
    images = []
    warnings = []
    doc = fitz.open(pdf_path)
    try:
        for page_index in range(len(doc)):
            page = doc[page_index]
            page_no = page_index + 1
            seen = set()
            for image_index, image in enumerate(page.get_images(full=True), start=1):
                xref = image[0]
                rects = page.get_image_rects(xref)
                if not rects:
                    continue
                info = doc.extract_image(xref)
                ext = info.get("ext", "")
                for rect_index, rect in enumerate(rects, start=1):
                    bbox = round_bbox([rect.x0, rect.y0, rect.x1, rect.y1])
                    key = (xref, tuple(bbox))
                    if key in seen:
                        continue
                    seen.add(key)
                    images.append({
                        "page": page_no,
                        "imageIndex": image_index,
                        "rectIndex": rect_index,
                        "xref": xref,
                        "bbox": bbox,
                        "pixelWidth": info.get("width"),
                        "pixelHeight": info.get("height"),
                        "ext": ext,
                    })
    finally:
        doc.close()
    return images, warnings


def extract_one_pdf(pdf_path: Path, year: str, subject: str):
    """抽取單一 PDF，回傳中繼檔 dict。"""
    file_name = pdf_path.name
    text_only = subject in TEXT_ONLY_SUBJECTS

    result = {
        "source": {
            "path": str(pdf_path.relative_to(PROJECT_ROOT)),
            "year": year,
            "subject": subject,
            "fileName": file_name,
            "fileType": detect_file_type(file_name),
        },
        "meta": {
            "extractor": EXTRACTOR_VERSION,
            "extractedAt": datetime.now().isoformat(timespec="seconds"),
            "mode": "text-only" if text_only else "full",
            "pageCount": 0,
        },
        "pages": [],
        "tables": [],
        "images": [],
        "warnings": [],
    }

    with pdfplumber.open(pdf_path) as pdf:
        result["meta"]["pageCount"] = len(pdf.pages)
        pages, page_warn = extract_text_pages(pdf)
        result["pages"] = pages
        result["warnings"].extend(page_warn)

        if not text_only:
            tables, table_warn = extract_tables(pdf)
            result["tables"] = tables
            result["warnings"].extend(table_warn)

    if not text_only:
        images, image_warn = extract_image_coords(pdf_path)
        result["images"] = images
        result["warnings"].extend(image_warn)

    return result


def collect_pdfs(year_filter=None, subject_filter=None):
    """回傳 (year, subject, pdf_path) 清單。"""
    items = []
    if not PDF_ROOT.exists():
        raise FileNotFoundError(f"找不到 PDF 根目錄：{PDF_ROOT}")
    for year_dir in sorted(PDF_ROOT.iterdir()):
        if not year_dir.is_dir():
            continue
        year = year_dir.name.replace("學年度", "")
        if year_filter and year != year_filter:
            continue
        for subject_dir in sorted(year_dir.iterdir()):
            if not subject_dir.is_dir():
                continue
            subject = subject_dir.name
            if subject_filter and subject != subject_filter:
                continue
            for pdf_path in sorted(subject_dir.glob("*.pdf")):
                items.append((year, subject, pdf_path))
    return items


def out_path_for(year: str, subject: str, pdf_path: Path) -> Path:
    return OUT_ROOT / f"{year}學年度" / subject / (pdf_path.stem + ".json")


def run(year_filter=None, subject_filter=None):
    pdfs = collect_pdfs(year_filter, subject_filter)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    ok, failed = 0, 0
    errors = []
    need_review = []  # 有 warnings、建議人工看的檔案

    print(f"準備處理 {len(pdfs)} 個 PDF ...\n")
    for year, subject, pdf_path in pdfs:
        rel = pdf_path.relative_to(PROJECT_ROOT)
        try:
            result = extract_one_pdf(pdf_path, year, subject)
        except Exception as exc:
            failed += 1
            errors.append({
                "file": str(rel),
                "year": year,
                "subject": subject,
                "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc(),
            })
            print(f"  ✗ 失敗 {rel} — {type(exc).__name__}: {exc}")
            continue

        out_path = out_path_for(year, subject, pdf_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        ok += 1

        warn_n = len(result["warnings"])
        flag = f"  ⚠ {warn_n} 個提醒" if warn_n else ""
        print(
            f"  ✓ {rel}  "
            f"[{result['meta']['pageCount']}頁 / 表{len(result['tables'])} / 圖{len(result['images'])}]{flag}"
        )
        if warn_n:
            need_review.append({
                "file": str(rel),
                "output": str(out_path.relative_to(PROJECT_ROOT)),
                "warnings": result["warnings"],
            })

    # 寫入錯誤檔（含需人工檢查清單）
    ERROR_FILE.write_text(
        json.dumps(
            {
                "generatedAt": datetime.now().isoformat(timespec="seconds"),
                "scope": {"year": year_filter, "subject": subject_filter},
                "summary": {"total": len(pdfs), "ok": ok, "failed": failed},
                "readFailures": errors,
                "needManualReview": need_review,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\n=== 完成 ===")
    print(f"總共 {len(pdfs)} 個，成功 {ok}，失敗 {failed}")
    print(f"需人工檢查（有提醒）：{len(need_review)} 個")
    print(f"錯誤/提醒清單：{ERROR_FILE.relative_to(PROJECT_ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="批次把官方 PDF 轉成輕量中繼檔（純腳本，不做 AI 判斷）")
    parser.add_argument("--year", help="只跑某年度，例如 113")
    parser.add_argument("--subject", help="只跑某科目，例如 英文")
    parser.add_argument("--all", action="store_true", help="跑全部年度與科目")
    args = parser.parse_args()

    if not args.all and not args.year and not args.subject:
        parser.error("請指定範圍：--year / --subject，或用 --all 跑全部")

    run(year_filter=args.year, subject_filter=args.subject)


if __name__ == "__main__":
    main()
