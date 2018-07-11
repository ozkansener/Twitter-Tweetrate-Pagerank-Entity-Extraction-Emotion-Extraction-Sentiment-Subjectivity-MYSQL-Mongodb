# -*- coding: utf-8 -*-
"""
Todo:
Challanges:
    Problems with websites like
    http://www.goal.com/en/news/paul-pogba-can-lead-france-to-world-cup-glory-says-claude/bdtneqpw48lt1sh9vdtmvdno6/

Questions:
    Shall I add zero for missing Value or Shall I terminate when features are not present
    Remove URLs from or analyse URLs they mention
    
@author: ozkan
"""
from pattern.en import suggest
from urllib2 import Request, urlopen, URLError
import sys
from pandas.io.json import json_normalize
import pandas as pd
import requests
from gensim.summarization import keywords
from gensim.summarization import summarize
from textstat.textstat import textstat
from textblob import TextBlob
import urllib2
import goose
import json
import simplejson
import sys
import os
from pattern.en import parse, Sentence, parse
from pattern.en import modality
from pattern.en import sentiment
import re
from twitterscraper import query_tweets
import csv
import subprocess
from json2html import *
import datetime
import matplotlib.pyplot as plt
#qqll = raw_input('Enter bellow the URL\n')
#req = Request(qqll)
#try:
#    response = urlopen(req)
#except URLError, e:
#    if hasattr(e, 'reason'):
#        print 'We failed to reach a server.'
#        print 'Reason: ', e.reason
#    elif hasattr(e, 'code'):
#        print 'The server couldn\'t fulfill the request.'
#        print 'Error code: ', e.code
#else:
#    print 'URL is good!'


#qqll='https://en.wikipedia.org/wiki/Terrorism'
#
#rec=re.compile(r"https?://(www\.)?")
#zz=rec.sub('', qqll).strip().strip
#zz=str                       
zz='Kim John-un'
zz=str(zz)
#==============================================================================
# Twitter URL
#==============================================================================
with open('Twittersite.csv','w') as tsout:
        wr = csv.writer(tsout, quoting=csv.QUOTE_ALL)
        tnslist=['polarity', 'subjectivity', 'likes', 'ŕeplies', 'language' , 'timestamp', 'year', 'tweets', 'íd']
        wr.writerow(tnslist)
        for tweet in query_tweets(zz, 1000)[:1000]:
            ops=TextBlob(tweet.text)
            tsp=ops.sentiment.polarity
            tss=ops.sentiment.subjectivity
            tt=(tweet.text.encode('ascii', 'ignore').decode('ascii'))
            tt = tt.replace(',','')
            taal=ops.detect_language()
            ts=tweet
            stamp=ts.timestamp
            leuk=ts.likes
            reactie=ts.replies
            nr=ts.id
            #print stamp.timetuple()
            year= stamp.timetuple().tm_year            
            #year = datetime.date.today().year
            tslist=tss, tsp, leuk, reactie, taal , stamp, year ,tt,nr
            wr.writerow(tslist)
            
            
df= pd.read_csv('Twittersite.csv')
mpol=df["polarity"].mean()
mdpol=df["polarity"].median()
stdpol=df["polarity"].std()
skpol=df["polarity"].skew()
kurpol=df["polarity"].kurtosis()
rel=df['polarity'].corr(df['year'], method='spearman')
#coryear=df['polarity'].corr(df['year'])
df.timestamp = pd.to_datetime(df.timestamp)

with open('Polarity.csv','w') as polout:
        wr = csv.writer(polout, quoting=csv.QUOTE_ALL)
        pollist=['mean', 'median', 'std', 'skewness', 'kurtosis' , 'coryear']
        wr.writerow(pollist)
        poltslist=mpol, mdpol, stdpol, skpol, kurpol , rel
        wr.writerow(poltslist)

fig, ax = plt.subplots()
fig,ax.set_xlabel("Time")
fig,ax.set_ylabel("Polarity")
ax.plot(df.timestamp, df.polarity)
plt.tight_layout()
#plt.figure(figsize=(30,20)).savefig('timeplot.png') 
fig.savefig('timeplot.png')   # save the figure to file
plt.close(fig) 

from pandas.stats.api import ols
#df['timestamp'] = df.index.to_julian_date()
sumstat = ols(x=df.year, y=df.polarity)

#pd.tseries.index.tim
#plt.show()

#model = pd.ols(y=df['polarity'], x=df['timestamp'], intercept=True)
#model = pd.ols(y=df['polarity'], x=df['year'], intercept=True)



#print mpol, stdpol, skpol, kurpol
##==============================================================================
## Twitter Keywords                        
##==============================================================================
#    with open('Twitterkeyword.csv','w') as tkout:
#        wr = csv.writer(tkout, quoting=csv.QUOTE_ALL)
#        for tweet in query_tweets(keyw, 100)[:100]:
#            ops=TextBlob(tweet.text)
#            tsp=ops.sentiment.polarity
#            tss=ops.sentiment.subjectivity
#            tt=(tweet.text.encode('ascii', 'ignore').decode('ascii'))
#            tt = tt.replace(',','')
#            td=ops.detect_language()
#            ts=tweet
#            tslist=tss, tsp, td ,tt,keyw
#            wr.writerow(tslist)

#==============================================================================
#            #Crawler and try to see if
#==============================================================================
#            from bs4 import BeautifulSoup
#            page = requests.get("https://www.google.com/search?q="+"site:"+qqll)
#            soup = BeautifulSoup(page.content, "lxml")
#            links = soup.findAll("a")
#            print links
#            with open('Crawler.csv', 'wb') as myfile:
#                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#                for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")): 
#                    a = (re.split(":(?=http)",link["href"].replace("/url?q=","")))
#                    a=[a[0].split("&sa")[0]]                    
#                    wr.writerow(a)
#                            
#except requests.ConnectionError, e:
#    print "We are not supporting this URL"
