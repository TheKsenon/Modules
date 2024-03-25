from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from .. import loader

@loader.tds
class DeleteAllModule(loader.Module):
    """Модуль для удаления всех подписчиков из указанного канала или чата."""

    async def dlallcmd(self, message):
        """Удалить всех подписчиков из указанного канала или чата."""
        try:
            args = message.text.split(" ", 1)
            if len(args) != 2:
                return await message.edit("[DeleteAll] Неправильный формат команды. Используйте: .dlall @username.")

            channel = args[1]

            async for user in message.client.iter_participants(channel):
                if user.is_self:
                    continue
                await message.client(EditBannedRequest(channel, user, ChatBannedRights(until_date=None, view_messages=True)))

            await message.edit(f"[DeleteAll] Успешно удалены все подписчики из {channel}.")

        except Exception as e:
            return await message.edit(f"[DeleteAll] Ошибка при удалении подписчиков: {str(e)}.")

