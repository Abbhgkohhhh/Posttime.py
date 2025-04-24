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
import json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY"
ADMIN_ID = 576916081  # آیدی عددی خودت رو اینجا بذار (از بات @userinfobot بگیر)

# فایل ذخیره‌ی داده‌ها
DATA_FILE = "data.json"

# بارگذاری یا ساخت دیتا
def load_categories():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "پوشاک": [],
            "اکسسوری": [],
            "زیبایی": [],
            "غذا": [],
            "کتاب": []
        }

def save_categories(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

categories = load_categories()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cat, callback_data=cat)] for cat in categories]
    await update.message.reply_text(
        "سلام! دسته‌بندی مورد نظر رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    pages = categories.get(category, [])
    if not pages:
        await query.edit_message_text(f"فعلاً پیجی توی دسته «{category}» ثبت نشده.")
        return
    keyboard = [[InlineKeyboardButton(p, url=f"https://instagram.com/{p[1:]}")] for p in pages]
    await query.edit_message_text(
        text=f"پیج‌های دسته «{category}»:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# افزودن پیج جدید فقط توسط ادمین
async def add_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("شما اجازه‌ی انجام این کار رو ندارید.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("فرمت درست: /addpage دسته @پیج")
        return

    category, page = context.args
    if category not in categories:
        await update.message.reply_text("دسته‌بندی وجود نداره.")
        return

    if page in categories[category]:
        await update.message.reply_text("این پیج قبلاً ثبت شده.")
        return

    categories[category].append(page)
    save_categories(categories)
    await update.message.reply_text(f"پیج {page} به دسته «{category}» اضافه شد.")

# اجرای ربات
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(category_handler))
app.add_handler(CommandHandler("addpage", add_page))

app.run_polling()
