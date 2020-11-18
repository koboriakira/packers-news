from packers_news.news import NewsList
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date as Date
from datetime import datetime as DateTime
from datetime import timedelta, timezone
from packers_news import controller
from packers_news.slack import Slack


app = FastAPI()
tzinfo = timezone(timedelta(hours=9))


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/packerscom/")
def get_packers_com_news():
    today = _today()
    news_list: NewsList = controller.get_news(
        'https://www.packers.com/rss/news', today)
    controller.add_todoist_reading_list(
        task_title=f'Packers.com {today}',
        news_list=news_list)
    Slack().post(
        text='PACKERS.COMの新着記事',
        content=news_list.to_markdown(),
        filename=f'packers_{today}.md')
    return {"status_code": 200}


@app.post("/packerscom/{date}")
def get_packers_com_news_by_date(date: str):
    news_list: NewsList = controller.get_news(
        'https://www.packers.com/rss/news', Date.fromisoformat(date))
    Slack().post(
        text='PACKERS.COMの新着記事',
        content=news_list.to_markdown(),
        filename=f'packers_{date}.md')
    return {"status_code": 200}


@app.post("/packerswire/")
def get_packerswire_news():
    today = _today()
    news_list: NewsList = controller.get_news(
        'https://packerswire.usatoday.com/feed/', today)
    controller.add_todoist_reading_list(
        task_title=f'PackersWire {today}',
        news_list=news_list)
    Slack().post(
        text='PACKERSWIREの新着記事',
        content=news_list.to_markdown(),
        filename=f'packerswire_{today}.md')
    return {"status_code": 200}


@app.post("/packerswire/{date}")
def get_packerswire_news_by_date(date: str):
    _date = Date.fromisoformat(date)
    news_list: NewsList = controller.get_news(
        url='https://packerswire.usatoday.com/feed/',
        date=_date)
    controller.add_todoist_reading_list(
        task_title=f'PackersWire {_date }',
        news_list=news_list)
    Slack().post(
        text='PACKERSWIREの新着記事',
        content=news_list.to_markdown(),
        filename=f'packerswire_{date}.md')
    return {"status_code": 200}


@app.post("/packers-espn/")
def get_packers_espn():
    today = _today()
    news_list: NewsList = controller.get_espn_news(date=today)
    controller.add_todoist_reading_list(
        task_title=f'ESPN {today}',
        news_list=news_list)
    Slack().post(
        text='ESPNの新着記事',
        content=news_list.to_markdown(),
        filename=f'espn_{today}.md')
    return {"status_code": 200}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/today")
def today():
    return {'today': _today(), 'now': _today()}


def _today() -> Date:
    now = DateTime.now(tz=tzinfo)
    return Date(now.year, now.month, now.day)
