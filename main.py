# main.py
import telebot
from config import config
from utils.logger import setup_logger
import time

logger = setup_logger()

def main():
    # Инициализация бота с таймаутами
    bot = telebot.TeleBot(config.TOKEN, parse_mode="HTML", threaded=False)
    
    # Проверка соединения
    try:
        bot.get_me()
        logger.info("Бот успешно подключен к Telegram API")
    except Exception as e:
        logger.error(f"Ошибка подключения: {e}")
        return

    # Импорт и регистрация обработчиков
    from handlers.start import register_start_handlers
    from handlers.files import register_files_handlers
    from handlers.errors import register_error_handlers
    
    register_start_handlers(bot)
    register_files_handlers(bot)
    register_error_handlers(bot)
    
    # Уведомление админа о запуске
    try:
        bot.send_message(config.ADMIN_ID, "🤖 Бот успешно запущен!")
    except Exception as e:
        logger.error(f"Не удалось отправить уведомление админу: {e}")

    # Бесконечный цикл с переподключением
    while True:
        try:
            logger.info("Запуск polling...")
            bot.infinity_polling(timeout=30, long_polling_timeout=10)
        except Exception as e:
            logger.error(f"Ошибка polling: {e}")
            time.sleep(5)  # Пауза перед переподключением
            continue

if __name__ == "__main__":
    main()
