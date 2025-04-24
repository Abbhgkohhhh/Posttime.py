import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ——— تنظیمات اولیه ———
API_TOKEN = "7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY"
ADMIN_ID = 576916081

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ——— داده‌ها در حافظه ———
categories: dict[str, str] = {}   # { "نام_دسته": "توضیحات" }
pages: dict[str, str]     = {}    # { "نام_پیج": "لینک" }
admin_states: dict[int, str] = {} # { chat_id: "state_name" }

# ——— توابع کمکی ———
async def send_admin_menu(chat_id: int):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("➕ افزودن دسته", "➖ حذف دسته")
    kb.add("➕ افزودن پیج", "➖ حذف پیج")
    kb.add("📊 آمار", "/viewcategories", "/viewpages", "/help")
    await bot.send_message(chat_id, "👑 پنل ادمین:", reply_markup=kb)

# ——— هندلرها ———

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply(
        "سلام! من ربات معرفی فروشگاه‌ها هستم.\n"
        "برای راهنمایی از /help استفاده کن."
    )

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply(
        "**دستورات کاربران:**\n"
        "/viewcategories - مشاهده دسته‌بندی‌ها\n"
        "/viewpages      - مشاهده پیج‌ها\n\n"
        "**دستورات ادمین:**\n"
        "/admin          - ورود به پنل ادمین",
        parse_mode="Markdown"
    )

@dp.message_handler(commands=['viewcategories'])
async def cmd_viewcategories(message: types.Message):
    if not categories:
        return await message.reply("❗️ هیچ دسته‌ای ثبت نشده.")
    text = "**دسته‌بندی‌ها:**\n"
    for name, desc in categories.items():
        text += f"• **{name}**: {desc}\n"
    await message.reply(text, parse_mode="Markdown")

@dp.message_handler(commands=['viewpages'])
async def cmd_viewpages(message: types.Message):
    if not pages:
        return await message.reply("❗️ هیچ پیجی ثبت نشده.")
    text = "**پیج‌های ثبت‌شده:**\n"
    for name, url in pages.items():
        text += f"• **{name}**: [بازدید]({url})\n"
    await message.reply(text, parse_mode="Markdown")

@dp.message_handler(commands=['admin'])
async def cmd_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply("❌ شما دسترسی به پنل ادمین ندارید.")
    await send_admin_menu(message.chat.id)

@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and m.text == "➕ افزودن دسته")
async def add_category_prompt(message: types.Message):
    admin_states[message.chat.id] = "add_category"
    await message.reply("لطفاً نام دسته و توضیحات را با فرمت زیر ارسال کنید:\n\n`نام|توضیحات`", parse_mode="Markdown")

@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and admin_states.get(m.chat.id) == "add_category")
async def add_category(message: types.Message):
    admin_states.pop(message.chat.id, None)
    try:
        name, desc = map(str.strip, message.text.split("|", 1))
        categories[name] = desc
        await message.reply(f"✅ دسته «{name}» افزوده شد.")
    except:
        await message.reply("❌ فرمت اشتباه! مثال:\n`پوشاک|لباس‌های مردانه و زنانه`", parse_mode="Markdown")
    await send_admin_menu(message.chat.id)

@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and m.text == "➖ حذف دسته")
async def delete_category_prompt(message: types.Message):
    if not categories:
        return await message.reply("❗️ هیچ دسته‌ای برای حذف وجود ندارد.")
    admin_states[message.chat.id] = "delete_category"
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in categories:
        kb.add(name)
    await message.reply("یک دسته برای حذف انتخاب کن:", reply_markup=kb)

@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and admin_states.get(m.chat.id) == "delete_category")
async def delete_category(message: types.Message):
    admin_states.pop(message.chat.id, None)
    name = message.text.strip()
    if name in categories:
        categories.pop(name)
        await message.reply(f"✅ دسته «{name}» حذف شد.")
    else:
        await message.reply("❌ دسته پیدا نشد.")
    await send_admin_menu(message.chat.id)

@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and m.text == "➕ افزودن پیج")
async def add_page_prompt(message: types.Message):
    admin_states[message.chat.id] = "add_page"
    await message.reply("لطفاً نام پیج و لینک را با فرمت زیر ارسال کنید:\n\n`نام|https://instagram.com/yourpage`", parse_mode="Markdown")

@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and admin_states.get(m.chat.id) == "add_page")
async def add_page(message: types.Message):
    admin_states.pop(message.chat.id, None)
    try:
        name, url = map(str.strip, message.text.split("|", 1))
        pages[name] = url
        await message.reply(f"✅ پیج «{name}» افزوده شد.")
    except:
        await message.reply("❌ فرمت اشتباه! مثال:\n`boutique|https://instagram.com/boutique`", parse_mode="Markdown")
    await send_admin_menu(message.chat.id)

@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and m.text == "➖ حذف پیج")
async def delete_page_prompt(message: types.Message):
    if not pages:
        return await message.reply("❗️ هیچ پیجی برای حذف وجود ندارد.")
    admin_states[message.chat.id] = "delete_page"
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in pages:
        kb.add(name)
    await message.reply("یک پیج برای حذف انتخاب کن:", reply_markup=kb)

@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and admin_states.get(m.chat.id) == "delete_page")
async def delete_page(message: types.Message):
    admin_states.pop(message.chat.id, None)
    name = message.text.strip()
    if name in pages:
        pages.pop(name)
        await message.reply(f"✅ پیج «{name}» حذف شد.")
    else:
        await message.reply("❌ پیج پیدا نشد.")
    await send_admin_menu(message.chat.id)

@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and m.text == "📊 آمار")
async def show_stats(message: types.Message):
    await message.reply(
        f"🔹 تعداد دسته‌ها: {len(categories)}\n"
        f"🔹 تعداد پیج‌ها: {len(pages)}"
    )

# ——— اجرای ربات ———
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
