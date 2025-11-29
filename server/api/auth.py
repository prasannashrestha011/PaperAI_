# auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from  database.models import  User
from database.deps import get_db
from utils.hashing import hash_password, verify_password
from utils.jwt import create_access_token
auth_router = APIRouter()
class UserCreate(BaseModel):
    username: str
    password: str

@auth_router.post("/auth/create")
async def create_user(new_user: UserCreate, db: AsyncSession = Depends(get_db)):

    hashed_password=hash_password(new_user.password)
    user = User(username=new_user.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return {"id": user.id, "username": user.username}

@auth_router.post("/auth/login")
async def login_user(user:UserCreate,res:Response,db:AsyncSession=Depends(get_db)):
    result=await db.execute(select(User).where(User.username==user.username))
    db_user=result.scalars().first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not verify_password(user.password,str(db_user.password)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect password"
        )
    token = create_access_token({"user_id": str(db_user.id)})
    res.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  
        samesite="lax",
        max_age=60*60,  # 1 hour
    )
    return {"id": db_user.id, "username": db_user.username, "message": "Login successful"}


