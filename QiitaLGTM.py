import http.client
import json
import math

CONN = http.client.HTTPSConnection('qiita.com', 443)
USER_ID = 'riekure'
PER_PAGE = 100

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
     article = Api.request('GET', '/api/v2/users/' + USER_ID + '/items?page=' + str(i+1) + '&per_page=' + str(PER_PAGE))
     for j in range(PER_PAGE) :
         try :
             all_article[article[j]['title']] = article[j]['likes_count']
         except IndexError :
             break


# いいね（LGTM）の降順にソート
# items() を使用するので tuple になる
tuple_items = sorted(all_article.items(), key=lambda x:x[1], reverse=True)

# markdown の表形式で表示
print('| 記事タイトル | いいねカウント |')
print('|------------|--------------|')
for title, likes_count in tuple_items:
    print('| ' + title + ' | ' + str(likes_count) + ' |')