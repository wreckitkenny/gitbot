import os
from slack_sdk import WebClient

proxy = 'http://10.20.23.210:9090'
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

def slack(token, channel, app, msg):
    # slack_token = os.environ["SLACK_BOT_TOKEN"]
    slack_token = token
    client = WebClient(token=slack_token)

    response = client.chat_postMessage(
        channel=channel,
        text=msg,
        user=app
    )