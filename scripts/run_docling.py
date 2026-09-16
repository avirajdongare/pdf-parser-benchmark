import json
from pathlib import Path

from src.providers.docling_parser import parse_pdf


MANIFEST = Path("data/sample/manifest.json")
OUTPUT_DIR = Path("outputs/raw/docling")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with MANIFEST.open("r", encoding="utf-8") as f:
    benchmark = json.load(f)


# Warm-up run — excluded from benchmark latency.
print("Warming up Docling...")
_ = parse_pdf(benchmark[0]["pdf_path"])
print("Warm-up complete.\n")


for i, item in enumerate(benchmark, start=1):
    benchmark_id = item["benchmark_id"]

    print(f"[{i:02d}/{len(benchmark)}] Parsing {benchmark_id}...")

    try:
        result = parse_pdf(item["pdf_path"])

    except Exception as e:
        result = {
            "provider": "docling",
            "text": "",
            "latency_seconds": None,
            "cost_usd": 0.0,
            "error": str(e),
        }

    result["benchmark_id"] = benchmark_id
    result["benchmark_group"] = item["benchmark_group"]
    result["data_source"] = item["data_source"]
    result["layout"] = item["layout"]

    output_path = OUTPUT_DIR / f"{benchmark_id}.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(
        f"       latency={result['latency_seconds']} "
        f"chars={len(result.get('text', ''))} "
        f"error={result['error']}"
    )


print("\nFinished.")
print("Outputs:", OUTPUT_DIR)