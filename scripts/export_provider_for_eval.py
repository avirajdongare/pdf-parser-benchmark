import argparse
import json
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument(
    "--provider",
    required=True
)
args = parser.parse_args()

provider = args.provider

MANIFEST = Path(
    "data/sample/manifest.json"
)

RAW_DIR = Path(
    f"outputs/raw/{provider}"
)

OUT_DIR = Path(
    f"outputs/eval/{provider}"
)

OUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


with MANIFEST.open(
    "r",
    encoding="utf-8"
) as f:

    manifest = json.load(f)


for item in manifest:

    benchmark_id = item["benchmark_id"]

    result_path = (
        RAW_DIR /
        f"{benchmark_id}.json"
    )

    with result_path.open(
        "r",
        encoding="utf-8"
    ) as f:

        result = json.load(f)

    original_name = Path(
        item["source_image"]
    )

    output_name = (
        original_name
        .with_suffix(".md")
        .name
    )

    with (
        OUT_DIR / output_name
    ).open(
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            result.get("text", "")
        )


print(
    f"Exported {len(manifest)} "
    f"files for {provider}"
)