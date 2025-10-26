import asyncio
from app.db.database import Base, engine
from app.db.models import AnalysisLog  # noqa: F401


async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created in DB")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_all_tables())
