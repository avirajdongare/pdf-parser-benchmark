import os
import time
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral


load_dotenv(".env.local")

MODEL = "mistral-ocr-4-1"

# Current public list price as of 2026-09-16.
PRICE_PER_PAGE_USD = 4 / 1000

client = Mistral(
    api_key=os.environ["MISTRAL_API_KEY"]
)


def parse_pdf(pdf_path: str) -> dict:
    path = Path(pdf_path)

    start = time.perf_counter()

    uploaded = client.files.upload(
        file={
            "file_name": path.name,
            "content": path.read_bytes(),
        },
        purpose="ocr",
    )

    signed_url = client.files.get_signed_url(
        file_id=uploaded.id,
        expiry=1,
    )

    response = client.ocr.process(
        model=MODEL,
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        },
        include_blocks=True,
    )

    latency = time.perf_counter() - start

    text = "\n\n".join(
        page.markdown
        for page in response.pages
    )

    pages_processed = (
        response.usage_info.pages_processed
        if response.usage_info
        else len(response.pages)
    )

    return {
        "provider": "mistral_ocr",
        "model": response.model,
        "text": text,

        "page_count": pages_processed,

        "latency_seconds": latency,

        "cost_usd":
            pages_processed * PRICE_PER_PAGE_USD,

        "usage_info":
            response.usage_info.model_dump(
                mode="json"
            )
            if hasattr(
                response.usage_info,
                "model_dump"
            )
            else None,

        "error": None,
    }