# main.py
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from handlers.start_handler import start
from handlers.add_handler import add_page, handle_text
from handlers.approve_handler import approve
from handlers.show_handler import show_category
from handlers.rate_handler import handle_rating_callback
from handlers.help_handler import help_command

from config import TOKEN

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_page))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("show", show_category))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(CallbackQueryHandler(handle_rating_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("ربات در حال اجراست...")
    app.run_polling()
