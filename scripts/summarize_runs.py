import json
from pathlib import Path

import pandas as pd


rows = []

for path in Path("outputs/raw/docling").glob("*.json"):
    with path.open("r", encoding="utf-8") as f:
        result = json.load(f)

    rows.append({
        "benchmark_id": result["benchmark_id"],
        "group": result["benchmark_group"],
        "source": result["data_source"],
        "layout": result["layout"],
        "latency_seconds": result["latency_seconds"],
        "output_chars": len(result.get("text", "")),
        "error": result["error"],
    })


df = pd.DataFrame(rows).sort_values("benchmark_id")

print("\n=== DOCLING PILOT ===\n")
print(df.to_string(index=False))

print("\n=== SUMMARY ===")
print("Documents:", len(df))
print("Failures:", df["error"].notna().sum())
print("Mean latency:", round(df["latency_seconds"].mean(), 2))
print("Median latency:", round(df["latency_seconds"].median(), 2))
print("Mean output chars:", round(df["output_chars"].mean(), 0))

df.to_csv("outputs/docling_pilot_summary.csv", index=False)