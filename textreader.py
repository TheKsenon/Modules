
from .. import loader
import requests

@loader.tds
class TextReaderMod(loader.Module):
    """Модуль для чтения текста с заданного URL."""

    strings = {"name": "TextReader"}

    async def client_ready(self, client, db):
        self.db = db

    async def textreadcmd(self, message):
        """Загрузить и отобразить текст с указанного URL."""
        args = message.text.split(" ")
        if len(args) != 2:
            return await message.edit("<b>[TextReader]</b> Неправильный формат команды. Используй: <code>/readtxt URL</code>.")

        url = args[1]
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            text = response.text
        except Exception as e:
            return await message.edit(f"<b>[TextReader]</b> Ошибка при чтении текста: {str(e)}.")

        await message.edit("<b>[TextReader]</b> Загрузка...")
        
        await message.client.send_file(message.chat_id, text, force_document=True)
        await message.delete()


