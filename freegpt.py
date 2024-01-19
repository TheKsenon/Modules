#Module has created by @officialKsenon/@XenonModules
#You can modify, or edit this code. 

from .. import loader
import asyncio

@loader.tds
class FreeGPTMod(loader.Module):
    """Модуль для отправки запроса к ChatGPT с использованием промпта.
    Разработчик: @XenonModules
    
"""

    strings = {"name": "FreeGPT"}

    async def client_ready(self, client, db):
        self.db = db

    async def askcmd(self, message):
        """Отправить запрос ChatGPT с использованием промпта."""
        try:
            args = message.text.split(" ", 1)
            if len(args) != 2:
                return await message.edit("<b>[FreeGPT]</b> Неправильный формат команды. Используйте: <code>.ask PROMPT</code>.")

            prompt = args[1]
            chat_id = await self.get_chat_id(message)

            await message.edit("<b>[FreeGPT]</b> Запрос отправлен, ждем ответа 🪄")
            
            async with message.client.conversation(chat_id) as conv:
                response = await conv.send_message(prompt)
                await asyncio.sleep(15)

                limit = 40  # Лимит проверок
                count = 0

                while count < limit:
                    messages = await message.client.get_messages(chat_id, limit=2)
                    for msg in messages:
                        if msg.id > response.id:
                            await message.edit(msg.text)
                            return
                    
                    await asyncio.sleep(1)
                    count += 1

                await message.edit("<b>[FreeGPT]</b> Превышено время ожидания ответа.")

        except Exception as e:
            return await message.edit(f"<b>[FreeGPT]</b> Ошибка при отправке запроса: {str(e)}.")

    async def get_chat_id(self, message):
        async for dialog in message.client.iter_dialogs():
            if dialog.entity.username == "NeuroConnect_Bot":
                return dialog.id
        raise ValueError("Бот @NeuroConnect_Bot не найден в списке диалогов.")
