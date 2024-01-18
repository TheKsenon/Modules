from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputChannel

from .. import loader

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
            channel = await message.client.get_entity(InputChannel(channel_id=channel_username, access_hash=0))
            full_channel = await message.client(GetFullChannelRequest(channel=channel))
            messages = full_channel.full_chat.messages
            
            if not messages:
                return await message.reply("<b>[MemeReader]</b> К сожалению, в канале сейчас нет мемов.")

            random_meme = self.get_random_message(messages)
            await message.reply(random_meme.message)
        except Exception as e:
            return await message.reply(f"<b>[MemeReader]</b> Ошибка при получении мема: {str(e)}.")

    def get_random_message(self, messages):
        random_index = self.random_index(len(messages))
        return messages[random_index]

    def random_index(self, length):
        return hash(str(length)) % length

