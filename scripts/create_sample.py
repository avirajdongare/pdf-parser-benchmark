import json
import random
import shutil
from pathlib import Path
from PIL import Image

SEED = 42

DATASET = Path("data/raw/OmniDocBench/OmniDocBench.json")
IMAGE_DIR = Path("data/raw/OmniDocBench/images")

OUT_DIR = Path("data/sample")
OUT_IMAGES = OUT_DIR / "images"
OUT_PDFS = OUT_DIR / "pdfs"
OUT_MANIFEST = OUT_DIR / "manifest.json"

OUT_IMAGES.mkdir(parents=True, exist_ok=True)
OUT_PDFS.mkdir(parents=True, exist_ok=True)

with DATASET.open("r", encoding="utf-8") as f:
    data = json.load(f)

random.seed(SEED)


def attrs(page):
    return page["page_info"]["page_attribute"]


def subset(page):
    return attrs(page).get("subset")


def language(page):
    return attrs(page).get("language")


def categories(page):
    return sorted({
        det.get("category_type")
        for det in page["layout_dets"]
        if not det.get("ignore", False)
    })


# English-only for pilot
english_pages = [
    page for page in data
    if language(page) == "english"
]

groups = {
    "table_hard": [
        p for p in english_pages
        if subset(p) == "table_hard"
    ],
    "equation_hard": [
        p for p in english_pages
        if subset(p) == "equation_hard"
    ],
    "layout_hard": [
        p for p in english_pages
        if subset(p) == "layout_hard"
    ],
    "general": [
        p for p in english_pages
        if subset(p) == "v1.5"
    ],
}

print("\nAvailable English pages:")
for name, pages in groups.items():
    print(f"{name:20} {len(pages)}")


selected = []
used_images = set()

for group_name, candidates in groups.items():

    random.shuffle(candidates)

    count = 0

    for page in candidates:
        image_name = page["page_info"]["image_path"]

        if image_name in used_images:
            continue

        selected.append((group_name, page))
        used_images.add(image_name)

        count += 1

        if count == 5:
            break

    if count < 5:
        raise RuntimeError(
            f"Not enough English pages for {group_name}: only {count}"
        )


manifest = []

for i, (group_name, page) in enumerate(selected, start=1):

    info = page["page_info"]
    page_attrs = info["page_attribute"]

    image_name = info["image_path"]

    src_image = IMAGE_DIR / image_name

    benchmark_id = f"doc_{i:03d}"

    dst_image = OUT_IMAGES / f"{benchmark_id}.png"
    dst_pdf = OUT_PDFS / f"{benchmark_id}.pdf"

    shutil.copy2(src_image, dst_image)

    # Convert benchmark image → single-page PDF.
    # This ensures every provider receives identical visual content.
    with Image.open(src_image) as img:
        rgb = img.convert("RGB")
        rgb.save(dst_pdf, "PDF", resolution=150.0)

    manifest.append({
        "benchmark_id": benchmark_id,
        "benchmark_group": group_name,
        "pdf_path": str(dst_pdf),
        "image_path": str(dst_image),
        "source_image": image_name,

        "data_source": page_attrs.get("data_source"),
        "language": page_attrs.get("language"),
        "layout": page_attrs.get("layout"),
        "subset": page_attrs.get("subset"),

        "categories": categories(page),

        # Keep full human-reviewed OmniDocBench annotations
        "ground_truth": page["layout_dets"],
    })


with OUT_MANIFEST.open("w", encoding="utf-8") as f:
    json.dump(
        manifest,
        f,
        ensure_ascii=False,
        indent=2
    )


print("\n=== PILOT BENCHMARK ===\n")

for item in manifest:
    print(
        f"{item['benchmark_id']:8} "
        f"{item['benchmark_group']:16} "
        f"{item['data_source']:24} "
        f"{item['layout']}"
    )

print("\nTotal:", len(manifest))
print("Manifest:", OUT_MANIFEST)
print("PDFs:", OUT_PDFS)