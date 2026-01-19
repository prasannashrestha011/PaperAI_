from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.document import router as upload_router 
from src.api.auth import auth_router
from fastapi.middleware.cors import CORSMiddleware
from .middleware import JWTMiddleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

"""
@asynccontextmanager   
async def lifespan(app:FastAPI):
    await kg_store.initialize()
    yield
    await kg_store.driver.close()



"""
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # important for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(JWTMiddleware)
app.include_router(upload_router)
app.include_router(auth_router)