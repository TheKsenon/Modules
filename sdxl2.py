import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '6869308437:AAGUE5NM7TgI7kSCJwFdpUid3UQqEx8QDNA'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['sdxl'])
async def process_sdxl_command(message: types.Message):
    prompt = message.text.split('/sdxl ', 1)[1]
    
    # Отправляем сообщение "Изображение готовится"
    msg_processing = await message.reply(f"Изображение по запросу '{prompt}' готовится...")

    while True:
        try:
            # Отправляем запрос на сервер с использованием prompt
            response = requests.post("https://opo.k.vu/private/apis/sdxl", json={"prompt": prompt})
            
            # Проверяем успешность запроса
            response.raise_for_status()
            
            # Получаем URL изображения из ответа
            image_url = response.json().get('url')
            
            # Отправляем изображение пользователю
            await bot.send_photo(message.chat.id, photo=image_url)
            
            # Удаляем сообщение "Изображение готовится"
            await msg_processing.delete()
            
            # Уведомляем пользователя о завершении
            await message.reply(f"Ваше изображение по запросу '{prompt}' готово.")
            break
        
        except requests.exceptions.RequestException as req_err:
            # Если произошла ошибка запроса, удаляем предыдущее сообщение с ошибкой
            await msg_processing.delete()
            
            # Отправляем новое сообщение "Изображение готовится"
            msg_processing = await message.reply(f"Изображение по запросу '{prompt}' готовится...")

            # Пропускаем остальной код, чтобы не отправлять сообщение об ошибке
            continue

        except Exception as e:
            # Если произошла другая ошибка, отправляем сообщение с описанием ошибки
            await message.reply(f"Произошла ошибка: {str(e)}", parse_mode=ParseMode.MARKDOWN)
            break

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
