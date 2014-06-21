**Summary**

Python scripts to read in raw Arabic text, remove diacritics, perform basic normalisation and stemming and then derive sentiment from term frequency. Positive and negative words are supplied and based on Egyptian and Levantine dialects as well as Fus'ha.

`normalise_file.py` reads input file, cleans and normalises text, produces normalised output file and file with all links and their frequency.

`get_sentiment.py` reads normalised text file, assigns a positive and a negative sentiment value to each line based on term frequency. Saves sentiments to a file

**Citation**

The list of stop words and labelled positive and negative words in based on the Masters Thesis of Amira Magdy Shoukry
Arabic Sentence Level Sentiment Analysis
American University in Cairo
Spring 2013
[(link)](https://dar.aucegypt.edu/handle/10526/3536)

**Dependencies**

`get_sentiment.py` requires NumPy and Matplotlib, otherwise all code in pure Python

**To Do**

Implement generator for memory friendly treatment of large files
