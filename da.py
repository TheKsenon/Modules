from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

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
                await message.client(EditAdminRequest(channel, user, ChatAdminRights(add_admins=False, invite_users=False, change_info=False, ban_users=True, delete_messages=True, pin_messages=False)))

            await message.edit(f"[DeleteAll] Успешно удалены все подписчики из {channel}.")

        except Exception as e:
            return await message.edit(f"[DeleteAll] Ошибка при удалении подписчиков: {str(e)}.")
