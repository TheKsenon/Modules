import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '6869308437:AAGUE5NM7TgI7kSCJwFdpUid3UQqEx8QDNA'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['sdxl'])
async def process_sdxl_command(message: types.Message):
    try:
        # Получаем prompt из команды пользователя
        prompt = message.text.split('/sdxl ', 1)[1]
        
        # Отправляем запрос на указанный сервер с использованием prompt
        response = requests.post("https://opo.k.vu/private/apis/sdxl", json={"prompt": prompt})
        
        # Получаем URL изображения из ответа
        image_url = response.json().get('url')
        
        # Отправляем изображение пользователю
        await bot.send_photo(message.chat.id, photo=image_url)
    
    except Exception as e:
        # Если произошла ошибка, отправляем сообщение с описанием ошибки
        await message.reply(f"Произошла ошибка: {str(e)}", parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
