from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED
from src.database.deps import get_db
from src.schemas.response import  SessionOut
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
        
