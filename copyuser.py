import os
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import EditAboutRequest
from telethon import functions, types, errors
from asyncio import sleep
from ... import loader, utils

@loader.tds
class CopyUserMod(loader.Module):
    """Модуль для копирования информации о пользователе"""

    strings = {"name": "CopyUser"}

    async def client_ready(self, client, db):
        self.client = client

    async def copyusercmd(self, message):
        """.cu @username - копирует информацию о пользователе"""
        if message.is_reply:
            user = await message.get_reply_message()
        else:
            args = utils.get_args_raw(message)
            if not args:
                return await message.edit("<b>[CopyUser]</b> Не указан пользователь или недостаточно аргументов.")
            try:
                user = await self.client.get_input_entity(args)
            except ValueError:
                return await message.edit("<b>[CopyUser]</b> Не удалось найти пользователя.")
        try:
            chat = await self.client.get_entity(user)
            username = "@{}".format(chat.username) if chat.username else None
            
            if username == None:
                return await message.edit("<b>[CopyUser]</b> У указанного пользователя отсутствует username.")
            
            await message.edit("<b>[CopyUser]</b> Копируем информацию о пользователе...")
            
            # Копирование аватарки
            if chat.photo:
                photo = await self.client.download_profile_photo(entity=user, file=await self.client.upload_file(chat.photo))
                await self.client(UploadProfilePhotoRequest(await self.client.upload_file(photo)))
                os.remove(photo)
            
            # Копирование имени
            if chat.first_name:
                await self.client(functions.account.UpdateProfileRequest(first_name=chat.first_name))
            
            # Копирование описания
            if chat.about:
                await self.client(EditAboutRequest(chat.id, chat.about[:70] + "..." if len(chat.about) > 70 else chat.about))
                
            await message.edit(f"<b>[CopyUser]</b> Информация о пользователе {username} была успешно скопирована.")
          
        except errors.FloodWaitError as e:
            return await message.edit(f"<b>[CopyUser]</b> Ошибка: нет возможности копировать информацию об этом пользователе. "
                                     f"Попробуйте позже.\n\n{str(e)}")
        except Exception as e:
            return await message.edit(f"<b>[CopyUser]</b> Произошла ошибка:\n{str(e)}")
        await sleep(2)
        await message.delete()
