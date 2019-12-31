# モジュールのインポート
import pandas as pd
import urllib
import urllib.error #urllib.requestが発生させる例外
import urllib.request # URLを開いて読むためのモジュール。これで、Webサイトにあるデータにアクセスできる。
import json
import math
from bs4 import BeautifulSoup
import api_key

API_KEY = api_key.API_KEY
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

jiro_location = {}

def scraping(url):
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, features='html.parser')
    response.close()

    jiro_name = []
    cpy_rst_name = soup.find_all('a', class_ = 'list-rst__rst-name-target cpy-rst-name')
    for item in cpy_rst_name:
        jiro_name.append(item.text)

    jiro_value = []
    rating_val = soup.find_all('span', class_ = 'c-rating__val c-rating__val--strong list-rst__rating-val')
    for item in rating_val:
        jiro_value.append(item.text)

    # 辞書の作成
    for i in range(len(jiro_name)):
        jiro_location[jiro_name[i]] = jiro_value[i]



def calc_dist(now_location):
    dist_dict = {}
    for jiro in jiro_location:
        nav_request = 'language=ja&origin={}&destination={}&key={}'.format(now_location,jiro,API_KEY)
        nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
        request = endpoint + nav_request

        #Google Maps Platform Directions APIを実行
        response = urllib.request.urlopen(request).read()

        # 結果をjson形式で取得
        directions = json.loads(response)
        # print(type(directions))
        # print(directions)
        distance = directions['routes'][0]['legs'][0]['distance']['text']
        distance = distance.replace(',', '')
        dist_dict[jiro] = float(distance[0:-3])

    dist_dict_sorted = sorted(dist_dict.items(), key = lambda x:x[1])
    return dist_dict_sorted


if __name__ == '__main__':
    scraping('https://tabelog.com/rstLst/1/?sw=%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3%E4%BA%8C%E9%83%8E&sk=%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3%E4%BA%8C%E9%83%8E')
    scraping('https://tabelog.com/rstLst/2/?sw=%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3%E4%BA%8C%E9%83%8E&sk=%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3%E4%BA%8C%E9%83%8E')
    scraping('https://tabelog.com/rstLst/3/?sw=%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3%E4%BA%8C%E9%83%8E&sk=%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3%E4%BA%8C%E9%83%8E')
    now_location = input('あなたの現在地を入力してください。 : ').replace(' ', '+')
    # gmaps = googlemaps.Client(key = API_KEY)
    # geocode_result = gmaps.geocode(now_location)
    # now_lat = geocode_result[0]['geometry']['location']['lat']
    # now_lng = geocode_result[0]['geometry']['location']['lng']
    # nearest_jiro = near_jiro(now_lat, now_lng)

    dist_list = calc_dist(now_location) # 距離でsortされたラーメン二郎の配列
    print('もっとも近いラーメン二郎は、{ans}です。距離は{dist}km、食べログの評価は、{val}です。いますぐ食べにいきましょう！'.format(ans = dist_list[0][0], dist = str(dist_list[0][1]), val = str(jiro_location[dist_list[0][0]])))

    # 現在地から近いラーメン二郎上位10件を表示するプログラム
    print('---------------------------------------------------------------------------------------------------------------------------------------------')
    print('')
    print('[その他の店舗]')
    for i in range(1, min(100, len(jiro_location))):
        print('{loc} , {dist}km , 食べログ評価 : {val}'.format(loc = dist_list[i][0], dist = dist_list[i][1], val = str(jiro_location[dist_list[i][0]])))