#!/usr/bin/env python3
"""build_crop_studio.py — 產生「人機協同裁圖台」的資料檔。

給一份試題 PDF（＋對應中繼檔），本腳本會：
  1. 用 PyMuPDF 把每頁渲染成高清 PNG（主圖）與縮圖。
  2. 讀中繼檔（batch_extract.py 產物），整理每頁的純文字、偵測到的表格/圖片座標。
  3. 自動判斷「規則頁」：頁面文字沒有「第X頁/共Y頁」標記者，預設標記為不需製作。
  4. 把以上寫成 tools/裁圖台/data.js，供 index.html 載入。

原則（見 CLAUDE.md／docs/圖文混合題庫解析規範.md）：
  - 不做任何 AI 判斷、不改來源，只忠實渲染與搬運。
  - 輸出的頁面圖屬「完整試卷內容」，僅供本機裁圖使用，不進公開 repo
    （pages/ thumbs/ data.js 已於 .gitignore 排除）。

用法：
    python tools/build_crop_studio.py \
        --pdf "資料/大考中心官方PDF/115學年度/國綜/115學測-國綜-試題內容-01-115學測國綜試卷.pdf" \
        --extract "data/raw-extract/115學年度/國綜/115學測-國綜-試題內容-01-115學測國綜試卷.json" \
        --year 115 --subject 國文 --dpi 300

若 --pdf 給的是相對路徑，會先在本 worktree 找，找不到再往主 repo（上兩層的 學測歷屆考題）找。
"""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import fitz  # PyMuPDF

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOOL_DIR = PROJECT_ROOT / "tools" / "裁圖台"
PAGES_DIR = TOOL_DIR / "pages"
THUMBS_DIR = TOOL_DIR / "thumbs"
DATA_FILE = TOOL_DIR / "data.js"

PAGE_MARK_RE = re.compile(r"第\s*(\d+)\s*頁")
THUMB_WIDTH = 200  # 縮圖寬度（px）


def resolve_pdf(raw: str) -> Path:
    """先在本 worktree 找；找不到再往主 repo 找（來源 PDF 常只在主工作區）。"""
    p = Path(raw)
    if p.is_absolute() and p.exists():
        return p
    here = PROJECT_ROOT / raw
    if here.exists():
        return here
    # 主 repo：worktree 位於 <repo>/.claude/worktrees/<name>，往上找同名相對路徑
    for parent in PROJECT_ROOT.parents:
        candidate = parent / raw
        if candidate.exists() and "worktrees" not in str(candidate):
            return candidate
    raise FileNotFoundError(f"找不到 PDF：{raw}（本 worktree 與主 repo 都沒有）")


def render_pages(pdf_path: Path, dpi: int):
    doc = fitz.open(pdf_path)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    THUMBS_DIR.mkdir(parents=True, exist_ok=True)
    # 清掉舊圖，避免換考卷時殘留
    for old in list(PAGES_DIR.glob("*.png")) + list(THUMBS_DIR.glob("*.png")):
        old.unlink()

    zoom = dpi / 72
    pages = []
    for i in range(len(doc)):
        page = doc[i]
        pm = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        name = f"page-{i + 1:02d}.png"
        pm.save(PAGES_DIR / name)

        tzoom = THUMB_WIDTH / pm.width * zoom
        tpm = page.get_pixmap(matrix=fitz.Matrix(tzoom, tzoom), alpha=False)
        tpm.save(THUMBS_DIR / name)

        pages.append({
            "pdfPage": i + 1,
            "img": f"pages/{name}",
            "thumb": f"thumbs/{name}",
            "width": pm.width,
            "height": pm.height,
            "pdfWidth": round(page.rect.width, 3),
            "pdfHeight": round(page.rect.height, 3),
            "fitzText": page.get_text(),  # 無官方中繼檔時，中間欄改用這份文字
        })
    doc.close()
    return pages


def load_extract(extract_path: Path):
    """讀中繼檔，回傳每頁的文字與偵測到的表格/圖片（座標為 PDF points）。"""
    data = json.loads(extract_path.read_text(encoding="utf-8"))
    text_by, tables_by, images_by = {}, {}, {}
    for p in data.get("pages", []):
        text_by[p["page"]] = p.get("text", "")
    for t in data.get("tables", []):
        tables_by.setdefault(t["page"], []).append({
            "bbox": t.get("bbox"), "rows": t.get("rowCount"), "cols": t.get("colCount"),
        })
    for im in data.get("images", []):
        images_by.setdefault(im["page"], []).append({
            "bbox": im.get("bbox"), "w": im.get("pixelWidth"), "h": im.get("pixelHeight"),
        })
    return text_by, tables_by, images_by


def paper_page_of(text: str):
    """從頁面文字抓印在紙上的頁碼（第X頁）；抓不到代表可能是規則頁/封面。"""
    m = PAGE_MARK_RE.search(text or "")
    return int(m.group(1)) if m else None


def build(pdf_path: Path, extract_path: Path, year: str, subject: str, dpi: int):
    pages = render_pages(pdf_path, dpi)

    text_by, tables_by, images_by = ({}, {}, {})
    if extract_path is not None:
        text_by, tables_by, images_by = load_extract(extract_path)

    for pg in pages:
        n = pg["pdfPage"]
        text = text_by.get(n, "") or pg.get("fitzText", "")
        paper = paper_page_of(text)
        pg["paperPage"] = paper           # 印在紙上的頁碼（可能 None）
        pg["isRule"] = paper is None      # 預設：抓不到頁碼 => 規則頁，跳過
        pg["text"] = text
        pg["tables"] = tables_by.get(n, [])
        pg["images"] = images_by.get(n, [])
        # 座標換算比例：中繼檔 bbox 是 PDF points，乘這個比例得到主圖像素座標
        pg["ptToPx"] = round(pg["width"] / pg["pdfWidth"], 5) if pg.get("pdfWidth") else dpi / 72
        pg.pop("fitzText", None)  # 已併進 text，不重複寫進 data.js

    payload = {
        "meta": {
            "year": year,
            "subject": subject,
            "dpi": dpi,
            "pdf": pdf_path.name,
            "generatedAt": datetime.now().isoformat(timespec="seconds"),
            "pageCount": len(pages),
        },
        "pages": pages,
    }

    DATA_FILE.write_text(
        "// 由 build_crop_studio.py 自動產生，內容為完整試卷頁面資料，勿提交公開 repo。\n"
        "window.CROP_STUDIO_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    rule_pages = [p["pdfPage"] for p in pages if p["isRule"]]
    print("=== 裁圖台資料已產生 ===")
    print(f"考卷：{year} {subject}  來源：{pdf_path.name}")
    print(f"頁數：{len(pages)}（{dpi}dpi）")
    print(f"自動判定規則頁（預設跳過）：第 {rule_pages} 頁 PDF" if rule_pages else "未偵測到規則頁")
    print(f"資料檔：{DATA_FILE.relative_to(PROJECT_ROOT)}")
    print(f"開啟工具：tools/裁圖台/index.html")


def main():
    ap = argparse.ArgumentParser(description="產生人機協同裁圖台資料檔")
    ap.add_argument("--pdf", required=True, help="試題內容 PDF 路徑")
    ap.add_argument("--extract", help="對應中繼檔 JSON（batch_extract.py 產物），可省略")
    ap.add_argument("--year", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--dpi", type=int, default=300)
    args = ap.parse_args()

    pdf_path = resolve_pdf(args.pdf)
    extract_path = None
    if args.extract:
        ep = Path(args.extract)
        extract_path = ep if ep.is_absolute() else (PROJECT_ROOT / args.extract)
        if not extract_path.exists():
            print(f"⚠ 找不到中繼檔，改為只渲染頁面、中間欄沒有解析文字：{extract_path}")
            extract_path = None

    build(pdf_path, extract_path, args.year, args.subject, args.dpi)


if __name__ == "__main__":
    main()
