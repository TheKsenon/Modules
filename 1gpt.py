from .. import loader
import asyncio

@loader.tds
class FreeGPTMod(loader.Module):
    """Модуль для отправки запроса к @NeuroConnect_Bot с использованием промпта."""

    strings = {"name": "FreeGPT"}

    async def client_ready(self, client, db):
        self.db = db

    async def askcmd(self, message):
        """Отправить запрос @NeuroConnect_Bot с использованием промпта."""
        try:
            args = message.text.split(" ", 1)
            if len(args) != 2:
                return await message.edit("<b>[FreeGPT]</b> Неправильный формат команды. Используйте: <code>/ask PROMPT</code>.")

            prompt = args[1]
            chat_id = await self.get_chat_id(message)

            await message.edit("<b>[FreeGPT]</b> Отправка запроса...")
            
            async with message.client.conversation(chat_id) as conv:
                response = await conv.send_message(prompt)
                await asyncio.sleep(8)

                async for message in conv.iter_messages():
                    if message.id != response.id:
                        await message.edit(message.text)
                        return

        except Exception as e:
            return await message.edit(f"<b>[FreeGPT]</b> Ошибка при отправке запроса: {str(e)}.")

    async def get_chat_id(self, message):
        async for dialog in message.client.iter_dialogs():
            if dialog.entity.username == "NeuroConnect_Bot":
                return dialog.id
        raise ValueError("Бот @NeuroConnect_Bot не найден в списке диалогов.")
