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
# حذف پیج از دسته‌بندی‌ها
async def remove_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        await update.message.reply_text("شما اجازه‌ی انجام این کار رو ندارید.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("فرمت درست: /removepage دسته @پیج")
        return

    category, page = context.args
    if category not in categories:
        await update.message.reply_text("دسته‌بندی وجود نداره.")
        return

    if page not in categories[category]:
        await update.message.reply_text(f"پیج {page} در این دسته وجود ندارد.")
        return

    categories[category].remove(page)
    save_categories(categories)
    await update.message.reply_text(f"پیج {page} از دسته «{category}» حذف شد.")

# افزودن دسته جدید
async def add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        await update.message.reply_text("شما اجازه‌ی انجام این کار رو ندارید.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("فرمت درست: /addcategory نام_دسته")
        return

    category = context.args[0]
    if category in categories:
        await update.message.reply_text(f"دسته «{category}» قبلاً وجود دارد.")
        return

    categories[category] = []
    save_categories(categories)
    await update.message.reply_text(f"دسته «{category}» اضافه شد.")

# هندلرهای جدید
app.add_handler(CommandHandler("removepage", remove_page))
app.add_handler(CommandHandler("addcategory", add_category))
# کاربران پیج پیشنهاد بدن
pending_requests = {}

async def suggest_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("فرمت درست: /suggest دسته @پیج")
        return

    category = context.args[0]
    page = context.args[1]

    if category not in categories:
        await update.message.reply_text("دسته‌بندی وجود نداره.")
        return

    request_id = str(update.effective_chat.id) + "_" + page
    pending_requests[request_id] = {
        "user_id": update.effective_chat.id,
        "category": category,
        "page": page
    }

    # ارسال برای ادمین
    await context.bot.send_message(
        chat_id=576916081,
        text=f"درخواست جدید اضافه‌کردن پیج:\nدسته: {category}\nپیج: {page}\nبرای تایید:\n/approve {request_id}\nبرای رد:\n/reject {request_id}"
    )

    await update.message.reply_text("درخواست شما ثبت شد و برای بررسی به ادمین ارسال گردید.")

# تأیید درخواست توسط ادمین
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 576916081:
        return

    if len(context.args) != 1:
        await update.message.reply_text("فرمت درست: /approve request_id")
        return

    request_id = context.args[0]
    req = pending_requests.pop(request_id, None)

    if not req:
        await update.message.reply_text("درخواستی با این شناسه وجود ندارد.")
        return

    categories[req["category"]].append(req["page"])
    save_categories(categories)
    await update.message.reply_text(f"پیج {req['page']} به دسته {req['category']} اضافه شد.")

# رد درخواست
async def reject_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 576916081:
        return

    if len(context.args) != 1:
        await update.message.reply_text("فرمت درست: /reject request_id")
        return

    request_id = context.args[0]
    req = pending_requests.pop(request_id, None)

    if not req:
        await update.message.reply_text("درخواستی با این شناسه وجود ندارد.")
        return

    await update.message.reply_text("درخواست رد شد.")

# ثبت هندلرها
app.add_handler(CommandHandler("suggest", suggest_page))
app.add_handler(CommandHandler("approve", approve_request))
app.add_handler(CommandHandler("reject", reject_request))
# ساختار جدید برای ذخیره‌ی پیج‌ها با اطلاعات کامل
detailed_pages = {}  # {category: [{username, desc, products, verified, scores: [5, 4, 3]}]}

# افزودن پیج توسط ادمین با اطلاعات کامل
async def add_detailed_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 576916081:
        return

    if len(context.args) < 4:
        await update.message.reply_text("فرمت: /adddetail دسته @پیج توضیح محصولات مطمئن/نامطمئن")
        return

    category = context.args[0]
    username = context.args[1]
    desc = context.args[2]
    products = context.args[3]
    verified = context.args[4].lower() == "مطمئن"

    if category not in detailed_pages:
        detailed_pages[category] = []

    detailed_pages[category].append({
        "username": username,
        "desc": desc,
        "products": products,
        "verified": verified,
        "scores": []
    })

    await update.message.reply_text(f"پیج {username} با اطلاعات کامل اضافه شد.")

# نمایش پیج‌ها با توضیحات و امتیاز
async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("فرمت: /show دسته")
        return

    category = context.args[0]
    if category not in detailed_pages or not detailed_pages[category]:
        await update.message.reply_text("هیچ پیجی در این دسته نیست.")
        return

    response = f"پیج‌های دسته «{category}»:\n\n"
    for page in detailed_pages[category]:
        avg_score = round(sum(page["scores"]) / len(page["scores"]), 2) if page["scores"] else "ثبت نشده"
        verified_str = "✅ مطمئن" if page["verified"] else "❌ نامطمئن"
        response += (
            f"{page['username']}\n"
            f"توضیح: {page['desc']}\n"
            f"محصولات: {page['products']}\n"
            f"وضعیت: {verified_str}\n"
            f"میانگین امتیاز: {avg_score}\n\n"
        )

    await update.message.reply_text(response)

# امتیازدهی (محدود به یکبار در هر پیج برای هر کاربر)
rated = {}  # user_id + page_username: True

async def rate_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("فرمت: /rate @پیج امتیاز (از 1 تا 5)")
        return

    username = context.args[0]
    try:
        score = int(context.args[1])
        if score < 1 or score > 5:
            raise ValueError
    except:
        await update.message.reply_text("امتیاز باید عددی بین 1 تا 5 باشد.")
        return

    user_key = str(update.effective_user.id) + "_" + username
    if rated.get(user_key):
        await update.message.reply_text("شما قبلاً به این پیج امتیاز داده‌اید.")
        return

    # جستجوی پیج
    for pages in detailed_pages.values():
        for page in pages:
            if page["username"] == username:
                page["scores"].append(score)
                rated[user_key] = True
                await update.message.reply_text("امتیاز شما ثبت شد.")
                return

    await update.message.reply_text("پیجی با این نام یافت نشد.")

# ثبت هندلرها
app.add_handler(CommandHandler("adddetail", add_detailed_page))
app.add_handler(CommandHandler("show", show_category))
app.add_handler(CommandHandler("rate", rate_page))
app.add_handler(CallbackQueryHandler(handle_rating_callback))
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
        await query.message.reply_text("شما قبلاً به این پیج امتیاز داده‌اید.")
        return

    for pages in detailed_pages.values():
        for page in pages:
            if page["username"] == username:
                page["scores"].append(score)
                rated[user_key] = True
                await query.message.reply_text("امتیاز شما ثبت شد.")
                return

    await query.message.reply_text("پیجی با این نام یافت نشد.")
    if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run_polling())
