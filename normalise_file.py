# -*- coding: utf-8 -*-
#################
# Alex Rutherford 2013
# Code to pre-process Arabic tweets
# Running time ~4m for 400k tweets
#################
import csv,re,sys
import string
import collections

v=False
# Flag to print steps verbosely

vv=False
# Flag to print out completed tweet
# Set to false if redirecting 
# with '> trash.txt', can't handle unicode


############
def getWordLists():
############
  stopWords=[line[0].decode('utf-8') for line in csv.reader(open('stop_words.txt','r'),delimiter='\t')]
  negationWords=[line[0].decode('utf-8') for line in csv.reader(open('negation_words.txt','r'),delimiter='\t')]
  exemptWords=[line[0].decode('utf-8') for line in csv.reader(open('exempt_words.txt','r'),delimiter='\t')]

  return stopWords,negationWords,exemptWords

############
def main():
############

  try:
    inFileHandle=open(sys.argv[1],'r')
    outFile=csv.writer(open(sys.argv[1].partition('.')[0]+'_normalised.txt','w'),delimiter=' ')
  except:
    print 'NEED FILE AS FIRST ARG'
    sys.exit(1)

  tweets=[t.decode('utf-8') for t in inFileHandle.readlines()]
#tweets=['?Hello._','http://bbc.co.uk']
#tweets=[u'سَنة',u'كِتاب',u'مُدّة']
#tweets=[u'@arutherfordium I hate you']
#tweets=[u'انا بغير سعيد']
  
  stopWords,negationWords,exemptWords=getWordLists()

  exemptCount=0

  links=collections.defaultdict(int)
  ats=collections.defaultdict(int)

  puncRe=re.compile('(\n|،|\.|,|!|\?|\]|\[|:|;|\|–|­|‑)')
# Standard punctuation
  underscoreRe=re.compile('_')
# Underscore (for hashtags)
  httpRe=re.compile(u'http')
  atRe=re.compile(u'\A\@')

  alifRe=re.compile(u'(آ|أ|إ|آ)')
  alifMaksourRe=re.compile(u'ى')
# Variations of letter alif
  wawRe=re.compile(u'ؤ')
# Letter waw
  hahRe=re.compile(u'ه\Z')
# Letter hah
  alRe=re.compile(u'(\Aال|\Aفال|\Aوال|\Aلل)')
# Variations of al
  tuhaRe=re.compile(u'تها\Z')
  haRe=re.compile(u'ها\Z')
# Strip feminine pronoun
  verbSuffixesRe=re.compile(u'(ون\Z|ين\Z|وا)')
# Verb sufixes
  harakatRe=re.compile(u'(ٍ|َ|ُ|ِ|ّ|ْ||ً)')
# Accents

######################
  for t,tweet in enumerate(tweets):
######################
#  print t,tweet
    if (t+1)%100000==0:
      print t+1,'PROCESSED....'
    tweet=re.sub(underscoreRe,' ',tweet)
## Break up underscores eg in hash tags
    if vv:print '+++',tweet

    outTweet=[]
######################
    for w,word in enumerate(tweet.split(' ')):
######################
      isAt=re.match(atRe,word)
      isHttp=re.match(httpRe,word)
      isNeg=(word in negationWords)
      isStop=(word in stopWords)
      isExempt=(word in exemptWords)
    
      if not (isStop or isNeg or isExempt):
        if v:print '>>>',word
        if not (isHttp or isAt):
        # Don't clean URLs or @-mentions
############
## Normalising
          word=re.sub(puncRe,'',word)
## Remove punctuation and line endings
          word=re.sub(harakatRe,u'',word)
          if v:print '>>>',word
# remove diacritics        
          word=re.sub(u'آ',u'ا',word)
          if v:print '>>>',word
          word=re.sub(alifRe,u'ا',word)
          if v:print '>>>',word
          word=re.sub(alifMaksourRe,u'ي',word)
          if v:print '>>>',word
# Normalise alifs
          word=re.sub(wawRe,u'و',word)
          if v:print '>>>',word
# Normalise waw

          word=re.sub(hahRe,u'ة',word)
          if v:print '>>>',word
# Add nuktas to tama'buta
############
## Stemming
          word=re.sub(alRe,'',word)
          if v:print '>>>',word
# Strips 'al' and variants at beginning of word only
## Prefixes
          word=re.sub(tuhaRe,u'ة',word)
          if v:print '>>>',word
# Replaces feminine personal pronoun with tama'buta
          word=re.sub(haRe,u'',word)
          if v:print '>>>',word
          word=re.sub(verbSuffixesRe,'',word)
          if v:print '>>>',word
# 3rd person pl
## Suffixes
          if v:print '>>>',word
          outTweet.append(unicode(word))
          if v:print '============='
        
        elif isHttp:
          links[word]+=1
        elif isAt:
          ats[word]+=1
        # Count mentions and links
      elif isExempt:
        exemptCount+=1

    for t in outTweet:
      if vv:print t,
    if vv:print ''
    if vv:print '============'
    outFile.writerow([t.encode('utf-8') for t in outTweet])

if __name__=="__main__":
  main()
