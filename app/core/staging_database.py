from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# print("="*50)
# print(f"DATABASE URL YANG TERBACA: ->{DATABASE_URL}<-")
# print("="*50)


# DATABASE_URL = "sqlite+aiosqlite:///./gateway.db"



# Async Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)


# Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Base ORM Model
class Base(DeclarativeBase):
    pass


# Dependency Injection
async def get_db():

    async with AsyncSessionLocal() as session:
        yield session