import json
from pathlib import Path

MANIFEST = Path("data/sample/manifest.json")
RAW_DIR = Path("outputs/raw/docling")
OUT_DIR = Path("outputs/eval/docling")

OUT_DIR.mkdir(parents=True, exist_ok=True)

with MANIFEST.open("r", encoding="utf-8") as f:
    manifest = json.load(f)

for item in manifest:
    benchmark_id = item["benchmark_id"]
    source_image = item["source_image"]

    with (RAW_DIR / f"{benchmark_id}.json").open("r", encoding="utf-8") as f:
        result = json.load(f)

    md_name = Path(source_image).with_suffix(".md").name

    with (OUT_DIR / md_name).open("w", encoding="utf-8") as f:
        f.write(result["text"])

print(f"Exported {len(manifest)} markdown files to {OUT_DIR}")