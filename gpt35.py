from .. import loader
import requests

@loader.tds
class GPT35Mod(loader.Module):
    """Модуль для отправки запроса к GPT-3.5 Turbo с использованием промпта.
    
    🪅 Разработчик: @XenonModules

    🪄 Скачать модуль через .dlmod
    
    🪩 .dlmod https://raw.githubusercontent.com/TheKsenon/Modules/main/gpt35mod.py
"""

    strings = {"name": "GPT35"}

    async def gpt35cmd(self, message):
        """Отправить запрос GPT-3.5 Turbo с использованием промпта."""
        try:
            args = message.text.split(" ", 1)
            if len(args) != 2:
                return await message.edit("<b>[GPT35]</b> Неправильный формат команды. Используйте: <code>.gpt35 PROMPT</code>.")

            prompt = args[1]
            headers = {'Authorization': 'ddosxd-api-1jq4e9xbzu2ilgn'}
            data = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': prompt}]}

            response = requests.post('https://api.ddosxd.ru/v1/chat', headers=headers, json=data)
            reply = response.json().get('reply')

            if reply:
                await message.edit(f"<b>[GPT35]</b> Ответ: {reply}")
            else:
                await message.edit("<b>[GPT35]</b> Не удалось получить ответ от сервера.")

        except Exception as e:
            return await message.edit(f"<b>[GPT35]</b> Ошибка при отправке запроса: {str(e)}.")
