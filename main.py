import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InputTextMessageContent
from aiogram.utils import executor
import sqlite3
import time

API_TOKEN = '7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY'  # توکن بات خودت رو وارد کن
ADMIN_ID = 576916081  # آیدی عددی ادمین (این رو با آیدی خودت جایگزین کن)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# اتصال به دیتابیس SQLite
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# ایجاد جدول کاربران اگر وجود نداشته باشد
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    score INTEGER DEFAULT 0
)
''')
conn.commit()

# صفحه اصلی منو
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("دعوت از دوستان")
    markup.add(item1)
    return markup
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
# دستورات مدیریتی (فقط برای ادمین)
@dp.message_handler(commands=['admin'])
async def admin_commands(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.answer("سلام ادمین! خوش آمدید.\nدر اینجا می‌تونید دستورات مدیریتی رو اجرا کنید.")
        
        # اضافه کردن دستورات مدیریتی مانند:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("مشاهده آمار کاربران")
        item2 = types.KeyboardButton("حذف کاربر")
        markup.add(item1, item2)
        await message.answer("دستورات مدیریتی:", reply_markup=markup)
    else:
        await message.answer("شما دسترسی به دستورات مدیریتی ندارید.")
        # مشاهده آمار کاربران
@dp.message_handler(lambda message: message.text == "مشاهده آمار کاربران")
async def show_user_stats(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        cursor.execute("SELECT user_id, score FROM users")
        users = cursor.fetchall()
        
        stats = "آمار کاربران:\n"
        for user in users:
            stats += f"کاربر {user[0]}: {user[1]} امتیاز\n"
        
        await message.answer(stats)
    else:
        await message.answer("شما دسترسی به این بخش را ندارید.")

# حذف کاربر
@dp.message_handler(lambda message: message.text == "حذف کاربر")
async def delete_user(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.answer("لطفاً آیدی کاربری که می‌خواهید حذف کنید وارد کنید:")
        
        @dp.message_handler(lambda msg: msg.text.isdigit())
        async def process_user_id(msg: types.Message):
            target_user_id = int(msg.text)
            cursor.execute("DELETE FROM users WHERE user_id = ?", (target_user_id,))
            conn.commit()
            await msg.answer(f"کاربر با آیدی {target_user_id} حذف شد.")
    else:
        await message.answer("شما دسترسی به این بخش را ندارید.")
        # اجرای بات
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
