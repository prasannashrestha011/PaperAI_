from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")       # "user"
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") # "9843"
POSTGRES_DB = os.getenv("POSTGRES_DB")           # "mydb"

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5433/{POSTGRES_DB}"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True,
 connect_args={
        "ssl":False,
        "timeout": 30,
        "command_timeout": 30,
    })

# Correct async session using async_sessionmaker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base for models
Base = declarative_base()
