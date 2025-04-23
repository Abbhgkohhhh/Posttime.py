import schedule
import time
import threading
from telegram.ext import Application
from content_scraper import get_random_content

def job(app: Application):
    async def send():
        content = get_random_content()
        for chat_id in app.chat_data:
            await app.bot.send_message(chat_id=chat_id, text=content)
    app.create_task(send())

def start_scheduling(app: Application):
    schedule.every().day.at("09:00").do(lambda: job(app))
    schedule.every().day.at("19:00").do(lambda: job(app))

    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    t = threading.Thread(target=run_schedule)
    t.start()
