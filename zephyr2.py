import asyncio
import aiogram
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram import executor
from aiogram.types import ContentType
import requests

API_TOKEN = '6869308437:AAGUE5NM7TgI7kSCJwFdpUid3UQqEx8QDNA'

# Замените YOUR_BOT_API_TOKEN на реальный токен вашего бота

prodia_model = "Realistic Vision V2"  # Выбранная модель
prompt_text = "[🪄] Ваше изображение уже готово 🔥\nМы используем самую быструю модель для вашего использования."

# Инициализация бота и диспетчера
bot = aiogram.Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['rv2'])
async def process_rv2_command(message: types.Message):
    # Получаем аргументы из команды
    args = message.get_args()

    # Проверяем, есть ли аргументы
    if not args:
        await message.reply("Вы не указали текст в команде /rv2.")
        return

    # Подготавливаем запрос к Prodia API
    prodia_url = "https://api.prodia.com/generate"
    data = {
        "new": "true",
        "prompt": args,
        "model": "realistic-vision-2.safetensors [79587710]",
        "seed": 42,  # Вы можете выбрать любое значение здесь
        "aspect_ratio": "square",
    }

    # Отправляем запрос к Prodia API
    response = requests.get(prodia_url, params=data)
    job_id = response.json().get("job")

    # Ожидаем завершения генерации изображения
    while True:
        response = requests.get(f"https://api.prodia.com/job/{job_id}")
        status = response.json().get("status")
        if status == "succeeded":
            break
        await asyncio.sleep(0.15)

    # Отправляем текстовое сообщение и изображение пользователю
    await message.reply(prompt_text)
    image_url = f"https://images.prodia.xyz/{job_id}.png"
    await bot.send_photo(message.chat.id, photo=image_url)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
