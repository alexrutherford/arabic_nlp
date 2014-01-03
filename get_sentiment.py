# -*- coding: utf-8 -*-
#################
# Alex Rutherford 2013
# Code to assign sentiment to Arabic 
# tweets by counting terms
# ~2.5m to process 400k tweets
#################
import csv,re,sys
import numpy as np


###########
def getWordLists():
###########

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

  posCount=0
  negCount=0
  stopCount=0
  negationCount=0

  posWords=[p.decode('utf-8') for p in posWords]
  negWords=[p.decode('utf-8') for p in negWords]
  stopWords=[p.decode('utf-8') for p in stopWords]
  negationWords=[p.decode('utf-8') for p in negationWords]

  return posWords,negWords,stopWords,negationWords

###########
def main():
###########

  try:
    inFileHandle=open(sys.argv[1],'r')
  except:
    print 'NEED FILE AS FIRST ARG'
    sys.exit(1)

  v=False
  # Flag to print verbosely

  if len(sys.argv)>2:
    if sys.argv[2]=='-v':
      v=True
# Set verbose logging

  tweets=[t.decode('utf-8') for t in inFileHandle.readlines()]  
  
  posWords,negWords,stopWords,negationWords=getWordLists()

########################
  
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
  
  np.savetxt('sentiments.txt',np.vstack((positives,negatives)).T,fmt="%d",delimiter='\t') 

if __name__=="__main__":
  main()

