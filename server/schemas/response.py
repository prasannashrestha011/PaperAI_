


from typing import List
from pydantic import BaseModel


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
