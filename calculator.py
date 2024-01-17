from telethon import functions
from telethon.tl.types import Message
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class CalculatorMod(loader.Module):
    """
    Модуль для калькулятора. Выполняет математические операции.
    """

    strings = {
        "name": "Calculator",
        "no_args": "🚫 Не указано выражение для вычисления!",
    }

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def calculatecmd(self, message: Message):
        """
        {expression} - вычислить математическое выражение
        """
        args = utils.get_args_raw(message)

        if not args:
            return await utils.answer(message, self.strings["no_args"])

        try:
            result = eval(args)
            text = f"<b>✅ Результат:</b> {result}"
        except Exception as e:
            text = f"⚠️ Ошибка при вычислении: {str(e)}"

        return await utils.answer(message, text
