from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton("📚 وارد کردن درس", callback_data="add_lesson"),
        InlineKeyboardButton("🔄 مرورهای امروز", callback_data="today_reviews")
    )

    return keyboard


def review_menu(review_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            "✅ مرور کردم",
            callback_data=f"complete:{review_id}"
        )
    )
    return keyboard