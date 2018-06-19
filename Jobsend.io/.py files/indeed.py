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
'''url = "https://www.indeed.com/jobs?as_and="+fields[0]+"&fromage=1&limit=50&sort=date"
jobs = urllib2.urlopen(url)
soup = BeautifulSoup(jobs, 'html.parser')
for link in soup('div', class_='  row  result'):
    print link('h2', class_='jobtitle')[0].a.text, 'https://www.indeed.com' + link('h2', class_='jobtitle')[0].a['href'],
    try:
        print link('span', class_='company')[0].a.text.strip(), link('span', {'itemprop':'addressLocality'})[0].text.strip()
    except AttributeError:
        print link('span', class_='company')[0].text.strip(), link('span', {'itemprop':'addressLocality'})[0].text.strip()
#DEBUG'''

for field in fields: 
    url = "https://www.indeed.com/jobs?as_and="+field+"&fromage=1&limit=50&sort=date"
    sql = "INSERT INTO `%s-jobs` VALUES"%(field)
    counter = 50
    while True:
        try:
            jobs = urllib2.urlopen(url)
        except urllib2.HTTPError:
            print "URL error: ", url
            break
        soup = BeautifulSoup(jobs, 'html.parser')
        for link in soup('div', class_='  row  result'):
            sql += '("%s","%s",' %(link('h2', class_='jobtitle')[0].a.text.replace('"','\\"'), 'https://www.indeed.com' + link('h2', class_='jobtitle')[0].a['href'])
            try:
                sql += '"%s","%s","%s"),'%(link('span', class_='company')[0].a.text.strip().replace('"','\\"'), link('span', {'itemprop':'addressLocality'})[0].text.strip().replace('"','\\"'),\
                                          re.sub(r'.*?, *', '', link('span', {'itemprop':'addressLocality'})[0].text.strip().replace('"','\\"')))
            except AttributeError:
                try:
                    sql += '"%s","%s","%s"),'%(link('span', class_='company')[0].text.strip().replace('"','\\"'), link('span', {'itemprop':'addressLocality'})[0].text.strip().replace('"','\\"'),\
                                          re.sub(r'.*?, *', '', link('span', {'itemprop':'addressLocality'})[0].text.strip().replace('"','\\"')))
                except:
                    sql += '"%s","%s","%s"),'%('','','')
            except IndexError:
                print "Index error"
                pass
            except Exception as e:
                print e.message
                pass
        if any('Next' in spans.text for spans in soup('span', class_='pn')):
            url = "https://www.indeed.com/jobs?as_and="+field+"&fromage=1&limit=50&sort=date&start="+str(counter)
            counter += 50
        else: 
            break
    if sql != "INSERT INTO `%s-jobs` VALUES"%(field):
        try:
            engine.execute(sqlalchemy.text(sql[:-1]))
        except Exception as e:
            print e
            pass
        
print "Completed in " + str(dt.datetime.now() - startTime)