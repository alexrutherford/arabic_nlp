# -*- coding: utf-8 -*-
'''Code to assign sentiment to Arabic tweets by counting terms 
~22.5m to process 400k tweets on Macbook Pro'''
#################
import csv,re,sys
import numpy as np
import matplotlib.pyplot as plt
stem=''

###########
def getWordLists():
###########
    '''Reads terms to be tsted against text from files. Returns tuple of lists of words.'''
    posFile=csv.reader(open(stem+'pos_words.txt','r'),delimiter='\t')
    negFile=csv.reader(open(stem+'neg_words_all.txt','r'),delimiter='\t')
    negFileAdd=csv.reader(open(stem+'neg_words_add.txt','r'),delimiter='\t')
    stopFile=csv.reader(open(stem+'stop_words.txt','r'),delimiter='\t')
    negationFile=csv.reader(open(stem+'negation_words.txt','r'),delimiter='\t')

    posEmojiFile=csv.reader(open(stem+'pos_emojis.txt','r'),delimiter='\t')
    negEmojiFile=csv.reader(open(stem+'neg_emojis.txt','r'),delimiter='\t')

    posWords=[line[0].decode('utf-8') for line in posFile if len(line)>0]
    negWords=[line[0].decode('utf-8') for line in negFile if len(line)>0]
    negWords+=[line[0].decode('utf-8') for line in negFileAdd if len(line)>0]
    stopWords=[line[0].decode('utf-8') for line in stopFile if len(line)>0]
    negationWords=[line[0].decode('utf-8') for line in negationFile if len(line)>0]
    
    posEmojis=[line[0].decode('utf-8') for line in posEmojiFile if len(line)>0]
    negEmojis=[line[0].decode('utf-8') for line in negEmojiFile if len(line)>0]

    posEmojis=[e.replace('(','\(').replace(')','\)').replace('.','\.').replace('|','\|') for e in posEmojis]
    negEmojis=[e.replace('(','\(').replace(')','\)').replace('.','\.').replace('|','\|') for e in negEmojis]
    
    return posWords,negWords,stopWords,negationWords,posEmojis,negEmojis
###########
def main():
###########
    posCount=0
    negCount=0
    stopCount=0
    negationCount=0

    try:
        inFileHandle=open(sys.argv[1],'r')
    except:
        print 'NEED FILE AS FIRST ARG'
        sys.exit(1)

    v=False
    # Flag to print verbosely

    if len(sys.argv)>2:
        v=True
        # Set verbose logging

    tweets=[t.decode('utf-8') for t in inFileHandle.readlines()]
#    tweets=tweets[0:1000]
    posWords,negWords,stopWords,negationWords,posEmojis,negEmojis=getWordLists()

#    for s in stopWords:
#        print s
#    sys.exit(1)
########################
    positives=np.zeros(shape=len(tweets))
    negatives=np.zeros(shape=len(tweets))

    for t,tweet in enumerate(tweets):
        if (t+1)%100000==0:print t+1,'PROCESSED....'

        posCount=negCount=stopCount=negationCount=0
        for w,word in enumerate(tweet.split('\t')):
   
            if v:print word

            if word in posWords:
                posCount+=1
                if v:print ' => POS'
     
            if word in negWords:
                negCount+=1
                if v:print ' => NEG'
          
            if word in stopWords:
            # Don't do RE match as single/double letter 
            # combos included in stop words
                stopCount+=1
                if v:print ' => STOP'
          
            if word in negationWords:
                negationCount+=1
                if v:print ' => NEGATION'
          
            if any([re.match(r'('+e+r')+',word,re.U) for e in posEmojis]):
                posCount+=1
                if v:print ' => POS EMOJI'
            if any([re.match(r'('+e+r')+',word,re.U) for e in negEmojis]):
                negCount+=1    
                if v:print ' => NEG EMOJI'
        if v:print ''
        if v:print '(pos,neg,stop,negation) = ',(posCount,negCount,stopCount,negationCount)
        positives[t]=posCount
        negatives[t]=negCount

        if negCount>4 or posCount>4:
            if False:print tweet,posCount,negCount
    combined=np.vstack((positives,negatives)).T

    np.savetxt('sentiments.txt',combined,fmt="%d",delimiter='\t')

    counts,xedges,yedges,im=plt.hist2d(positives,negatives,bins=[int(np.max(positives)),int(np.max(negatives))])
    print '%2.2f HAVE ZERO SENTIMENT' % (100.0*counts[0,0]/len(positives))

    if False:
    # Plot distribution of sentiments?
        fig=plt.figure()
        ax=fig.add_subplot(211)
        posRange=range(0,int(np.max(positives))+1)
        ax.hist(positives,bins=posRange)
        plt.xticks([0.5+i for i in posRange],[str(i) for i in posRange])
        plt.ylabel('Positive Sentiment')

        ax=fig.add_subplot(212)
        negRange=range(0,int(np.max(negatives))+1)
        ax.hist(negatives,bins=negRange)
        plt.xticks([0.5+i for i in negRange],[str(i) for i in negRange])
        plt.ylabel('Negative Sentiment')
        plt.show()

if __name__=="__main__":
  main()
