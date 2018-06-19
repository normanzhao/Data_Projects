import time
import sqlalchemy
from sqlalchemy import create_engine
import common
import datetime as dt
fields = common.fields
import re
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None
pd.set_option('display.max_colwidth', -1)
import boto.ses
AWS_ACCESS_KEY = 'AWS_ACCESS_KEY'  
AWS_SECRET_KEY = 'AWS_SECRET_KEY'
connection = boto.ses.connect_to_region(
            'us-east-1',
            aws_access_key_id=AWS_ACCESS_KEY, 
            aws_secret_access_key=AWS_SECRET_KEY
        )

engine = create_engine('mysql+pymysql://reader:vkSJ9XpMtMCJd6Fq@localhost:3306/jobsend.io')
conn = engine.connect()

def cleanPosition(words):
    completed = []
    for word in words.split('-'):
        completed.append(word[0].upper() + word[1:])
    return ' '.join(completed)
    
def send_email(to, data):
    return connection.send_email(
    source = "Jobsend.io <no-reply@jobsend.io>",
    subject = "Your daily Jobsend alert for %s %s in %s!"%(cleanPosition(to.position), cleanPosition(to.field),to.location),
    body = None,
    to_addresses = to.email,
    format='html',
    return_path='no-reply@jobsend.io',
    html_body = data)


startTime = dt.datetime.now()

locations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

positions = {"intern":".*?intern | coop |co-op| co op .*", "entry level":".*?entry.*|\\bI\\b", "mid level":".*?jr|junior.*|\\bII\\b|\\bIII\\b",\
             "senior level":".*?sr|senior.*|\\bIII\\b", "all":""}

greeting = """
Here is your cream of the crop today!
"""

unsub_link = """
If you've gotten a job(Yay!) or just want to stop recieving these emails, press <a href="http://www.jobsend.io/unsubscribe.php?email=%s&unsub=%s">here</a>.
"""

for field in fields:
    sql = "SELECT * FROM `emails` WHERE field='%s'"%(field)	
    emails = pd.read_sql(sql, engine)
    for user in emails.itertuples():
        try:
            locs = "'" +  "','".join(user.location.split(",")) + "'" 
            poss = user.position.split(",") 
            sql = "SELECT * FROM `%s-jobs` WHERE state in (%s)"%(field, locs)
            jobs = pd.read_sql(sql, engine)
            to_email = pd.DataFrame()
            if 'all' in poss:
                to_email = jobs
            else:
                for pos in poss:
                    to_email = pd.concat([to_email,jobs[jobs['title'].str.contains(pos)]], axis=0, ignore_index=True)
            if to_email.shape[0] > 0:
                to_email['title'] = "<a href='" + to_email['link'] + "'>" + to_email['title'] + "</a>"
                to_email.drop(['state','link'], axis=1, inplace = True)
                to_email = to_email.reindex(np.random.permutation(to_email.index))
                data = greeting + to_email[0:20].to_html(escape=False, border=0, index=False)\
                .replace('style="text-align: right;','style="text-align: left;').\
                replace("<td>", "<td style='width:275px; vertical-align:top; padding-right: 25px;'>")
                data += unsub_link%(user.email, user.unsub)
                send_email(user, data)
        except:
            pass
    
connection.send_email(
    source = "Jobsend.io <no-reply@jobsend.io>",
    subject = "The Jobsend for %s was executed successfully!"%(dt.datetime.now().date()),
    body = None,
    to_addresses = "",
    format='html',
    return_path='no-reply@jobsend.io',
    html_body = "The Jobsend for %s was executed successfully!"%(dt.datetime.now().date()))
print "Completed in " + str(dt.datetime.now() - startTime)