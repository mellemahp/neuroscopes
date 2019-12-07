import urllib
import bs4

from bs4 import BeautifulSoup

sign_options = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", 
    "capricorn", "aquarius", "pisces", ]
day_options = ["today", "yesterday", "tomorrow"]

url_base = "https://fortunetellingplus.com/horoscope/daily/{}-{}.html"
div_class = "mb-30 mt-10"

data = []
for sign in sign_options: 
    for day in day_options:
        url = url_base.format(sign, day)
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, features="html.parser")
        text_div = soup.find('p', class_=div_class)
        txt = text_div.contents[1].replace('â\x80\x94', ' ')
        txt_list = [ x.strip() + '.\n' for x in txt.split('.') if x != '']
        for l in txt_list:
            data.append(l)
            