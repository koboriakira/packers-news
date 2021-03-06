from datetime import date as Date
from packers_news.news import NewsList
from packers_news import rss
from packers_news import espn
from packers_news import todoist


def get_news(url: str, date: Date) -> NewsList:
    return rss.get_news_feed(url=url).extract_news(date=date)


def get_espn_news(date: Date) -> NewsList:
    """
    ESPNはrssフィードを使っていないので、スクレイピングで取得する
    """
    return espn.get_news().extract_news(date=date)


def add_todoist_reading_list(task_title: str, news_list: NewsList):
    """
    Todoistの「リーディングリスト」に登録する
    """
    if news_list.is_not_empty():
        todoist.add_reading_list(
            parent_title=task_title,
            sub_titles=news_list.to_todoist_titles(),
            due="today")
