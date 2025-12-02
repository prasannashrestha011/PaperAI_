
import uuid
from pydantic import BaseModel


class AskQuery(BaseModel):
    query:str 
    user_id:uuid.UUID
    document_id:uuid.UUID
