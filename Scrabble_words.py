import urllib2
from bs4 import BeautifulSoup
import time
import sys

base_url = "http://scrabble.merriam.com/browse/"
#indices of letters
indices = {}
#a=97, z=122
all_words = []
for letter in xrange(97,123):
    indices[chr(letter)] = len(all_words)
    page_num = 1
    last_word = ""
    #loop through all the pages
    while True:
        #open url and load entries
        url = base_url + "%s/%s"%(chr(letter),page_num)
        try:
            entries = BeautifulSoup(urllib2.urlopen(url), 'html.parser')
        except:
            continue
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
        time.sleep(0.75)

f = open("words.txt", "w")
for word in all_words:
    f.write("%s\n" % word)

f = open("indices.txt", "w")
for letter in xrange(97,123):
    f.write("%s\n" % indices[chr(letter)])

