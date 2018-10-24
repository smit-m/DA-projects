# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 12:52:36 2018

@author: smehta

Scrape justwatch.com
"""


from datetime import datetime
import urllib.request, json
import numpy as np
import time
from time import strftime
import os
import requests
from bs4 import BeautifulSoup
import re


path = 'C:/user/temp'
if not os.path.exists(path + '/' + strftime("%m.%d.%Y") + '/'):
	os.makedirs(path + '/' + strftime("%m.%d.%Y") + '/')
filepath = path + '/' + strftime("%m.%d.%Y") + '/'


#create providers list
providers = ['nfx',			#Netflix
             'amp',			#Amazon Prime
             'hlu',			#hulu
             'vyh',			#Yahoo View
             'amz',			#Amazon Video
             'hbn',			#HBO Now
             'yot',			#Youtube
             'ytr',			#Youtube Premium
             'ply',			#Google Play Movies
             'itu',			#iTunes
             'cbs',			#CBS
             'rkc',			#The Roku Channel
             'hop',			#hoopla
             'tcw',			#The CW
             'cws',			#CW Seed
             'stz',			#Starz
             'fdg',			#Fandango Now
             'vdu',			#Vudu
             'sho',			#Showtime
             'pbs',			#PBS
             'pfx',			#Pantaflix
             'knp',			#kanopy
             'fxn',			#FX Now
             'tbv',			#tubi TV
             'pls',			#Playstation
             'msf',			#Microsoft Store
             'mxg',			#Max Go
             'fsk',			#Filmstruck
             'hbg',			#HBO Go
             'abc',			#ABC
             'crk',			#Crackle
             'amc',			#AMC
             'cts',			#Curiosity Stream
             'fnd',			#Fandor
             'nbc',			#NBC
             'epx',			#ePiX
             'ffm',			#freeform
             'his',			#History
             'aae',			#A&E
             'lft',			#Lifetime
             'shd',			#shudder
             'scb',			#Screambox
             'act',			#Acorn TV
             'sdn',			#Sundance Now
             'bbo',			#Britbox
             'gdc',			#Guide Doc
             'rlz',			#Real Eyz
             'mbi',			#MUBI TV
             'nfk']			#Netflix Kids

#create genre list
genre_list = ['act',        #Action 
              'ani',        #Animation
              'cmy',        #Comedy 
              'crm',        #Crime
              'doc',        #Documentary
              'drm',        #Drama
              'fnt',        #Fantasy
              'hst',        #History
              'hrr',        #Horror
              'fml',        #Kids&Family
              'msc',        #Musical
              'trl',        #Thriller
              'rma',        #Romance
              'scf',        #SciFi
              'spt',        #Sports&Fitness
              'war',        #War
              'wsn']        #Western

#create monetization type list
m_type_list = ['flatrate',  #Subscription
               'ads',       #Ads
               'free',      #Free
               'rent',      #Rent
               'buy']       #Buy 
   
#create the year sequence: 2 at a time
seq_length = list(np.arange(1900, datetime.now().year+1, 2))



log1 = open(filepath + 'log_getTotPages_' + strftime("%Y-%m-%d_%H-%M-%S") + '.txt', 'a')
log2 = open(filepath + 'log_getTitlesInfo_' + strftime("%Y-%m-%d_%H-%M-%S") + '.txt', 'a')

jw_url_list = []


for provider in providers:
    f1 = open(filepath + 'JW_' + provider + '_info.txt', 'a', encoding = 'utf-8')
    f1.write('JW_ID' + '|' + 'title' + '|' + 'title_type' + '|' + 'provider' + '|' + 'monetization_type' + '|' + 'genre' + '|' + 'original_language' + '|' + 'original_release_year' + '|' + 'runtime' + '|' + 'max_seasons' + '|' + 'age_certification' + '|' + 'title_url' + '|' + 'poster_url' + '\n')
    f2 = open(filepath + 'JW_' + provider + '_ids.txt', 'a', encoding = 'utf-8')
    f2.write('JW_ID' + '|' + 'title_url' + '\n')
    jw_ids_list = []
    for m_type in m_type_list:
        for genre in genre_list:
            for period in seq_length:
                #find tot_pages
                pageLink = 'https://apis.justwatch.com/content/titles/en_US/popular?body=%7B"age_certifications":null,"content_types":null,"genres":%5B"' + genre + '"%5D,"languages":null,"max_price":null,"min_price":null,"monetization_types":%5B"' + m_type + '"%5D,"page":1,"page_size":30,"presentation_types":null,"providers":%5B"' + provider + '"%5D,"release_year_from":' + str(period) + ',"release_year_until":' + str(period + 1) + ',"scoring_filter_types":null,"timeline_type":null%7D'
                for trial in range(1,6):
                    log1.write(provider + '-' + m_type + '-' + genre + ': from:' + str(period) + ' to:' + str(period+1) + ':Attempt ' + str(trial) + ':')
                    try:
                        with urllib.request.urlopen(pageLink) as url1:
                            data=json.loads(url1.read().decode())
                            
                        tot_pages = data['total_pages']
                        tot_results = data['total_results']
                        log1.write('Success:- Total Pages:' + str(tot_pages) + ' Total Results:' + str(tot_results) + '\n')
                        break
                    except Exception as e:
                        log1.write('Fail' + '\n')
                        time.sleep(2)
                                       
                for pagenum in range(1,tot_pages+1):
                    url = 'https://apis.justwatch.com/content/titles/en_US/popular?body=%7B"age_certifications":null,"content_types":null,"genres":%5B"' + genre + '"%5D,"languages":null,"max_price":null,"min_price":null,"monetization_types":%5B"' + m_type + '"%5D,"page":' + str(pagenum) + ',"page_size":30,"presentation_types":null,"providers":%5B"' + provider + '"%5D,"release_year_from":' + str(period) + ',"release_year_until":' + str(period + 1) + ',"scoring_filter_types":null,"timeline_type":null%7D'
                    for trial in range(1,6):
                        log2.write(provider + ':' + m_type + ":" + genre + ': from:' + str(period) + ' to:' + str(period+1) + ': Page ' + str(pagenum) + ':Attempt ' + str(trial) + ':')
                        try:
                            with urllib.request.urlopen(url) as url2:
                                data=json.loads(url2.read().decode())    
                            log2.write('Success' + '\n')
                            break
                        except Exception as e:
                            log2.write('Fail' + '\n')
                            time.sleep(2)
                    print("Getting... " + provider + ':' + m_type + ":" + genre + ': from:' + str(period) + ' to:' + str(period+1) + ': Page ' + str(pagenum))
                    for ii in range(0,len(data['items'])):
                        jw_id = data['items'][ii].get('id', 'NA')
                        title_url = data['items'][ii].get('full_path', 'NA')
                        
                        if jw_id not in jw_ids_list:
                            jw_ids_list.append(jw_id)
                            jw_url_list.append(title_url)
                            f2.write(str(jw_id) + '|' + str(title_url) + '\n')
                        
                        try:
                            title = data['items'][ii].get('title', 'NA')
                        except:
                            title = data['items'][ii].get('title', 'NA').encode(encoding = 'ascii', errors = 'replace')
                        title_type = data['items'][ii].get('object_type', 'NA')
                        poster_url = data['items'][ii].get('poster', 'NA')
                        language = data['items'][ii].get('original_language', 'NA')
                        runtime = data['items'][ii].get('runtime', 'NA')
                        max_seasons = data['items'][ii].get('max_season_number', 'NA')
                        age_cert = data['items'][ii].get('age_certification', 'NA')
                        release_year = data['items'][ii].get('original_release_year', 'NA')
                        
                        f1.write(str(jw_id) + '|' + str(title) + '|' + title_type + '|' + provider + '|' + m_type + '|' + genre + '|' + language + '|' + str(release_year) + '|' + str(runtime) + '|' + str(max_seasons) + '|' + str(age_cert) + '|' + 'https://www.justwatch.com' + title_url + '|' + 'https://images.justwatch.com' + poster_url.replace('{profile}', '') + 's166' + '\n')
                                
    f1.close()
    f2.close()
        
    
    
    
    
log1.close()    
log2.close()


f3 = open(filepath + 'JW_urls.txt', 'a')
urls = list(set(jw_url_list))
for url in urls:
    f3.write(url + '\n')
    
f3.close()
 

################################
#
#Phase 2: Get info from individual pages
#
################################

#filepath = 'S:/Analytics Clients/OTT Content Repo/'


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from time import strftime

print('Start: ' + strftime('%b %d, %Y %H:%M'))   


ua=UserAgent()
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (ua.random)
service_args=['--ssl-protocol=any','--ignore-ssl-errors=true']

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome('chromedriver',desired_capabilities=dcap,service_args=service_args, options=chrome_options)

url_base = 'https://www.justwatch.com'

url_list = open('JW_urls.txt', 'r')
info = open('JW_ratings.txt', 'a')
info.write('url_base_key' + '|' + 'JW_Rating' + '|' + 'IMDB_Score' + '|' + 'TomatoMeter' + '\n') 

for urls in url_list:
    pageurl = url_base + urls.strip()
    driver.get(pageurl)
    time.sleep(0.5)
    print('Getting info for: ' + pageurl)
    
    jw = driver.find_elements_by_xpath('//*[contains(@id,"justwatch_rating")]')
    tm = driver.find_elements_by_xpath('//*[contains(@id,"tomato_meter")]')
    im = driver.find_elements_by_xpath('//*[contains(@id,"imdb_score")]')
    
    info.write(urls.strip() + '|')
    if jw != []: 
        info.write(jw[1].text + '|')
    else:
        info.write('NA' + '|')
    if im != []: 
        info.write(str(im[1].text) + '|')
    else:
        info.write('NA' + '|')
    if tm != []: 
        info.write(tm[1].text)
    else:
        info.write('NA')
    
    info.write('\n')

info.close()    
url_list.close()


print('End: ' + strftime('%b %d, %Y %H:%M'))   

