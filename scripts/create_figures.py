from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT = Path("results/provider_results.csv")
OUT = Path("results/figures")
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)

# Clean labels
df["provider_label"] = df["provider"].map({
    "docling": "Docling",
    "mistral_ocr": "Mistral OCR",
}).fillna(df["provider"])

# Convert lower-is-better edit distances into higher-is-better quality
df["text_quality"] = 1 - df["text_edit_distance"]
df["reading_order_quality"] = 1 - df["reading_order_edit_distance"]


# ---------------------------------------------------------
# FIGURE 1 — Capability comparison
# ---------------------------------------------------------

capabilities = pd.DataFrame({
    "Capability": [
        "Text",
        "Tables",
        "Formulas",
        "Reading order",
    ],
    "Docling": [
        df.loc[df["provider"] == "docling", "text_quality"].iloc[0],
        df.loc[df["provider"] == "docling", "table_teds"].iloc[0],
        df.loc[df["provider"] == "docling", "formula_cdm"].iloc[0],
        df.loc[df["provider"] == "docling", "reading_order_quality"].iloc[0],
    ],
    "Mistral OCR": [
        df.loc[df["provider"] == "mistral_ocr", "text_quality"].iloc[0],
        df.loc[df["provider"] == "mistral_ocr", "table_teds"].iloc[0],
        df.loc[df["provider"] == "mistral_ocr", "formula_cdm"].iloc[0],
        df.loc[df["provider"] == "mistral_ocr", "reading_order_quality"].iloc[0],
    ],
})

ax = capabilities.set_index("Capability").plot(
    kind="bar",
    figsize=(9, 6),
)

ax.set_title("Document Parsing Quality by Capability")
ax.set_ylabel("Score — higher is better")
ax.set_xlabel("")
ax.set_ylim(0, 1.05)
ax.legend(frameon=False)

plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    OUT / "capability_comparison.png",
    dpi=220,
)
plt.close()


# ---------------------------------------------------------
# FIGURE 2 — Overall quality vs latency
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(
    df["mean_latency_seconds"],
    df["overall_score"],
    s=120,
)

for _, row in df.iterrows():
    ax.annotate(
        row["provider_label"],
        (
            row["mean_latency_seconds"],
            row["overall_score"],
        ),
        xytext=(8, 7),
        textcoords="offset points",
    )

ax.set_title("Quality vs. Latency")
ax.set_xlabel("Mean latency per page (seconds) — lower is better")
ax.set_ylabel("Overall OmniDocBench score — higher is better")

plt.tight_layout()

plt.savefig(
    OUT / "quality_vs_latency.png",
    dpi=220,
)
plt.close()


# ---------------------------------------------------------
# FIGURE 3 — Overall benchmark score
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(7, 5))

bars = ax.bar(
    df["provider_label"],
    df["overall_score"],
)

ax.set_title("Overall Document Parsing Score")
ax.set_ylabel("OmniDocBench score")
ax.set_ylim(0, 100)

for bar, value in zip(bars, df["overall_score"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.1f}",
        ha="center",
    )

plt.tight_layout()

plt.savefig(
    OUT / "overall_score.png",
    dpi=220,
)
plt.close()


# ---------------------------------------------------------
# FIGURE 4 — Latency
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(7, 5))

bars = ax.bar(
    df["provider_label"],
    df["mean_latency_seconds"],
)

ax.set_title("Mean Parsing Latency")
ax.set_ylabel("Seconds per page — lower is better")

for bar, value in zip(bars, df["mean_latency_seconds"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.1,
        f"{value:.2f}s",
        ha="center",
    )

plt.tight_layout()

plt.savefig(
    OUT / "latency.png",
    dpi=220,
)
plt.close()


print("Saved figures to:", OUT)

for path in sorted(OUT.glob("*.png")):
    print(" -", path)