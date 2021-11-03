import os
from slack_sdk import WebClient

def slack(token, channel, app, msg):
    # slack_token = os.environ["SLACK_BOT_TOKEN"]
    slack_token = token
    client = WebClient(token=slack_token)

    response = client.chat_postMessage(
        channel=channel,
        text=msg,
        user=app
    )