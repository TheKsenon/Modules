from telethon import events, Button
from .. import loader
import requests

@loader.tds
class GPT35Mod(loader.Module):
    """Модуль для отправки запроса к GPT-3.5 Turbo с использованием промпта."""
    
    strings = {"name": "testestest"}

    async def client_ready(self, client, db):
        """Инициализация модуля при запуске клиента."""
        self.client = client

    @events.register(events.NewMessage(incoming=True, from_users=True))
    async def gpt35_handler(self, event):
        """Обработчик для отправки запроса к GPT-3.5 Turbo и получения ответа."""
        try:
            prompt = event.raw_text
            headers = {'Authorization': 'ddosxd-api-1jq4e9xbzu2ilgn'}
            data = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': prompt}]}

            response = requests.post('https://api.ddosxd.ru/v1/chat', headers=headers, json=data)
            reply = response.json().get('reply')

            if reply:
                await event.reply(f"Ответ от GPT-3.5 Turbo: {reply}")
            else:
                await event.respond("Не удалось получить ответ от сервера.", buttons=[Button.url("Подписаться", "https://t.me/XenonModules")])

        except Exception as e:
            await event.respond(f"Ошибка при отправке запроса: {str(e)}")
