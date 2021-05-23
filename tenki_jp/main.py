import re
import requests
from bs4 import BeautifulSoup
import json

import os
from os.path import join, dirname
from dotenv import load_dotenv

def main(url):
    # bs4でパース
    s = soup(url)

    dict = {}

    # 予測地点
    l_pattern = r"(.+)の1時間天気"
    l_src = s.title.text
    dict['location'] = re.findall(l_pattern, l_src)[0]
    print(dict['location'] + "の天気")

    soup_tdy = s.find(id='forecast-point-1h-today')
    soup_tmr = s.find(id='forecast-point-1h-tomorrow')
    soup_dat = s.find(id='forecast-point-1h-dayaftertomorrow')

    dict["today"] = forecast2dict(soup_tdy)
    dict["tomorrow"] = forecast2dict(soup_tmr)
    dict["dayaftertomorrow"] = forecast2dict(soup_dat)

    # JSON形式で出力
    # print(json.dumps(dict, ensure_ascii=False))

def soup(url):
    r = requests.get(url)
    html = r.text.encode(r.encoding)
    return BeautifulSoup(html, 'lxml')

def forecast2dict(soup):
    data = {}

    # 日付処理
    d_pattern = r"(\d+)年(\d+)月(\d+)日"
    d_src = soup.select('.head p')
    date = re.findall(d_pattern, d_src[0].text)[0]
    data["date"] = "%s-%s-%s" % (date[0], date[1], date[2])
    print("=====" + data["date"] + "=====")

    # 一時間ごとのデータ
    ## 取得
    hour          = soup.select('.hour > td')
    weather       = soup.select('.weather > td')
    temperature   = soup.select('.temperature > td')
    prob_precip   = soup.select('.prob-precip > td')
    precipitation = soup.select('.precipitation > td')
    humidity      = soup.select('.humidity > td')
    wind_blow     = soup.select('.wind-blow > td')
    wind_speed    = soup.select('.wind-speed > td')

    ## 格納
    data["forecasts"] = []
    for itr in range(0, 24):
        forecast = {}
        forecast["hour"] = hour[itr].text.strip()
        forecast["weather"] = weather[itr].text.strip()
        forecast["temperature"] = temperature[itr].text.strip()
        forecast["prob-precip"] = prob_precip[itr].text.strip()
        forecast["precipitation"] = precipitation[itr].text.strip()
        forecast["humidity"] = humidity[itr].text.strip()
        forecast["wind-blow"] = wind_blow[itr].text.strip()
        forecast["wind-speed"] = wind_speed[itr].text.strip()
        data["forecasts"].append(forecast)

        print(
            "時刻         ： " + forecast["hour"] + "時" + "\n"
            "天気         ： " + forecast["weather"] + "\n"
            "気温(C)      ： " + forecast["temperature"] + "\n"
            "降水確率(%)  ： " + forecast["prob-precip"] + "\n"
            "降水量(mm/h) ： " + forecast["precipitation"] + "\n"
            "湿度(%)      ： " + forecast["humidity"] + "\n"
            "風向         ： " + forecast["wind-blow"] + "\n"
            "風速(m/s)    ： " + forecast["weather"] + "\n"
        )

    return data

if __name__ == '__main__':

    load_dotenv(verbose=True)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    TENKI_URL = os.environ.get("TENKI_URL")

    # 1時間ごとの気象情報URL
    # 1時間天気のURLを指定してね
    main(TENKI_URL)
