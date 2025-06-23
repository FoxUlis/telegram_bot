from config import config
from utils.logger import setup_logger
import traceback

logger = setup_logger()

def register_error_handlers(bot):
    @bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'document', 'audio', 'video'])
    def handle_all_messages(message):
        try:
            pass
        except Exception as e:
            handle_error(bot, e)

    @bot.callback_query_handler(func=lambda call: True)
    def handle_all_callbacks(call):
        try:
            pass
        except Exception as e:
            handle_error(bot, e)

def handle_error(bot, exception):
    error_message = (
        f"⚠️ Произошла ошибка:\n"
        f"• Тип: {type(exception).__name__}\n"
        f"• Сообщение: {str(exception)}\n"
        f"• Трассировка: {traceback.format_exc()}"
    )
    
    logger.error(error_message)
    
    if config.ADMIN_ID:
        try:
            bot.send_message(
                chat_id=config.ADMIN_ID,
                text=error_message[:4000]
            )
        except Exception as admin_error:
            logger.error(f"Не удалось отправить уведомление админу: {admin_error}")
