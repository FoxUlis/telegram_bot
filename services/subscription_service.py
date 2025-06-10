from aiogram import Bot
from config import config

async def check_subscription(bot: Bot, user_id: int, channel_id: str = None) -> bool:
    channel_id = channel_id or config.CHANNEL_ID
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False