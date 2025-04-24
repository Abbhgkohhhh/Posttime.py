from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

TOKEN = "7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY"

admin_id = 576916081  # آیدی عددی ادمین

# دیتا ذخیره‌شده
pending_pages = []  # پیج‌هایی که منتظر تأیید ادمین هستن
detailed_pages = {}  # دسته‌بندی‌شده با اطلاعات کامل
rated = {}  # امتیازهای داده‌شده برای جلوگیری از تکرار

# استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای افزودن پیج از دستور /add استفاده کن.")

# افزودن پیج
async def add_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفاً به ترتیب اطلاعات زیر رو بنویس:\n"
                                    "1. آیدی پیج (مثلاً @yourpage)\n"
                                    "2. دسته‌بندی\n"
                                    "3. توضیحات کوتاه\n"
                                    "4. چه چیزهایی می‌فروشید؟\n"
                                    "همه رو در یک پیام بفرست.")

    context.user_data["adding"] = True

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("adding"):
        parts = update.message.text.strip().split("\n")
        if len(parts) < 4:
            await update.message.reply_text("همه‌ی موارد را کامل بنویس.")
            return
        username, category, desc, products = parts[:4]
        page = {
            "user_id": update.effective_user.id,
            "username": username,
            "category": category,
            "desc": desc,
            "products": products,
            "verified": False,
            "scores": []
        }
        pending_pages.append(page)
        await context.bot.send_message(admin_id,
            f"درخواست جدید اضافه کردن پیج:\n"
            f"آیدی: {username}\n"
            f"دسته: {category}\n"
            f"توضیح: {desc}\n"
            f"محصولات: {products}\n\n"
            f"برای تأیید:\n/approve {len(pending_pages)-1}")
        await update.message.reply_text("درخواست شما ثبت شد و در انتظار تأیید ادمین است.")
        context.user_data["adding"] = False
    else:
        await update.message.reply_text("پیامی نامشخص دریافت شد.")

# تأیید توسط ادمین
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != admin_id:
        await update.message.reply_text("دسترسی ندارید.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("مثال: /approve 0")
        return
    idx = int(context.args[0])
    if idx >= len(pending_pages):
        await update.message.reply_text("چنین موردی وجود ندارد.")
        return
    page = pending_pages.pop(idx)
    page["verified"] = True
    detailed_pages.setdefault(page["category"], []).append(page)
    await update.message.reply_text("پیج تأیید شد و اضافه شد.")

# نمایش دسته
async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("فرمت: /show دسته")
        return
    category = context.args[0]
    if category not in detailed_pages or not detailed_pages[category]:
        await update.message.reply_text("هیچ پیجی در این دسته نیست.")
        return
    for page in detailed_pages[category]:
        avg_score = round(sum(page["scores"]) / len(page["scores"]), 2) if page["scores"] else "ثبت نشده"
        verified_str = "✅ مطمئن" if page["verified"] else "❌ نامطمئن"
        text = (
            f"{page['username']}\n"
            f"توضیح: {page['desc']}\n"
            f"محصولات: {page['products']}\n"
            f"وضعیت: {verified_str}\n"
            f"میانگین امتیاز: {avg_score}"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("بازدید از پیج", url=f"https://t.me/{page['username'].strip('@')}")],
            [
                InlineKeyboardButton("امتیاز 1", callback_data=f"rate|{page['username']}|1"),
                InlineKeyboardButton("امتیاز 2", callback_data=f"rate|{page['username']}|2"),
                InlineKeyboardButton("امتیاز 3", callback_data=f"rate|{page['username']}|3"),
                InlineKeyboardButton("امتیاز 4", callback_data=f"rate|{page['username']}|4"),
                InlineKeyboardButton("امتیاز 5", callback_data=f"rate|{page['username']}|5"),
            ]
        ])
        await update.message.reply_text(text, reply_markup=keyboard)

# هندلر امتیازدهی
async def handle_rating_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("|")
    if len(data) != 3 or data[0] != "rate":
        return
    username = data[1]
    score = int(data[2])
    user_key = str(query.from_user.id) + "_" + username
    if rated.get(user_key):
        await query.edit_message_reply_markup()
        await query.message.reply_text("شما قبلاً امتیاز داده‌اید.")
        return
    for pages in detailed_pages.values():
        for page in pages:
            if page["username"] == username:
                page["scores"].append(score)
                rated[user_key] = True
                await query.message.reply_text("امتیاز ثبت شد. ممنون!")
                return

# اجرای ربات
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_page))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("show", show_category))
    app.add_handler(CallbackQueryHandler(handle_rating_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()
