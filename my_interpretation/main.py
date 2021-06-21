# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

import requests


# 環境変数の展開
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_URL = os.environ.get("API_URL")

params = (
    ('text', 'African elephant'),
    ('source', 'en'),
    ('target', 'ja'),
)

response = requests.get( API_URL, params=params)

print( response.text )
