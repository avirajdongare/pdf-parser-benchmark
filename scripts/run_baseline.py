import json
from pathlib import Path

from src.providers.pymupdf_parser import parse_pdf


MANIFEST = Path("data/sample/manifest.json")
OUTPUT_DIR = Path("outputs/raw/pymupdf")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


with MANIFEST.open("r", encoding="utf-8") as f:
    benchmark = json.load(f)


for item in benchmark:
    benchmark_id = item["benchmark_id"]
    pdf_path = item["pdf_path"]

    print(f"Parsing {benchmark_id}...")

    try:
        result = parse_pdf(pdf_path)

    except Exception as e:
        result = {
            "provider": "pymupdf",
            "text": "",
            "pages": [],
            "latency_seconds": None,
            "cost_usd": 0.0,
            "error": str(e),
        }

    result["benchmark_id"] = benchmark_id

    output_path = OUTPUT_DIR / f"{benchmark_id}.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=2,
        )


print("\nFinished.")
print(f"Outputs: {OUTPUT_DIR}")