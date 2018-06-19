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
'''url = "https://www.monster.com/jobs/search/?q="+fieldS[0]+"&sort=dt.rv.di"
jobs = urllib2.urlopen(url)
soup = BeautifulSoup(jobs, 'html.parser')
for link in soup('div', class_='js_result_details'):
    cur_link = link('div', class_='js_result_details-left')[0]
    print cur_link('div', class_='jobTitle')[0].a['title'], cur_link('div', class_='jobTitle')[0].a['href'], cur_link('div', class_='company')[0].a['title'],
    print cur_link('div',class_='job-specs job-specs-location')[0].a.text.strip()'''
#DEBUG

for field in fields: 
    url = "https://www.monster.com/jobs/search/?q="+field+"&sort=dt.rv.di"
    sql = "INSERT INTO `%s-jobs` VALUES"%(field)
    for page in range(2,41):
        try:
            jobs = urllib2.urlopen(url)
        except urllib2.HTTPError:
            print "URL error: ", url
            break
        soup = BeautifulSoup(jobs, 'html.parser')
        for link in soup('div', class_='js_result_details'):
            cur_link = link('div', class_='js_result_details-left')[0]
            try:
                sql += '("%s","%s","%s",' %(cur_link('div', class_='jobTitle')[0].a['title'].replace('"','\\"'), cur_link('div', class_='jobTitle')[0].a['href'], \
                                            cur_link('div', class_='company')[0].span.text.strip().replace('"','\\"'))
                try:
                    sql += '"%s", "%s"),'%(cur_link('div',class_='job-specs job-specs-location')[0].a.text.strip().replace('"','\\"'),\
                                         re.sub(r'.*?, *', '', cur_link('div',class_='job-specs job-specs-location')[0].a.text.strip().replace('"','\\"')))
                except AttributeError: 
                    sql += '"%s", "%s"),'%(cur_link('div',class_='job-specs job-specs-location')[0].p.text.strip().replace('"','\\"'),\
                                         re.sub(r'.*?, *', '', cur_link('div',class_='job-specs job-specs-location')[0].p.text.strip().replace('"','\\"')))
                if dt.date.today() != dt.datetime.strptime(link('div', class_='job-specs job-specs-date')[0].p.time['datetime'],'%Y-%m-%dT%I:%M').date():
                    break
            except AttributeError: 
                print "Attribute error" 
                pass
            except IndexError: 
                print "Index error"
                pass
            except Exception as e:
                print e
                pass
        url = "https://www.monster.com/jobs/search/?q="+field+"&sort=dt.rv.di&page="+str(page)
    if sql != "INSERT INTO `%s-jobs` VALUES"%(field):
        try:
            engine.execute(sqlalchemy.text(sql[:-1]))
        except Exception as e:
            print e
            pass
    
print "Completed in " + str(dt.datetime.now() - startTime)