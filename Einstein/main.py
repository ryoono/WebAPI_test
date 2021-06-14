# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

import json
import requests

# JWT用
import time
import base64
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

def main():

    # 環境変数の展開
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    jwt = get_OAuth_Token()
    get_Access_Token( jwt )
    #print(jwt)


# OAuthトークンの取得
# https://metamind.readme.io/docs/generate-an-oauth-token-using-your-key
def get_OAuth_Token():

    EINSTEIN_PLATFORM_KEY = os.environ.get("EINSTEIN_PLATFORM_KEY")
    EINSTEIN_PLATFORM_SERVICES_USERNAME = os.environ.get("EINSTEIN_PLATFORM_SERVICES_USERNAME")

    # JWT header
    # RS256 ... SHA-256を使用したRSA署名
    jwt_headers = {
        "alg" : "RS256",
        "typ" : "JWT"
    }

    # エポック秒の取得(現在時刻から1分後)
    ut = int(time.time()) + 60
    ut = 1623640359

    #JWT Payload
    jwt_payload = {
        "sub": EINSTEIN_PLATFORM_SERVICES_USERNAME,
        "aud": "https://api.einstein.ai/v2/oauth2/token",
        "exp": ut
    }

    # print(json.dumps(jwt_payload))

    # https://ja.wikipedia.org/wiki/JSON_Web_Token
    # Base64エンコード
    # .replace(b'=', b'') ... パディングの'='を消す
    jwt_headers_base64 = base64.b64encode( str(jwt_headers).encode() )#.replace(b'=', b'')
    jwt_payload_base64 = base64.b64encode( str(json.dumps(jwt_payload) ).encode() )#.replace(b'=', b'')
    print(jwt_headers_base64)
    print(jwt_payload_base64)
    signature_target = jwt_headers_base64 + b'.' + jwt_payload_base64
    # print(signature_target)

    # メッセージと秘密鍵から署名を生成
    # https://qiita.com/sho7650/items/1dd65a1db785f902a2d6
    # https://www.python.ambitious-engineer.com/archives/2042
    # print( EINSTEIN_PLATFORM_KEY.replace('\\n', '\n') )
    private_key = RSA.import_key( EINSTEIN_PLATFORM_KEY.replace('\\n', '\n') )
    h = SHA256.new( signature_target )
    jwt_signature = pkcs1_15.new( private_key ).sign( h )

    print(jwt_signature.encode('bytes'))

    jwt = signature_target + b'.' + base64.b64encode( str(jwt_signature).encode() )

    return jwt

def get_Access_Token( jwt ):

    headers = {
        'Content-type': 'application/x-www-form-urlencoded'
    }
    data = 'grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=' + str(jwt)
    # print(data)
    response = requests.post('https://api.einstein.ai/v2/oauth2/token', headers=headers, data=data)
    #print(response.text)

if __name__ == '__main__':
    main()
