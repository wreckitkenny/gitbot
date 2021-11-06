import os
from slack_sdk import WebClient

def enableProxy(proxy):
    os.environ['http_proxy'] = proxy 
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy

def slack(oldTag, newTag, cluster, env, repoName, proxy, proxyInfo, token, channel, app):
    slack_token = token
    client = WebClient(token=slack_token)
    
    # Check Proxy enabled
    if proxy == "true": enableProxy(proxyInfo)

    response = client.chat_postMessage(
        channel=channel,
        attachments=[
        {
            "fallback": "There is a fallback message.",
            "color": "#36a64f",
            "author_name": "VNPAY-GITBOT",
            "author_link": "https://github.com/wreckitkenny/gitBot",
            "author_icon": "https://avatars.slack-edge.com/2021-11-03/2704701932560_9e73e7a58c9ddea5cbf6_512.png",
            "title": "{}".format(repoName.split("/")[-1]),
            "title_link": "https://registry.vnpaytest.vn",
            "text": "*Cluster*: {}-{}-workload".format(cluster, env),
            "fields": [
                {
                    "title": "Old tag",
                    "value": "{}".format(oldTag),
                    "short": "fasle"
                },
                {
                    "title": "New tag",
                    "value": "{}".format(newTag),
                    "short": "fasle"
                }
            ]
        }
        ],
        user=app
    )