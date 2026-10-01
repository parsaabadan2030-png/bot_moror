from telebot import types
from database import add_lesson, get_today_reviews, complete_review
from keyboards.main_menu import main_menu, review_menu


user_states = {}


def register_callback_handlers(bot):

    @bot.callback_query_handler(func=lambda call: call.data == "add_lesson")
    def add_lesson_start(call):
        user_states[call.from_user.id] = {"step": "subject"}

        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "📚 اسم درس یا درس‌ماده رو بفرست:\nمثلاً: ریاضی"
        )


    @bot.callback_query_handler(func=lambda call: call.data == "today_reviews")
    def today_reviews(call):
        bot.answer_callback_query(call.id)

        reviews = get_today_reviews(call.from_user.id)

        if not reviews:
            bot.send_message(
                call.message.chat.id,
                "🎉 امروز مرور برنامه‌ریزی‌شده‌ای نداری!",
                reply_markup=main_menu()
            )
            return

        bot.send_message(
            call.message.chat.id,
            "📚 مرورهای امروز:"
        )

        for review in reviews:
            text = (
                f"🔹 {review['subject']} — {review['lesson']}\n"
                f"📅 تاریخ مرور: {review['review_date']}"
            )

            bot.send_message(
                call.message.chat.id,
                text,
                reply_markup=review_menu(review["review_id"])
            )


    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("complete:")
    )
    def complete(call):
        review_id = int(call.data.split(":")[1])

        complete_review(
            review_id,
            call.from_user.id
        )

        bot.answer_callback_query(
            call.id,
            "مرور ثبت شد ✅"
        )

        try:
            bot.edit_message_reply_markup(
                call.message.chat.id,
                call.message.message_id,
                reply_markup=None
            )
        except Exception:
            pass