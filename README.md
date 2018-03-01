## Summary

Python scripts to read in raw Arabic text, remove diacritics, perform basic normalisation and stemming and then derive sentiment from term frequency. Positive and negative words are supplied and based on Egyptian and Levantine dialects as well as Fus'ha.

`normalise_file.py` reads input file, cleans and normalises text, produces normalised output file and file with all links and their frequency.

`get_sentiment.py` reads normalised text file, assigns a positive and a negative sentiment value to each line based on term frequency. Saves sentiments to a file.

## Files

- `exempt_words.txt` Words that are exempt from cleaning since they trivially match stop words or lemmatisation e.g. 'و' in 'ﻭﺎﻠﻠﻫ'  
- `negation_words.txt` Words that can be used to negate (for more sophisticated bigram analysis)  
- `neg_emojis.txt` Emojis that imply negative emotion  
- `pos_emojis.txt` Emojis that imply positive emotion  
- `neg_words.txt` Arabic words with negative sentiment  
- `pos_words.txt` Arabic words with positive sentiment  
- `stop_words.txt` Arabic words that do not impart meaning e.g. 'و'

## Citation

The list of stop words and labelled positive and negative words in based on the Masters Thesis of Amira Magdy Shoukry:
_Arabic Sentence Level Sentiment Analysis_
American University in Cairo
Spring 2013
[(link)](https://dar.aucegypt.edu/handle/10526/3536)

## Dependencies

`get_sentiment.py` requires NumPy and Matplotlib, otherwise all code in pure Python

## To Do

- Implement generator for memory friendly treatment of large files
- Update lists of emojis  
- ~~Parse arguments with `argparser`~~
