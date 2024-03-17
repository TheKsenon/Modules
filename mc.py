from telethon import events
from .. import loader


@loader.tds
class MonacoPromo(loader.Module):
    """Модуль для отправки промокода боту MonacoGamebot."""

    strings = {"name": "MonacoPromo"}

    async def client_ready(self, client, db):
        self.client = client

    async def watcher(self, message):
        if isinstance(message, events.NewMessage):
            channels = self.settings.get("channels", [])
            if str(message.chat_id) in channels:
                text = message.text
                if "Название:" in text:
                    promo_name = text.split("Название:")[1].strip().split("\n")[0]
                    await self.client.send_message("MonacoGamebot", f"Промо {promo_name}")

    async def monacopromo_cmd(self, message):
        """Активировать работу модуля"""
        channels = await self.get_channels(message)
        if channels:
            self.settings["channels"] = channels
            await self.save_settings()
            await message.edit("[🏡] MonacoPromo Eater\nМодуль успешно активирован.")
        else:
            await message.edit("[🚫] Нет указанных каналов.")

    async def monacostop_cmd(self, message):
        """Отключить работу модуля."""
        if "channels" in self.settings:
            del self.settings["channels"]
            await self.save_settings()
            await message.edit("[🛑] MonacoPromo Eater\nМодуль успешно отключен.")
        else:
            await message.edit("[🚫] Модуль уже отключен.")

    async def get_channels(self, message):
        args = message.text.split(" ", 1)
        if len(args) == 2:
            channels = args[1].split(";")
            return channels
        else:
            return [
