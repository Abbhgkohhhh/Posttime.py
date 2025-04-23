import telebot

TOKEN = "7922878871:AAGRUsoUOwIV5HnjUsiqharyOAFJs4pnZPY"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من ربات همیشه آنلاین هستم.")

bot.polling()
