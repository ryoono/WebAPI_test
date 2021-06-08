# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import time
from datetime import datetime

def main():
    # 環境変数の展開
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    get_OAuth_token()

# OAuthトークンの取得
# https://metamind.readme.io/docs/generate-an-oauth-token-using-your-key
def get_OAuth_token():

    EINSTEIN_PLATFORM_SERVICES_USERNAME = os.environ.get("EINSTEIN_PLATFORM_SERVICES_USERNAME")

    # エポック秒の取得(現在時刻から1分後)
    ut = int(time.time()) + 60

    #JWT Payload
    jwt = {
        "sub": EINSTEIN_PLATFORM_SERVICES_USERNAME,
        "aud": "https://api.einstein.ai/v2/oauth2/token",
        "exp": ut
    }
    print( json.dumps(jwt) )

if __name__ == '__main__':
    main()
