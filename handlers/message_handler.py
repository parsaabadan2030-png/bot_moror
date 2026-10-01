from telebot import types
from keyboards.main_menu import main_menu


def register_message_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(
            message.chat.id,
            "سلام 👋\nبه بات مرور درس خوش اومدی!\n\nاز منوی زیر انتخاب کن:",
            reply_markup=main_menu()
        )