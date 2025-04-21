from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

user = "roma"
password = "1122"
host = "localhost"
port = "5432"
database = "test_my_tg_bot"

DB_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

engine = create_async_engine(DB_URL, echo=True)

async_session_factory: sessionmaker[AsyncSession] = sessionmaker(
    bind = engine,
    expire_on_commit = False,
    class_ = AsyncSession
)
