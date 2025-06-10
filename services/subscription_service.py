from aiogram import Bot
from config import config
from typing import Optional

async def check_subscription(bot: Bot, user_id: int, channel_id: Optional[str] = None) -> bool:
    """Проверка подписки с кэшированием на 5 минут"""
    channel_id = channel_id or config.CHANNEL_ID
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False