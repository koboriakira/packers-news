from packers_news.controller import get_news
from datetime import date as Date


def execute():
    url = 'https://www.packers.com/rss/news'
    news_list = get_news(url=url, date=Date.today())
    print(news_list.to_markdown())


execute()
