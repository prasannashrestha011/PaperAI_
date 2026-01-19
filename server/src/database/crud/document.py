from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from typing import List, Optional

from src.schemas.document import DocumentBase, DocumentCreate, DocumentUpdate 

class DocumentCRUD:
   def __init__(self,model) -> None:
        self.model=model

   async def create(self,db:AsyncSession,obj_in:DocumentCreate)->DocumentBase:
        db_obj=self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
   async def get(self,db:AsyncSession,document_id:UUID)->Optional[DocumentBase]:
        doc_obj=await db.execute(select(self.model).where(self.model.document_id==document_id))
        return doc_obj.scalars().first()

   async def list(self,db:AsyncSession,user_id:UUID)->Optional[List[DocumentBase]]:
        docs_obj=await db.execute(select(self.model).where(self.model.user_id==user_id))
        docs=docs_obj.scalars().all()
        if not docs_obj:
             raise ValueError("Document list is empty")
        return list(docs) 

   async def update(
     self,
     db: AsyncSession,
     doc_obj: DocumentBase,
     obj_in: DocumentUpdate
     ) -> DocumentBase:
     # Get only the fields that were set
     update_data = obj_in.model_dump(exclude_unset=True)
     
     if not update_data:
          raise ValueError("No fields provided for update")
     
     # Update fields
     for field, value in update_data.items():
          if hasattr(doc_obj, field):
               setattr(doc_obj, field, value)
     
     try:
          await db.commit()
          await db.refresh(doc_obj)
     except SQLAlchemyError:
          await db.rollback()
          raise
     
     return doc_obj

   async def delete(self, db: AsyncSession, document_id: UUID) -> Optional[DocumentBase]:
        result=await db.execute(select(self.model).where(self.model.document_id==document_id))
        doc_obj=result.scalars().first()
        if doc_obj:
           await db.delete(doc_obj)
           await db.commit()
        return doc_obj

    

