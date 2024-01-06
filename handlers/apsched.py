from aiogram import Bot
from services import get_delta_price

async def send_message(bot: Bot, chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=text)


async def send_price_message(bot: Bot, chat_id: int):
    coins = await get_delta_price(5)
    if not coins:
        return  # Завершить функцию, если нет значительных изменений

    message_lines = ['<b>📈 Price Updates:</b>']
    for symbol, data in coins.items():
        emoji = '🔴' if data["Delta Price"] < 0 else '🟢'
        message_line = (f'{emoji} <b><a href="https://coinmarketcap.com/ru/currencies/{data["slug"]}">{symbol}</a></b>:'
                        f' {data["Price Change"]} - <i>{data["Delta Percent"]}%</i>')
        message_lines.append(message_line)

    message = "\n".join(message_lines)
    await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML', disable_web_page_preview=True)





