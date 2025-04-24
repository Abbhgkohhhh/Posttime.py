import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# اتصال به دیتابیس SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# ساخت جدول کاربران (در صورت نبود)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        phone_number TEXT,
        score INTEGER DEFAULT 0
    )
''')
conn.commit()

# هندلر استارت
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    full_name = message.from_user.full_name

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (user_id, username, full_name) VALUES (?, ?, ?)",
                       (user_id, username, full_name))
        conn.commit()
        await message.answer("به ربات خوش آمدی! لطفاً شماره‌ات رو ارسال کن.")
    else:
        await message.answer("خوش برگشتی! شماره‌ات قبلاً ثبت شده.")
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# کیبورد ارسال شماره تلفن
request_phone_kb = ReplyKeyboardMarkup(resize_keyboard=True)
request_phone_kb.add(KeyboardButton("ارسال شماره تلفن", request_contact=True))

@dp.message_handler(lambda message: not message.contact and message.text == "ارسال شماره تلفن")
async def ask_for_phone(message: types.Message):
    await message.answer("لطفاً با دکمه زیر شماره‌ات رو بفرست:", reply_markup=request_phone_kb)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    user_id = message.from_user.id
    phone_number = message.contact.phone_number

    cursor.execute("UPDATE users SET phone_number = ? WHERE user_id = ?", (phone_number, user_id))
    conn.commit()

    await message.answer("شماره تلفن با موفقیت ثبت شد!", reply_markup=types.ReplyKeyboardRemove())
    await show_main_menu(message)

# منوی اصلی
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("مشاهده امتیاز", "دعوت از دوستان")
    return markup

async def show_main_menu(message):
    await message.answer("چه کاری می‌خوای انجام بدی؟", reply_markup=main_menu())

# نمایش امتیاز
@dp.message_handler(lambda message: message.text == "مشاهده امتیاز")
async def show_score(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT score FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        await message.answer(f"امتیاز فعلی شما: {result[0]}")
    else:
        await message.answer("کاربر یافت نشد.")
        # سیستم دعوت از دوستان
@dp.message_handler(lambda message: message.text == "دعوت از دوستان")
async def invite_friends(message: types.Message):
    user_id = message.from_user.id
    invite_link = f"https://t.me/{(await bot.get_me()).username}?start={user_id}"
    await message.answer(f"با ارسال این لینک به دوستات، امتیاز بگیر:\n\n{invite_link}")

# ثبت امتیاز دعوت
@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args()

    # بررسی اینکه کاربر وجود داره یا نه
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_exists = cursor.fetchone()

    if not user_exists:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()

        # بررسی وجود معرف
        if args.isdigit():
            referrer_id = int(args)
            if referrer_id != user_id:
                cursor.execute("UPDATE users SET score = score + 1 WHERE user_id = ?", (referrer_id,))
                conn.commit()
                await bot.send_message(referrer_id, "یک نفر با لینک شما عضو شد و امتیاز گرفتید!")

    await message.answer("خوش آمدی!", reply_markup=main_menu())

# اجرای بات
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
