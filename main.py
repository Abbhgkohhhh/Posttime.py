import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scheduler import start_scheduling

# توکن ربات رو اینجا بذار
BOT_TOKEN = "7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من یه ربات گمانه‌زن هستم.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    start_scheduling(app)  # اجرای زمان‌بندی پست‌های خودکار

    app.run_polling()
