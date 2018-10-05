# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 17:19:46 2018

@author: smehta

Scrape Amazon ads
"""


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime



#make browser
ua=UserAgent()
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (ua.random)
service_args=['--ssl-protocol=any','--ignore-ssl-errors=true']

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome('chromedriver',desired_capabilities=dcap,service_args=service_args, chrome_options=chrome_options)


keyword = 'Echo'
client = 'Amazon'


driver.get('https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=' + str(keyword))
time.sleep(1.5)

# Find the location of sponsored ads on the first page
temp_list1 = []
counter = 0
locations = []

for i in range(0,25):
    temp_list1.append(driver.find_elements_by_xpath('//*[@id="result_' + str(i) + '"]/div/div/div/div[2]/h5'))

for el in temp_list1:
    if el != [] :
        locations.append(counter)
    counter = counter + 1


b = open('amazon_keyword_v2.txt', 'a')
#Find the product details at the sponsored location


for i in locations:
    products = driver.find_elements_by_xpath('//*[@id="result_' + str(i) + '"]/div/div/div/div[2]/div[2]/div[1]/a')
    company = driver.find_elements_by_xpath('//*[@id="result_' + str(i) + '"]/div/div/div/div[2]/div[2]/div[2]/span[2]')
    prices = driver.find_elements_by_xpath('//*[@id="result_' + str(i) + '"]/div/div/div/div[2]/div[3]/div[1]/div[1]/div[3]/a/span[2]/span')
    
    for prod, comp, price in zip(products, company, prices):
        b.write('Keyword Search' + '|' + client + '|' + str(datetime.now()) + '|' + keyword + '|' + str(i+1) + '|' + prod.text + '|' + comp.text + '|' + price.text + '\n')
                        

b.close()






