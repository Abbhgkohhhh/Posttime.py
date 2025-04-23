import requests
from bs4 import BeautifulSoup
import random

headers = {'User-Agent': 'Mozilla/5.0'}

def scrape_tahlilbazaar():
    url = "https://www.tahlilbazaar.com/tag/علم+و+تکنولوژی"
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('h3.news-title a')
        return [t.text.strip() for t in titles[:5]]
    except:
        return []

def scrape_goodreads_fantasy():
    url = "https://www.goodreads.com/shelf/show/fantasy"
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('a.bookTitle span')
        return [t.text.strip() for t in titles[:5]]
    except:
        return []

def scrape_afsaneha():
    url = "https://fa.wikipedia.org/wiki/رده:افسانه‌ها"
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('#mw-pages a')
        return [l.text.strip() for l in links[:5]]
    except:
        return []

def scrape_quotes():
    url = "https://www.goodreads.com/quotes/tag/fantasy"
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        quotes = soup.select('.quoteText')
        return [q.get_text(strip=True).split('”')[0] + '”' for q in quotes[:5]]
    except:
        return []

def get_random_scraped_post():
    all_data = (
        scrape_tahlilbazaar() +
        scrape_goodreads_fantasy() +
        scrape_afsaneha() +
        scrape_quotes()
    )
    return random.choice(all_data) if all_data else "محتوایی یافت نشد."
