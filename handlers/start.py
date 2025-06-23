# start.py
import telebot
from utils.keyboards import get_subscription_keyboard

def register_start_handlers(bot):
    @bot.message_handler(commands=['start'])
    def cmd_start(message):
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(
                chat_id=message.chat.id,
                text=f"👋 Привет, {message.from_user.first_name}!\n\n"
                     "Я предоставляю доступ к эксклюзивным файлам после подписки на наш канал.\n\n"
                     "Нажмите кнопку ниже чтобы проверить подписку:",
                reply_markup=get_subscription_keyboard()
            )
        except Exception as e:
            bot.reply_to(message, "⚠️ Произошла ошибка. Попробуйте позже.")
            raise e
