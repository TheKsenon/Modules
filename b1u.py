import httpx
from aiogram import Bot, Dispatcher, types, exceptions
from aiogram import executor
from io import BytesIO
import time
import os

bot = Bot(token="6402469481:AAEV5DwRavNsbAuqL_IDMi-yuNtSgfysVFg")
dp = Dispatcher(bot)
users = set()
admins = set()
gpt_count = 0
sdxl_count = 0
start_count = 0
last_send_message_time = {}

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    global users, start_count
    if message.from_user.id not in users:
        with open("users.txt", "a") as file:
            file.write(f"{message.from_user.id};")
        users.add(message.from_user.id)
    start_count += 1
    await message.reply("""[🔥] Вы используете самый быстрый GPT Бот. 

[🪄] Команды:
/gpt PROMPT - Получить ответ от GPT-Dev4. Вместо PROMPT напишите запрос.
/sdxl PROMPT - Получить изображение от SDXL. Вместо PROMPT напишите запрос.
/sendmessage MESSAGE - Отправить сообщение всем пользователям бота.
/readusers - Посмотреть пользователей бота.
/nano FILE.FORMAT TEXT - Редактировать текст в файле.
/infousers - Получить статистику использования бота.
/addfile FILE.NAME - Создать новый файл.

[🔊] Разработчик бота: @officialksenon""")

@dp.message_handler(commands=["gpt"])
async def gpt_cmd(message: types.Message):
    global gpt_count
    args = message.get_args()
    gpt_count += 1
    await message.reply("""[🪄] Ваш ответ уже готов 🔥
Мы используем самую быструю модель для вашего использования.""")

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post("https://opo.k.vu/private/apis/gpt", json={"prompt": args})
        data = resp.text
        await message.reply(f"Ответ GPT 🤖: {data}")

@dp.message_handler(commands=["sdxl"])
async def sdxl_cmd(message: types.Message):
    global sdxl_count
    args = message.get_args()
    sdxl_count += 1
    await message.reply("""[🪄] Ваше изображение уже готово 🔥
Мы используем самую быструю модель для вашего использования.""")

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post("https://opo.k.vu/private/apis/sdxl", json={"prompt": args})
        data = resp.text
        image_bytes_io = BytesIO(data.encode())
        await message.reply_photo(types.InputFile(image_bytes_io), caption=f"Ваше изображение готово, вот оно: {args}")

@dp.message_handler(commands=["readusers"])
async def readusers_cmd(message: types.Message):
    if is_admin(message.from_user.id):
        with open("users.txt", "r") as file:
            user_list = file.read().split(";")
        users_list_formatted = "\n".join([f"{user}" for user in user_list if user])
        await message.reply(f"""Люди, которые используют бота:
{users_list_formatted}""")
    else:
        await message.reply("У вас нет прав для использования этой команды.")

@dp.message_handler(commands=["sendmessage"])
async def sendmessage_cmd(message: types.Message):
    if is_admin(message.from_user.id):
        args = message.get_args()
        current_time = time.time()

        if current_time - last_send_message_time.get(message.from_user.id, 0) >= 5:
            with open("users.txt", "r") as file:
                user_list = file.read().split(";")

            for user_id_str in user_list:
                if user_id_str:
                    try:
                        user_id = int(user_id_str)
                        await bot.send_message(user_id, args)
                    except exceptions.ChatNotFound:
                        print(f"Chat not found for user: {user_id}")
                    except ValueError:
                        print(f"Invalid user_id format: {user_id_str}")

            last_send_message_time[message.from_user.id] = current_time
            await message.reply(f"""[📬] Сообщение отправлено всем пользователям: {args}""")
        else:
            await message.reply("""[⚠️] Пожалуйста, подождите 5 секунд перед отправкой нового сообщения.""")
    else:
        await message.reply("У вас нет прав для использования этой команды.")

@dp.message_handler(commands=["nano"])
async def nano_cmd(message: types.Message):
    if is_admin(message.from_user.id):
        args = message.get_args().split(" ", 2)
        if len(args) == 3:
            file_name, file_format, new_text = args
            file_path = f"{file_name}.{file_format}"
            with open(file_path, "w") as file:
                file.write(new_text)
            await message.reply(f"""[🖊️] Текст в файле {file_path} успешно изменен на: {new_text}""")
        else:
            await message.reply("""[❌] Неправильный формат команды /nano. Пример: /nano users txt hi!""")
    else:
        await message.reply("У вас нет прав для использования этой команды.")

@dp.message_handler(commands=["infousers"])
async def infousers_cmd(message: types.Message):
    global users, gpt_count, sdxl_count, start_count
    users_count = len(users)
    await message.reply(f"""[ℹ️] Используют ИИ: {users_count}
Написано /gpt: {gpt_count}
Написано /sdxl: {sdxl_count}
Написано /start: {start_count}""")

@dp.message_handler(commands=["addfile"])
async def addfile_cmd(message: types.Message):
    if is_admin(message.from_user.id):
        args = message.get_args().split(" ", 1)
        if len(args) == 1:
            file_name = args[0]
            with open(file_name, "w"):
                pass
            await message.reply(f"""[📄] Файл {file_name} успешно создан.""")
        else:
            await message.reply("""[❌] Неправильный формат команды /addfile. Пример: /addfile example.txt""")
    else:
        await message.reply("У вас нет прав для использования этой команды.")

@dp.message_handler(commands=["adminhelp"])
async def adminhelp_cmd(message: types.Message):
    if is_admin(message.from_user.id):
        await message.reply("""Команды для администраторов:
/sdxl PROMPT - Получить изображение от SDXL. Вместо PROMPT напишите запрос.
/sendmessage MESSAGE - Отправить сообщение всем пользователям бота.
/readusers - Посмотреть пользователей бота.
/nano FILE.FORMAT TEXT - Редактировать текст в файле.
/infousers - Получить статистику использования бота.
/addfile FILE.NAME - Создать новый файл.
/deletefile FILE.NAME - Удалить файл.""")
    else:
        await message.reply("У вас нет прав для использования этой команды.")

@dp.message_handler(commands=["deletefile"])
async def deletefile_cmd(message: types.Message):
    if is_admin(message.from_user.id):
        file_name = message.get_args()
        try:
            os.remove(file_name)
            await message.reply(f"Файл {file_name} был удален.")
        except FileNotFoundError:
            await message.reply(f"Файл {file_name} не найден.")
    else:
        await message.reply("У вас нет прав для использования этой команды.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
