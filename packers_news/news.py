from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from datetime import datetime as DateTime
from datetime import date as Date
from googletrans import Translator


translator = Translator()


@dataclass
class News:
    title: str
    published_at: DateTime
    link: str
    summary: str


@dataclass
class NewsList:
    news_list: List[News]
    _i: int = field(init=False, default=0)

    def extract_news(self, date: Date) -> NewsList:
        # print(date.year, date.month, date.day)
        begin_published_at = DateTime(
            date.year, date.month, date.day - 1, 18, 0, 0)
        end_published_at = DateTime(
            date.year, date.month, date.day, 18, 0, 0)

        result = list(
            filter(
                lambda n: n.published_at >= begin_published_at and n.published_at <= end_published_at,
                self.news_list))
        return NewsList(result)

    def to_markdown(self) -> str:
        str_list: List[str] = []
        for news in self:
            str_list.append(f'- [{news.title}]({news.link})')
            ja_title = translator.translate(news.title, dest='ja').text
            str_list.append(f'  - {ja_title}')
            str_list.append(f'  - {news.summary}')
            ja_summary = translator.translate(news.summary, dest='ja').text
            str_list.append(f'  - {ja_summary}')
        return "\n".join(str_list)

    def __iter__(self):
        return self

    def __next__(self) -> News:
        if self._i == len(self.news_list):
            self._i = 0
            raise StopIteration()
        news = self.news_list[self._i]
        self._i += 1
        return news
