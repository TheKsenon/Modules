from telethon import functions, types
from telethon.errors.rpcerrorlist import PeerIdInvalidError
from .. import loader


@loader.tds
class MessengerModule(loader.Module):
    """Модуль для отправки сообщений в чаты, каналы и по указанному юзернейму."""

    strings = {"name": "Мессендж-Модуль"}

    async def client_ready(self, client, db):
        self.client = client

    async def send_cmd(self, message):
        """Отправить сообщение по указанному юзернейму, чату или каналу."""
        args = message.text.split(" ", 2)
        if len(args) < 3:
            await message.edit("[🚫] Неправильный формат команды. Используйте: .send @USERNAME/CHAT_ID MESSAGE")
            return
        username_or_chat_id = args[1]
        text = args[2]
        try:
            entity = await self.client.get_entity(username_or_chat_id)
            if isinstance(entity, (types.User, types.Chat, types.Channel)):
                await self.client.send_message(entity, text)
                await message.edit(f"[✅] Сообщение отправлено: {username_or_chat_id}")
            else:
                await message.edit("[🚫] Указанный юзернейм или ID чата не является пользователем, чатом или каналом.")
        except PeerIdInvalidError:
            await message.edit("[🚫] Такого чата не существует.")
