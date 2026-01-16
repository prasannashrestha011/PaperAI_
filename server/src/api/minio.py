from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from minio import Minio
from minio.error import S3Error
import io

router = APIRouter(prefix="/pdf", tags=["PDF Storage"])

# MinIO client configuration
minio_client = Minio(
    "localhost:9000",
    access_key="minio",
    secret_key="minio123",
    secure=False
)

BUCKET_NAME ="paperaibucket"

# Create bucket if it doesn't exist
def ensure_bucket_exists():
    try:
        if not minio_client.bucket_exists(BUCKET_NAME):
            minio_client.make_bucket(BUCKET_NAME)
            print(f"Bucket '{BUCKET_NAME}' created successfully")
    except S3Error as e:
        print(f"Error creating bucket: {e}")

ensure_bucket_exists()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file to MinIO"""
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        content = await file.read()
        content_size = len(content)
        
        minio_client.put_object(
            BUCKET_NAME,
            file.filename,
            io.BytesIO(content),
            content_size,
            content_type="application/pdf"
        )
        
        return {
            "message": "PDF uploaded successfully",
            "filename": file.filename,
            "size": content_size,
            "bucket": BUCKET_NAME
        }
    
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.get("/download/{filename}")
async def download_pdf(filename: str):
    """Download a PDF file from MinIO"""
    
    try:
        response = minio_client.get_object(BUCKET_NAME, filename)
        pdf_data = response.read()
        
        return StreamingResponse(
            io.BytesIO(pdf_data),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except S3Error as e:
        if e.code == "NoSuchKey":
            raise HTTPException(status_code=404, detail=f"PDF '{filename}' not found")
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")
    finally:
        response.close()
        response.release_conn()


@router.get("/list")
async def list_pdfs():
    """List all PDF files in MinIO"""
    
    try:
        objects = minio_client.list_objects(BUCKET_NAME)
        
        pdf_list = []
        for obj in objects:
            pdf_list.append({
                "filename": obj.object_name,
                "size": obj.size,
                "last_modified": obj.last_modified
            })
        
        return {
            "bucket": BUCKET_NAME,
            "count": len(pdf_list),
            "pdfs": pdf_list
        }
    
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")

@router.get("/view/{filename}")
async def view_pdf(filename: str):
    """View/preview a PDF file from MinIO in browser"""
    
    try:
        response = minio_client.get_object(BUCKET_NAME, filename)
        pdf_data = response.read()
        
        return StreamingResponse(
            io.BytesIO(pdf_data),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={filename}"
            }
        )
    
    except S3Error as e:
        if e.code == "NoSuchKey":
            raise HTTPException(status_code=404, detail=f"PDF '{filename}' not found")
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error viewing file: {str(e)}")
    finally:
        response.close()
        response.release_conn()
@router.delete("/delete/{filename}")
async def delete_pdf(filename: str):
    """Delete a PDF file from MinIO"""
    
    try:
        minio_client.remove_object(BUCKET_NAME, filename)
        
        return {
            "message": "PDF deleted successfully",
            "filename": filename
        }
    
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")