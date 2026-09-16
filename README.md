# Document Parsing for AI Agents

A reproducible **quality × latency × cost** benchmark for document parsers used in AI workflows.

**v0 pilot · 20 OmniDocBench pages · Docling vs Mistral OCR 4.1**

---

## What this benchmark asks

Document parsing is an upstream dependency for RAG systems and AI agents. A parser can preserve the document structure an agent needs — or quietly destroy it.

This pilot compares two parsers on the **same frozen visual inputs** and measures:

- text extraction
- table reconstruction
- formula extraction
- reading order
- end-to-end latency
- API cost
- failures

The goal is not just to ask **“which parser scores highest?”**, but **“which parser is the better fit for a given workload?”**

---

## Results

| Provider | Overall ↑ | Text edit ↓ | Table TEDS ↑ | Table structure ↑ | Formula CDM ↑ | Reading-order edit ↓ | Mean latency ↓ | Failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Mistral OCR** | **87.34** | 0.125 | **0.752** | 0.829 | **0.993** | **0.173** | **2.87s** | 1 |
| **Docling** | 52.62 | **0.113** | 0.674 | **0.840** | 0.017 | 0.348 | 5.15s | **0** |

**↑ higher is better · ↓ lower is better**

### What stood out

- **Mistral OCR led on overall score, tables, formulas, reading order, and measured latency.**
- **Docling slightly led on plain-text edit distance and table-structure TEDS.**
- The largest gap was in **formula extraction**: `0.993` vs `0.017`.
- Mistral had **1 failed page**; Docling completed all 20.
- Docling has **$0 API fee**, but local compute cost is not included.

This is a **20-page pilot**, so the results are directional rather than a definitive industry ranking.

---

## Capability comparison

![Capability comparison](results/figures/capability_comparison.png)

Text performance is relatively close. The larger differences appear in formulas and reading order.

Table performance is more nuanced: Mistral leads on full Table TEDS, while Docling slightly leads on structure-only TEDS.

---

## Quality vs latency

![Quality vs latency](results/figures/quality_vs_latency.png)

Measured mean latency:

| Provider | Mean | Median |
|---|---:|---:|
| **Mistral OCR** | **2.87s** | **2.56s** |
| **Docling** | 5.15s | 3.54s |

Latency is **developer-observed wall-clock time**, not hardware-normalized inference speed:

- Docling ran locally.
- Mistral ran through a hosted API.
- Docling cold-start/model-download time was excluded.

---

## Overall score

![Overall score](results/figures/overall_score.png)

The aggregate score is useful, but it should not replace capability-level analysis. A parser that performs well overall can still be a poor fit for equation-heavy, table-heavy, or complex-layout workloads.

---

## Latency

![Latency](results/figures/latency.png)

---

## Cost

### Mistral OCR

- Total recorded API cost: **$0.076**
- Mean cost per attempted page: **$0.0038**

### Docling

- External API fee: **$0**
- Local compute, infrastructure, and engineering costs: **not included**

So `$0 API fee` should not be interpreted as `$0 production cost`.

---

## Dataset

The benchmark uses **OmniDocBench**, a document-parsing dataset with human-reviewed annotations for text, tables, formulas, layout, and reading order.

For this v0 pilot, I sampled **20 English-language pages** with a fixed seed:

| Cohort | Pages |
|---|---:|
| `table_hard` | 5 |
| `equation_hard` | 5 |
| `layout_hard` | 5 |
| general `v1.5` | 5 |

Not every page contains every content type. The official evaluator scored:

- text: 19 pages
- tables: 7 pages
- display formulas: 7 pages
- reading order: 20 pages

---
## OmniDocBench Pilot (v0) & Benchmark Analysis

Raw benchmark evidence should be inspectable below the leaderboard. For each provider, this repository preserves:

- **Input**
- **Raw provider response**
- **Normalized Markdown**
- **Official evaluator output**
- **Aggregate result**

The OmniDocBench evaluator produces per-page and per-element artifacts for:
- Text blocks
- Tables
- Formulas
- Reading order

These artifacts enable detailed failure analysis without needing to rerun the providers.

---

## What the Aggregate Score Hides

The v0 results demonstrate why parser selection should not collapse into a single leaderboard number.

### Plain Text
Docling slightly outperformed Mistral OCR on text edit distance (*lower is better*):

| Provider | Edit Distance |
| :--- | :--- |
| **Docling** | **0.113** |
| **Mistral OCR** | 0.125 |

### Tables
The top provider changes depending on what "good table parsing" means to your pipeline.

* **Full TEDS** (*higher is better*)
  * **Mistral OCR:** `0.752`
  * **Docling:** `0.674`
* **Structure-Only TEDS** (*higher is better*)
  * **Docling:** `0.840`
  * **Mistral OCR:** `0.829`

> **Takeaway:** Content recovery and structural reconstruction should be analyzed separately.

### Formulas
This metric showed the largest observed gap (*higher is better*):

| Provider | Score |
| :--- | :--- |
| **Mistral OCR** | **0.993** |
| **Docling** | 0.017 |

*Note: Before treating this as a definitive product conclusion, future release iterations should inspect formula-level outputs to distinguish genuine recognition failures from Markdown / LaTeX representation differences.*

### Reading Order
Evaluated via normalized distance (*lower is better*):

| Provider | Score |
| :--- | :--- |
| **Mistral OCR** | **0.173** |
| **Docling** | 0.348 |

*This metric is critical: a document can contain every correct sentence and still become poor agent context if those sentences are returned out of order.*

---

## Failure Analysis

The final benchmark goes beyond aggregate metrics. The evaluator preserves page-level and element-level outputs to investigate targeted questions:

- **Layout Gaps:** Which document layouts produce the largest performance differences?
- **Column Handling:** Do parsers fail differently on multi-column or double-column documents?
- **Table Discrepancies:** Are table errors driven by OCR transcription or structural reconstruction?
- **Formula Parsing:** Are formulas missing entirely or simply represented in an alternate syntax?
- **Order Correlation:** Does a low reading-order score correlate directly with complex/unusual layouts?
- **Category Clustering:** Are failures heavily concentrated in specific document domains?

*While the v0 repository preserves these artifacts, it intentionally avoids over-generalizing from a 20-page sample size. A larger release will surface representative failure cases directly in the benchmark report.*

---

## Limitations

This repository represents an intentionally lightweight **v0 pilot**, not a definitive parser leaderboard.

1. **Small Sample:** Only 20 pages are evaluated to validate the methodology before scaling.
2. **English Only:** The source dataset includes multilingual documents, but v0 isolates English pages.
3. **Two Providers:** Evaluates only `Docling` and `Mistral OCR`. Potential future additions:
   - LlamaParse
   - Reducto
   - Unstructured
   - Additional open-source parsers
4. **Local vs. Hosted Latency:** Docling (local) and Mistral (API) use different execution environments. Latency represents developer-observed end-to-end time, not normalized model inference speed.
5. **Excluded Compute Costs:** Docling has no metered API charge, but self-hosting infrastructure costs are excluded.
6. **Existing Ground Truth:** Reuses OmniDocBench's human-reviewed annotations to maintain reproducibility, inheriting its underlying dataset limitations.

---

## v1 Roadmap

The next planned release transitions from methodology validation to production-grade comparisons:

### Expanded Dataset
- Scale from **20 → 75–100 balanced pages**
- Stratify across document source, complex layout, tables, equations, visually complex pages, and standard pages

### Provider Expansion
- Broaden beyond Docling and Mistral OCR to include additional production-relevant alternatives

### Advanced Metrics
- Page-level confidence intervals
- Latency distribution profiles
- Cost-quality Pareto frontier
- Taxonomies for failure modes
- Document-type-specific rankings
- Multilingual evaluations
- Self-hosted compute cost estimates

---

## Why This Matters for AI Agents

The long-term goal is to make benchmark evidence **machine-usable**. Instead of relying on vague marketing claims (*"Vendor A has excellent OCR"*), an agent can reason dynamically over independent evidence:

```yaml
Input Context:
  - Dense tables
  - No equations
  - Two-column layout

Agent Priorities:
  - High structural fidelity
  - Latency < 5s
  - Cost < $0.01 / page

Action:
  - Query benchmark evidence -> Select optimal parser for workload
```

---


## Fairness and methodology

Every provider received the **same image-only single-page PDFs** generated from the frozen OmniDocBench page images.

This prevents one parser from benefiting from an embedded PDF text layer.

Pipeline:

```text
OmniDocBench page image
        ↓
frozen image-only PDF
        ↓
provider parser
        ↓
Markdown output
        ↓
official OmniDocBench evaluator
        ↓
quality + latency + cost + failures
```

Metrics:

- **Text edit distance** — lower is better
- **Table TEDS** — higher is better
- **Table structure TEDS** — higher is better
- **Formula CDM** — higher is better
- **Reading-order edit distance** — lower is better
- **Overall score** — OmniDocBench aggregate

Raw provider outputs and evaluator artifacts are preserved so results can be inspected below the leaderboard.

---

## Reproduce

Create the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run providers:

```bash
PYTHONPATH=. python scripts/run_docling.py
PYTHONPATH=. python scripts/run_mistral.py
```

Export predictions:

```bash
PYTHONPATH=. python scripts/export_provider_for_eval.py --provider docling
PYTHONPATH=. python scripts/export_provider_for_eval.py --provider mistral_ocr
```

Save benchmark results:

```bash
python scripts/save_provider_result.py --provider docling
python scripts/save_provider_result.py --provider mistral_ocr
```

Generate figures:

```bash
python scripts/create_figures.py
```

Final consolidated results:

```text
results/provider_results.csv
```

---


## Takeaway

On this pilot, **Mistral OCR produced the stronger overall result**, especially on formulas and reading order, while **Docling remained competitive on text, slightly led on table structure, ran locally, and avoided metered API fees**.

The more useful benchmark question is not:

> Which parser wins overall?

It is:

> **Which parser should an AI agent use for this document, under this quality, latency, and cost constraint?**
