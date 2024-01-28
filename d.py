;import httpx
from aiogram import Bot, Dispatcher, types, exceptions
from aiogram import executor

bot = Bot(token="6402469481:AAEV5DwRavNsbAuqL_IDMi-yuNtSgfysVFg")
dp = Dispatcher(bot)
users = set()

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    global users
    if message.from_user.id not in users:
        with open("users.txt", "a") as file:
            file.write(f"{message.from_user.id};")
        users.add(message.from_user.id)
    await message.reply("""[🔥] Вы используете самый быстрый GPT Бот. 

[🪄] Команды:
/gpt PROMPT - Получить ответ от GPT-Dev4. Вместо PROMPT напишите запрос.
/sdxl PROMPT - Получить изображение от SDXL. Вместо PROMPT напишите запрос.
/sendmessage MESSAGE - Отправить сообщение всем пользователям бота.
/readusers - Посмотреть пользователей бота.

[🔊] Разработчик бота: @officialksenon""")

@dp.message_handler(commands=["gpt"])
async def gpt_cmd(message: types.Message):
    args = message.get_args()
    await message.reply("""[🪄] Ваш ответ уже готов 🔥
Мы используем самую быструю модель для вашего использования.""")
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post("https://opo.k.vu/private/apis/gpt", json={"prompt": args})
        data = resp.text
        await message.reply(f"Ответ GPT 🤖: {data}")

@dp.message_handler(commands=["sdxl"])
async def sdxl_cmd(message: types.Message):
    args = message.get_args()
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
    users = "\n".join([f"@{user}" for user in user_list if user])
    await message.reply(f"""Люди, которые используют бота:
{users}""")

@dp.message_handler(commands=["sendmessage"])
async def sendmessage_cmd(message: types.Message):
    args = message.get_args()
    with open("users.txt", "r") as file:
        user_list = file.read().split(";")
    for user_id_str in user_list:
        if user_id_str:
            user_id = int(user_id_str)
            try:
                await bot.send_message(user_id, args)
            except exceptions.ChatNotFound:
                print(f"Chat not found for user: {user_id}")
    await message.reply(f"""[📬] Сообщение отправлено всем пользователям: {args}""")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
