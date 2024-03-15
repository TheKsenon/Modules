from telethon import events, Button
from .. import loader
import requests

@loader.tds
class GPT35Mod(loader.Module):
    """Модуль для отправки запроса к GPT-3.5 Turbo с использованием промпта.
    
    [🔮] GPT 3.5 Turbo

    [🔺] Разработчик: @officialksenon / @XenonModules

    [😚] Скачать модуль:
    [‼️] .dlm https://raw.githubusercontent.com/TheKsenon/Modules/main/gpt35turbo.py

"""

    strings = {"name": "GPT35Turbo"}

    async def gpt35cmd(self, message):
        """Отправить запрос GPT-3.5 Turbo с использованием промпта."""
        try:
            args = message.text.split(" ", 1)
            if len(args) != 2:
                return await message.edit("<b>[GPT35]</b> Неправильный формат команды. Используйте: <code>.gpt35 PROMPT</code>.")

            prompt = args[1]
            await message.edit(f"<b>[GPT35]</b> Ждите ответа... Ваш запрос: {prompt}")

            headers = {'Authorization': 'ddosxd-api-1jq4e9xbzu2ilgn'}
            data = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': prompt}]}

            response = requests.post('https://api.ddosxd.ru/v1/chat', headers=headers, json=data)
            reply = response.json().get('reply')

            if reply:
                await message.edit(f"<b>[GPT35]</b> Ответ: {reply}")
            else:
                await message.respond("<b>[GPT35]</b> Не удалось получить ответ от сервера.", buttons=[Button.url("🔥 Подписаться", "https://t.me/XenonModules")])

        except Exception as e:
            return await message.edit(f"<b>[GPT35]</b> Ошибка при отправке запроса: {str(e)}.")
