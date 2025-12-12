import httpx
from io import BytesIO
from pypdf import PdfReader

url = "https://cwlklruqhmtcgrtsrmkh.supabase.co/storage/v1/object/public/pdfs/1cfeba82-12ac-4bdd-b77c-c26973fd5551/66b39fba-f617-4359-b753-7356926d526c/sample.pdf"

response = httpx.get(url, follow_redirects=True)
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

result = extract_pdf_text(pdf_file_like)

print(result)
