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
    news_list = controller.get_news(
        'https://www.packers.com/rss/news', today)
    Slack().post_message(text=news_list.to_markdown())


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
