from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.deep_agent import deep_agent_router 
from src.api.auth import auth_router
from src.api.uploader import upload_router
from src.api.agent_session import session_router 
from fastapi.middleware.cors import CORSMiddleware
# from src.agent.graph_store import kg_store 
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
app.include_router(deep_agent_router)
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(session_router)
