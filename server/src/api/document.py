from csv import Error
import io
from typing import List
import uuid
from amqp import NotFound
from celery import Task
from fastapi import APIRouter, Depends, File, Form, HTTPException ,UploadFile
from fastapi.responses import StreamingResponse
from minio import S3Error
from src.celery_app import build_kg_task 
from src.database.crud.chat_session import ChatSessionCRUD
from src.schemas import document
from src.schemas.request import AskQuery, SessionBody
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.database.crud.document import DocumentCRUD
from src.database.crud.storage import StorageCRUD
from src.database.deps import get_db
from src.database.models import DocumentModel
from src.schemas.document import  DocumentBase, DocumentOut, DocumentUpdate
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND,HTTP_200_OK
from src.schemas.response import AgentResponse,ExtractionResponse
from sqlalchemy.exc import SQLAlchemyError
router=APIRouter(prefix="/pdf")


document_crud=DocumentCRUD(DocumentModel)       
storage_crud=StorageCRUD()


@router.get("/info/{id}", response_model=DocumentBase, status_code=HTTP_200_OK)
async def get_info(id: str, db: AsyncSession = Depends(get_db)):
    try:
        doc_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid document ID"
        )

    doc_out = await document_crud.get(db, document_id=doc_id)

    if not doc_out:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Document details not found"
        )

    return doc_out


@router.post("/upload",response_model=ExtractionResponse,status_code=HTTP_201_CREATED)
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
        doc_in=await storage_crud.upload_doc(user_id,file)
        if doc_in is None:
            raise HTTPException( 
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload the file to the bucket"

            )
        doc_out=await document_crud.create(db=db,obj_in=doc_in)
        build_kg_task.delay(pdf_path=str(doc_out.file_path),document_id=str(doc_out.document_id),provider="gemini",model="gemini-2.5-flash",quality="L")
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
@router.get("/view/{doc_id:path}")
async def view_pdf(doc_id: str, db: AsyncSession = Depends(get_db)):
    """View/preview a PDF file from MinIO in browser"""
    if not doc_id:
        raise HTTPException(
            status_code=400,
            detail="Document ID is missing"
        )

    try:
        pdf_data = await storage_crud.view_doc(doc_id)
        if not pdf_data:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        return StreamingResponse(
            io.BytesIO(pdf_data),
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={doc_id.split('/')[-1]}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document: {str(e)}"
        )

    

@router.get("/list/{user_id}",response_model=List[DocumentBase])
async def list_pdfs(user_id,db:AsyncSession=Depends(get_db)):
    """List all PDF files in MinIO"""
    
    try:
        doc_list=await document_crud.list(db,user_id)
        return doc_list
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{str(e)}")


@router.patch("/update/{document_id}", response_model=DocumentBase)
async def update_pdf(
    document_id: uuid.UUID,
    doc_in: DocumentUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        doc_obj = await document_crud.get(db, document_id)
        if doc_obj is None:
            raise HTTPException(
                status_code=404,
                detail=f"Document not found with id {document_id}"
            )
        
        updated_doc = await document_crud.update(db, doc_obj, doc_in)
        return updated_doc
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error during update: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.delete("/delete/{document_id}")
async def delete_pdf(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Get document first
        doc_obj = await document_crud.get(db, document_id)
        if doc_obj is None:
            raise HTTPException(
                status_code=404,
                detail=f"Document not found with id {document_id}"
            )
        
        file_path = doc_obj.file_path  # Store before deletion
        
        await document_crud.delete(db, document_id)
        
        try:
            storage_crud.delete_pdf(file_path)
        except Exception as storage_error:
            print(f"Warning: Storage deletion failed: {storage_error}")
        
        return {"message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")