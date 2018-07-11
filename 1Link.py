# -*- coding: utf-8 -*-
"""
Todo:

    
@author: ozkan
"""
from pattern.en import suggest
from urllib2 import Request, urlopen, URLError
import sys
from pandas.io.json import json_normalize
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
import pandas as pd
from pattern.en import parse, Sentence, parse
from pattern.en import modality
from pattern.en import sentiment
import re
from twitterscraper import query_tweets
import csv
import subprocess
from json2html import *
qqll = raw_input('Enter bellow the URL\n')
req = Request(qqll)
try:
    response = urlopen(req)
except URLError, e:
    if hasattr(e, 'reason'):
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    elif hasattr(e, 'code'):
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
else:
    print 'URL is good!'



#==============================================================================
# Bellow is opensourced
#==============================================================================
try:
    with open('basicsite.csv','w') as dsite:
        wr = csv.writer(dsite, quoting=csv.QUOTE_ALL)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(qqll)
        rt=response
        raw_html = response.read()
        g = goose.Goose()
        a = g.extract(raw_html=raw_html)
        htext=a.cleaned_text
        opinion = TextBlob(htext)
        pol=opinion.sentiment.polarity
        sub=opinion.sentiment.subjectivity
        rt=requests.get(qqll).elapsed.total_seconds()
        kw=str(keywords(htext, lemmatize=True))
        kw = kw.replace('\r', ' ').replace('\n', ' ')
        keyw=' '.join(kw.split()[:3])
        sbody= htext.replace(',','')
        fkg=textstat.flesch_kincaid_grade(htext)
        wc=textstat.lexicon_count(htext)        
        sc=textstat.sentence_count(htext)     
        fre=textstat.flesch_reading_ease(htext)
        sinsite=['response time','subjective','polarity','fgrade','fscore','words.counts','sentence.count','keywords','title','link','text']
        wr.writerow(sinsite)        
        insite=[rt,sub,pol,fkg,fre,wc,sc,keyw,a.title,qqll]
        wr.writerow(insite)

    rec=re.compile(r"https?://(www\.)?")
    zz=rec.sub('', qqll).strip().strip('/')        
    with open('rowTwittersite.csv','w') as tsout:
        wr = csv.writer(tsout, quoting=csv.QUOTE_ALL)
        tnslist=['polarity', 'subjectivity', 'likes', 'ŕeplies', 'language' , 'timestamp', 'year', 'tweets', 'íd']
        wr.writerow(tnslist)
        for tweet in query_tweets(zz, 10000)[:10000]:
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
            
            
            df= pd.read_csv('rowTwittersite.csv')
            mpol=df["polarity"].mean()
            mdpol=df["polarity"].median()
            stdpol=df["polarity"].std()
            skpol=df["polarity"].skew()
            kurpol=df["polarity"].kurtosis()
            rel=df['polarity'].corr(df['year'], method='spearman')
            df.timestamp = pd.to_datetime(df.timestamp)
            
            with open('concurator.csv','w') as polout:
                    wr = csv.writer(polout, quoting=csv.QUOTE_ALL)
                    pollist=['mean', 'median', 'std', 'skewness', 'kurtosis' , 'coryear']
                    wr.writerow(pollist)
                    poltslist=tss, tsp, leuk, reactie, taal , stamp, year ,tt,nr
                    wr.writerow(poltslist)

               
                          
except requests.ConnectionError, e:
    print "We are not supporting this URL"
