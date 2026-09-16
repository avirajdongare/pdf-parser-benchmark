import json
from pathlib import Path

import pandas as pd


SCORE_FILE = Path(
    "outputs/scores/docling/"
    "predictions_quick_match_run_summary.json"
)

LATENCY_FILE = Path(
    "outputs/docling_pilot_summary.csv"
)

RESULTS_FILE = Path(
    "results/provider_results.csv"
)


with SCORE_FILE.open("r", encoding="utf-8") as f:
    score_data = json.load(f)

metrics = score_data["notebook_metric_summary"]["metrics"]

latency_df = pd.read_csv(LATENCY_FILE)

row = {
    "provider": "docling",

    "sample_size": len(latency_df),

    "text_edit_distance":
        metrics["text_block_Edit_dist"]["raw"],

    "table_teds":
        metrics["table_TEDS"]["raw"],

    "table_structure_teds":
        metrics["table_TEDS_structure_only"]["raw"],

    "formula_cdm":
        metrics["display_formula_CDM"]["raw"],

    "reading_order_edit_distance":
        metrics["reading_order_Edit_dist"]["raw"],

    "overall_score":
        score_data["notebook_metric_summary"]["overall_notebook"],

    "mean_latency_seconds":
        latency_df["latency_seconds"].mean(),

    "median_latency_seconds":
        latency_df["latency_seconds"].median(),

    "failure_count":
        latency_df["error"].notna().sum(),

    "cost_usd_per_page": 0.0,
}


new_df = pd.DataFrame([row])

if RESULTS_FILE.exists() and RESULTS_FILE.stat().st_size > 0:
    existing = pd.read_csv(RESULTS_FILE)

    # Replace previous result for same provider
    existing = existing[
        existing["provider"] != row["provider"]
    ]

    new_df = pd.concat(
        [existing, new_df],
        ignore_index=True
    )

new_df.to_csv(
    RESULTS_FILE,
    index=False
)

print("\nSaved benchmark result:\n")
print(new_df.to_string(index=False))
print("\nFile:", RESULTS_FILE)