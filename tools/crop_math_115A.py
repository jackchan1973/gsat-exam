#!/usr/bin/env python3
"""
crop_math_115A.py — 115 數學A 每題裁圖（題幹＋選項一起）。

數學公式無法可靠文字化，依規範每題裁官方 PDF 為圖，答題卡另放作答輸入。
裁圖座標為 (page_index, top, bottom)，x 固定 50–548，200 DPI。
改座標後重跑即可覆蓋 public/images/115學年度/數學A/qNN.png。

2026-07-10 已依傑克驗收修正 Q5/Q6/Q10/Q11/Q12/Q14 邊界；並新增 Q19/Q20（手寫題，僅展示）。
"""
import glob
import fitz

PDF = glob.glob("資料/大考中心官方PDF/115學年度/數學A/*試卷*.pdf")[0]
OUT = "public/images/115學年度/數學A"

# (page_index, top, bottom)；x 固定 50–548
BOXES = {
    1: (1, 153, 265), 2: (1, 265, 434), 3: (1, 434, 589), 4: (1, 589, 793),
    5: (2, 82, 212),  6: (2, 274, 340), 7: (2, 446, 592), 8: (2, 592, 793),
    9: (3, 84, 445),  10: (3, 445, 640),
    11: (4, 87, 262), 12: (4, 440, 600),
    13: (5, 128, 293), 14: (5, 296, 413), 15: (5, 409, 590), 16: (5, 590, 784),
    17: (6, 84, 300), 18: (6, 410, 566),
    19: (6, 570, 610), 20: (6, 612, 662),
}


def main():
    doc = fitz.open(PDF)
    z = fitz.Matrix(200 / 72, 200 / 72)
    for n, (pi, top, bot) in BOXES.items():
        doc[pi].get_pixmap(matrix=z, clip=fitz.Rect(50, top, 548, bot)).save("%s/q%02d.png" % (OUT, n))
    print("cropped %d questions -> %s" % (len(BOXES), OUT))


if __name__ == "__main__":
    main()
