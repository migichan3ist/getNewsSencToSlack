import requests
import json
from bs4 import BeautifulSoup

# Slackに送る機能
WEB_HOOK_URL = ""

# ニュースを取得する実装
# ヤフー
get_category = ["world", "business", "it-science", "life"]
get_category_name = ["国際", "経済", "IT-科学", "ライフ"]

for i, cate in enumerate(get_category):

    html_doc = requests.get(
        "https://news.yahoo.co.jp/ranking/access/news/" + cate).text
    # print(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')  # BeautifulSoupの初期化

    topics = soup.find_all(
        "li", class_="newsFeed_item newsFeed_item-normal newsFeed_item-ranking")

    requests.post(WEB_HOOK_URL, data=json.dumps({
        "type": "mrkdwn",
        "text": "*" + get_category_name[i] + "*"
    }))

    requests.post(WEB_HOOK_URL, data=json.dumps({
        "type": "divider",
        "text": ""
    }))

    for rank, topic in enumerate(topics[:10]):
        # タイトル取得
        title = topic.find("div", class_="newsFeed_item_title").text
        # URL取得
        URL_div = topic.find("a", class_="newsFeed_item_link")
        URL = URL_div.get("href")
        # print(title)
        # print(URL)

        requests.post(WEB_HOOK_URL, data=json.dumps({
            "type": "mrkdwn",
            "text": str(rank + 1) + "位：" + "<" + URL + "|" + title + ">"
        }))

    requests.post(WEB_HOOK_URL, data=json.dumps({
        "type": "divider",
        "text": "-------------------------------------------------------------------------------------------"
    }))
