# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

import json
import time
import requests

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15



def main():
    # 環境変数の展開
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    get_OAuth_token()

# OAuthトークンの取得
# https://metamind.readme.io/docs/generate-an-oauth-token-using-your-key
def get_OAuth_token():

    EINSTEIN_PLATFORM_KEY = os.environ.get("EINSTEIN_PLATFORM_KEY")
    EINSTEIN_PLATFORM_SERVICES_USERNAME = os.environ.get("EINSTEIN_PLATFORM_SERVICES_USERNAME")

    # ヘッダーの作成
    headers = {
        "Content-type: application/x-www-form-urlencoded"
    }

    # エポック秒の取得(現在時刻から1分後)
    ut = int(time.time()) + 60

    #JWT Payload
    jwt = '{"sub": ' +EINSTEIN_PLATFORM_SERVICES_USERNAME + ',"aud": "https://api.einstein.ai/v2/oauth2/token","exp": ' + str(ut) + '}'

    # JWT Payloadに電子署名を行う
    key = RSA.importKey(EINSTEIN_PLATFORM_KEY)  # , passphrase='hogehoge')
    h = SHA256.new(jwt)
    signature = pkcs1_15.new(key).sign(h)

    data = "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=" + signature + "&scope=offline"

    response = requests.post('https://api.einstein.ai/v2/oauth2/token', headers=headers, data=data)

    print( json.dumps(response) )

if __name__ == '__main__':
    main()
