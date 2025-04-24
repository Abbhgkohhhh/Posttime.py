# main.py
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TOKEN
from handlers import (
    start_handler,
    add_handler,
    approve_handler,
    show_handler,
    rate_handler,
    help_handler
)

app = Application.builder().token(TOKEN).build()

# ثبت هندلرها
app.add_handler(CommandHandler("start", start_handler.start))
app.add_handler(CommandHandler("add", add_handler.add_page))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_handler.handle_text))
app.add_handler(CommandHandler("approve", approve_handler.approve))
app.add_handler(CommandHandler("show", show_handler.show_category))
app.add_handler(CallbackQueryHandler(rate_handler.handle_rating_callback))
app.add_handler(CommandHandler("help", help_handler.help_command))

app.run_polling()
