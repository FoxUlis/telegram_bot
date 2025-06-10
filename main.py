import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import config
from utils.logger import setup_logger

# Импорт обработчиков
from handlers.start import register_start_handlers
from handlers.files import register_files_handlers
from handlers.errors import register_error_handlers

logger = setup_logger()

async def on_startup(bot: Bot):
    try:
        await bot.send_message(config.ADMIN_ID, "🤖 Бот успешно запущен!")
    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}")

async def on_shutdown(bot: Bot):
    try:
        await bot.send_message(config.ADMIN_ID, "🛑 Бот остановлен")
    except Exception as e:
        logger.error(f"Ошибка при остановке: {e}")

async def main():
    bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    
    register_error_handlers(dp)
    register_start_handlers(dp)
    register_files_handlers(dp)
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())