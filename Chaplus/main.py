# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AP = os.environ.get("API_KEY") # 環境変数の値をAPに代入
print(AP)