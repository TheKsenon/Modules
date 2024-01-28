import httpx
from aiogram import Bot, Dispatcher, types, exceptions
from aiogram import executor
import os

bot = Bot(token="6402469481:AAEV5DwRavNsbAuqL_IDMi-yuNtSgfysVFg")
dp = Dispatcher(bot)
users = set()
gpt_count = 0
sdxl_count = 0
start_count = 0

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
        await message.reply(file=data, caption=f"Ваше изображение готово, вот оно: {args}")

@dp.message_handler(commands=["readusers"])
async def readusers_cmd(message: types.Message):
    with open("users.txt", "r") as file:
        user_list = file.read().split(";")
    users = "\n".join([f"{user}" for user in user_list if user])
    await message.reply(f"""Люди, которые используют бота:
{users}""")

@dp.message_handler(commands=["sendmessage"])
async def sendmessage_cmd(message: types.Message):
    args = message.get_args()
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
    await message.reply(f"""[📬] Сообщение отправлено всем пользователям: {args}""")

@dp.message_handler(commands=["nano"])
async def nano_cmd(message: types.Message):
    args = message.get_args().split(" ", 2)
    if len(args) == 3:
        file_name, file_format, new_text = args
        file_path = f"{file_name}.{file_format}"
        with open(file_path, "w") as file:
            file.write(new_text)
        await message.reply(f"""[🖊️] Текст в файле {file_path} успешно изменен на: {new_text}""")
    else:
        await message.reply("""[❌] Неправильный формат команды /nano. Пример: /nano users txt hi!""")

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
    args = message.get_args().split(" ", 1)
    if len(args) == 1:
        file_name = args[0]
        with open(file_name, "w"):
            pass
        await message.reply(f"""[📄] Файл {file_name} успешно создан.""")
    else:
        await message.reply("""[❌] Неправильный формат команды /addfile. Пример: /addfile example.txt""")

@admin_check
async def admin_check(message: types.Message):
    return message.from_user.id in admins

@dp.message_handler(commands=["adminhelp"])
async def admin_help_cmd(message: types.Message):
    if not admin_check(message):
        return
    await message.reply("""[🛡️] Команды для администратора:
/sendmessage MESSAGE - Отправить сообщение всем пользователям бота.
/readusers - Посмотреть пользователей бота.
""")

@dp.message_handler(commands=["ownerhelp"])
async def admin_help_cmd(message: types.Message):
    if not admin_check(message):
        return
    await message.reply("""[🛡️] Команды для владельца
/adminlist - админы бота.
/addfile FILE.NAME - Создать новый файл.
/deletefile FILE.NAME - Удалить файл.
/infousers - Получить статистику использования бота.
/nano FILE.FORMAT TEXT - Редактировать текст в файле.
""")
@dp.message_handler(commands=["password"])
async def password_cmd(message: types.Message):
    global admins
    password = message.get_args()

    if password == "adm!gptbot":
        admins.add(message.from_user.id)
        await message.reply("[🔐] Вы получили статус администратора.")
    elif password == "gptowner":
        admins.add(message.from_user.id)
        await message.reply("[👑] Вы получили статус владельца.")
    else:
        await message.reply("[❌] Неверный пароль.")

@dp.message_handler(commands=["addadmin"])
async def addadmin_cmd(message: types.Message):
    if not admin_check(message):
        return

    username = message.get_args()
    user = await bot.get_chat_member(message.chat.id, username)
    
    if user and user.user:
        admins.add(user.user.id)
        await message.reply(f"[🛡️] Пользователь {username} добавлен в администраторы.")
    else:
        await message.reply(f"[❌] Невозможно найти пользователя с именем {username}.")

@dp.message_handler(commands=["deleteadmin"])
async def deleteadmin_cmd(message: types.Message):
    if not admin_check(message):
        return

    username = message.get_args()
    user = await bot.get_chat_member(message.chat.id, username)
    
    if user and user.user:
        admins.remove(user.user.id)
        await message.reply(f"[🛡️] Пользователь {username} удален из администраторов.")
    else:
        await message.reply(f"[❌] Невозможно найти пользователя с именем {username}.")

@dp.message_handler(commands=["deletefile"])
async def deletefile_cmd(message: types.Message):
    if not admin_check(message):
        return

    file_name = message.get_args()
    try:
        os.remove(file_name)
        await message.reply(f"[🗑️] Файл {file_name} успешно удален.")
    except FileNotFoundError:
        await message.reply(f"[❌] Файл {file_name} не найден.")

@dp.message_handler(commands=["deletefile"])
async def deletefile_cmd(message: types.Message):
    args = message.get_args().split(" ", 1)
    if len(args) == 1:
        file_name = args[0]
        try:
            os.remove(file_name)
            await message.reply(f"""[🗑️] Файл {file_name} успешно удален.""")
        except FileNotFoundError:
            await message.reply(f"""[❌] Файл {file_name} не найден.""")
    else:
        await message.reply("""[❌] Неправильный формат команды /deletefile. Пример: /deletefile example.txt""")
        
@dp.message_handler(commands=["adminlist"])
async def adminlist_cmd(message: types.Message):
    admins = await bot.get_chat_administrators(message.chat.id)
    admin_list = "\n".join([f"@{admin.user.username}" for admin in admins])
    await message.reply(f"""[👥] Список администраторов чата:
{admin_list}""")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
