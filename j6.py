from aiogram import Bot, Dispatcher, executor, types

# Замените TOKEN на ваш токен бота
API_TOKEN = '6513902650:AAHHMflFfFl31nKmbWW65xRuY14GNzoRvRE'

# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправьте мне сообщение и сделайте реплей на него с командой /id, чтобы получить id пользователя.")

# Обработчик команды /id с реплеем
@dp.message_handler(commands=['id'], is_reply=True)
async def get_user_id(message: types.Message):
    # Получаем id пользователя, на сообщение которого сделали реплей
    replied_user_id = message.reply_to_message.from_user.id
    
    # Формируем ответ
    reply_text = f"ID: {replied_user_id}"
    
    # Отправляем ответ
    await message.reply(reply_text)

# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
