import os
from slack import WebClient
from slack.errors import SlackApiError

client = WebClient(token=os.getenv('OAUTH_ACCESS_TOKEN'))


class Slack:
    def __init__(self, channel: str = '') -> None:
        self.webhook: str = str(
            os.getenv('SLACK_DEVELOPMENT_WEBHOOK'))

    def post(self, text: str, content: str, filename: str) -> None:
        try:
            _ = client.files_upload(
                content=content, initial_comment=text, channels='#develop',
                filename=filename, filetype='markdown')
        except SlackApiError as error:
            print(f'Got an error {error.response["error"]}')
