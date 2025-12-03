


from typing import List
import uuid
from pydantic import BaseModel

from src.schemas.document import DocumentBase



class AgentResponse(BaseModel):
    query_type: str 
    entities: List[str]  
    core_definition: str 
    applications: str  
    answer: str  
    confidence: str      
    citation: List[str] 
    follow_up_questions:List[str]
    answer_type:str 
    tool_called:List[str]

    model_config={
        "from_attributes":True
    }

class SessionOut(BaseModel):
      session_id:uuid.UUID
      user_id:uuid.UUID
      document_id:uuid.UUID
      provider:str
      model:str
      model_config={
            "from_attributes":True
    }
      
        
    
class ExtractionResponse(BaseModel):
      doc_out: DocumentBase
      session_out:SessionOut

