import json
from pathlib import Path

root = Path("outputs/scores/docling")

print("\n=== EVALUATION ARTIFACTS ===\n")

for path in sorted(root.rglob("*")):
    if not path.is_file():
        continue

    size_kb = path.stat().st_size / 1024

    print(f"{path}  ({size_kb:.1f} KB)")

    if path.suffix == ".json":
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            print("   type:", type(data).__name__)

            if isinstance(data, dict):
                print("   keys:", list(data.keys())[:15])

            elif isinstance(data, list):
                print("   rows:", len(data))

                if data and isinstance(data[0], dict):
                    print("   first-row keys:", list(data[0].keys())[:20])

        except Exception:
            pass