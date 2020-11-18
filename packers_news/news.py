from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime as DateTime
from datetime import date as Date
from googletrans import Translator
from datetime import timezone, timedelta

translator = Translator()

tzinfo = timezone(timedelta(hours=9))


@dataclass
class News:
    title: str
    published_at: DateTime
    link: str
    summary: str

    def to_attachment(self) -> Dict:
        summary = f'{self.summary}\n{_translate(self.summary)}'
        return {
            "title": self.title,
            "title_link": self.link,
            "fields": [
                {
                    "title": self.translated_title(),
                    "value": summary
                }
            ]
        }

    def translated_title(self) -> str:
        return _translate(self.title)


@dataclass
class NewsList:
    news_list: List[News]
    _i: int = field(init=False, default=0)

    def extract_news(self, date: Date) -> NewsList:
        begin_published_at = DateTime(
            date.year, date.month, date.day - 1, 8, 0, 0, 0, tzinfo=tzinfo)
        end_published_at = DateTime(
            date.year, date.month, date.day, 8, 0, 0, 0, tzinfo=tzinfo)

        result = list(
            filter(
                lambda n: n.published_at >= begin_published_at and n.published_at <= end_published_at,
                self.news_list))
        return NewsList(result)

    def to_attachments(self) -> List[Dict]:
        return list(map(lambda n: n.to_attachment(), self))

    def to_markdown(self) -> str:
        str_list: List[str] = []
        for news in self:
            str_list.append(f'- [{news.title}]({news.link})')
            ja_title = _translate(text=news.title)
            str_list.append(f'  - {ja_title}')
            str_list.append(f'  - {news.summary}')
            ja_summary = _translate(text=news.summary)
            str_list.append(f'  - {ja_summary}')
        return "\n".join(str_list)

    def to_todoist_titles(self) -> List[str]:
        return list(
            map(lambda n: f'{n.translated_title()} {n.link}', self.news_list))

    def is_not_empty(self) -> bool:
        return len(self.news_list) > 0

    def __iter__(self):
        return self

    def __next__(self) -> News:
        if self._i == len(self.news_list):
            self._i = 0
            raise StopIteration()
        news = self.news_list[self._i]
        self._i += 1
        return news


def _translate(text: str) -> str:
    try:
        return translator.translate(text, dest='ja').text
    except Exception:
        print('can\'t translate')
        return ''
