import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from  src.database.models import UserModel 
from src.database.deps import get_db
from src.schemas.user import UserResponse
from src.utils.hashing import hash_password, verify_password
from src.utils.jwt import create_access_token
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR
auth_router = APIRouter()
class UserCreate(BaseModel):
    username: str
    password: str

@auth_router.post("/auth/register")
async def create_user(new_user: UserCreate, db: AsyncSession = Depends(get_db)):

    hashed_password=hash_password(new_user.password)
    user = UserModel(username=new_user.username, password=hashed_password)
    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
    except IntegrityError as e:
        await db.rollback()
        if "unique constraint" in str(e.orig):
            raise HTTPException(status_code=400,detail="Username already exists")
        raise
    return {"id": user.user_id, "username": user.username}

@auth_router.post("/auth/login")
async def login_user(user:UserCreate,res:Response,db:AsyncSession=Depends(get_db)):
    result=await db.execute(select(UserModel).where(UserModel.username==user.username))
    db_user:UserModel=result.scalars().first()
    print(db_user)
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
    token = create_access_token({"user_id": str(db_user.user_id)})
    res.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  
        samesite="lax",
        max_age=60*60,  # 1 hour
    )
    return {"id": db_user.user_id, "username": db_user.username, "message": "Login successful"}

@auth_router.get("/auth/me", response_model=UserResponse)
async def get_me(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await db.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user