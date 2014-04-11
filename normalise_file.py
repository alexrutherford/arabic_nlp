# -*- coding: utf-8 -*-
#################
# Alex Rutherford 2013
# Code to pre-process Arabic tweets
# Running time ~4m for 400k tweets
# Input file <name>.txt; output <name>_normalised.txt
#################
import csv,re,sys
import string
import collections

############
def getWordLists():
############
  stopWords=[line[0].decode('utf-8') for line in csv.reader(open('/Users/alex/SYRIA/TWEETS/SENTIMENT/stop_words.txt','r'),delimiter='\t')]
  negationWords=[line[0].decode('utf-8') for line in csv.reader(open('/Users/alex/SYRIA/TWEETS/SENTIMENT/negation_words.txt','r'),delimiter='\t')]
  exemptWords=[line[0].decode('utf-8') for line in csv.reader(open('/Users/alex/SYRIA/TWEETS/SENTIMENT/exempt_words.txt','r'),delimiter='\t')]

  posEmojis=[line[0].decode('utf-8') for line in csv.reader(open('/Users/alex/SYRIA/TWEETS/SENTIMENT/pos_emojis.txt','r'),delimiter='\t')]
  negEmojis=[line[0].decode('utf-8') for line in csv.reader(open('/Users/alex/SYRIA/TWEETS/SENTIMENT/neg_emojis.txt','r'),delimiter='\t')]

  return stopWords,negationWords,exemptWords,posEmojis,negEmojis

############
def main():
############
  v=False
#  v=True
# Flag to print steps verbosely

  vv=False
#  vv=True
# Flag to print out completed tweet
# Set to false if redirecting
# with '> trash.txt', can't handle unicode

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

  stopWords,negationWords,exemptWords,posEmojis,negEmojis=getWordLists()
  emojis=posEmojis+negEmojis

  exemptCount=0

  links=collections.defaultdict(int)
  ats=collections.defaultdict(int)

  puncRe=u'(\n|،|\.|,|!|\?|\]|\[|:|;|\|–|­|‑)|"'
# Standard punctuation
  underscoreRe=u'_'
# Underscore (for hashtags)
  httpRe=u'http'
  httpCleanRe=u'(\n|"|”)'
  atRe=u'\A\@'

  alifRe=u'(آ|أ|إ|آ)'
  alifMaksourRe=u'ى'
# Variations of letter alif
  wawRe=u'ؤ'
# Letter waw
  hahRe=u'ه\Z'
# Letter hah
  alRe=u'(\Aال|\Aفال|\Aوال|\Aلل)'
# Variations of al
  tuhaRe=u'تها\Z'
  haRe=u'ها\Z'
# Strip feminine pronoun
  verbSuffixesRe=u'(ون\Z|ين\Z|وا)'
# Verb sufixes
  harakatRe=u'(ٍ|َ|ُ|ِ|ّ|ْ|ً)'
# Diacritics

######################
  for t,tweet in enumerate(tweets):
######################
#  print t,tweet
    if (t+1)%20000==0:
      print t+1,'PROCESSED....'
    tweet=re.sub(underscoreRe,' ',tweet)
## Break up underscores eg in hash tags
    if vv:print '+++',tweet

    outTweet=[]
######################
    for w,word in enumerate(tweet.split(r' ')):
######################
      isAt=re.match(atRe,word,re.U)
      isHttp=re.match(httpRe,word,re.U)
      isNeg=(word in negationWords)
      isStop=(word in stopWords)
      isExempt=(word in exemptWords)
      isEmoji=(word in emojis)

      if not (isStop or isNeg or isExempt):
        if v:print '>>>',word
        if not (isHttp or isAt or isEmoji):
        # Don't clean URLs or @-mentions
############
## Normalising
          word=re.sub(puncRe,'',word)
# Remove punctuation and line endings...
# ...but only if not emoji, otherwise keep
# it unchanged to be counted later
          word=re.sub(harakatRe,u'',word,flags=re.U)
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
          word=re.sub(httpCleanRe,'',word)
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
#    sys.exit(1)

  linkFile=csv.writer(open('links.csv','w'),delimiter='\t')
  for k,v in links.items():linkFile.writerow([v,k.encode('utf-8')])

if __name__=="__main__":
  main()
