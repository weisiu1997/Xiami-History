#coding:utf-8
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


class Song_info:
    name = "name"
    singer = "name"
    album = "name"
    def __init__(self, n, s, a):
        self.name = n
        self.singer = s
        self.album = a
    def __hash__(self):
        return hash((self.name, self.singer, self.album))

    def __eq__(self, other):
        return (self.name, self.singer, self.album) == (other.name, other.singer, other.album)


song_list = {}

# prepare output file
out = open('Songs.csv','a')
csv_write = csv.writer(out, dialect='excel')

# get internet driver

option = webdriver.ChromeOptions()
# option.add_argument("headless")
driver = webdriver.Chrome('path to chrome driver', chrome_options=option)
link = "https://www.xiami.com/record/account id"
driver.get(link)
time.sleep(1.5)

# get page number
soup = BeautifulSoup(driver.page_source, "lxml")
bottom = soup.find("div", class_= "record-content").find('ul')
page_num = bottom.find_all("li")[-2].text

song_num = 1

for p in range(0,  int(page_num)):
    soup = BeautifulSoup(driver.page_source, "lxml")
    content = soup.find("div", class_= "record-content")
    songs = content.find("div", class_ = "table-container")
    s1 = songs.find("tbody").find_all("tr")
    for i in range(0, len(s1)):
        raw_info = s1[i].find_all("td")

        # get song info    
        name = raw_info[1].text
        singer = raw_info[2].text
        album = raw_info[3].text
        song_info = Song_info(name, singer, album)
        key = hash(song_info)
        
        if key in song_list.keys():
            song_list[key].append(song_num)
        else:
            song_list[key] = [name, singer, album, song_num]
        song_num += 1
       

    # get next page
    button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//li[contains(@title, "下一页")]')))
    button.click()
    time.sleep(0.8)

driver.quit()

# # output
csv_write.writerow(['Song', 'Artist', 'Album', 'Times', 'ID'])
song_list = sorted(song_list.items(), key=lambda d: len(d[1]), reverse = True)
for v in song_list:
    v = v[1]
    if v[0][-1]=='\ue61d':
        v[0] = v[0][:-1]
    w = [v[0], v[1], v[2], len(v)-3]
    for i in range(3, len(v)):
        w.append(song_num - v[len(v) - i + 2])
    csv_write.writerow(w)