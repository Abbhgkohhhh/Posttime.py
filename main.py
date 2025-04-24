import os
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# تنظیمات متغیرهای محیطی برای توکن و آیدی ادمین
API_TOKEN = os.getenv('7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY')  # توکن بات از متغیر محیطی
ADMIN_ID = int(os.getenv('576916081'))  # آیدی ادمین از متغیر محیطی

# اتصال به دیتابیس SQLite
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# ایجاد جدول کاربران در صورت نبود
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    score INTEGER DEFAULT 0
)
''')
conn.commit()

# ایجاد شی Bot و Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# فرمان /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    
    # بررسی اینکه آیا کاربر قبلاً در دیتابیس ثبت شده است یا خیر
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    
    if user is None:
        # اگر کاربر در دیتابیس وجود نداشت، یک رکورد جدید ایجاد می‌کنیم
        cursor.execute("INSERT INTO users (user_id, score) VALUES (?, ?)", (user_id, 0))
        conn.commit()
        await message.reply("سلام! من ربات شما هستم. شما هم‌اکنون ثبت‌نام شدید.")
    else:
        await message.reply("سلام! خوش آمدید، شما قبلاً ثبت‌نام کرده‌اید.")
    
# فرمان /score برای دریافت امتیاز کاربر
@dp.message_handler(commands=['score'])
async def cmd_score(message: types.Message):
    user_id = message.from_user.id
    
    # دریافت امتیاز کاربر از دیتابیس
    cursor.execute("SELECT score FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    
    if user is None:
        await message.reply("شما هنوز ثبت‌نام نکرده‌اید. از دستور /start برای ثبت‌نام استفاده کنید.")
    else:
        await message.reply(f"امتیاز شما: {user[0]}")

# فرمان /admin فقط برای ادمین
@dp.message_handler(commands=['admin'])
async def cmd_admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.reply("سلام ادمین! خوش آمدید.")
    else:
        await message.reply("شما دسترسی به این فرمان ندارید.")

# فرمان /addscore برای ادمین (افزایش امتیاز کاربران)
@dp.message_handler(commands=['addscore'])
async def cmd_addscore(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        # استخراج آیدی کاربر و امتیاز جدید از پیام
        try:
            parts = message.text.split()
            target_user_id = int(parts[1])  # آیدی کاربر هدف
            score_to_add = int(parts[2])    # امتیاز افزوده‌شده
            
            # به روز رسانی امتیاز کاربر
            cursor.execute("UPDATE users SET score = score + ? WHERE user_id = ?", (score_to_add, target_user_id))
            conn.commit()
            
            await message.reply(f"امتیاز کاربر {target_user_id} به میزان {score_to_add} افزایش یافت.")
        except (IndexError, ValueError):
            await message.reply("فرمت دستور اشتباه است. لطفاً از دستور به شکل زیر استفاده کنید:\n/addscore <user_id> <score>")
    else:
        await message.reply("شما دسترسی به این فرمان ندارید.")

# فرمان /resetscore برای ادمین (بازنشانی امتیاز کاربران)
@dp.message_handler(commands=['resetscore'])
async def cmd_resetscore(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        try:
            parts = message.text.split()
            target_user_id = int(parts[1])  # آیدی کاربر هدف
            
            # بازنشانی امتیاز کاربر
            cursor.execute("UPDATE users SET score = 0 WHERE user_id = ?", (target_user_id,))
            conn.commit()
            
            await message.reply(f"امتیاز کاربر {target_user_id} به صفر بازنشانی شد.")
        except (IndexError, ValueError):
            await message.reply("فرمت دستور اشتباه است. لطفاً از دستور به شکل زیر استفاده کنید:\n/resetscore <user_id>")
    else:
        await message.reply("شما دسترسی به این فرمان ندارید.")

# فرمان /help برای نمایش دستورات
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    help_text = (
        "دستورات موجود:\n"
        "/start - شروع کار با ربات\n"
        "/score - مشاهده امتیاز خود\n"
        "/admin - فقط برای ادمین\n"
        "/addscore <user_id> <score> - افزودن امتیاز به کاربر (فقط برای ادمین)\n"
        "/resetscore <user_id> - بازنشانی امتیاز کاربر به صفر (فقط برای ادمین)"
    )
    await message.reply(help_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
