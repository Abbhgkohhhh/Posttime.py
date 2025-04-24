from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# توکن رباتت اینجا قرار بگیره
TOKEN = "7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY"

# دسته‌بندی فروشگاهی
categories = {
    "پوشاک": ["@clothingstore1", "@menswear_iran", "@womenfashion_iran"],
    "اکسسوری": ["@accessoryland", "@bijouterie.ir", "@luxuryaccessories"],
    "زیبایی": ["@beautystore_ir", "@makeupline", "@skincarecenter"],
    "غذا": ["@homemadefood", "@iranfoodshop", "@fastfoodmarket"],
    "کتاب": ["@bookstore_iran", "@ketabforoshi", "@digitalbooks_ir"]
}

# دستور start برای نمایش دسته‌بندی‌ها
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cat, callback_data=cat)] for cat in categories]
    await update.message.reply_text(
        "سلام! دسته‌بندی مورد نظر خودتو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# هندلر انتخاب دسته و نمایش پیج‌ها
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    pages = categories.get(category, [])
    keyboard = [[InlineKeyboardButton(p, url=f"https://instagram.com/{p[1:]}")] for p in pages]
    await query.edit_message_text(
        text=f"پیج‌های مربوط به دسته «{category}»:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# راه‌اندازی ربات
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(category_handler))

app.run_polling()
