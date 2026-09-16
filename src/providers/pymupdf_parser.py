import time
import pymupdf

def parse_pdf(pdf_path: str) -> dict:
    start = time.perf_counter()

    doc = pymupdf.open(pdf_path)

    pages = []

    for page in doc:
        text = page.get_text("text")

        pages.append({
            "page_number": page.number,
            "text": text,
        })

    latency = time.perf_counter() - start

    return {
        "provider": "pymupdf",
        "text": "\n".join(p["text"] for p in pages),
        "pages": pages,
        "latency_seconds": latency,
        "cost_usd": 0.0,
        "error": None,
    }