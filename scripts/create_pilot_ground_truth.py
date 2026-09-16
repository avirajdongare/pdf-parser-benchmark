import json
from pathlib import Path

FULL_GT = Path("data/raw/OmniDocBench/OmniDocBench.json")
MANIFEST = Path("data/sample/manifest.json")
OUT = Path("data/sample/OmniDocBench_pilot.json")

with FULL_GT.open("r", encoding="utf-8") as f:
    full_data = json.load(f)

with MANIFEST.open("r", encoding="utf-8") as f:
    manifest = json.load(f)

selected_names = {
    item["source_image"]
    for item in manifest
}

pilot = [
    page for page in full_data
    if Path(page["page_info"]["image_path"]).name in selected_names
]

with OUT.open("w", encoding="utf-8") as f:
    json.dump(pilot, f, ensure_ascii=False, indent=2)

print("Pilot GT pages:", len(pilot))
print("Saved:", OUT)