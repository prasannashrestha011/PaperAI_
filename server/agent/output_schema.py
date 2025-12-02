"""
-Output structure schema 
The LLM follows this schema to generate the final output
"""

from typing import TypedDict,List
class KnowledgeGraphAnswer(TypedDict):
    query_type: str 
    entities: List[str]  
    core_definition: str 
    applications: str  
    answer: str  
    confidence: str  # high, medium, low
    citation: List[str] 
    follow_up_questions:List[str]
    answer_type:str # LLM parametric knowledge | knowledge graph source
    tool_called:List[str]
