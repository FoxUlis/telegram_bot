from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from services.subscription import check_subscription
from utils.keyboards import get_subscription_keyboard
from config import config

class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Получаем пользователя в зависимости от типа события
        if isinstance(event, CallbackQuery):
            user = event.from_user
            message = event.message
        elif isinstance(event, Message):
            user = event.from_user
            message = event
        else:
            return await handler(event, data)

        # Исключения для команды /start и проверки подписки
        if isinstance(event, Message) and event.text and event.text.startswith('/start'):
            return await handler(event, data)
            
        if isinstance(event, CallbackQuery) and event.data == "check_sub":
            return await handler(event, data)
            
        bot = data['bot']
        if await check_subscription(bot, user.id, config.CHANNEL_ID):
            return await handler(event, data)
            
        if isinstance(event, Message):
            await event.answer(
                "❌ Доступ ограничен. Подпишитесь на канал для использования бота.",
                reply_markup=get_subscription_keyboard()
            )
        elif isinstance(event, CallbackQuery):
            await event.answer("❌ Сначала подпишитесь на канал!", show_alert=True)
        
        return False
