# handlers/add_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from data.models import Page
from data import storage
from config import ADMIN_ID

async def add_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "لطفاً به ترتیب اطلاعات زیر رو بنویس:\n"
        "1. آیدی پیج (مثلاً @yourpage)\n"
        "2. دسته‌بندی\n"
        "3. توضیحات کوتاه\n"
        "4. چه چیزهایی می‌فروشید؟\n"
        "همه رو در یک پیام بفرست."
    )
    context.user_data["adding"] = True

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("adding"):
        parts = update.message.text.strip().split("\n")
        if len(parts) < 4:
            await update.message.reply_text("همه‌ی موارد را کامل بنویس.")
            return
        username, category, desc, products = parts[:4]
        page = Page(
            user_id=update.effective_user.id,
            username=username,
            category=category,
            desc=desc,
            products=products
        )
        storage.pending_pages.append(page)
        await context.bot.send_message(
            ADMIN_ID,
            f"درخواست جدید اضافه کردن پیج:\n"
            f"آیدی: {username}\n"
            f"دسته: {category}\n"
            f"توضیح: {desc}\n"
            f"محصولات: {products}\n\n"
            f"برای تأیید:\n/approve {len(storage.pending_pages)-1}"
        )
        await update.message.reply_text("درخواست شما ثبت شد و در انتظار تأیید ادمین است.")
        context.user_data["adding"] = False
    else:
        await update.message.reply_text("پیامی نامشخص دریافت شد.")
