from src.providers.mistral_ocr_parser import parse_pdf


result = parse_pdf(
    "data/sample/pdfs/doc_001.pdf"
)

print("Provider:", result["provider"])
print("Model:", result["model"])
print("Latency:", result["latency_seconds"])
print("Cost:", result["cost_usd"])
print("Error:", result["error"])

print("\n=== OUTPUT ===\n")
print(result["text"][:3000])    