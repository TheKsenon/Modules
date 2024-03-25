from telethon import events, functions, types
from telethon.errors.rpcerrorlist import ChatAdminRequiredError
from .. import loader

@loader.tds
class DeleteAllMod(loader.Module):
    """Модуль для удаления всех подписчиков из указанного канала или чата."""
    strings = {"name": "DeleteAll"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def dlallcmd(self, message):
        """.dlall @username - удалить всех подписчиков из указанного канала или чата."""
        if not message.is_reply:
            await message.edit("Пожалуйста, ответьте на сообщение с @username канала или чата, чтобы удалить всех подписчиков.")
            return
        try:
            target = await message.get_reply_message()
            if not isinstance(target.sender, types.User):
                await message.edit("Пожалуйста, ответьте на сообщение с @username канала или чата, чтобы удалить всех подписчиков.")
                return
            entity = await self.client.get_entity(target.sender.username)
            if not entity:
                await message.edit("Не удалось найти канал или чат с данным @username.")
                return
            if not isinstance(entity, types.Channel):
                await message.edit("Этот @username не является каналом или чатом.")
                return
            async for user in self.client.iter_participants(entity):
                try:
                    await self.client.edit_permissions(entity, user, view_messages=False)
                except ChatAdminRequiredError:
                    await message.edit("У меня нет достаточных прав для удаления подписчиков. Убедитесь, что я администратор канала и имею соответствующие права.")
                    return
            await message.edit(f"Все подписчики из @{entity.username} были успешно удалены.")
        except Exception as e:
            await message.edit(f"Произошла ошибка: {str(e)}"
