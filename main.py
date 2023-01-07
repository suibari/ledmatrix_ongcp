import requests
from bs4 import BeautifulSoup
import datetime
import re

def getNews():
    atcl_arr_new = []
    
    # 接続
    print(str(datetime.datetime.now())+": getting NEWS...")
    #URL = "https://www.japantimes.co.jp/" # JT
    URL = "https://www.nikkei.com/news/category/" # 日経
    rest = requests.get(URL)
    soup = BeautifulSoup(rest.text, "html.parser")
    
    # HTMLパース
    #atcl_list = soup.find_all(attrs={"class" : "article-title"}) #JT
    atcl_list = soup.select('#CONTENTS_MAIN')[0].find_all(class_=re.compile("_titleL")) # 日経
    
    # 格納
    for atcl in atcl_list:
        print(atcl.string)
        atcl_arr_new.append(atcl.string)
    atcl_arr = atcl_arr_new
    
    return atcl_arr

def getTemperatureAndWeather():
    print(str(datetime.datetime.now())+": getting weather information...")
    URL = "https://tenki.jp/forecast/3/17/4610/14117/" # 青葉区のアメダス
    rest = requests.get(URL)
    soup = BeautifulSoup(rest.text, "html.parser")
    
    temp_tag = soup.select('#rain-temp-btn')[0]
    temp_tag.select('.diff')[0].decompose()
    temp = temp_tag.text
    print(temp)
    
    weather_tag = soup.select('.today-weather')[0].select('p.weather-telop')[0]
    weather_icon_url = soup.select('.today-weather')[0].select('img')[0].get('src')
    weather = weather_tag.text
    print(weather)
    
    return [temp , weather]

def getNewsAndWeather(request):
    result = {}
    
    result["news"] = getNews()
    result["temp"] = getTemperatureAndWeather()[0]
    result["weather"] = getTemperatureAndWeather()[1]
    
    return result