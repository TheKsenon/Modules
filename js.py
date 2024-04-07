from .. import loader

@loader.tds
class FakePingMod(loader.Module):
    """Модуль для автоматической замены всех сообщений на "привет"."""

    strings = {"name": "FakePinsg"}

    async def client_ready(self, client, db):
        self.db = db

    async def incoming_message(self, message):
        message.text = "привет"
