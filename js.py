from .. import loader

@loader.tds
class MessageReplaceMod(loader.Module):
    """Модуль для автоматической замены всех сообщений на "привет"."""

    async def client_ready(self, client, db):
        self.db = db

    async def incoming_message(self, message):
        message.text = "привет"
