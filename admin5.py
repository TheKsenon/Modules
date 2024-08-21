from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode, InputFile
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageIsTooLong
import os
import subprocess
import threading
import tempfile

API_TOKEN = '6946709273:AAHbbJhpiUOuZG5ALc454hY0aNw6gw1Vhow'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

ALLOWED_USER_IDS = {7371775495, 5343627430}
ADMINS = {7371775495, 5343627430}

def run_command_with_timeout(command, timeout=5):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
        return result.stdout or result.stderr or "Команда выполнена успешно без ответа."
    except subprocess.TimeoutExpired:
        return "⌛ Команда превысила время выполнения."

@dp.message_handler(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("🧑‍💻 Бот для выполнения команд на VPS. ")

@dp.message_handler(Command('os'))
async def execute_os_command(message: types.Message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("🚫 У тебя нету прав для выполнения этой команды!")
        return

    command = message.get_args()
    if not command:
        await message.reply("‼️ Укажи команду для выполнения. ")
        return

    def run_command():
        return run_command_with_timeout(command)

    result_thread = threading.Thread(target=run_command)
    result_thread.start()
    result_thread.join(timeout=5)

    if result_thread.is_alive():
        await message.reply("⌛ Команда превысила время выполнения.")
    else:
        result = run_command()
        try:
            await message.reply(f"Результат выполнения команды:\n```\n{result}\n```", parse_mode=ParseMode.MARKDOWN)
        except MessageIsTooLong:
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt', prefix='logs_', dir='.') as temp_file:
                temp_file.write(result)
                temp_file_path = temp_file.name
            await message.reply_document(InputFile(temp_file_path, filename='logs.txt'))
            os.remove(temp_file_path)

@dp.message_handler(Command('os_file'))
async def execute_os_command_file(message: types.Message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("🚫 У тебя нету прав для выполнения команды!")
        return

    command = message.get_args()
    if not command:
        await message.reply("‼️ Укажи команду для выполнения.")
        return

    def run_command():
        return run_command_with_timeout(command)

    result_thread = threading.Thread(target=run_command)
    result_thread.start()
    result_thread.join(timeout=5)

    if result_thread.is_alive():
        await message.reply("⌛ Команда превысила время выполнения.")
    else:
        result = run_command()
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt', prefix='logs_', dir='.') as temp_file:
            temp_file.write(result)
            temp_file_path = temp_file.name
        await message.reply_document(InputFile(temp_file_path, filename='logs.txt'))
        os.remove(temp_file_path)

@dp.message_handler(Command('add_admin'))
async def add_admin(message: types.Message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_USER_IDS:
        await message.reply("🚫 У тебя нету прав для выполнения команды!")
        return

    admin_id = message.get_args()
    if not admin_id:
        await message.reply("💫 Введи ID для добавления администратора.")
        return

    try:
        admin_id = int(admin_id)
    except ValueError:
        await message.reply("🚫 Неверный формат ID пользователя.")
        return

    ADMINS.add(admin_id)
    await message.reply(f"✅ Добавлен админ с ID: {admin_id}")

@dp.message_handler(Command('remove_admin'))
async def remove_admin(message: types.Message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_USER_IDS:
        await message.reply("🚫 У тебя нету прав для выполнения команды.")
        return

    admin_id = message.get_args()
    if not admin_id:
        await message.reply("💫 Введи ID для удаления администратора.")
        return

    try:
        admin_id = int(admin_id)
    except ValueError:
        await message.reply("‼️ Неверный формат ID пользователя.")
        return

    if admin_id in ADMINS:
        ADMINS.remove(admin_id)
        await message.reply(f"✅ Удален админ с ID: {admin_id}.")
    else:
        await message.reply(f"🚫 Админ с ID: {admin_id} не найден.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
