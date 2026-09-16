import json
from pathlib import Path

from src.providers.mistral_ocr_parser import parse_pdf


MANIFEST = Path("data/sample/manifest.json")
OUTPUT_DIR = Path("outputs/raw/mistral_ocr")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

with MANIFEST.open("r", encoding="utf-8") as f:
    benchmark = json.load(f)


for i, item in enumerate(benchmark, start=1):

    benchmark_id = item["benchmark_id"]

    print(
        f"[{i:02d}/{len(benchmark)}] "
        f"{benchmark_id}"
    )

    try:

        result = parse_pdf(
            item["pdf_path"]
        )

    except Exception as e:

        result = {
            "provider": "mistral_ocr",
            "model": None,
            "text": "",
            "latency_seconds": None,
            "cost_usd": None,
            "error": str(e),
        }

    result["benchmark_id"] = benchmark_id
    result["benchmark_group"] = (
        item["benchmark_group"]
    )
    result["data_source"] = (
        item["data_source"]
    )
    result["layout"] = (
        item["layout"]
    )

    output = (
        OUTPUT_DIR /
        f"{benchmark_id}.json"
    )

    with output.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(
        "    latency:",
        result["latency_seconds"],
        "| cost:",
        result["cost_usd"],
        "| error:",
        result["error"],
    )


print("\nFinished.")