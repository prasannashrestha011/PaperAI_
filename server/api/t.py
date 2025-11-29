
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel
import uuid
from pathlib import Path
from datetime import datetime,timezone

# Create router
router = APIRouter(prefix="/upload", tags=["upload"])

# Configuration
UPLOAD_DIR = Path("uploads/pdfs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Response models
class UploadResponse(BaseModel):
    document_id: str
    user_id: str
    filename: str
    file_path: str
    file_size: int
    upload_timestamp: str
    message: str

class ErrorResponse(BaseModel):
    detail: str
    error_code: str


@router.post("/pdf", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    user_id: str = Form(..., description="User ID"),
    file: UploadFile = File(..., description="PDF file to upload")
):
    """
    Upload a PDF file with user details.
    
    - **user_id**: The ID of the user uploading the file
    - **file**: PDF file (max 10MB)
    
    Returns document_id and file details
    """
    # Validate file type
    if not file.content_type == "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename missing"
        )   
        # Validate file extension
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must have .pdf extension"
        )
    
    # Read file content
    try:
        content = await file.read()
        file_size = len(content)
        
        # Validate file size
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error reading file: {str(e)}"
        )
    
    # Generate unique document ID
    document_id = str(uuid.uuid4())
    
    # Create safe filename: document_id_original_name.pdf
    safe_filename = f"{document_id}_{file.filename}"
    file_path = UPLOAD_DIR / safe_filename
    
    # Create user-specific directory
    user_dir = UPLOAD_DIR / user_id
    user_dir.mkdir(parents=True, exist_ok=True)
    file_path = user_dir / safe_filename
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Get timestamp
    upload_timestamp = datetime.now(timezone.utc).isoformat()
    
    # Return response
    return UploadResponse(
        document_id=document_id,
        user_id=user_id,
        filename=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        upload_timestamp=upload_timestamp,
        message="PDF uploaded successfully"
    )


@router.get("/document/{document_id}")
async def get_document_info(document_id: str):
    """
    Get information about an uploaded document.
    """
    # Search for the document in all user directories
    for user_dir in UPLOAD_DIR.iterdir():
        if user_dir.is_dir():
            for file_path in user_dir.glob(f"{document_id}_*"):
                if file_path.is_file():
                    stat = file_path.stat()
                    return {
                        "document_id": document_id,
                        "filename": file_path.name.split("_", 1)[1],
                        "file_path": str(file_path),
                        "file_size": stat.st_size,
                        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat()
                    }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Document with ID {document_id} not found"
    )


@router.delete("/document/{document_id}")
async def delete_document(document_id: str):
    """
    Delete an uploaded document.
    """
    # Search for the document in all user directories
    for user_dir in UPLOAD_DIR.iterdir():
        if user_dir.is_dir():
            for file_path in user_dir.glob(f"{document_id}_*"):
                if file_path.is_file():
                    try:
                        file_path.unlink()
                        return {
                            "message": "Document deleted successfully",
                            "document_id": document_id
                        }
                    except Exception as e:
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error deleting file: {str(e)}"
                        )
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Document with ID {document_id} not found"
    )


@router.get("/user/{user_id}/documents")
async def list_user_documents(user_id: str):
    """
    List all documents uploaded by a specific user.
    """
    user_dir = UPLOAD_DIR / user_id
    
    if not user_dir.exists():
        return {"user_id": user_id, "documents": []}
    
    documents = []
    for file_path in user_dir.glob("*.pdf"):
        # Extract document_id from filename
        document_id = file_path.stem.split("_")[0]
        stat = file_path.stat()
        
        documents.append({
            "document_id": document_id,
            "filename": "_".join(file_path.stem.split("_")[1:]) + ".pdf",
            "file_size": stat.st_size,
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat()
        })
    
    return {
        "user_id": user_id,
        "total_documents": len(documents),
        "documents": documents
    }
