import logging
import os
from datetime import timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.chat_action import ChatActionSender
from aiogram.exceptions import TelegramAPIError

# Настройки бота
TOKEN = "862090266:AAGN0fM-M_n9xCdW8mxFoREbV_cNttLNYsw"  # Замените на токен вашего бота
CHANNEL_ID = "@bot_test_kitmedia"  # Замените на username или ID вашего канала
ADMIN_ID = 824462834 # Замените на ваш ID для получения уведомлений



# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Папка с файлами для отправки
FILES_DIR = "test"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def check_subscription(user_id: int) -> bool:
    """Проверяет, подписан ли пользователь на канал"""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Ошибка при проверке подписки: {e}")
        return False

def get_subscription_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для проверки подписки"""
    builder = InlineKeyboardBuilder()
    builder.button(text="Проверить подписку ✅", callback_data="check_sub")
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n\n"
        "Этот бот предоставляет доступ к файлам после подписки на наш канал.\n\n"
        "Пожалуйста, подпишитесь на канал, чтобы продолжить.",
        reply_markup=get_subscription_keyboard(),
    )

@dp.callback_query(F.data == "check_sub")
async def check_sub_callback(callback: types.CallbackQuery):
    """Обработчик проверки подписки"""
    await callback.answer()
    
    if await check_subscription(callback.from_user.id):
        await callback.message.edit_text("Спасибо за подписку! Вот доступные файлы:")
        await send_files(callback.message)
    else:
        await callback.message.edit_text(
            "Вы ещё не подписались на канал. Пожалуйста, подпишитесь и попробуйте снова.",
            reply_markup=get_subscription_keyboard(),
        )

async def send_files(message: types.Message):
    """Отправляет файлы пользователю"""
    chat_id = message.chat.id
    
    # Проверяем наличие папки с файлами
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
        await message.answer("Файлы ещё не загружены. Попробуйте позже.")
        await bot.send_message(ADMIN_ID, "Внимание! Папка с файлами пуста. Загрузите файлы.")
        return
    
    files = os.listdir(FILES_DIR)
    if not files:
        await message.answer("Файлы ещё не загружены. Попробуйте позже.")
        await bot.send_message(ADMIN_ID, "Внимание! В папке нет файлов. Загрузите файлы.")
        return

    # Отправляем каждый файл с индикатором "печатает..."
    async with ChatActionSender.upload_document(bot=bot, chat_id=chat_id):
        for file_name in files:
            file_path = os.path.join(FILES_DIR, file_name)

            try:
                with open(file_path, "rb") as file:
                    await bot.send_document(
                        chat_id=chat_id,
                        document=types.BufferedInputFile(file.read(), filename=file_name),
                        caption=f"Файл: {file_name}",
                    )
            except Exception as e:
                logger.error(f"Ошибка при отправке файла {file_name}: {e}")
                await message.answer(f"Не удалось отправить файл {file_name}. Попробуйте позже.")
    
    await message.answer(
        "Все файлы отправлены. Если у вас есть вопросы, обращайтесь к администратору."
    )

@dp.message()
async def handle_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    await message.answer(
        "Пожалуйста, подпишитесь на наш канал, чтобы получить доступ к файлам.",
        reply_markup=get_subscription_keyboard(),
    )
    # Можно добавить отложенное напоминание здесь

async def on_startup(bot: Bot):
    """Действия при запуске бота"""
    await bot.send_message(ADMIN_ID, "Бот успешно запущен!")
    logger.info("Бот запущен...")

async def on_shutdown(bot: Bot):
    """Действия при остановке бота"""
    await bot.send_message(ADMIN_ID, "Бот остановлен.")
    logger.info("Бот остановлен...")

async def main():
    # Устанавливаем обработчики запуска и остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
