# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import json

word = input("なにか話しかけてみてください：")

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CHAPLUS_KEY = os.environ.get("CHAPLUS_KEY")

# リクエストに必要なパラメーター
headers = {'content-type':'text/json'}
payload = { 'utterance':word, 'username':'先輩', 'agentState':{'agentName':'エージェント', 'age':'20歳'}}

# APIKEYの部分は自分のAPI鍵を代入してください
url = 'https://www.chaplus.jp/v1/chat?apikey=' + CHAPLUS_KEY

# APIを叩く
res = requests.post(url=url, headers=headers, data=json.dumps(payload))

# 最適と思われるレスポンスを抽出
print( res.json()['bestResponse']['utterance'] )

# jsonの全文を表示する
# jsonファイルはrawデータのため、整形して出力する
data = json.loads( json.dumps( res.json(), ensure_ascii=False))
print( json.dumps( data, ensure_ascii=False, indent=3) ) # インデントはスペース3文字
# print( res.json() )
