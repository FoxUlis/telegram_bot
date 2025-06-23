# files.py
import os
import telebot
from config import config
from utils.keyboards import get_subscription_keyboard

active_users = set()

def register_files_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "check_sub")
    def check_sub_callback(call):
        try:
            bot.answer_callback_query(call.id)
            
            # Проверка подписки
            try:
                member = bot.get_chat_member(config.CHANNEL_ID, call.from_user.id)
                is_subscribed = member.status in ["member", "administrator", "creator"]
            except Exception as e:
                bot.send_message(config.ADMIN_ID, f"Ошибка проверки подписки: {e}")
                is_subscribed = False

            if is_subscribed:
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=None
                )
                send_files(bot, call.message)
            else:
                bot.send_message(
                    call.message.chat.id,
                    f"❌ Вы не подписаны на канал! Подпишитесь {config.CHANNEL_ID} и нажмите кнопку снова.",
                    reply_markup=get_subscription_keyboard()
                )
        except Exception as e:
            bot.send_message(call.message.chat.id, "⚠️ Произошла ошибка. Попробуйте позже.")
            raise e

def send_files(bot, message):
    user_id = message.from_user.id
    
    if user_id in active_users:
        return
        
    active_users.add(user_id)
    try:
        bot.send_chat_action(message.chat.id, 'upload_document')
        
        if not os.path.exists(config.FILES_DIR):
            raise FileNotFoundError("Папка с файлами не найдена")
        
        files = [f for f in os.listdir(config.FILES_DIR) if os.path.isfile(os.path.join(config.FILES_DIR, f))]
        if not files:
            raise FileNotFoundError("Нет файлов в папке")

        for file_name in files:
            file_path = os.path.join(config.FILES_DIR, file_name)
            with open(file_path, 'rb') as file:
                bot.send_document(
                    chat_id=message.chat.id,
                    document=file,
                    caption=f"📁 {file_name}",
                    timeout=60
                )
        bot.send_message(message.chat.id, "✅ Все файлы отправлены!")
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Файлы временно недоступны. Попробуйте позже.")
        bot.send_message(config.ADMIN_ID, f"⚠️ Ошибка отправки файлов: {e}")
    finally:
        active_users.remove(user_id)
