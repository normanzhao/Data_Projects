from bs4 import BeautifulSoup
import urllib2
import time
import sqlalchemy
from sqlalchemy import create_engine
import common
import datetime as dt
fields = common.fields
engine = common.engine
import re
startTime = dt.datetime.now()

#DEBUG
'''url = "https://www.firstjob.com/jobs/?date_posted=1&q=/jobs/?date_posted=1&q="+fields[0]
jobs = urllib2.urlopen(url)
soup = BeautifulSoup(jobs, 'html.parser')
for link in soup('div', class_='pos-item clearfix'):
    print link('h4', class_='pos-title text-pad')[0].text.strip(), link('h4', class_='pos-title text-pad')[0].a['href'],\
    link('div', class_='h5 pos-company spc-flush-top text-book text-pad text-trunc')[0].text.strip(), \
    link('div', class_='pos-location text-trunc text-fancy')[0].text.strip()'''
#DEBUG

for field in fields: 
    url = "https://www.firstjob.com/jobs/?date_posted=1&q=/jobs/?date_posted=1&q="+field
    sql = "INSERT INTO `%s-jobs` VALUES"%(field)
    while True:
        try:
            jobs = urllib2.urlopen(url)
        except urllib2.HTTPError:
            print "URL error: ", url
            time.sleep(5)
            break
        soup = BeautifulSoup(jobs, 'html.parser')
        for link in soup('div', class_='pos-item clearfix'):
            try:
                sql += '("%s","%s","%s","%s","%s"),' %(link('h4', class_='pos-title text-pad')[0].text.strip().replace('"','\\"'), link('h4', class_='pos-title text-pad')[0].a['href'],\
                link('div', class_='h5 pos-company spc-flush-top text-book text-pad text-trunc')[0].text.strip().replace('"','\\"'), \
                link('div', class_='pos-location text-trunc text-fancy')[0].text.strip().replace('"','\\"'),\
                re.sub(r'.*?, *', '', link('div', class_='pos-location text-trunc text-fancy')[0].text.strip().replace('"','\\"')))
            except AttributeError: 
                print "Attribute error" 
                pass
            except IndexError: 
                print "Index error"
                pass
            except Exception as e:
                print e
        if soup('a', class_='btn btn-default js-page-button js-next-page-button'):
            url = "https://www.firstjob.com" + soup('a', class_='btn btn-default js-page-button js-next-page-button')[0]['href']
        else: 
            break
            pass
    if sql != "INSERT INTO `%s-jobs` VALUES"%(field):
        try:
            engine.execute(sqlalchemy.text(sql[:-1]))
        except Exception as e:
            print e
            pass

print "Completed in " + str(dt.datetime.now() - startTime)