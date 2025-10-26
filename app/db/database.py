from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()

# ---------------------------
# DB URL 定義
# ---------------------------
DB_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 5432)}/{os.getenv('DB_NAME')}"
)

# ---------------------------
# エンジン・セッション生成
# ---------------------------
engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# ---------------------------
# DI用セッション生成
# ---------------------------
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
