from feedparser import parse
from datetime import datetime as DateTime
from packers_news.news import News, NewsList
from typing import List
from datetime import timezone, timedelta

tzinfo = timezone(timedelta(hours=0))


def get_news_feed(url: str) -> List[News]:
    news_list: List[News] = []
    for entry in parse(url).entries:
        date: DateTime = DateTime(
            entry.published_parsed.tm_year,
            entry.published_parsed.tm_mon,
            entry.published_parsed.tm_mday,
            entry.published_parsed.tm_hour,
            entry.published_parsed.tm_min,
            0,
            tzinfo=tzinfo
        )
        news = News(
            title=entry.title,
            summary=entry.summary if 'summary' in entry else '',
            published_at=date,
            link=entry.link)
        news_list.append(news)
    return NewsList(news_list)
