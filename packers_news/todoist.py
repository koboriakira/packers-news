from typing import List
import requests
import json

ENDPOINT = 'https://shytiger-bq2t6hyrka-an.a.run.app/readings/add/'


def add_reading_list(parent_title: str, sub_titles: List[str], due: str):
    url = ENDPOINT
    data = {
        "parent_title": parent_title,
        "sub_titles": sub_titles,
        "due": due
    }
    res = requests.post(url, data=json.dumps(data))
    if res.status_code > 400:
        raise Exception('Todoistへの追加に失敗しました')
