from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND
from src.database.crud.document import DocumentCRUD
from src.database.deps import get_db
from src.database.models import DocumentModel
from src.schemas.request import SessionBody
from src.utils.extractor import get_pdf_from_url
from src.test import answer_question
import asyncio

deep_agent_router = APIRouter(prefix="/deep")
doc_crud = DocumentCRUD(DocumentModel)

@deep_agent_router.post("/ask")
async def question(session: SessionBody, query: str = Body(), db: AsyncSession = Depends(get_db)):
    doc_obj = await doc_crud.get(db, session.document_id)
    if not doc_obj:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Document not found")

    text = await get_pdf_from_url(url=str(doc_obj.file_path))

    # --- collect full answer ---
    full_answer = []
    async for chunk in answer_question(query, text):
        full_answer.append(chunk)
    full_answer_text = "".join(full_answer)

    # --- parse citations ---
    answer_text = full_answer_text
    citations = []


    print(answer_text)

    if "---EVIDENCE---" in full_answer_text:
        parts = full_answer_text.split("---EVIDENCE---")
        answer_text = parts[0].strip()
        evidence_text = parts[1].replace("---END-EVIDENCE---", "").strip()
        # parse each citation line
        lines = evidence_text.splitlines()
        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                citations.append(lines[i+1].strip())

    return {
        "answer": answer_text,
        "citations": citations
    }
