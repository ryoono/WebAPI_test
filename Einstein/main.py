# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

import requests
import json

from PIL import Image
import io

# JWT用
import jwt
import time
from Crypto.PublicKey import RSA


def main():

    # 環境変数の展開
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    encoded_jwt = generate_OAuth_Token()
    oauth = get_Access_Token( encoded_jwt )

    # file_path = "./zou.jpg"
    # img = Image.open(file_path, mode='r')
    # img_bytes = io.BytesIO()
    # img.save(img_bytes, format='PNG')
    # img_bytes = img_bytes.getvalue()
    print(oauth)

    headers = {
        'Authorization': 'Bearer ' + oauth,
        'Cache-Control': 'no-cache',
        'Content-Type': 'multipart/form-data'
    }

    files = {
        'sampleLocation': 'https://einstein.ai/images/generalimage.jpg',
        'modelId': 'GeneralImageClassifier'
    }

    print("")
    print(headers)
    print("")
    print(files)
    print("")

    response = requests.post('https://api.einstein.ai/v2/vision/predict', headers=headers, files=files)

    print(response.text)


# OAuthトークンを取得するためのJWT作成
# @return   encoded_jwt     OAuthトークンを取得するためのJWT
# https://metamind.readme.io/docs/generate-an-oauth-token-using-your-key
def generate_OAuth_Token():

    # 環境変数の展開
    EINSTEIN_PLATFORM_KEY = os.environ.get("EINSTEIN_PLATFORM_KEY")
    EINSTEIN_PLATFORM_SERVICES_USERNAME = os.environ.get("EINSTEIN_PLATFORM_SERVICES_USERNAME")

    # エポック秒の取得(現在時刻から30秒後)
    # OAuthトークンの有効時間
    ut = int(time.time()) + 30

    #JWT Payload
    # https://ja.wikipedia.org/wiki/JSON_Web_Token
    jwt_payload = {
        "sub": EINSTEIN_PLATFORM_SERVICES_USERNAME,
        "aud": "https://api.einstein.ai/v2/oauth2/token",
        "exp": ut
    }

    # メッセージと秘密鍵から署名を生成
    # https://qiita.com/sho7650/items/1dd65a1db785f902a2d6
    # https://www.python.ambitious-engineer.com/archives/2042
    private_key = RSA.import_key( EINSTEIN_PLATFORM_KEY.replace('\\n', '\n') )
    key = private_key.exportKey()

    # RS256 ... SHA-256を使用したRSA署名
    encoded_jwt = jwt.encode( jwt_payload, key=key, algorithm="RS256")

    return encoded_jwt


# OAuthトークン取得
# @param    encoded_jwt     EinstuinのOAuthトークン取得用のJWT
def get_Access_Token( encoded_jwt ):

    # ヘッダーとデータの組み立て
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type'    : 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion'     : str(encoded_jwt)
    }

    # OAuthトークン取得申請
    response = requests.post('https://api.einstein.ai/v2/oauth2/token', headers=headers, data=data)
    res_json = json.loads(response.text)

    return res_json['access_token']


if __name__ == '__main__':
    main()
