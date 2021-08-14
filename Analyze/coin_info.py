from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import joblib
import pandas as pd
import numpy as np

driver = webdriver.Chrome(ChromeDriverManager().install())

#The search url link
url = 'https://www.huobi.com/en-us/markets/'
driver.get(url)
content = driver.page_source
#Render the html to BeautifulSoup format
soup = BeautifulSoup(content, 'html.parser')

print(soup)

# search = soup.find_all('div', class_='left-wrap')
search = soup.find_all('div', class_='coin-title')
search = soup.find_

print(search)
print(len(search))

# data-v-14c4722b

# for i in search:
    #Select the a tag from the h3 tag (This a tag is nested inside the h3 tg). Index the raw tag out from the list using [0]
    # atag = i.select('p')[0]
    # #Index out the text from the a tag
    # text = atag.findAll(text=True)[0]
    # # print(text)
    # print(i)




