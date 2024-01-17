from .. import loader

@loader.tds
class EditMod(loader.Module):
    """Модуль для редактирования сообщений."""
    strings = {'name': 'Edit'}

    async def client_ready(self, client, db):
        self.db = db

    async def editcmd(self, message):
        """Изменить сообщение на указанное."""
        args = message.text.split(' ', 1)

        if len(args) < 2:
            return await message.edit("<b>[Edit Mode]</b> Не указано сообщение для замены!")

        new_message = args[1]
        self.db.set("Edit", "message", new_message)

        return await message.edit("<b>[Edit Mode]</b> Сообщение успешно изменено!")

    async def watcher(self, message):
        new_message = self.db.get("Edit", "message", None)

        if not new_message:
            return

        if message.raw_text.startswith('/edit'):
            return

        await message.edit(new_message)
