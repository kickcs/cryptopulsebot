import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from middlewares.db import DbSessionMiddleware
from middlewares.scheduler import SchedulerMiddleware
from db.models import sessionmaker, create_tables
from handlers import user_handlers

from services import fetch_and_process_coins
from config import config

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    logging.info('Starting bot')

    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_and_process_coins, 'interval', minutes=15)
    scheduler.start()
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.update.middleware(SchedulerMiddleware(scheduler=scheduler))
    dp.include_router(user_handlers.router)

    await create_tables()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
