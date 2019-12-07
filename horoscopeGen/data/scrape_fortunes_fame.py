import urllib 
from bs4 import BeautifulSoup
import bs4

file_name = "fortunes_and_fame.html"
with open(file_name) as f: 
    html = f.read()
    
soup = BeautifulSoup(html, features="html.parser")

# find all of certain tag
fortune_divs = soup.find_all("p", class_="fortunes-wall__fortune") 
data = []

for div in fortune_divs: 
    txt = ''
    for i in div.contents: 
        if not isinstance(i, bs4.element.Tag): 
            txt += i

    if txt != '': 
        data.append(txt + '\n')

with open("fortunes_and_fame_cleaned.txt", 'w') as f: 
    for l in data: 
        f.write(l)