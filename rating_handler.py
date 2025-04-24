# handlers/rating_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from data import storage

async def handle_rating_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("|")
    
    if len(data) != 3 or data[0] != "rate":
        return

    username = data[1]
    score = int(data[2])
    user_key = f"{query.from_user.id}_{username}"

    if storage.rated.get(user_key):
        await query.edit_message_reply_markup()
        await query.message.reply_text("شما قبلاً امتیاز داده‌اید.")
        return

    for pages in storage.detailed_pages.values():
        for page in pages:
            if page.username == username:
                page.scores.append(score)
                storage.rated[user_key] = True
                await query.message.reply_text("امتیاز ثبت شد. ممنون!")
                return
