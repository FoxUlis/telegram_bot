from aiogram import types, Dispatcher
from aiogram.utils.chat_action import ChatActionSender
from config import config
from utils.keyboards import get_subscription_keyboard
from services.subscription_service import check_subscription
import os

async def send_files(message: types.Message):
    try:
        if not os.path.exists(config.FILES_DIR):
            raise FileNotFoundError
        
        files = os.listdir(config.FILES_DIR)
        if not files:
            raise FileNotFoundError

        async with ChatActionSender.upload_document(bot=message.bot, chat_id=message.chat.id):
            for file_name in files:
                file_path = os.path.join(config.FILES_DIR, file_name)
                with open(file_path, "rb") as file:
                    await message.bot.send_document(
                        chat_id=message.chat.id,
                        document=types.BufferedInputFile(file.read(), filename=file_name),
                        caption=f"📁 {file_name}"
                    )
        await message.answer("✅ Все файлы отправлены!")
        
    except Exception as e:
        await message.answer("⚠️ Файлы временно недоступны. Попробуйте позже.")
        await message.bot.send_message(config.ADMIN_ID, "⚠️ Внимание! Папка с файлами пуста!")

async def check_sub_callback(callback: types.CallbackQuery):
    """Обработчик кнопки проверки подписки"""
    await callback.answer()
    
    if await check_subscription(callback.bot, callback.from_user.id, config.CHANNEL_ID):
        await send_files(callback.message)
    else:
        await callback.message.answer(
            "❌ Вы не подписаны на канал!",
            reply_markup=get_subscription_keyboard()
        )

def register_files_handlers(dp: Dispatcher):
    dp.callback_query.register(check_sub_callback, lambda c: c.data == "check_sub")