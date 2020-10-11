from packers_news.news import NewsList
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date as Date
from packers_news import controller
from packers_news.slack import Slack

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/packerscom/")
def get_packers_com_news():
    today = Date.today()
    news_list: NewsList = controller.get_news(
        'https://www.packers.com/rss/news', today)
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
    today = Date.today()
    news_list: NewsList = controller.get_news(
        'https://packerswire.usatoday.com/feed/', today)
    Slack().post(
        text='PACKERSWIREの新着記事',
        content=news_list.to_markdown(),
        filename=f'packerswire_{today}.md')
    return {"status_code": 200}


@app.post("/packerswire/{date}")
def get_packerswire_news_by_date(date: str):
    today = Date.today()
    news_list: NewsList = controller.get_espn_news(date=today)
    Slack().post(
        text='ESPNの新着記事',
        content=news_list.to_markdown(),
        filename=f'espn_{date}.md')
    return {"status_code": 200}


@app.post("/packers-espn/")
def get_packers_espn():
    today = Date.today()
    news_list: NewsList = controller.get_news(
        'https://packerswire.usatoday.com/feed/',
        Date.fromisoformat(today))
    Slack().post(
        text='PACKERSWIREの新着記事',
        content=news_list.to_markdown(),
        filename=f'packerswire_{today}.md')
    return {"status_code": 200}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
