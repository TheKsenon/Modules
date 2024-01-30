import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

BOT_TOKEN = '6869308437:AAGUE5NM7TgI7kSCJwFdpUid3UQqEx8QDNA'
DDOSXD_API_KEY = 'ddosxd-api-1jq4e9xbzu2ilgn'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['zephyr'])
async def zephyr_command(message: types.Message):
    await message.reply("[🎲] Ваш запрос отправлен. Ждём ответа!\n\nМы используем только быстрые модели!")

    # Your existing code to send request and get response
    data = {'model': 'zephyr', 'messages': [{'role': 'user', 'content': 'Привет'}]}
    headers = {'Authorization': DDOSXD_API_KEY}
    response = requests.post('https://api.ddosxd.ru/v1/chat', headers=headers, json=data)
    response_data = response.json()

    if response_data.get('status') == 200:
        reply_text = response_data.get('reply')
        await message.reply(reply_text, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(executor.start_polling(dp, skip_updates=True))
    loop.run_forever()
