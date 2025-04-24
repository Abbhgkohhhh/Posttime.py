# handlers/show_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data import storage

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("فرمت درست: /show دسته")
        return

    category = context.args[0]
    if category not in storage.detailed_pages or not storage.detailed_pages[category]:
        await update.message.reply_text("هیچ پیجی در این دسته ثبت نشده.")
        return

    for page in storage.detailed_pages[category]:
        avg_score = round(sum(page.scores) / len(page.scores), 2) if page.scores else "ثبت نشده"
        verified_str = "✅ مطمئن" if page.verified else "❌ نامطمئن"
        text = (
            f"{page.username}\n"
            f"توضیح: {page.desc}\n"
            f"محصولات: {page.products}\n"
            f"وضعیت: {verified_str}\n"
            f"میانگین امتیاز: {avg_score}"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("بازدید از پیج", url=f"https://t.me/{page.username.strip('@')}")],
            [
                InlineKeyboardButton("امتیاز 1", callback_data=f"rate|{page.username}|1"),
                InlineKeyboardButton("امتیاز 2", callback_data=f"rate|{page.username}|2"),
                InlineKeyboardButton("امتیاز 3", callback_data=f"rate|{page.username}|3"),
                InlineKeyboardButton("امتیاز 4", callback_data=f"rate|{page.username}|4"),
                InlineKeyboardButton("امتیاز 5", callback_data=f"rate|{page.username}|5"),
            ]
        ])
        await update.message.reply_text(text, reply_markup=keyboard)
