#!/usr/bin/env python
# coding: utf-8

# In[157]:

# from contextlib import redirect_stdout
import os
import nltk
# with redirect_stdout(open(os.devnull, "w")):
nltk.download('stopwords',quiet=True)
from nltk.corpus import stopwords 
from nltk.stem.porter import *
import sys
# from nltk.stem.snowball import SnowballStemmer
import Stemmer 
from collections import defaultdict


# In[158]:


globalDictionary={}


# In[159]:


def createDictionary(indexPath):
    global globalDictionary
    with open(indexPath, "r") as infile:
        for line in infile:
            line=line.strip()
            wordList=line.split(":")
            globalDictionary[wordList[0]]=wordList[1]
    infile.close()


# In[160]:


def handlePlainQuery(query):
    global globalDictionary
    words=query.split(" ")
    words= [w.casefold() for w in words]
    #stemming
    stemmer=Stemmer.Stemmer('english')
    words= [stemmer.stemWord(w) for w in words]
    for w in words:
        if w in globalDictionary:
            print(w,": ",globalDictionary[w])
        else:
            print(w,": []")


# In[161]:


def handleFieldQuery(query):
    global globalDictionary
    words=query.split(" ")
    currTag=""
    stemmer=Stemmer.Stemmer('english')
    for w in words:
        if ":" in w:
            split_word=w.split(":")
            currTag="#"+split_word[0]
            w=split_word[1]
        w=w.casefold()
        w=stemmer.stemWord(w)
        if w in globalDictionary:
            if currTag in globalDictionary[w]:
                print(w,": ",globalDictionary[w])
            else:
                print(w,": []")
        else:
            print(w,": []")


# In[162]:


if __name__=="__main__":
#     indexPath="./output/indexfile1.txt"
    indexPath=sys.argv[1]
#     query1="shell seattle 1864"
#     query="t:Anarch AccessibleComputing swqwe Shell b:1864 17"
    query=' '.join(sys.argv[2:])
    createDictionary(indexPath+"indexfile1.txt")
    queryType="plain"
    if ":" in query:
        queryType="field"
    
    if queryType=="plain":
        handlePlainQuery(query)
    
    elif queryType=="field":
        handleFieldQuery(query)
    

