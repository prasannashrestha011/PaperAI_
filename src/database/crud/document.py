from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from uuid import UUID
from typing import List, Optional

from src.database.models import DocumentModel
from src.schemas.document import DocumentCreate, DocumentUpdate 

class DocumentCRUD:
   def __init__(self,model) -> None:
        self.model=model

   async def create(self,db:AsyncSession,obj_in:DocumentCreate)->DocumentModel:
        db_obj=self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
   async def get(self,db:AsyncSession,document_id:UUID)->Optional[DocumentModel]:
        doc_obj=await db.execute(select(self.model).where(self.model.document_id==document_id))
        return doc_obj.scalars().first()

   async def list(self,db:AsyncSession,user_id:UUID)->Optional[List[DocumentModel]]:
        docs_obj=await db.execute(select(self.model).where(self.model.user_id==user_id))
        return list(docs_obj.scalars().all()) 

   async def update(self,db:AsyncSession,doc_obj:DocumentModel,obj_in:DocumentUpdate)->DocumentModel:
        update_data=obj_in.model_dump(exclude_unset=True)
        for field,value in update_data:
            setattr(doc_obj,field,value)
        await db.commit()
        await db.refresh(doc_obj)
        return doc_obj

   async def delete(self, db: AsyncSession, document_id: UUID) -> Optional[DocumentModel]:
        result=await db.execute(select(self.model).where(self.model.document_id==document_id))
        doc_obj=result.scalars().first()
        if doc_obj:
           await db.delete(doc_obj)
           await db.commit()
        return doc_obj

    

