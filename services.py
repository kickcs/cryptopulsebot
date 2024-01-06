from db.requests import *
from config import config
import json
import asyncio
import requests
import csv


async def fetch_and_process_coins():
    # Загрузка списка символов
    with open('filtered_coins.json', 'r', encoding='utf-8') as file:
        filtered_coins = json.load(file)
    symbol_string = ','.join([coin['symbol'] for coin in filtered_coins.values()])

    # API запрос
    api_key = config.api_token.get_secret_value()
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
    parameters = {'symbol': symbol_string, 'convert': 'USD'}
    response = requests.get(url, headers=headers, params=parameters)

    # Обработка данных и сохранение в базу данных
    if response.status_code == 200:
        data = response.json()['data']
        tasks = [add_coins(coin_id=coin_data['id'],
                           symbol=coin_symbol,
                           slug=coin_data['slug'],
                           price=coin_data['quote']['USD']['price'],
                           date=coin_data['last_updated']) for coin_symbol, coin_data in data.items()]
        await asyncio.gather(*tasks)


async def get_delta_price(percent: int):
    # Чтение списка монет
    with open('coins.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        symbols = [row[0].strip() for row in csv_reader]

    results = {}

    for symbol in symbols:
        coins = await get_coins(symbol)
        if len(coins) >= 2:
            price_delta = round(coins[0].price - coins[1].price, 4)
            delta_percent = round((price_delta / coins[1].price) * 100, 1)
            slug = coins[0].slug
            if abs(delta_percent) > percent:
                price_change = f"{round(coins[1].price, 4)}->{round(coins[0].price, 4)}"
                results[symbol] = {'Price Change': price_change, 'Delta Price': price_delta,
                                   'Delta Percent': delta_percent, 'slug': slug}

    return results
