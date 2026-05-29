import os
import telebot

TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً! أرسل رسالتك وسأقوم بتوصيلها للإدارة.")

@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def forward_to_admin(message):
    text = f"رسالة جديدة من {message.chat.id}:\n\n{message.text}"
    bot.send_message(ADMIN_ID, text)

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID)
def reply_to_user(message):
    if message.reply_to_message:
        # استخراج الـ ID من الرسالة
        lines = message.reply_to_message.text.split('\n')
        user_id = lines[0].split(': ')[1]
        bot.send_message(user_id, message.text)
    else:
        bot.reply_to(message, "يرجى عمل رد (Reply) على رسالة الشخص لكي تصل إليه.")

bot.infinity_polling()
