from selenium import webdriver
import datetime
import time
import requests
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(chrome_options=options)
driver.get("https://www.jiosaavn.com/s/playlist/2f2eb4bf021ec45fe1f092f1b530fd68/Selection/VQiQItdV-,xuOxiEGmm6lQ__")

pause_time = 2

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # wait to load page
    time.sleep(pause_time)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height: # which means end of page
        break
    # update the last height
    last_height = new_height

src = driver.page_source

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

for x in range(len(result_list)):
    result_list[x] = result_list[x].replace(", ", "^")
    # print(x)

for h1 in soup.findAll("h1", {"class": "u-h2"}):
    name = h1.text

f = open(name+".txt", "w")
for x in result_list:
    f.write(x+"\n")
f.close
