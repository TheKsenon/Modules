import httpx
import json
from aiogram import Bot, Dispatcher, types, exceptions
from aiogram import executor
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import requests
import asyncio
from aiogram.types import ParseMode

API_K = 'ddosxd-api-1jq4e9xbzu2ilgn'
DDOSXD_API_KEY = 'ddosxd-api-1jq4e9xbzu2ilgn'

bot = Bot(token="6640154150:AAHgZJRXwzsw-jA8ffXoVlhjZXm8oFTyNu4")
dp = Dispatcher(bot)
users = set()
admins = set()
gpt_count = 0
sdxl_count = 0
start_count = 0

API_KEY = 'ddosxd-api-1jq4e9xbzu2ilgn'
headers = {'Authorization': API_KEY}

API_URL = 'https://api.ddosxd.ru/v1/chat'

logging.basicConfig(level=logging.INFO)

dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

API_KY = 'ddosxd-api-1jq4e9xbzu2ilgn'
headers = {'Authorization': API_KY}

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    global users, start_count
    if message.from_user.id not in users:
        with open("users.txt", "a") as file:
            file.write(f"{message.from_user.id};")
        users.add(message.from_user.id)
    start_count += 1
    await message.reply("""[🔥] Вы используете лучшего их лучших бота!

[🔊] Модели текста: 

[🪄] Команды:
/gpt PROMPT - Получить ответ от GPT. 

/gpt35 PROMPT — Быстрая, сильная модель!

/claude2 PROMPT — Еще лучше, чем другие

[🪩] Модели изображений:

/pixart PROMPT — Реалистичные, минимализм и многое другое!


[🔊] Разработчик бота: @officialksenon / thx to opo && ddosxd""")

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

@dp.message_handler(commands=['gpt35'])
async def generate_response(message: types.Message):
    user_prompt = message.get_args()

    # Отправляем первое сообщение о том, что ответ готовится
    await message.reply("""[📶] Ответ уже готов... Вы используете быструю GPT 3.5 модель!""")

    # Запрашиваем ответ от GPT-3.5
    data = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': user_prompt}]}
    response = requests.post(API_URL, headers=headers, json=data)

    try:
        response_json = response.json()
        generated_text = response_json['reply']
        result_text = f"{generated_text}"
    except KeyError:
        result_text = "Не удалось получить ответ от модели."

    # Добавляем ответ от GPT-3.5 к предыдущему сообщению
    await message.reply(result_text)

@dp.message_handler(commands=["claude2"])
async def process_claude2_command(message: types.Message):
    user_prompt = message.get_args()

    # Отправляем первое сообщение о том, что ответ готовится
    await message.reply("""[📶] Ответ уже готов... Вы используете быструю Claude2 модель!""")

    # Отправляем запрос к API
    data = {
        'model': 'claude-2',
        'prompt': f'\n\nHuman: {user_prompt}\n\nAssistant: ',
        'userId': str(message.from_user.id)
    }

    response = requests.post('https://beta.ddosxd.ru/v1/prompt', headers=headers, json=data)
    result_json = json.loads(response.text)

    # Извлекаем текстовый ответ
    result_text = result_json.get('reply', 'Произошла ошибка при получении ответа от модели.')

    # Отправляем только текстовый ответ от модели
    await message.reply(result_text)

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

@dp.message_handler(commands=['pixart'])
async def pixart_command(message: types.Message):
    try:
        prompt = message.get_args()
        if not prompt:
            await message.reply("Вы неправильно написали команду.")
            return

        await message.reply("""[🪄] Ваше изображение уже готово 🔥
Мы используем самую быструю модель для вашего использования.""")

        data = {
            'model': 'pixart',
            'prompt': prompt
        }

        response = requests.post('https://api.ddosxd.ru/v1/image', headers={'Authorization': API_K}, json=data)
        image_url = response.json()['photos'][0]

        await bot.send_photo(message.chat.id, photo=image_url)
    
    except Exception as e:
        print(f"Error: {e}")


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
