from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

from .. import loader, utils

@loader.tds
class MemeReaderMod(loader.Module):
    """Модуль для отправки случайного мема из канала @prg_memes_tg.
    Разработчик: @XenonModules"""

    strings = {"name": "MemeReader"}

    async def client_ready(self, client, db):
        self.db = db
    
    async def find_message(self, client, channel_id):
        async for participant in client.iter_participants(channel_id, search="", limit=1, filter=ChannelParticipantsSearch()):
            return participant

    async def memecmd(self, message):
        """Отправляет случайный мем из канала @prg_memes_tg."""
        try:
            channel_username = "prg_memes_tg"
            channel_id = await utils.resolve_id(client, channel_username)
            participant = await self.find_message(client, channel_id)
            if participant:
                participant_id = participant.id
                response = await client(GetParticipantsRequest(channel=channel_id, filter=ChannelParticipantsSearch(q=participant_id), offset=0, limit=1, hash=0), )
                message = response.users[0]
                await client.send_message(message, ".meme")
        except Exception as e:
            return await message.reply(f"[Ошибка]\n{str(e)}")

