import uuid
from sqlalchemy import Column,UUID,String 
from database.database import Base
class User(Base):
    __tablename__="user"
    id=Column(UUID,primary_key=True,index=True,default=uuid.uuid4)
    username=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    
