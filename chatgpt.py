from .. import loader
import time

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
                return await message.reply("<b>[FreeGPT]</b> Неправильный формат команды. Используйте: <code>/ask PROMPT</code>.")

            prompt = args[1]
            chat_id = await self.get_chat_id()

            await message.edit("<b>[FreeGPT]</b> Отправка запроса...")
            
            while True:
                await message.client.send_message(chat_id, prompt)
                time.sleep(1)

                async for msg in message.client.iter_messages(chat_id, limit=1):
                    if msg.sender_id == (await message.client.get_me()).id:
                        await message.edit(msg.message)
                        return

        except Exception as e:
            return await message.edit(f"<b>[FreeGPT]</b> Ошибка при отправке запроса: {str(e)}.")

    async def get_chat_id(self):
        async for dialog in message.client.iter_dialogs():
            if dialog.entity.username == "NeuroConnect_Bot":
                return dialog.id
        raise ValueError("Бот @NeuroConnect_Bot не найден в списке диалогов.")

