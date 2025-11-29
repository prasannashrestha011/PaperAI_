from fastapi import FastAPI
from api.auth import auth_router
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
origins = ["http://localhost:3000"]  # React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # important for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
