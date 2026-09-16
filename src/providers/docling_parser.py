import time

from docling.document_converter import DocumentConverter


_converter = DocumentConverter()


def parse_pdf(pdf_path: str) -> dict:
    start = time.perf_counter()

    result = _converter.convert(pdf_path)
    document = result.document

    markdown = document.export_to_markdown()

    latency = time.perf_counter() - start

    return {
        "provider": "docling",
        "text": markdown,
        "latency_seconds": latency,
        "cost_usd": 0.0,
        "error": None,
    }