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


#qqll='https://en.wikipedia.org/wiki/Vaccine'
#
#==============================================================================
# URLS infor
#==============================================================================
#headers = {
#}
#params = (('url', qqll),)
#r=requests.get('https://mercury.postlight.com/parser', headers=headers, params=params)
#datas = r.json()
#df = json_normalize(data)


#==============================================================================
# Reputation WOT and Google Safe
#==============================================================================
hrep = {
    'X-Mashape-Key': 'EPKyBpclL1mshw9UVieagzhgC5XBp1P7Q1gjsnIHWy4kC1hl3h',
}

mrep = (
    ('uth_token', 'Yw-xEK-UcyxxbsrUdzyn'),
    ('url', qqll),
)

tr=requests.get('https://enclout-reputation.p.mashape.com/show.json', headers=hrep, params=mrep)
tdata=tr.json()
with open('Reputation.json', 'w') as rep:
    json.dump(tdata, rep)
    
#==============================================================================
# 
#==============================================================================

#==============================================================================
# IBM
#==============================================================================
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud import WatsonException
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features
  
natural_language_understanding = NaturalLanguageUnderstandingV1(
  username="dedb2eb6-86b3-454b-bf74-b2ad8601e26e",
  password="wfW87duTErOu",
  version="2017-02-27")
with open('IBMjson', 'w') as ibmoutfile:
    try:
        response = natural_language_understanding.analyze(
          url=qqll,
          features=[
              Features.Emotion(),
        Features.Sentiment(),
      Features.Concepts(limit=1),
    Features.Keywords(limit=1, sentiment=False, emotion=False),
    Features.Categories(),
      Features.Entities(limit=1, sentiment=False, emotion=False),
        Features.MetaData()
          ]
        )
        #print(json.dumps(response, indent=2))
        json.dump(response, ibmoutfile)    
    except WatsonException as e:  # This is the correct syntax 
        json.dump(qqll, ibmoutfile)  

        
        
#==============================================================================
# URL        
#==============================================================================
#==============================================================================
# Leesbaarheid APi
#==============================================================================
headers = {
    'X-Mashape-Key': 'EPKyBpclL1mshw9UVieagzhgC5XBp1P7Q1gjsnIHWy4kC1hl3h',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
}

link='https://en.wikipedia.org/wiki/Vaccine'
params = (('text', qqll),)
rr=requests.post('https://ipeirotis-readability-metrics.p.mashape.com/getReadabilityMetrics', headers=headers, params=params)
readdata= rr.json()

nlptrust=[tdata,response]
        
orig_stdout = sys.stdout
f = open('demotest.html', 'w')
sys.stdout = f
print json2html.convert(json = nlptrust)
sys.stdout = orig_stdout
f.close()        


#==============================================================================
# Fast way
#==============================================================================
#import json
#b='{ curl "https://api.havenondemand.com/1/api/sync/gettextstatistics/v1?url=https%3A%2F%2Fqupid-project.net%2Fabout%2F&apikey=8a9cb89a-504c-4d23-b634-51e6a1772459" | python -mjson.tool > ht.json \
#  && curl "https://api.havenondemand.com/1/api/sync/extractconcepts/v1?url=https%3A%2F%2Fqupid-project.net%2Fabout%2F&apikey=8a9cb89a-504c-4d23-b634-51e6a1772459"  | python -mjson.tool > hc.json \
#  && curl "https://api.havenondemand.com/1/api/sync/analyzesentiment/v2?url=https%3A%2F%2Fqupid-project.net%2Fabout%2F&apikey=8a9cb89a-504c-4d23-b634-51e6a1772459" | python -mjson.tool > hs.json;}'
#p = subprocess.Popen(b, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#for line in p.stdout.readlines():
#    print line,        
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
        insite=[rt,sub,pol,fkg,fre,wc,sc,keyw,a.title,qqll]
        wr.writerow(insite)
#==============================================================================
# Recompile URL    
#==============================================================================
    rec=re.compile(r"https?://(www\.)?")
    zz=rec.sub('', qqll).strip().strip('/')                       
#==============================================================================
# Twitter URL
#==============================================================================
    with open('Twittersite.csv','w') as tsout:
        wr = csv.writer(tsout, quoting=csv.QUOTE_ALL)
        for tweet in query_tweets(zz, 100)[:100]:
            ops=TextBlob(tweet.text)
            tsp=ops.sentiment.polarity
            tss=ops.sentiment.subjectivity
            tt=(tweet.text.encode('ascii', 'ignore').decode('ascii'))
            tt = tt.replace(',','')
            td=ops.detect_language()
            ts=tweet
            tslist=tss, tsp, td ,tt
            wr.writerow(tslist)
##==============================================================================
## Twitter Keywords                        
##==============================================================================
    with open('Twitterkeyword.csv','w') as tkout:
        wr = csv.writer(tkout, quoting=csv.QUOTE_ALL)
        for tweet in query_tweets(keyw, 100)[:100]:
            ops=TextBlob(tweet.text)
            tsp=ops.sentiment.polarity
            tss=ops.sentiment.subjectivity
            tt=(tweet.text.encode('ascii', 'ignore').decode('ascii'))
            tt = tt.replace(',','')
            td=ops.detect_language()
            ts=tweet
            tslist=tss, tsp, td ,tt,keyw
            wr.writerow(tslist)

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
                            
except requests.ConnectionError, e:
    print "We are not supporting this URL"