import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ---------------------------
# ۱. تنظیمات اولیه و چک متغیرها
# ---------------------------
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY")
ADMIN_ID_STR = os.getenv("576916081")

if not API_TOKEN:
    raise RuntimeError("❌ متغیر محیطی API_TOKEN ست نشده!")
if not ADMIN_ID_STR:
    raise RuntimeError("❌ متغیر محیطی ADMIN_ID ست نشده!")

try:
    ADMIN_ID = int(ADMIN_ID_STR)
except ValueError:
    raise RuntimeError("❌ ADMIN_ID باید عدد باشد!")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ---------------------------
# ۲. ساختار داده‌ها (در حافظه)
# ---------------------------
categories = {}   # { "نام_دسته": "توضیحات" }
pages = {}        # { "نام_پیج": "لینک_پیج" }

# ---------------------------
# ۳. هندلرها
# ---------------------------

# /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply(
        "سلام! من ربات معرفی فروشگاه‌هام.\n"
        "برای راهنمایی از /help استفاده کن."
    )

# /help
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply(
        "**راهنمای دستورات:**\n"
        "/help - نمایش این راهنما\n"
        "/admin - ورود به پنل ادمین\n"
        "/viewcategories - دیدن دسته‌ها\n"
        "/viewpages - دیدن پیج‌ها\n",
        parse_mode="Markdown"
    )

# /admin
@dp.message_handler(commands=['admin'])
async def cmd_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply("❌ شما ادمین نیستید.")
    # منوی کلی ادمین
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ افزودن دسته", "➖ حذف دسته")
    markup.add("➕ افزودن پیج", "➖ حذف پیج")
    markup.add("📊 آمار")
    await message.reply("👑 پنل ادمین:", reply_markup=markup)

# افزودن دسته
@dp.message_handler(lambda m: m.text == "➕ افزودن دسته")
async def add_category_prompt(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.reply("لطفاً نام دسته و توضیحات را با فرمت زیر ارسال کنید:\n\nنام|توضیحات")

@dp.message_handler(lambda m: "|" in m.text and m.chat.id == ADMIN_ID)
async def add_category(message: types.Message):
    try:
        name, desc = message.text.split("|", 1)
        name, desc = name.strip(), desc.strip()
        categories[name] = desc
        await message.reply(f"✅ دسته «{name}» با توضیح «{desc}» افزوده شد.")
    except:
        await message.reply("❌ فرمت اشتباه است! مثال: پوشاک|لباس‌های مردانه و زنانه")

# حذف دسته
@dp.message_handler(lambda m: m.text == "➖ حذف دسته")
async def delete_category_prompt(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    if not categories:
        return await message.reply("هیچ دسته‌ای وجود ندارد.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for cat in categories:
        markup.add(cat)
    await message.reply("دسته‌ای برای حذف انتخاب کنید:", reply_markup=markup)

@dp.message_handler(lambda m: m.text in categories and m.chat.id == ADMIN_ID)
async def delete_category(message: types.Message):
    cat = message.text
    categories.pop(cat, None)
    await message.reply(f"✅ دسته «{cat}» حذف شد.", reply_markup=types.ReplyKeyboardRemove())

# مشاهده دسته‌ها
@dp.message_handler(commands=['viewcategories'])
async def cmd_viewcategories(message: types.Message):
    if not categories:
        return await message.reply("هیچ دسته‌ای ثبت نشده.")
    text = "**دسته‌بندی‌ها:**\n"
    for name, desc in categories.items():
        text += f"• **{name}**: {desc}\n"
    await message.reply(text, parse_mode="Markdown")

# افزودن پیج
@dp.message_handler(lambda m: m.text == "➕ افزودن پیج")
async def add_page_prompt(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.reply("لطفاً نام پیج و لینک را با فرمت زیر ارسال کنید:\n\nنام|https://instagram.com/yourpage")

@dp.message_handler(lambda m: "|" in m.text and m.chat.id == ADMIN_ID)
async def add_page(message: types.Message):
    try:
        key, url = message.text.split("|", 1)
        key, url = key.strip(), url.strip()
        pages[key] = url
        await message.reply(f"✅ پیج «{key}» افزوده شد.")
    except:
        await message.reply("❌ فرمت اشتباه! مثال: boutique|https://instagram.com/boutique")

# حذف پیج
@dp.message_handler(lambda m: m.text == "➖ حذف پیج")
async def delete_page_prompt(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    if not pages:
        return await message.reply("هیچ پیجی وجود ندارد.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key in pages:
        markup.add(key)
    await message.reply("پیجی را برای حذف انتخاب کن:", reply_markup=markup)

@dp.message_handler(lambda m: m.text in pages and m.chat.id == ADMIN_ID)
async def delete_page(message: types.Message):
    key = message.text
    pages.pop(key, None)
    await message.reply(f"✅ پیج «{key}» حذف شد.", reply_markup=types.ReplyKeyboardRemove())

# مشاهده پیج‌ها
@dp.message_handler(commands=['viewpages'])
async def cmd_viewpages(message: types.Message):
    if not pages:
        return await message.reply("هیچ پیجی ثبت نشده.")
    text = "**پیج‌های ثبت‌شده:**\n"
    for key, url in pages.items():
        text += f"• **{key}**: [بازدید]({url})\n"
    await message.reply(text, parse_mode="Markdown")

# آمار ساده
@dp.message_handler(lambda m: m.text == "📊 آمار")
async def show_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.reply(f"🔹 تعداد دسته‌بندی‌ها: {len(categories)}\n🔹 تعداد پیج‌ها: {len(pages)}")

# ---------------------------
# ۴. حذف کیبوردهای اضافی پس از هر انتخاب
# ---------------------------
@dp.message_handler(lambda m: m.chat.id == ADMIN_ID)
async def remove_keyboard(message: types.Message):
    # این هندلر برای پاک کردن کیبورد بعد از عملیات است
    if message.reply_markup:
        await message.reply("", reply_markup=types.ReplyKeyboardRemove())

# ---------------------------
# ۵. اجرای ربات
# ---------------------------
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
