#!/usr/bin/env python3
"""apply_crop_coords.py — 把裁圖台匯出的座標 JSON 還原成實際 PNG。

裁圖台（index.html）只吐座標＋預覽；正式產圖由本腳本負責，
從已渲染的 300dpi 頁面圖（tools/裁圖台/pages/）精準裁出，確保可重現。

用法：
    python tools/apply_crop_coords.py --coords ~/Desktop/裁圖座標-115-國文.json --out <輸出資料夾>
"""
import argparse
import json
from pathlib import Path

from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = PROJECT_ROOT / "tools" / "裁圖台" / "pages"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--coords", required=True)
    ap.add_argument("--pages-dir", default=str(PAGES_DIR))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    coords = json.loads(Path(args.coords).expanduser().read_text(encoding="utf-8"))
    pages_dir = Path(args.pages_dir)
    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    done = []
    for c in coords["crops"]:
        page_png = pages_dir / f"page-{c['pdfPage']:02d}.png"
        with Image.open(page_png) as im:
            x0, y0, x1, y1 = c["box"]
            crop = im.crop((x0, y0, x1, y1))
            out_path = out_dir / c["file"]
            crop.save(out_path)
            done.append((c["file"], c["pdfPage"], c.get("paperPage"), crop.size))

    print(f"=== 已還原 {len(done)} 張裁圖 → {out_dir} ===")
    for name, pdfp, paperp, size in done:
        print(f"  {name}  PDF{pdfp}/卷{paperp}  {size[0]}×{size[1]}px")


if __name__ == "__main__":
    main()
