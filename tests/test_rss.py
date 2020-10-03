from datetime import datetime as DateTime
from packers_news import rss
from packers_news.news import News


def test_get_news_feed():
    URL = 'https://www.packers.com/rss/news'
    actual = rss.get_news_feed(url=URL)

    title = 'Packers WR Darrius Shepherd never stopped believing in himself'
    description = 'Second-year receiver completes comeback to Green Bay’s 53-man roster'
    link = 'https://www.packers.com/news/packers-wr-darrius-shepherd-never-stopped-believing-in-himself'
    pub_jp_date = DateTime(2020, 10, 3, 8, 5, 0)
    news = {
        'title': title,
        'summary': description,
        'published_at': pub_jp_date,
        'link': link
    }
    expect = News(**news)
    print(expect)
    assert expect in actual.news_list
