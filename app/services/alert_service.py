from app.config import settings
from telegram import Bot


class AlertService():
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.chat_id = settings.TELEGRAM_CHAT_ID

    async def send_alert(self, message: str):
        await self.bot.send_message(chat_id=self.chat_id, text=message)