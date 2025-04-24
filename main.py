import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# تنظیمات متغیرهای محیطی برای توکن و آیدی ادمین
API_TOKEN = os.getenv('7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY')  # توکن بات از متغیر محیطی
ADMIN_ID = int(os.getenv('576916081'))  # آیدی ادمین از متغیر محیطی

# ایجاد شی Bot و Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ذخیره‌سازی دسته‌بندی‌ها در حافظه
categories = {}

# فرمان /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("سلام! من ربات شما هستم. شما می‌توانید از دستورات زیر استفاده کنید.")

# فرمان /addcategory برای ادمین
@dp.message_handler(commands=['addcategory'])
async def cmd_addcategory(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        try:
            parts = message.text.split(maxsplit=2)
            category_name = parts[1]  # نام دسته‌بندی
            description = parts[2]  # توضیحات دسته‌بندی
            
            categories[category_name] = description
            await message.reply(f"دسته‌بندی '{category_name}' با موفقیت اضافه شد.")
        except IndexError:
            await message.reply("فرمت دستور اشتباه است. لطفاً از دستور به شکل زیر استفاده کنید:\n/addcategory <نام_دسته‌بندی> <توضیحات>")
    else:
        await message.reply("شما دسترسی به این فرمان ندارید.")

# فرمان /viewcategories برای مشاهده دسته‌بندی‌ها
@dp.message_handler(commands=['viewcategories'])
async def cmd_viewcategories(message: types.Message):
    if categories:
        response = "دسته‌بندی‌های موجود:\n"
        for category_name, description in categories.items():
            response += f"• {category_name}: {description}\n"
        await message.reply(response)
    else:
        await message.reply("هیچ دسته‌بندی‌ای اضافه نشده است.")

# فرمان /addpage برای ادمین (اضافه کردن پیج)
@dp.message_handler(commands=['addpage'])
async def cmd_addpage(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        try:
            parts = message.text.split(maxsplit=2)
            page_name = parts[1]  # نام پیج
            page_url = parts[2]  # لینک پیج
            
            if 'pages' not in globals():
                global pages
                pages = {}
            
            pages[page_name] = page_url
            await message.reply(f"پیج '{page_name}' با لینک {page_url} با موفقیت اضافه شد.")
        except IndexError:
            await message.reply("فرمت دستور اشتباه است. لطفاً از دستور به شکل زیر استفاده کنید:\n/addpage <نام_پیج> <لینک_پیج>")
    else:
        await message.reply("شما دسترسی به این فرمان ندارید.")

# فرمان /viewpages برای مشاهده پیج‌ها
@dp.message_handler(commands=['viewpages'])
async def cmd_viewpages(message: types.Message):
    if 'pages' in globals() and pages:
        response = "پیج‌های موجود:\n"
        for page_name, page_url in pages.items():
            response += f"• {page_name}: {page_url}\n"
        await message.reply(response)
    else:
        await message.reply("هیچ پیجی اضافه نشده است.")

# فرمان /admin فقط برای ادمین
@dp.message_handler(commands=['admin'])
async def cmd_admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.reply("سلام ادمین! خوش آمدید.")
    else:
        await message.reply("شما دسترسی به این فرمان ندارید.")

# فرمان /help برای نمایش دستورات
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    help_text = (
        "دستورات موجود:\n"
        "/start - شروع کار با ربات\n"
        "/addcategory <نام_دسته‌بندی> <توضیحات> - افزودن دسته‌بندی جدید (فقط برای ادمین)\n"
        "/viewcategories - مشاهده دسته‌بندی‌های موجود\n"
        "/addpage <نام_پیج> <لینک_پیج> - افزودن پیج جدید (فقط برای ادمین)\n"
        "/viewpages - مشاهده پیج‌های موجود\n"
        "/admin - فقط برای ادمین\n"
        "/help - نمایش لیست دستورات"
    )
    await message.reply(help_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
