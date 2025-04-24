# handlers/approve_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from data import storage

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("دسترسی ندارید.")
        return
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("مثال: /approve 0")
        return
    idx = int(context.args[0])
    if idx >= len(storage.pending_pages):
        await update.message.reply_text("چنین موردی وجود ندارد.")
        return
    page = storage.pending_pages.pop(idx)
    page.verified = True
    storage.detailed_pages.setdefault(page.category, []).append(page)
    await update.message.reply_text("پیج تأیید شد و اضافه شد.")
