
# coding: utf-8

# In[12]:

import urllib2
from bs4 import BeautifulSoup
import time
import sys


# In[39]:

base_url = "http://scrabble.merriam.com/browse/"

#a=97, z=122
all_words = []
for letter in xrange(97,123):
    page_num = 1
    last_word = ""
    #loop through all the pages
    while True:
        #open url and load entries
        url = base_url + "%s/%s"%(chr(letter),page_num)
        entries = BeautifulSoup(urllib2.urlopen(url), 'html.parser')
        entries = entries.findAll("div", {"class": "entries"})[0].findAll("a")
        
        #save the last word and break loop if the word is the same across 2 pages
        if last_word == entries[-1].text:
            break
        last_word = entries[-1].text
        
        #save words
        for entry in entries:
            all_words.append(entry.text)
            
        #print current url to monitor progress
        page_num += 1
        sys.stdout.write("\r%s" % url)
        sys.stdout.flush()     
        time.sleep(0.5)


# In[40]:

#TODO: save index of the first word of a letter

