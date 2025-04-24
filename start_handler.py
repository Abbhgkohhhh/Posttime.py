# handlers/start_handler.py
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای افزودن پیج از دستور /add استفاده کن.")
