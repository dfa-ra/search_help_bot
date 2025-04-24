import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


load_dotenv(dotenv_path="/media/ra/_work/ra/QUESTIONABLE PROJECTS/help_search_bot/.env")

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

DB_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

engine = create_async_engine(DB_URL, echo=True)

async_session_factory: sessionmaker[AsyncSession] = sessionmaker(
    bind = engine,
    expire_on_commit = False,
    class_ = AsyncSession
)
