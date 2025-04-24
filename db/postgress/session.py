from sqlalchemy.ext.asyncio import async_sessionmaker
from db.postgress.config import engine

AsuncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)