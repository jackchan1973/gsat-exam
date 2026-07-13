#!/usr/bin/env python3
"""
Crop 114 Math A official PDF into per-question images.

數學公式與圖形以官方 PDF 局部裁圖保留原貌；18-20 題組共用題幹另裁一張，
避免每題重複存放相同資料。
"""
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "資料/大考中心官方PDF/114學年度/數學A/114學測-數學A-試題內容-03-114學測數學a試題.pdf"
OUT = ROOT / "public/images/114學年度/數學A"

# page_index is zero-based in PyMuPDF. Coordinates are PDF points.
BOXES = {
    "q01": (1, 50, 150, 548, 332),
    "q02": (1, 50, 392, 548, 520),
    "q03": (1, 50, 590, 548, 765),
    "q04": (2, 50, 90, 548, 175),
    "q05": (2, 50, 260, 548, 360),
    "q06": (2, 50, 390, 548, 500),
    "q07": (2, 50, 535, 548, 765),
    "q08": (3, 50, 85, 548, 260),
    "q09": (3, 50, 290, 548, 500),
    "q10": (3, 50, 575, 548, 735),
    "q11": (4, 50, 85, 548, 300),
    "q12": (4, 50, 335, 548, 610),
    "q13": (4, 50, 690, 548, 785),
    "q14": (5, 50, 85, 548, 220),
    "q15": (5, 50, 260, 548, 430),
    "q16": (5, 50, 480, 548, 660),
    "q17": (6, 50, 85, 548, 175),
    "group-18-20": (6, 50, 225, 548, 490),
    "q18": (6, 50, 490, 548, 552),
    "q19": (6, 50, 548, 548, 622),
    "q20": (6, 50, 640, 548, 735),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    matrix = fitz.Matrix(200 / 72, 200 / 72)
    for name, (page_index, x0, y0, x1, y1) in BOXES.items():
        pix = doc[page_index].get_pixmap(matrix=matrix, clip=fitz.Rect(x0, y0, x1, y1), alpha=False)
        pix.save(OUT / f"{name}.png")
    doc.close()
    print(f"cropped {len(BOXES)} images -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
