from datetime import date as Date
from packers_news.news import NewsList
from packers_news import rss
from packers_news import espn


def get_news(url: str, date: Date) -> NewsList:
    return rss.get_news_feed(url=url).extract_news(date=date)


def get_espn_news(date: Date) -> NewsList:
    """
    ESPNはrssフィードを使っていないので、スクレイピングで取得する
    """
    return espn.get_news().extract_news(date=date)
