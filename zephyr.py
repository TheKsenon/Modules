import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor
import requests

API_KEY = 'ddosxd-api-1jq4e9xbzu2ilgn'
BOT_TOKEN = '6725080732:AAH25qXr1SpMS8M8YoHyxuIcfuu7hyHGGT4'
ZEPHYR_API_URL = 'https://api.ddosxd.ru/v1/chat'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['zephyr'])
async def zephyr_command(message: types.Message):
    content = message.get_args()
    if content:
        headers = {'Authorization': API_KEY}
        data = {'model': 'zephyr', 'messages': [{'role': 'user', 'content': content}]}

        response = requests.post(ZEPHYR_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            reply_text = response.json().get('reply', '')
            await message.reply(reply_text, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.reply(f'Ошибка запроса: {response.status_code}')
    else:
        await message.reply('Пожалуйста, введите текст для отправки модели Zephyr.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True
