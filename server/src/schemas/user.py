
from datetime import datetime
import uuid
from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id:uuid.UUID
    username:str
    created_at:datetime
    model_config={
        "from_attributes":True
    }