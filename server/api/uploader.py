import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException ,UploadFile
from server.database.crud.chat_session import ChatSessionCRUD
from server.schemas.request import AskQuery, SessionBody
from sqlalchemy.ext.asyncio.session import AsyncSession
from server.database.crud.document import DocumentCRUD
from server.database.crud.storage import StorageCRUD
from server.database.deps import get_db
from server.database.models import DocumentModel
from server.schemas.document import  DocumentOut
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR 
from server.agent.builder import build_knowledge_graph
from server.schemas.response import AgentResponse,ExtractionResponse
upload_router=APIRouter(prefix="/upload")


document_crud=DocumentCRUD(DocumentModel)       
storage_crud=StorageCRUD()

@upload_router.post("/pdf",response_model=ExtractionResponse,status_code=HTTP_201_CREATED)
async def extract_pdf(user_id:uuid.UUID=Form(...,description="user id"),file:UploadFile=File(...,description="pdf file to upload"),db:AsyncSession=Depends(get_db)):
    if not file.filename :
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="File name not found"
        )
    if not file.content_type=="application/pdf":
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Only pdf files are accepted"
        )
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid file type"
        )
    try:
        doc_in=await storage_crud.upload_pdf(user_id,file)
        if doc_in is None:
            raise HTTPException( 
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload the file to the bucket"

            )
        doc_out=await document_crud.create(db=db,obj_in=doc_in)
        await build_knowledge_graph(pdf_path=str(doc_out.file_path),document_id=str(doc_out.document_id),provider="gemini",model="gemini-2.5-flash",quality="H")

        session_in=SessionBody(user_id=user_id,document_id=uuid.UUID(str(doc_out.document_id)),provider="gemini",model="gemini-2.5-flash")
        session_out=await ChatSessionCRUD.create_session(session_in,db)

        response=ExtractionResponse(doc_out=doc_out,session_out=session_out)

        return response 

    except Exception as e:
        print(f"Error reading file:{e}")
        raise HTTPException( 
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )



