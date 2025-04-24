# handlers/help_handler.py
from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "**راهنمای ربات فروشگاهی:**\n\n"
        "/start - شروع استفاده از ربات\n"
        "/add - افزودن پیج جدید (برای ثبت فروشگاهت)\n"
        "/show <دسته> - نمایش فروشگاه‌های هر دسته\n"
        "/approve <شماره> - (فقط ادمین) تأیید پیج\n\n"
        "روی دکمه‌های پایین هر پیج می‌تونی کلیک کنی:\n"
        "- 'بازدید از پیج' برای رفتن به فروشگاه\n"
        "- 'امتیاز ۱ تا ۵' برای ثبت نظر (فقط یک‌بار)\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")
