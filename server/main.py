from contextlib import asynccontextmanager
from fastapi import FastAPI
from server.api.auth import auth_router
from server.api.uploader import upload_router
from server.api.agent_session import session_router 
from fastapi.middleware.cors import CORSMiddleware
from server.agent.graph_store import kg_store 
origins = ["http://localhost:3000"]  # React dev server

@asynccontextmanager   
async def lifespan(app:FastAPI):
    await kg_store.initialize()
    yield
    await kg_store.driver.close()

app=FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # important for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(upload_router)
