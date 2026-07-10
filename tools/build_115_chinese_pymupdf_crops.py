#!/usr/bin/env python3
import json
from pathlib import Path

import fitz
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "資料/大考中心官方PDF/115學年度/國綜/115學測-國綜-試題內容-01-115學測國綜試卷.pdf"
REFERENCE_PAGES = ROOT / "assets/questions/115/chinese/pages"
OUT_DIR = ROOT / "assets/questions/115/chinese/pymupdf-groups"
DPI = 300


# Coordinates are based on the already-reviewed page crop boundaries from the
# first 160dpi prototype, then converted back to PDF points for 300dpi rendering.
CROPS = [
    {"page": 2, "name": "pm-group-1-5-p02.png", "box": [45, 70, 1279, 1811], "label": "1-5 題"},
    {"page": 3, "name": "pm-group-6-8-p03.png", "box": [45, 70, 1279, 1811], "label": "6-8 題組"},
    {"page": 4, "name": "pm-group-9-10-p04.png", "box": [45, 70, 1279, 1212], "label": "9-10 題組"},
    {"page": 4, "name": "pm-group-11-13-p04.png", "box": [45, 1168, 1279, 1816], "label": "11-13 題組"},
    {"page": 5, "name": "pm-group-11-13-p05.png", "box": [45, 70, 1279, 770], "label": "11-13 題組"},
    {"page": 5, "name": "pm-group-14-15-p05.png", "box": [45, 815, 1279, 1811], "label": "14-15 題組"},
    {"page": 6, "name": "pm-group-16-18-p06.png", "box": [45, 70, 1279, 1811], "label": "16-18 題組"},
    {"page": 7, "name": "pm-group-19-21-p07.png", "box": [45, 70, 1279, 1811], "label": "19-21 題組"},
    {"page": 8, "name": "pm-group-22-25-p08.png", "box": [45, 70, 1279, 1811], "label": "22-25 題組"},
    {"page": 9, "name": "pm-group-26-29-p09.png", "box": [45, 70, 1279, 1811], "label": "26-29 題"},
    {"page": 10, "name": "pm-group-30-31-p10.png", "box": [45, 70, 1279, 1515], "label": "30-31 題組"},
    {"page": 10, "name": "pm-group-32-36-p10.png", "box": [45, 1545, 1279, 1816], "label": "32-36 題組"},
    {"page": 11, "name": "pm-group-32-36-p11.png", "box": [45, 70, 1279, 1811], "label": "32-36 題組"},
    {"page": 12, "name": "pm-group-32-36-p12.png", "box": [45, 70, 1279, 1811], "label": "32-36 題組"},
]


def reference_size(page_no):
    with Image.open(REFERENCE_PAGES / f"page-{page_no:02d}.png") as image:
        return image.size


def old_pixels_to_pdf_rect(page, ref_size, box):
    ref_width, ref_height = ref_size
    page_rect = page.rect
    x0, y0, x1, y1 = box
    return fitz.Rect(
        x0 * page_rect.width / ref_width,
        y0 * page_rect.height / ref_height,
        x1 * page_rect.width / ref_width,
        y1 * page_rect.height / ref_height,
    )


def render_crop(page, clip, out_file):
    zoom = DPI / 72
    pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
    pixmap.save(out_file)
    return pixmap.width, pixmap.height


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    manifest = []

    for crop in CROPS:
        page = doc[crop["page"] - 1]
        clip = old_pixels_to_pdf_rect(page, reference_size(crop["page"]), crop["box"])
        out_file = OUT_DIR / crop["name"]
        width, height = render_crop(page, clip, out_file)
        manifest.append({
            "file": str(out_file.relative_to(ROOT)),
            "page": crop["page"],
            "label": crop["label"],
            "sourceBox160dpi": crop["box"],
            "pdfBox": [round(clip.x0, 3), round(clip.y0, 3), round(clip.x1, 3), round(clip.y1, 3)],
            "width": width,
            "height": height,
            "dpi": DPI,
        })

    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"created": len(manifest), "outDir": str(OUT_DIR)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
