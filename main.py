import telebot

from config import BOT_TOKEN
from database import init_db
from handlers.message_handler import register_message_handlers
from handlers.callback_handler import register_callback_handlers


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")


init_db()

bot = telebot.TeleBot(BOT_TOKEN)

register_message_handlers(bot)
register_callback_handlers(bot)


print("Bot is running...")

bot.infinity_polling()