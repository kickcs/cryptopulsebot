from sqlalchemy import BigInteger, String, Date, Float, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import config

engine = create_async_engine(url=config.db_url, echo=True)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Coins(Base):
    __tablename__ = 'coins'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    coin_id: Mapped[int] = mapped_column(BigInteger)
    symbol: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    date: Mapped[str] = mapped_column(TIMESTAMP)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

