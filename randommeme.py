from .. import loader
import requests
import random

@loader.tds
class MemeReaderMod(loader.Module):
    """Модуль для отправки случайного мема из канала @prg_memes_tg."""

    strings = {"name": "MemeReader"}

    async def client_ready(self, client, db):
        self.db = db
    
    async def memecmd(self, message):
        """Отправить случайный мем из канала @prg_memes_tg."""
        try:
            channel_username = "prg_memes_tg"
            response = await message.client.get_messages(channel_username, limit=10724)
            memes = [msg.text for msg in response if msg.text]
            if not memes:
                return await message.edit("<b>[MemeReader]</b> К сожалению, в канале сейчас нет мемов.")
        
            random_meme = random.choice(memes)
            await message.edit(random_meme)
        except Exception as e:
            return await message.edit(f"<b>[MemeReader]</b> Ошибка при получении мема: {str(e)}.")
