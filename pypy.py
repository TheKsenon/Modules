from .. import loader
import requests
import random

@loader.tds
class MemeReaderMod(loader.Module):
    """Модуль для отправки случайного мема из канала @prg_memes_tg."""

    strings = {"name": "MemeReader"}

    async def client_ready(self, client, db):
        self.db = db
        self.channel_username = "prg_memes_tg"

    async def memecmd(self, message):
        """Отправить случайный мем из канала @prg_memes_tg."""
        try:
            channel = await message.client.get_entity(self.channel_username)
            if not channel:
                return await message.reply(f"<b>[MemeReader]</b> Не удалось найти канал {self.channel_username}.")

            response = await message.client.get_messages(channel, limit=10724)
            memes = [msg.text for msg in response if msg.text]
            if not memes:
                return await message.reply("<b>[MemeReader]</b> К сожалению, в канале сейчас нет мемов.")

            random_meme = random.choice(memes)
            await message.reply(random_meme)
        except Exception as e:
            return await message.reply(f"<b>[MemeReader]</b> Ошибка при получении мема: {str(e)}.")

