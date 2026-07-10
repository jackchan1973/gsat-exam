#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

import fitz


QUESTION_RE = re.compile(r"^\s*(\d{1,2})[\.．、]\s")
GROUP_RE = re.compile(r"^\s*(\d{1,2})\s*[-－]\s*(\d{1,2})\s*為題組")
SECTION_RE = re.compile(r"^\s*第\s*[壹貳參肆伍陸柒捌玖拾]+\s*部\s*分")


def parse_pages(value, page_count):
    if not value:
        return list(range(page_count))

    pages = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = [int(item.strip()) for item in part.split("-", 1)]
            pages.update(range(start - 1, end))
        else:
            pages.add(int(part) - 1)

    return sorted(page for page in pages if 0 <= page < page_count)


def clean_text(text):
    return "\n".join(line.rstrip() for line in text.strip().splitlines()).strip()


def bbox_to_list(rect):
    return [round(rect.x0, 3), round(rect.y0, 3), round(rect.x1, 3), round(rect.y1, 3)]


def export_page_png(page, out_file, dpi):
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    pix.save(out_file)
    return pix.width, pix.height


def extract_pdf(pdf_file, out_dir, pages, dpi):
    doc = fitz.open(pdf_file)
    out_dir.mkdir(parents=True, exist_ok=True)
    pages_dir = out_dir / "pages"
    images_dir = out_dir / "images"
    pages_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    raw_items = []
    page_info = []
    selected_pages = parse_pages(pages, len(doc))

    for page_index in selected_pages:
      page = doc[page_index]
      page_no = page_index + 1
      page_png = pages_dir / f"page-{page_no:03d}.png"
      png_width, png_height = export_page_png(page, page_png, dpi)
      page_rect = page.rect
      page_info.append({
          "page": page_no,
          "width": round(page_rect.width, 3),
          "height": round(page_rect.height, 3),
          "png": str(page_png.relative_to(out_dir)),
          "pngWidth": png_width,
          "pngHeight": png_height,
          "dpi": dpi,
      })

      for block_index, block in enumerate(page.get_text("blocks")):
          x0, y0, x1, y1, text, block_no, block_type = block[:7]
          text = clean_text(text)
          if not text:
              continue
          raw_items.append({
              "page": page_no,
              "blockIndex": block_index,
              "y": round(y0, 3),
              "x": round(x0, 3),
              "bbox": [round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)],
              "type": "text",
              "content": text,
          })

      seen_images = set()
      for image_index, image in enumerate(page.get_images(full=True), start=1):
          xref = image[0]
          for rect_index, rect in enumerate(page.get_image_rects(xref), start=1):
              key = (xref, tuple(round(value, 3) for value in bbox_to_list(rect)))
              if key in seen_images:
                  continue
              seen_images.add(key)

              extracted = doc.extract_image(xref)
              ext = extracted.get("ext", "png")
              image_name = f"page-{page_no:03d}-img-{image_index:03d}-{rect_index:02d}.{ext}"
              image_file = images_dir / image_name
              image_file.write_bytes(extracted["image"])
              raw_items.append({
                  "page": page_no,
                  "blockIndex": f"image-{image_index}-{rect_index}",
                  "y": round(rect.y0, 3),
                  "x": round(rect.x0, 3),
                  "bbox": bbox_to_list(rect),
                  "type": "image",
                  "src": str(image_file.relative_to(out_dir)),
              })

      for drawing_index, drawing in enumerate(page.get_drawings(), start=1):
          rect = drawing.get("rect")
          if not rect or rect.is_empty:
              continue
          raw_items.append({
              "page": page_no,
              "blockIndex": f"drawing-{drawing_index}",
              "y": round(rect.y0, 3),
              "x": round(rect.x0, 3),
              "bbox": bbox_to_list(rect),
              "type": "drawing",
              "content": "vector drawing / table line / box",
          })

    raw_items.sort(key=lambda item: (item["page"], item["y"], item["x"], str(item["blockIndex"])))
    candidates = build_question_candidates(raw_items)

    (out_dir / "pages.json").write_text(json.dumps(page_info, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "questions_raw.json").write_text(json.dumps(raw_items, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "question_candidates.json").write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "pages": len(page_info),
        "rawItems": len(raw_items),
        "candidates": len(candidates),
        "outDir": str(out_dir),
    }


def item_starts_candidate(item):
    if item["type"] != "text":
        return None
    first_line = item["content"].splitlines()[0]
    group_match = GROUP_RE.match(first_line)
    if group_match:
        return {
            "kind": "group",
            "id": f"group-{group_match.group(1)}-{group_match.group(2)}",
            "label": f"{group_match.group(1)}-{group_match.group(2)} 題組",
            "questionNos": list(range(int(group_match.group(1)), int(group_match.group(2)) + 1)),
        }
    if SECTION_RE.match(first_line):
        return {
            "kind": "section",
            "id": f"section-{item['page']}-{int(item['y'])}",
            "label": "試卷段落說明",
            "questionNos": [],
        }
    question_match = QUESTION_RE.match(first_line)
    if question_match:
        number = int(question_match.group(1))
        return {
            "kind": "question",
            "id": f"q-{number}",
            "label": f"第 {number} 題",
            "questionNos": [number],
        }
    return None


def is_page_noise(item):
    if item["type"] == "drawing" and item["y"] < 80:
        return True

    if item["type"] != "text":
        return False

    content = item["content"].strip()
    if content.startswith("請記得在答題卷簽名欄位"):
        return True
    if re.fullmatch(r"-\s*\d+\s*-", content):
        return True
    if "115年學測" in content and "頁" in content and "國語文綜合能力測驗" in content:
        return True
    return False


def build_question_candidates(raw_items):
    candidates = []
    current = None
    previous_page = None

    for item in raw_items:
        if previous_page is not None and item["page"] > previous_page + 1 and current:
            finish_candidate(current)
            candidates.append(current)
            current = None
        previous_page = item["page"]

        start = item_starts_candidate(item)
        if start:
            if current:
                finish_candidate(current)
                candidates.append(current)
            current = {
                **start,
                "startPage": item["page"],
                "endPage": item["page"],
                "startY": item["y"],
                "endY": item["bbox"][3],
                "items": [],
                "images": [],
                "drawings": 0,
                "content": "",
            }

        if not current:
            continue
        if is_page_noise(item):
            continue

        current["items"].append(item)
        current["endPage"] = item["page"]
        current["endY"] = item["bbox"][3]
        if item["type"] == "text":
            current["content"] = (current["content"] + "\n" + item["content"]).strip()
        elif item["type"] == "image":
            current["images"].append({
                "page": item["page"],
                "src": item["src"],
                "bbox": item["bbox"],
            })
        elif item["type"] == "drawing":
            current["drawings"] += 1

    if current:
        finish_candidate(current)
        candidates.append(current)

    return candidates


def finish_candidate(candidate):
    candidate["itemCount"] = len(candidate["items"])
    candidate["pages"] = sorted({item["page"] for item in candidate["items"]})
    candidate["imageCount"] = len(candidate["images"])
    candidate.pop("items", None)


def main():
    parser = argparse.ArgumentParser(description="Extract raw PDF pages, blocks, images, and question candidates.")
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument("out_dir", help="Output directory")
    parser.add_argument("--pages", default="", help="1-based page range, for example: 4-5,10-12")
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()

    result = extract_pdf(Path(args.pdf), Path(args.out_dir), args.pages, args.dpi)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
