from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, User
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext

API_TOKEN = '7003089239:AAE9lj6PZRNMPD7qPIXnA_Dr2NrBVKgQ-Oo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

admins = []
muted_users = []

async def is_admin(message: Message):
    if not message.from_user:
        return False
    return message.from_user.id in admins

@dp.message_handler(commands=['admin'])
async def give_admin(message: Message):
    if await is_admin(message):
        if message.reply_to_message:
            user: User = message.reply_to_message.from_user
        elif message.get_args():
            user = await bot.get_chat_member(message.chat.id, message.get_args()).user
        else:
            user = message.from_user
        
        admins.append(user.id)
        await message.answer(f'{user.username} теперь администратор')
    else:
        await message.answer('У вас нет прав для выполнения этой команды')

@dp.message_handler(commands=['ban'])
async def ban_user(message: Message):
    if await is_admin(message):
        if message.reply_to_message:
            user: User = message.reply_to_message.from_user
        elif message.get_args():
            user = await bot.get_chat_member(message.chat.id, message.get_args()).user
        else:
            user = message.from_user
        
        await bot.kick_chat_member(message.chat.id, user.id)
        await message.answer(f'{user.username} забанен')
    else:
        await message.answer('У вас нет прав для выполнения этой команды')

@dp.message_handler(commands=['kick'])
async def kick_user(message: Message):
    if await is_admin(message):
        if message.reply_to_message:
            user: User = message.reply_to_message.from_user
        elif message.get_args():
            user = await bot.get_chat_member(message.chat.id, message.get_args()).user
        else:
            user = message.from_user
        
        await bot.kick_chat_member(message.chat.id, user.id)
        await message.answer(f'{user.username} кикнут')
    else:
        await message.answer('У вас нет прав для выполнения этой команды')

@dp.message_handler(commands=['mute'])
async def mute_user(message: Message):
    if await is_admin(message):
        if message.reply_to_message:
            user: User = message.reply_to_message.from_user
        elif message.get_args():
            user = await bot.get_chat_member(message.chat.id, message.get_args()).user
        else:
            user = message.from_user
        
        if user.id not in muted_users:
            muted_users.append(user.id)
            await message.answer(f'{user.username} заглушен')
        else:
            await message.answer(f'{user.username} уже заглушен')
    else:
        await message.answer('У вас нет прав для выполнения этой команды')

@dp.message_handler(commands=['unmute'])
async def unmute_user(message: Message):
    if await is_admin(message):
        if message.reply_to_message:
            user: User = message.reply_to_message.from_user
        elif message.get_args():
            user = await bot.get_chat_member(message.chat.id, message.get_args()).user
        else:
            user = message.from_user
        
        if user.id in muted_users:
            muted_users.remove(user.id)
            await message.answer(f'{user.username} разглушен')
        else:
            await message.answer(f'{user.username} не был заглушен')
    else:
        await message.answer('У вас нет прав для выполнения этой команды')

@dp.message_handler(commands=['unban'])
async def unban_user(message: Message):
    if await is_admin(message):
        if message.get_args():
            await bot.unban_chat_member(message.chat.id, message.get_args())
            await message.answer(f'Пользователь разбанен')
        else:
            await message.answer('Укажите id пользователя для разбана')
    else:
        await message.answer('У вас нет прав для выполнения этой команды')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
