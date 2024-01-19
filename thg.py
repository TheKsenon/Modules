#Module has created by @officialKsenon/@XenonModules
#You can modify, or edit this code. 

from .. import loader
import asyncio

@loader.tds
class FreeGPTMod(loader.Module):
    """Модуль для отправки запроса к ChatGPT с использованием промпта.
    
    🪅 Разработчик: @XenonModules

    🪄 Скачать модуль через .dlmod
    
    🪩 .dlmod https://raw.githubusercontent.com/TheKsenon/Modules/main/freechatgpt3.py
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

        seconds = 0  # Изначальное число секунд
        await message.edit(f"""<b>[FreeGPT]</b> Запрос отправлен, ждем ответа 🪄
        
        Ответ может пройти через многое время. Ждите 40-50 секунд. Осталось секунд: {seconds}""")

        async with message.client.conversation(chat_id) as conv:
            response = await conv.send_message(prompt)
            await asyncio.sleep(40)

            limit = 40  # Лимит проверок
            count = 0

            while count < limit:
                new_prompt = f"{prompt} {count + 1}"  # Добавляем число к промпту
                await response.edit(new_prompt)  # Редактируем отправленное сообщение с новым промптом

                await asyncio.sleep(1)
                count += 1
                seconds += 1  # Увеличиваем число секунд

                messages = await message.client.get_messages(chat_id, limit=2)
                for msg in messages:
                    if msg.id > response.id and msg.from_id == chat_id:  # Проверяем, что сообщение от бота
                        await message.edit(msg.text)
                        return

                await message.edit(f"""<b>[FreeGPT]</b> Запрос отправлен, ждем ответа 🪄
 Ответ может пройти через многое время. Ждите 40-50 секунд. Осталось секунд: {seconds}""")

            await message.edit("<b>[FreeGPT]</b> Превышено время ожидания ответа.")

    except Exception as e:
        return await message.edit(f"<b>[FreeGPT]</b> Ошибка при отправке запроса: {str(e)}.")
