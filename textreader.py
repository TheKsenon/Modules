import requests
from telethon import events
from .. import loader


@loader.tds
class TextReaderMod(loader.Module):
    """Модуль TextReader"""

    strings = {"name": "TextReader"}

    async def client_ready(self, client, db):
        await client.send_message("me", "TextReader модуль загружен")

    @loader.unrestricted
    @loader.ratelimit(1)
    async def readtxtcmd(self, message):
        """Копирует текст из указанного URL"""
        args = message.text.split(" ", maxsplit=1)
        if len(args) != 2:
            return await message.edit("Неверный формат команды. Используйте: /readtxt URL")
        
        url = args[1]
        await message.edit("Загрузка...")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return await message.edit(f"Произошла ошибка при загрузке из URL: {e}")
        
        text = response.text
        await message.edit(text)
