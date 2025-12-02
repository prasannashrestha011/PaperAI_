
import uuid

from sqlalchemy import select
from server.database.models import SessionModel
from server.schemas.request import SessionBody
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List, Optional

from server.schemas.response import SessionOut
class ChatSessionCRUD:
    def __init__(self) -> None:
        pass

    @staticmethod
    async def create_session(session_in:SessionBody,db:AsyncSession)->SessionOut:
        db_obj=SessionModel(**session_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    async def get_sessions(user_id:uuid.UUID,db:AsyncSession)->Optional[List[SessionModel]]:
        results=await db.execute(select(SessionModel).where(SessionModel.user_id==user_id))  
        return  list(results.scalars().all())

    @staticmethod
    async def delete_session(session_id:uuid.UUID,db:AsyncSession):
        result=await db.execute(select(SessionModel).where(SessionModel.session_id==session_id))
        db_obj=result.scalars().first()
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj



            


