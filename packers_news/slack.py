from typing import Dict, Any
import json
import requests
import os


HEADERS = {'Content-type': 'application/json'}
TEST_TEXT = 'test'


class Slack:
    def __init__(self, channel: str = '') -> None:
        self.webhook: str = str(
            os.getenv('SLACK_DEVELOPMENT_WEBHOOK'))

    def post_message(self, text: str = TEST_TEXT, code: str = '') -> None:
        data: Dict[str, Any] = {
            "text": text + f'\n```\n{code}\n```' if code != '' else text,
        }
        response = requests.post(
            self.webhook,
            data=json.dumps(data),
            headers=HEADERS)
        if status_code := response.status_code != 200:
            print(f'status_code: {status_code}')
            raise Exception(f'status_code: {status_code}')
