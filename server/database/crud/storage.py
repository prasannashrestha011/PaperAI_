

from datetime import  datetime,timezone
import uuid
from fastapi import HTTPException, UploadFile
from starlette.status import HTTP_413_CONTENT_TOO_LARGE
from  server.database.supabase_client import supabase
from server.schemas.document import DocumentCreate

BUCKET_NAME = "pdfs" 
MAX_FILE_SIZE=10*1024*1024

class StorageCRUD:
    def __init__(self) -> None:
        pass

    async def upload_pdf(self,user_id:uuid.UUID,uploaded_file:UploadFile)->DocumentCreate | None:
        try:
            if uploaded_file.filename is None:
                raise ValueError("Uploaded file has no file name")
            file_name=uploaded_file.filename.strip() 
            document_id=uuid.uuid4()
            file_content=await uploaded_file.read()
            file_size=len(file_content)

            if file_size>MAX_FILE_SIZE:
                raise HTTPException( 
                status_code=HTTP_413_CONTENT_TOO_LARGE,
                detail="File size exceeded")

            file_path=f"{user_id}/{document_id}/{file_name}"

            supabase.storage.from_(BUCKET_NAME).upload(file_path,file_content)

            public_url=supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)

            doc_in=DocumentCreate(
                user_id=user_id,
                document_id=document_id,
                file_name=file_name,
                file_path=public_url, 
                upload_timestamp=datetime.now(timezone.utc),
                file_size=file_size
            )
            return doc_in 

        except Exception as e:
            print(f"Bucket Upload error: {e}")

    def delete_pdf(self,file_path:str):
         try:
            response=supabase.storage.from_(BUCKET_NAME).remove([file_path])
         except Exception as e:
            print(f"Bucket Deletiton error:{e}")

