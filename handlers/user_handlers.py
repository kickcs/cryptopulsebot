from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.apsched import send_message, send_price_message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, scheduler: AsyncIOScheduler):
    user_id = message.from_user.id
    await message.answer("Привет! Я бот для отслеживания изменения цены монеты.")


@router.message(Command('coins'))
async def cmd_coins(message: Message, bot: Bot, scheduler: AsyncIOScheduler):
    user_id = message.from_user.id
    await send_price_message(bot, user_id)
    scheduler.add_job(send_price_message,
                      'interval',
                      minutes=15,
                      kwargs={'bot': bot,
                              'chat_id': user_id})
