import http.client
import requests
import json
import math

CONN = http.client.HTTPSConnection('qiita.com', 443)
USER_ID = 'riekure'
PER_PAGE = 20
URL = 'https://qiita.com/api/v2/authenticated_user/items'
HEADERS = {"content-type": "application/json", "Authorization": "Bearer "}

class Api:
    # リクエスト結果をJSON形式で返す
    @staticmethod
    def request(http, url) :
        CONN.request(http, url)
        res = CONN.getresponse()
        data = res.read().decode('utf-8')
        return json.loads(data)

    # 投稿数とからページ番号を計算する
    @staticmethod
    def page_count(items_count) :
        return math.floor(items_count / PER_PAGE) + 1

# 投稿数を取得
items_count = Api.request('GET', '/api/v2/users/' + USER_ID)['items_count']
page = Api.page_count(items_count)

# 投稿記事を全て取得
all_article = {}
for i in range(page) :
    res = requests.get(URL + '?page=' + str(i+1), headers=HEADERS)
    list = res.json()
    for item in list :
        item_id = item['id']
        title = item['title']
        url = 'https://qiita.com/api/v2/items/' + item_id
        res = requests.get(url, headers=HEADERS)
        json = res.json()
        page_views_count = json['page_views_count']
