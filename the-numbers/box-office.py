# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 18:40:57 2018

@author: smehta
"""


#Enter the number of movies on the website
tot_movies = 5568


import urllib.request, json
import re
import time
import requests
from bs4 import BeautifulSoup
from time import strftime


#Function to get the table from the html page
def getMovieBudgetInfo(pageNum):
    if pageNum == 1:
        url = 'https://www.the-numbers.com/movie/budgets/all'
    else:
        url = 'https://www.the-numbers.com/movie/budgets/all/' + str(pageNum)
    
    for i in range(5):
        page = None
        pagetext = None
        
        log3.write(str(pageNum) + '-' + str(pageNum + 100 - 1) + ': Attempt ' + str(i+1) + '-')
        try:
            page = requests.get(url)
            
            if not page:
                log3.write('Page request error' + '\n')
                time.sleep(2)
                continue
            pagetext = page.text
            
            if not pagetext:
                log3.write('Page decode error' + '\n')
                time.sleep(0.5)
                continue
            log3.write('Good page response' + '\n')
            
            soup = BeautifulSoup(pagetext, 'lxml')
            #counter = 1
            for tr in soup.find_all('tr'):
                #if counter % 2 == 0:
                #    continue
                #counter = counter + 1
                tds = tr.find_all('td')  
                for td in tds:
                    try:
                        temp.write(td.text + '|')
                    except:
                        temp.write(str(td.text.encode(encoding = 'ascii', errors = 'replace')).replace("b'", '').replace("'", '') + '|')
                        
                temp.write('\n')
            break
        except:
            log3.write('Failed page acquisition' + '\n')
            time.sleep(1)
            continue
        
    

temp = open('temp.txt', 'a')
temp.write('No' + '|' + 'Release_Date' + '|' + 'Movie_Name' + '|' + 'Budget' + '|' + 'Domestic_Gross' + '|' + 'Worldwide_Gross' + '|' + '\n')

log3 = open('log_getMovieBudget_' + strftime("%Y-%m-%d_%H-%M-%S") + '.txt', 'a')

for i in range(1, tot_movies, 100):
    getMovieBudgetInfo(i)
    
log3.close()
temp.close()    



new = open('MovieFinInfo_' + strftime("%Y-%m-%d_%H-%M-%S") + '.txt', 'a')
old = open('temp.txt', 'r')

for lines in old:
    if len(lines) > 2:
        new.write(lines)
    else:
        continue

old.close()
new.close()

