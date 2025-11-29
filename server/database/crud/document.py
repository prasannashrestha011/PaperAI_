        
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from models import DocumentModel
from schemas.document import DocumentCreate, DocumentUpdate 

class DocumentCRUD:
   def __init__(self,model) -> None:
        self.model=model

   def create(self,db:Session,obj_in:DocumentCreate)->DocumentModel:
        db_obj=self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
   def get(self,db:Session,document_id:UUID)->Optional[DocumentModel]:
        doc_obj=db.query(self.model).filter(self.model.document_id==document_id).first()
        return doc_obj

   def list(self,db:Session,user_id:UUID)->Optional[List[DocumentModel]]:
        docs_obj=db.query(self.model).filter(self.model.user_id==user_id).all()
        return docs_obj

   def update(self,db:Session,doc_obj:DocumentModel,obj_in:DocumentUpdate)->DocumentModel:
        update_data=obj_in.model_dump(exclude_unset=True)
        for field,value in update_data:
            setattr(doc_obj,field,value)
        db.commit()
        db.refresh(doc_obj)
        return doc_obj

   def delete(self, db: Session, document_id: UUID) -> Optional[DocumentModel]:
        obj = db.query(self.model).filter(self.model.document_id == document_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

       

    

