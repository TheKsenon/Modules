import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import requests

API_KEY = 'ddosxd-api-1jq4e9xbzu2ilgn'
headers = {'Authorization': API_KEY}

API_URL = 'https://api.ddosxd.ru/v1/chat'

logging.basicConfig(level=logging.INFO)

bot = Bot(token='6869308437:AAGUE5NM7TgI7kSCJwFdpUid3UQqEx8QDNA')
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['gpt35'])
async def generate_response(message: types.Message):
    prompt = message.get_args()
    
    data = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': prompt}]}
    response = requests.post(API_URL, headers=headers, json=data)
    
    try:
        response_json = response.json()
        generated_text = response_json['reply']
        result_text = f"[🪄] Ваш ответ уже готов 🔥\n{generated_text}"
    except KeyError:
        result_text = "Не удалось получить ответ от модели."

    await message.reply(result_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
