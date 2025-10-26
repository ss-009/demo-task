import asyncio
import os
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_session
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv

load_dotenv()


# ---------------------------
# DB URL 定義
# ---------------------------
DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 5432)}/{os.getenv('TEST_DB_NAME')}"
)

# ---------------------------
# エンジン・セッション生成
# ---------------------------
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# ---------------------------
# DI用セッション生成
# ---------------------------
@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session


# ---------------------------
# イベントループ
# ---------------------------
@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


# ---------------------------
# テーブル作成
# ---------------------------
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# ---------------------------
# TestClient
# ---------------------------
@pytest_asyncio.fixture
def client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()
