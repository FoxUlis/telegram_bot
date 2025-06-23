# keyboards.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_subscription_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="✅ Проверить подписку", 
        callback_data="check_sub"
    ))
    return markup
