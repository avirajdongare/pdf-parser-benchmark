import json
from collections import Counter
from pathlib import Path

path = Path("data/raw/OmniDocBench/OmniDocBench.json")

with path.open("r", encoding="utf-8") as f:
    data = json.load(f)

sources = Counter()
languages = Counter()
layouts = Counter()
subsets = Counter()
categories = Counter()

pages_with_text = 0
pages_with_tables = 0
pages_with_equations = 0

for page in data:
    attrs = page["page_info"]["page_attribute"]

    sources[attrs.get("data_source")] += 1
    languages[attrs.get("language")] += 1
    layouts[attrs.get("layout")] += 1

    subset = attrs.get("subset")

    if isinstance(subset, list):
        for item in subset:
            subsets[item] += 1
    elif subset:
        subsets[subset] += 1

    page_categories = set()

    for det in page["layout_dets"]:
        category = det.get("category_type")

        categories[category] += 1
        page_categories.add(category)

    if "text_block" in page_categories:
        pages_with_text += 1

    if "table" in page_categories:
        pages_with_tables += 1

    if any(
        category and "equation" in category
        for category in page_categories
    ):
        pages_with_equations += 1


print("\n=== DATA SOURCES ===")
for k, v in sources.most_common():
    print(f"{str(k):30} {v}")

print("\n=== LANGUAGES ===")
for k, v in languages.most_common():
    print(f"{str(k):30} {v}")

print("\n=== LAYOUTS ===")
for k, v in layouts.most_common():
    print(f"{str(k):30} {v}")

print("\n=== SUBSETS ===")
for k, v in subsets.most_common():
    print(f"{str(k):30} {v}")

print("\n=== ELEMENT TYPES ===")
for k, v in categories.most_common():
    print(f"{str(k):30} {v}")

print("\n=== PAGE FEATURES ===")
print("Pages:", len(data))
print("Pages with text:", pages_with_text)
print("Pages with tables:", pages_with_tables)
print("Pages with equations:", pages_with_equations)