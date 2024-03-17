from telethon import functions, types
from telethon.errors.rpcerrorlist import PeerIdInvalidError
from .. import loader


@loader.tds
class MessengerModule(loader.Module):
    """Модуль для отправки сообщений по указанному юзернейму."""

    strings = {"name": "Мессендж-Модуль"}

    async def client_ready(self, client, db):
        self.client = client

    async def send_cmd(self, message):
        """Отправить сообщение по указанному юзернейму."""
        args = message.text.split(" ", 2)
        if len(args) < 3:
            await message.edit("[🚫] Неправильный формат команды. Используйте: .send @USERNAME MESSAGE")
            return
        username = args[1]
        text = args[2]
        try:
            entity = await self.client.get_entity(username)
            if isinstance(entity, types.User):
                await self.client.send_message(entity, text)
                await message.edit(f"[✅] Сообщение отправлено по юзернейму: {username}")
            else:
                await message.edit("[🚫] Указанный юзернейм не является пользователем.")
        except PeerIdInvalidError:
            await message.edit("[🚫] Такого чата не существует.")
