from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class DocumentBase(BaseModel):
    user_id: UUID
    document_id:UUID
    file_name: str
    file_path: str
    file_size: int
    upload_timestamp: datetime  

    model_config={
        "from_attributes":True
    }

class DocumentCreate(DocumentBase):
    pass  # all fields required for creation are already in DocumentBase

class DocumentUpdate(BaseModel):
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    upload_timestamp: Optional[datetime] = None

class DocumentOut(DocumentBase):
    class Config:
         from_attributes= True
