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
'''url = "http://www.engineerjobs.com/jobs/"+fieldS[0]+"/?f=1"
jobs = urllib2.urlopen(url)
soup = BeautifulSoup(jobs, 'html.parser')
for link in soup('tr'):
    print link('td')[0].a.text, "http://www.engineerjobs.com"+link('td')[0].a['data-mdref'], link('td')[1].text, link('td')[2].text'''
#DEBUG

for field in fields: 
    url = "http://www.engineerjobs.com/jobs/"+field+"/?f=1"
    sql = "INSERT INTO `%s-jobs` VALUES"%(field)
    while True:
        try:
            jobs = urllib2.urlopen(url)
        except urllib2.HTTPError:
            print "URL error"
            break
        soup = BeautifulSoup(jobs, 'html.parser')
        for link in soup('tr'):
            try:
                sql += '("%s","%s","%s","%s","%s"),' %(link('td')[0].a.text.replace('"','\\"'), "http://www.engineerjobs.com"+link('td')[0].a['data-mdref'], link('td')[2].text.strip().replace('"','\\"'),\
                                                 link('td')[1].text.strip().replace('"','\\"'), re.sub(r'.*?, *', '', link('td')[1].text.strip().replace('"','\\"')))
            except AttributeError: 
                pass
            except IndexError: 
                pass
            except Exception as e:
                print e
                pass
        try:
            next_ = soup("li", class_="next")
            if next_[0]["class"] == ['next']:
                url = "http://www.engineerjobs.com/" + next_[0].a['href']
            else:
                break
        except IndexError:
            break
    if sql != "INSERT INTO `%s-jobs` VALUES"%(field):
        try:
            engine.execute(sqlalchemy.text(sql[:-1]))
        except Exception as e:
            print e
            pass
        
print "Completed in " + str(dt.datetime.now() - startTime)