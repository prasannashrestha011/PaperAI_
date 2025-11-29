

from datetime import  datetime,timezone
import uuid
from fastapi import APIRouter, File, HTTPException ,UploadFile
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_413_CONTENT_TOO_LARGE, HTTP_500_INTERNAL_SERVER_ERROR 
from pathlib import Path

upload_router=APIRouter(prefix="upload")

UPLOAD_DIR=Path("/uploads/pdfs")
UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
MAX_FILE_SIZE=10*1024*1024

class UploadModel(BaseModel):
    document_id:str
    user_id:str
    file_name:str
    file_path:str
    file_size:int
    uploaded_timestamp:str
        
@upload_router.post("/pdf",response_model=UploadModel,status_code=HTTP_201_CREATED)
async def upload_pdf(user_id:str,file:UploadFile=File(...,description="pdf file to upload")):
    if not user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid user id"
        )
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
        content=await file.read()
        file_size=len(content)
        if file_size>MAX_FILE_SIZE:
            raise HTTPException(
                status_code=HTTP_413_CONTENT_TOO_LARGE,
                detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE / (1024*1024)}MB"
            )
        user_path=UPLOAD_DIR/ user_id 
        user_path.mkdir(exist_ok=True,parents=True)
        document_id=uuid.uuid4().hex
        safe_filename=f"{user_id}-{document_id}"
        file_path=user_path/safe_filename

        try:
            with open(file_path,"wb") as f:
                f.write(content)
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Couldnot stored the file")
        uploaded_timestamp=datetime.now(timezone.utc).isoformat()

        return UploadModel(
            file_name=
        )


    except Exception as e:
        print(f"Error reading file:{e}")


