# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 18:19:50 2018

@author: smehta
"""


import datetime
import urllib.request, json
import re
import time
import requests
from bs4 import BeautifulSoup
from time import strftime


#Change the dates here 
start_date = datetime.date( year = 2015, month = 1, day = 1 )
end_date = datetime.date( year = 2018, month = 8, day = 15 )

base_url = 'https://www.the-numbers.com/box-office-chart/daily/'



#Function to get the table from the html page
def getMovieTheaterInfo(pageLink):
    for i in range(5):
        page = None
        pagetext = None
        
        log3.write(pageLink.replace(base_url, '') + ': Attempt ' + str(i+1) + '-')
        try:
            page = requests.get(pageLink)
            
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
            for tr in soup.find_all('tr')[1:]:
                tds = tr.find_all('td')
                temp.write(pageLink.replace(base_url, '') + '|')
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
        







dates = []

for n in range((end_date - start_date).days + 1):
    dates.append(datetime.datetime.strptime(str(start_date + datetime.timedelta(n)), '%Y-%m-%d').strftime('%Y/%m/%d'))




    

temp = open('temp2.txt', 'a')
temp.write('Date' + '|' + 'New_Rank' + '|' + 'Old_Rank' + '|' + 'Movie_Name' + '|' + 'Distributor' + '|' + 'Gross' + '|' + 'Change' + '|' + 'Theaters' + '|' + 'GrossPerTheater' + '|' + 'TotalGross' + '|' + 'Days' + '|' + '\n')

log3 = open('log_getMovieTheaterInfo_' + strftime("%Y-%m-%d_%H-%M-%S") + '.txt', 'a')

for each_date in dates:
    getMovieTheaterInfo(base_url + each_date)
    print(each_date)
    
log3.close()
temp.close()    



new = open('MovieTheaterInfo_' + strftime("%Y-%m-%d_%H-%M-%S") + '.txt', 'a')
old = open('temp2.txt', 'r')

for lines in old:
    if len(lines) > 12:
        new.write(lines)
    else:
        continue

old.close()
new.close()

