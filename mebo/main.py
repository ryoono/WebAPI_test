# coding: UTF-8

import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import json

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MEBO_API_KEY = os.environ.get("MEBO_API_KEY")
MEBO_AGENT_KEY = os.environ.get("MEBO_AGENT_KEY")
MEBO_UID = os.environ.get("MEBO_UID")

word = input("なにか話しかけてみてください：")

# リクエストに必要なパラメーター
headers = { 'Content-Type':'application/json'}
payload = { 'api_key':MEBO_API_KEY, 'agent_id':MEBO_AGENT_KEY, 'utterance':word, 'uid':MEBO_UID}

# APIKEYの部分は自分のAPI鍵を代入してください
url = 'https://api-mebo.dev/api'

# APIを叩く
res = requests.post(url=url, headers=headers, data=json.dumps(payload))

# 最適と思われるレスポンスを抽出
print( res.json()['bestResponse']['utterance'] )