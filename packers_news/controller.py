from datetime import date as Date
from packers_news import rss


def get_news(url: str, date: Date):
    return rss.get_news_feed(url=url).extract_news(date=date)
