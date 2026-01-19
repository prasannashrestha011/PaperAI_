
import io
from datetime import  datetime,timezone
import uuid
from fastapi import HTTPException, UploadFile
from datetime import timedelta
from minio import S3Error
from starlette.status import HTTP_413_CONTENT_TOO_LARGE
from src.schemas.document import DocumentCreate,DocumentOut
from src.database.minio_client import client,MINIO_BUCKET
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

            client.put_object(
                bucket_name=MINIO_BUCKET,
                object_name=file_path,
                data=io.BytesIO(file_content),
                length=len(file_content),
                content_type="pdf"
            )

            url = client.presigned_get_object(
                MINIO_BUCKET,
                file_path,
                expires=timedelta(hours=1)
            )

            doc_in=DocumentCreate(
                user_id=user_id,
                document_id=document_id,
                file_name=file_name,
                 file_path=url, 
                upload_timestamp=datetime.now(timezone.utc),
                file_size=file_size
            )
            return doc_in 

        except Exception as e:
            print(f"Bucket Upload error: {e}")

    async def list_docs(user_id:str)->DocumentOut:

        objects = client.list_objects(
            MINIO_BUCKET,
            prefix=f"{user_id}/",
            recursive=True
        )
        
        pdf_list = []
        for obj in objects:
            pdf_list.append({
                "filename": str(obj.object_name).split("/")[-1],
                "filePath":obj.object_name,
                "size": obj.size,
                "last_modified": obj.last_modified,
            })
        
        return {
            "bucket": MINIO_BUCKET,
            "count": len(pdf_list),
            "pdfs": pdf_list
        }
    def delete_pdf(self,file_path:str):
        try:
            client.remove_object(MINIO_BUCKET, file_path)
            
            return {
                "message": "PDF deleted successfully",
                "filename": file_path 
            }
        
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")