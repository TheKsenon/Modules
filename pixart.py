import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import asyncio

API_KEY = 'ddosxd-api-1jq4e9xbzu2ilgn'
bot_token = '6869308437:AAGUE5NM7TgI7kSCJwFdpUid3UQqEx8QDNA'  # Replace with your bot token
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['pixart'])
async def pixart_command(message: types.Message):
    try:
        prompt = message.get_args()
        if not prompt:
            await message.reply("Please provide a prompt after /pixart command.")
            return

        await message.reply("[🪄] Ваше изображение уже готово 🔥")

        data = {
            'model': 'pixart',
            'prompt': prompt
        }

        response = requests.post('https://api.ddosxd.ru/v1/image', headers={'Authorization': API_KEY}, json=data)
        image_url = response.json()['photos'][0]

        await bot.send_photo(message.chat.id, photo=image_url)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True
