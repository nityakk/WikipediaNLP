# -*- coding: utf-8 -*-
"""WikipediaDumpAnalysis.py
Created on Tue Oct  5 13:02:03 2021

@author: Nitya Krishna Kumar
"""

#%% Imports
import mwxml
import pandas as pd
import glob
import os
import csv
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import gensim
from gensim.utils import simple_preprocess
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
from heapq import nlargest
#%% Load data
#os.chdir(".//School//Columbia//ChildAbuse&Neglect_CodingExercise//WikipediaNLP")

print("Loading data...")
path = glob.glob("./*.xml*.*")[0]
dump = mwxml.Dump.from_file(path)

toptexts = pd.DataFrame(columns=['page_id', 'revision_id', 'text'])

# The dataset is too large causing a memory problem,
# looked at the first 10,000 articles
LIMIT = 10000
print(f'Getting the first {LIMIT} articles...')
for i, page in enumerate(dump):
    if i == LIMIT: break
    for revision in page:
        #if i == LIMIT: break
        #revision.id
        pageid = page.id
        revisionid = revision.id
        text = revision.text
        
        toptexts = toptexts.append({'page_id':pageid, 'revision_id':revisionid, 'text':text}, ignore_index=True)
        
#%% Text Processing
def lemmatize_stemming(text):
    stemmer = SnowballStemmer("english")
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


toptexts['text_processed'] = \
    toptexts['text'].map(lambda x: re.sub('[\\n:]', ' ', x))
toptexts['text_processed'] = \
    toptexts['text'].map(lambda x: re.sub('[\']', ' ', x))
toptexts['text_processed'] = \
    toptexts['text'].map(lambda x: re.sub('[{(#,|*\\)}[\]]', '', x))
toptexts['text_processed'] = \
    toptexts['text'].map(lambda x: re.sub(' = ', '=', x))
toptexts['text_processed'] = \
    toptexts['text'].map(lambda x: x.lower())
toptexts['text_processed'] = \
    toptexts['text'].map(lambda x: lemmatize_stemming(x))

print("Finished loading data...")

#%% 100 most commonly used words
""" What are the 100 most commonly used words in the body of the articles in 
these Wikipedia pages? The body is the section with the <text> heading. """

print("Finding 100 most commonly used words...")
# Define stopwords
def split_title(texts):
    for text in texts:
        yield(gensim.utils.simple_preprocess(str(text), deacc=True))

stop_words = stopwords.words('english')
stop_words.extend(['http', 'https', 'category', 'infobox', \
                   'wikipedia', 'redirect', 'from', \
                       'ref', 'like', 'user', 'com', 'www',
                       'title', 'url', 'otherlinks', 'basedomain',
                       'cite', 'span', 'flagicon', 'html'])
wordlist = toptexts.text_processed.values.tolist()
words = list(split_title(wordlist))

# Remove stopwords
wikiwords = [[word for word in simple_preprocess(str(w)) 
             if word not in stop_words] for w in words]

corpus = []
for wiki in wikiwords:
    corpus = corpus + wiki

wordcount = {}
for word in corpus:
    if word not in wordcount:
        wordcount[word] = 1
    else:
        wordcount[word] += 1

# get hundred most commonly used words
hundred_largest = nlargest(100, wordcount, key=wordcount.get)
print("100 most commonly used words found:")

# print to csv
with open('hundred_largest.csv', 'w', encoding="ISO-8859-1", newline='') as file:
    wr = csv.writer(file)
    for w in hundred_largest:
        if w!="":
            wr.writerow([w])

#%% 
"""Please choose any article in the dataset – what are the 10 words 
that would be most useful to detect articles that are similar to it?
Explain the algorithm you used to determine these words."""

article = toptexts.sample(1)
