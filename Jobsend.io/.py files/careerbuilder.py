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
'''url = "http://www.careerbuilder.com/jobs-"+fields[0]+"?posted=1"
jobs = urllib2.urlopen(url)
soup = BeautifulSoup(jobs, 'html.parser')
for link in soup('div', class_='job-row'):
    print link('h2', class_='job-title')[0].a.text,"(%s)"%(link('h4', class_='job-text')[0].text.strip()), \
    "http://www.careerbuilder.com/" + link('h2', class_='job-title')[0].a['href'], link('h4', class_='job-text')[1].text.strip(), link('h4', class_='job-text')[2].text.replace('\n','')
'''
#DEBUG

for field in fields: 
    url = "http://www.careerbuilder.com/jobs-"+field+"?posted=1"
    sql = "INSERT INTO `%s-jobs` VALUES"%(field)
    while True:
        try:
            jobs = urllib2.urlopen(url)
        except urllib2.HTTPError:
            print "URL error: ", url
            break
        soup = BeautifulSoup(jobs, 'html.parser')
        for link in soup('div', class_='job-row'):
            try:
                sql += '("%s(%s)","%s","%s","%s","%s"),' %(link('h2', class_='job-title hide-for-medium-up')[0].a.text.replace('"','\\"'), (link('h4', class_='job-text')[0].text.strip()), \
                "http://www.careerbuilder.com/" + link('h2', class_='job-title hide-for-medium-up')[0].a['href'], link('h4', class_='job-text')[1].text.strip().replace('"','\\"'), \
                link('h4', class_='job-text')[2].text.replace('\n','').strip().replace('"','\\"'),\
                re.sub(r'.*?, *', '', link('h4', class_='job-text')[2].text.replace('\n','').strip().replace('"','\\"')))
            except AttributeError: 
                print "Attribute error" 
                pass
            except IndexError: 
                print "Index error"
                pass
            except Exception as e:
                print e
                pass
        if soup('a', {"data-gtm":"jrp-job-list|pagination-next"}) and (soup('a', {"data-gtm":"jrp-job-list|pagination-next"})[0]['aria-disabled'] == 'false'):
            url = soup('a', {"data-gtm":"jrp-job-list|pagination-next"})[0]['href']
        else:
            break
    if sql != "INSERT INTO jobs VALUES":
        try:
            engine.execute(sqlalchemy.text(sql[:-1]))
        except Exception as e:
            print e
            pass
        
print "Completed in " + str(dt.datetime.now() - startTime)