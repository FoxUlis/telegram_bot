from aiogram import Dispatcher
from aiogram.types import ErrorEvent
from config import config
from utils.logger import setup_logger

logger = setup_logger()

async def error_handler(event: ErrorEvent):
    exception = event.exception
    update = event.update
    
    error_message = (
        f"⚠️ Произошла ошибка:\n"
        f"• Тип: {type(exception).__name__}\n"
        f"• Сообщение: {str(exception)}\n"
    )
    
    logger.error(error_message, exc_info=exception)
    
    if config.ADMIN_ID:
        bot = event.bot if hasattr(event, 'bot') else None
        if bot:
            try:
                await bot.send_message(
                    chat_id=config.ADMIN_ID,
                    text=error_message[:4000]  
                )
            except Exception as e:
                logger.error(f"Не удалось отправить уведомление админу: {e}")

def register_error_handlers(dp: Dispatcher):
    dp.errors.register(error_handler)
