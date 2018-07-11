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
import requests
import pandas as pd
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


qqll='https://en.wikipedia.org/wiki/Vaccine'

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
        book = pd.Series( [rt,sub,pol,fkg,fre,wc,sc,keyw,a.title,qqll],
                             index=['rt','sub','pol','fkg','fre','wc','sc','keyw','a.title','qqll'])
        print book
        dfT = df.book
        dfT.to_csv('Vert.csv')
        #wr.writerow(book)
                             #print book['Author']        
        #insite=[rt,sub,pol,fkg,fre,wc,sc,keyw,a.title,qqll]
        #wr.writerow(insite)

except requests.ConnectionError, e:
    print "We are not supporting this URL"
