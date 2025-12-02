from datetime import datetime,timezone
import uuid
from sqlalchemy import Column,UUID, Integer,String ,ForeignKey,Text,DateTime
from sqlalchemy.orm import relationship
from server.database.database import Base

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
    document_id=Column(UUID,primary_key=True)
    user_id=Column(UUID,index=True,nullable=False)
    file_name=Column(String,nullable=False)
    file_path=Column(String,nullable=False,unique=True)
    file_size=Column(Integer,nullable=False)
    upload_timestamp=Column(String,nullable=False)

class SessionModel(Base):
    __tablename__="sessions"
    session_id=Column(UUID,primary_key=True)
    user_id=Column(UUID,nullable=False)
    document_id=Column(UUID,nullable=False,unique=True)
    provider=Column(String,nullable=False)
    model=Column(String,nullable=False)
    created_at=Column(String,nullable=False)
    chat_history=relationship("ChatHistory",back_populates="session",cascade="all, delete-orphan")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    conversation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id"), nullable=False)
    message = Column(Text, nullable=False)
    role = Column(String, nullable=False)  # "user" or "assistant"
    created_at = Column(DateTime, default=datetime.now(timezone.utc).isoformat(), nullable=False)
    session = relationship("SessionModel", back_populates="chat_history")


