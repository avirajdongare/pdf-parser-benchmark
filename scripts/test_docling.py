from src.providers.docling_parser import parse_pdf

result = parse_pdf("data/sample/pdfs/doc_001.pdf")

print("\n=== RESULT ===")
print("Provider:", result["provider"])
print("Latency:", result["latency_seconds"])
print("Error:", result["error"])

print("\n=== OUTPUT ===")
print(result["text"][:3000])