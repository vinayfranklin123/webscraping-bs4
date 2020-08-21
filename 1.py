import requests
from bs4 import BeautifulSoup

result = requests.get("https://www.jiosaavn.com/s/playlist/2f2eb4bf021ec45fe1f092f1b530fd68/Selection/VQiQItdV-,xuOxiEGmm6lQ__")
src = result.content
result_list = []
abcd = []

soup = BeautifulSoup(src, 'lxml')

divdata = soup.findAll("div", {"class": "c-drag"})

i=0
for div in divdata:
    result_list.append(div.h4.text+'|')

    for p in div.findAll("p"):
        result_list[i]=result_list[i]+str(p.text+'|')

    result2 = requests.get("https://www.jiosaavn.com"+str(div.h4.a.get("href")))
    src2 = result2.content
    soup2 = BeautifulSoup(src2, 'lxml')
    figcap = soup2.findAll("figcaption")
    j=0

    for p in figcap[0].findAll("p"):
        if j == 1:
            result_list[i]=result_list[i]+str(p.span.text).split()[3]+"|"
        if j == 2:
            if(len(str(p.a.text).split())>=2):
                result_list[i]=result_list[i]+str(p.a.text).split()[1]+"|"
        j = j+1

    article = soup2.findAll("article")
    for a in article:
        for div1 in a.findAll("div", {"class": "o-block__body"}):
            if 'Music' in str(div1.p.span.text):
                result_list[i]=result_list[i]+str(div1.h4.text)+"^"

    result_list[i] = result_list[i] + "|" + "https://www.jiosaavn.com"+ str(div.h4.a.get("href"))
    for secdiv in div.findAll("div", {"class": "o-flag__img"}):
        result_list[i] = result_list[i]+ "|" + secdiv.img.get("src")
    i=i+1

for x in result_list:
    x = x.replace(", ", "^")
    # print(x)

for h1 in soup.findAll("h1", {"class": "u-h2"}):
    name = h1.text

f = open(name+".txt", "w")
for x in result_list:
    f.write(x+"\n")
f.close