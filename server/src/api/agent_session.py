import json
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED
from src.database.crud.agent_session import get_agent_session
from src.database.deps import get_db
from src.schemas.response import  AgentResponse, SessionOut
from src.schemas.request import SessionBody
from src.database.models import SessionModel
session_router=APIRouter(prefix="/agent/session")

@session_router.post("/create",response_model=SessionOut,status_code=HTTP_201_CREATED)
async def create_session(new_session:SessionBody,db:AsyncSession=Depends(get_db)):
    session_in=SessionModel(user_id=new_session.user_id,document_id=new_session.document_id,provider=new_session.provider,model=new_session.model)
    try:
        db.add(session_in)
        await db.commit()
        await db.refresh(session_in)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Session with this document_id already exists")

@session_router.post("/ask",response_model=AgentResponse)
async def get_agent(session_in:SessionBody,question:str=Body()):
    agent=await get_agent_session(**session_in.model_dump())
    if agent:
        response=await agent.answer_question(question)
        return response["answer"]
    else:
        raise  HTTPException(status_code=500,detail="Failed to initialize the agent response")
    



        

