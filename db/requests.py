from db.models import Coins, sessionmaker
from sqlalchemy import select, desc
from datetime import datetime
import pytz


async def add_coins(coin_id: int, symbol: str, slug: str, price: float, date: str):
    async with sessionmaker() as session:
        date = datetime.fromisoformat(date.rstrip('Z')).replace(tzinfo=pytz.UTC)
        coin = Coins(coin_id=coin_id, symbol=symbol, slug=slug, price=price, date=date)
        session.add(coin)
        await session.commit()


async def get_coins(symbol: str):
    async with sessionmaker() as session:
        coin = await session.execute(select(Coins).where(Coins.symbol == symbol).order_by(desc(Coins.date)).limit(2))
        return coin.scalars().all()
