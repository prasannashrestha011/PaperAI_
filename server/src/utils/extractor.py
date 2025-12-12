import asyncio
import httpx
from io import BytesIO
from PyPDF2 import PdfReader  

async def get_pdf_from_url(url: str) -> str:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()

    pdf_bytes = response.content
    pdf_file_like = BytesIO(pdf_bytes)

    def extract_pdf_text(file_like) -> str:
        reader = PdfReader(file_like)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return "\n".join(text)

    text = extract_pdf_text(pdf_file_like)
    return text

