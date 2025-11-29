import uuid
from sqlalchemy import Column,UUID, Integer,String 

from database.database import Base

def uuid_no_dash():
    return uuid.uuid4().hex   # removes dashes

document_id = Column(String(32), primary_key=True, default=uuid_no_dash)
class User(Base):
    __tablename__="user"
    id=Column(UUID,primary_key=True,index=True,default=uuid_no_dash)
    username=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)

class DocumentModel(Base):
    __tablename__="documents"
    document_id=Column(UUID,primary_key=True,index=True)
    file_name=Column(String,nullable=False)
    file_path=Column(String,nullable=False,unique=True)
    file_size=Column(Integer,nullable=False)
    upload_timestamp=Column(String,nullable=False)

