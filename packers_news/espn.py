from datetime import date as Date
from typing import List
from packers_news.news import News, NewsList
import requests
from bs4 import BeautifulSoup

ENDPOINT = 'https://www.espn.com'

MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def get_news():
    response = requests.get(f'{ENDPOINT}/blog/green-bay-packers/')
    soup = BeautifulSoup(response.content, 'html.parser')
    news_list: List[News] = []
    for article in soup.select('#article-feed .article'):
        data = {}
        data["title"] = _get_title(article=article)
        data["published_at"] = _get_date(article=article)
        data["summary"] = _get_summary(article=article)
        data["link"] = _get_link(article=article)
        news = News(**data)
        news_list.append(news)
    return NewsList(news_list=news_list)


def _get_title(article) -> str:
    return article.select_one('h1').text


def _get_summary(article) -> str:
    return article.select_one('.article-body p').text


def _get_link(article) -> str:
    return f'{ENDPOINT}{article.attrs["data-src"]}'


def _get_date(article) -> Date:
    for span in article.select('span'):
        if 'data-dateformat' in span.attrs:
            date_str_list = span.text.split(' ')
            month = _get_month(date_str_list[0])
            day = int(date_str_list[1].replace(',', ''))
            year = int(date_str_list[2])
            return Date(year, month, day)
    raise ValueError


def _get_month(text: str) -> int:
    for idx in range(len(MONTH)):
        if MONTH[idx] == text:
            return idx + 1
