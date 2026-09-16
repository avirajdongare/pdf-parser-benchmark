import argparse
import json
from pathlib import Path

import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("--provider", required=True)
args = parser.parse_args()

provider = args.provider

SCORE_FILE = Path(
    f"outputs/scores/{provider}/"
    "predictions_quick_match_run_summary.json"
)

RAW_DIR = Path(f"outputs/raw/{provider}")
RESULTS_FILE = Path("results/provider_results.csv")

RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

with SCORE_FILE.open("r", encoding="utf-8") as f:
    scores = json.load(f)

metrics = scores["notebook_metric_summary"]["metrics"]

raw_results = []

for path in RAW_DIR.glob("*.json"):
    with path.open("r", encoding="utf-8") as f:
        raw_results.append(json.load(f))

latencies = [
    r["latency_seconds"]
    for r in raw_results
    if r.get("latency_seconds") is not None
]

costs = [
    r.get("cost_usd", 0)
    for r in raw_results
    if r.get("cost_usd") is not None
]

failures = sum(
    bool(r.get("error"))
    for r in raw_results
)

row = {
    "provider": provider,
    "sample_size": len(raw_results),

    # Lower is better
    "text_edit_distance":
        metrics["text_block_Edit_dist"]["raw"],

    # Higher is better
    "table_teds":
        metrics["table_TEDS"]["raw"],

    "table_structure_teds":
        metrics["table_TEDS_structure_only"]["raw"],

    "formula_cdm":
        metrics["display_formula_CDM"]["raw"],

    # Lower is better
    "reading_order_edit_distance":
        metrics["reading_order_Edit_dist"]["raw"],

    "overall_score":
        scores["notebook_metric_summary"]["overall_notebook"],

    "mean_latency_seconds":
        sum(latencies) / len(latencies),

    "median_latency_seconds":
        pd.Series(latencies).median(),

    "failure_count":
        failures,

    "total_cost_usd":
        sum(costs),

    "mean_cost_usd_per_page":
        sum(costs) / len(raw_results)
        if raw_results else None,
}

new = pd.DataFrame([row])

if RESULTS_FILE.exists() and RESULTS_FILE.stat().st_size > 0:
    existing = pd.read_csv(RESULTS_FILE)
    existing = existing[
        existing["provider"] != provider
    ]

    new = pd.concat(
        [existing, new],
        ignore_index=True
    )

new.to_csv(RESULTS_FILE, index=False)

print("\n=== LEADERBOARD ===\n")
print(new.to_string(index=False))
print("\nSaved:", RESULTS_FILE)