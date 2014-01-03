# -*- coding: utf-8 -*-
#################
# Alex Rutherford 2013
# Code to assign sentiment to Arabic 
# tweets by counting terms
# ~2.5m to process 400k tweets
#################
import csv,re,sys
import numpy as np
import matplotlib.pyplot as plt

v=False
#v=True
# Flag to print verbosely

try:
  inFileHandle=open(sys.argv[1],'r')
  outFile=csv.writer(open(sys.argv[1].partition('.')[0]+'_normalised.txt','w'),delimiter=' ')
except:
  print 'NEED FILE AS FIRST ARG'
  sys.exit(1)

if len(sys.argv)>2:
  if sys.argv[2]=='-v':
    v=True
# Set verbose logging

tweets=[t.decode('utf-8') for t in inFileHandle.readlines()]

posFile=csv.reader(open('pos_words.txt','r'),delimiter='\t')
negFile=csv.reader(open('neg_words.txt','r'),delimiter='\t')
negFileAdd=csv.reader(open('neg_words_add.txt','r'),delimiter='\t')
stopFile=csv.reader(open('stop_words.txt','r'),delimiter='\t')
negationFile=csv.reader(open('negation_words.txt','r'),delimiter='\t')

posWords=[]
negWords=[]
stopWords=[]
negationWords=[]

for line in posFile:
  if len(line)>0:
    posWords.append(line[0])
for line in negFile:
  if len(line)>0:
    negWords.append(line[0])
if True:
  for line in negFileAdd:
    if len(line)>0:
      negWords.append(line[0])
for line in stopFile:
  if len(line)>0:
    stopWords.append(line[0])
for line in negationFile:
  if len(line)>0:
    negationWords.append(line[0])

########################
testTweet=u'انا سعيد جدا بس ما أعرف ليس انت هزين شرموط'
testTweet=u'مبقاش بياكل الشويتين دول خلاص وفر هم لنفسك'
#testTweet=u'كمان اسجل اعتراضى كمان محتجه'
# Negative ?

#testTweet=u'يارب اكتب الحريه لثوار المحاكمات العسكريه'
# Positive ?

posCount=0
negCount=0
stopCount=0
negationCount=0

posWords=[p.decode('utf-8') for p in posWords]
negWords=[p.decode('utf-8') for p in negWords]
stopWords=[p.decode('utf-8') for p in stopWords]
negationWords=[p.decode('utf-8') for p in negationWords]

positives=np.zeros(shape=len(tweets))
negatives=np.zeros(shape=len(tweets))

for t,tweet in enumerate(tweets):

  posCount=negCount=stopCount=negationCount=0

  for w,word in enumerate(tweet.split(' ')):

    if v:print word,

    if word in posWords:
      posCount+=1
      if v:print ' => POS'
      continue
    if word in negWords:
      negCount+=1
      if v:print ' => NEG'
      continue
    if word in stopWords:
      stopCount+=1
      if v:print ' => STOP'
      continue
    if word in negationWords:
      negationCount+=1
      if v:print ' => NEGATION'
      continue
    if v:print ''
  if v:print '(pos,neg,stop,negation) = ',(posCount,negCount,stopCount,negationCount)
  positives[t]=posCount
  negatives[t]=negCount

