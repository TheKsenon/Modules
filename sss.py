from telethon import functions, types
from .. import loader

@loader.tds
class DeleteAllMod(loader.Module):
    """Модуль для удаления всех подписчиков из указанного канала или чата."""
    strings = {"name": "DeleteAll"}

    async def deleteallcmd(self, message):
        """Удалить всех подписчиков из указанного канала или чата."""
        try:
            args = message.text.split(" ", 1)
            if len(args) != 2:
                return await message.edit("[DeleteAll] Неправильный формат команды. Используйте: .deleteal @username.")
            
            entity = args[1]
            chat = await message.client.get_entity(entity)
            
            if isinstance(chat, types.Chat):
                await message.edit(f"[DeleteAll] Начинаю удаление всех подписчиков из {entity}...")
                async for member in message.client.iter_participants(chat):
                    try:
                        await message.client.kick_participant(chat, member)
                    except Exception as e:
                        await message.edit(f"[DeleteAll] Ошибка при удалении пользователя: {str(e)}")
                await message.edit("[DeleteAll] Все подписчики были удалены.")
            else:
                await message.edit("[DeleteAll] Указанный объект не является каналом или чатом.")
        
        except Exception as e:
            await message.edit(f"[DeleteAll] Ошибка при выполнении команды: {str(e)}")
