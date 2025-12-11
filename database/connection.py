from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import SETTINGS
from database.models import Base
import logging

logger = logging.getLogger(__name__)

engine = create_async_engine(
    SETTINGS.DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """Инициализировать базу данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ База данных инициализирована")

async def get_db_session():
    """Получить сессию БД"""
    async with async_session() as session:
        yield session
