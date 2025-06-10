from aiogram import types, Dispatcher
from aiogram.filters import Command
from utils.keyboards import get_subscription_keyboard

async def cmd_start(message: types.Message):
    """Команда /start с обновленной клавиатурой"""
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я предоставляю доступ к эксклюзивным файлам после подписки на наш канал.\n\n"
        "Нажмите кнопку ниже чтобы проверить подписку:",
        reply_markup=get_subscription_keyboard()
    )

def register_start_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))