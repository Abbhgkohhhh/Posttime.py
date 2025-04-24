import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = "7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY"
ADMIN_ID   = 576916081

bot = Bot(token=API_TOKEN)
dp  = Dispatcher(bot)

# داده‌ها در حافظه
categories = {}   # { "دسته": "توضیحات" }
pages      = {}   # { "پیج": "لینک" }

HELP_TEXT = """
دستورات:
🛠️ /addcategory نام|توضیحات    (ادمین)
🗑️ /delcategory نام              (ادمین)
📋 /listcategories               

🛠️ /addpage نام|لینک            (ادمین)
🗑️ /delpage نام                  (ادمین)
📋 /listpages                   

ℹ️ /help
"""

@dp.message_handler(commands=["start","help"])
async def cmd_help(msg: types.Message):
    await msg.reply(HELP_TEXT)

@dp.message_handler(commands=["addcategory"])
async def cmd_addcat(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("⛔️ دسترسی ندارید.")
    try:
        name, desc = msg.text.split(" ",1)[1].split("|",1)
        categories[name.strip()] = desc.strip()
        await msg.reply(f"✅ دسته «{name.strip()}» اضافه شد.")
    except:
        await msg.reply("❌ فرمت اشتباه!\nمثال: /addcategory پوشاک|لباس مردانه و زنانه")

@dp.message_handler(commands=["delcategory"])
async def cmd_delcat(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("⛔️ دسترسی ندارید.")
    name = msg.text.split(" ",1)[1].strip() if " " in msg.text else ""
    if name in categories:
        categories.pop(name)
        await msg.reply(f"✅ دسته «{name}» حذف شد.")
    else:
        await msg.reply("❌ چنین دسته‌ای وجود ندارد.")

@dp.message_handler(commands=["listcategories"])
async def cmd_listcat(msg: types.Message):
    if not categories:
        return await msg.reply("ℹ️ هیچ دسته‌ای ثبت نشده.")
    text = "📂 دسته‌بندی‌ها:\n" + "\n".join(f"• {n}: {d}" for n,d in categories.items())
    await msg.reply(text)

@dp.message_handler(commands=["addpage"])
async def cmd_addpage(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("⛔️ دسترسی ندارید.")
    try:
        name, url = msg.text.split(" ",1)[1].split("|",1)
        pages[name.strip()] = url.strip()
        await msg.reply(f"✅ پیج «{name.strip()}» اضافه شد.")
    except:
        await msg.reply("❌ فرمت اشتباه!\nمثال: /addpage myshop|https://instagram.com/myshop")

@dp.message_handler(commands=["delpage"])
async def cmd_delpage(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("⛔️ دسترسی ندارید.")
    name = msg.text.split(" ",1)[1].strip() if " " in msg.text else ""
    if name in pages:
        pages.pop(name)
        await msg.reply(f"✅ پیج «{name}» حذف شد.")
    else:
        await msg.reply("❌ چنین پیجی وجود ندارد.")

@dp.message_handler(commands=["listpages"])
async def cmd_listp(msg: types.Message):
    if not pages:
        return await msg.reply("ℹ️ هیچ پیجی ثبت نشده.")
    text = "📸 پیج‌ها:\n" + "\n".join(f"• {n}: {u}" for n,u in pages.items())
    await msg.reply(text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
