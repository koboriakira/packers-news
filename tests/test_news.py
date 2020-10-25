from packers_news.news import News, NewsList
from datetime import datetime as DateTime
from datetime import date as Date


def test_extract_today_news():
    """
    10/2 08:00 - 10/3 08:00までを「10/3の日のニュース」とする
    """
    # setup
    title = summary = link = 'A'
    published_at = DateTime(2020, 10, 2, 9, 0, 0)
    include_news_A = News(
        title=title,
        summary=summary,
        link=link,
        published_at=published_at)
    title = summary = link = 'B'
    published_at = DateTime(2020, 10, 2, 7, 0, 0)
    exclude_news_B = News(
        title=title,
        summary=summary,
        link=link,
        published_at=published_at)
    title = summary = link = 'C'
    published_at = DateTime(2020, 10, 3, 7, 0, 0)
    include_news_C = News(
        title=title,
        summary=summary,
        link=link,
        published_at=published_at)
    title = summary = link = 'D'
    published_at = DateTime(2020, 10, 3, 9, 0, 0)
    exclude_news_D = News(
        title=title,
        summary=summary,
        link=link,
        published_at=published_at)
    news_list = NewsList([include_news_A, exclude_news_B,
                          include_news_C, exclude_news_D])

    # execute
    actual = news_list.extract_news(date=Date(2020, 10, 3))

    # verify
    expect = NewsList([include_news_A, include_news_C])
    assert actual == expect
