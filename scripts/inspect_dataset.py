import json
from pathlib import Path
from pprint import pprint

DATA = Path("data/raw/OmniDocBench/OmniDocBench.json")

with DATA.open("r", encoding="utf-8") as f:
    data = json.load(f)

print("\nTYPE:", type(data).__name__)

if isinstance(data, list):
    print("NUMBER OF RECORDS:", len(data))

    first = data[0]

    print("\nTOP-LEVEL KEYS:")
    pprint(list(first.keys()))

    print("\nFIRST RECORD:")
    pprint(first, depth=3, width=120)

elif isinstance(data, dict):
    print("TOP-LEVEL KEYS:")
    pprint(list(data.keys()))

    for key, value in data.items():
        print(f"\n{key}: {type(value).__name__}")

        if isinstance(value, list):
            print("COUNT:", len(value))

            if value:
                print("FIRST ITEM KEYS:")
                if isinstance(value[0], dict):
                    pprint(list(value[0].keys()))

                print("\nFIRST ITEM:")
                pprint(value[0], depth=3, width=120)

            break