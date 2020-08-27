#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import Files 
import xml.sax
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords 
import bz2
from nltk.stem.porter import *
import sys
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
from titleProcessor import TitleProcessor
from TextParser import TextFieldProcessor


# In[ ]:


class PageProcessor():
    
    def __init__(self):
        self.pageDictionary=defaultdict(int)
        self.default_val=[0,0,0,0,0,0] # [title info body categ links ref]
    
    def tokenizer(self,data):
        tokenizedata=re.findall("\d+|[\w]+",data)
        tokenizedata=[key for key in tokenizedata]
        return tokenizedata
    
    def removeStopwords(self,data):
        stop_word = set(stopwords.words('english'))
        removedStopW=[w for w in data if w not in stop_word] 
        return removedStopW
    
    def doStemming(self,data):
        stemmer=SnowballStemmer("english")
        stemmed_data=[]
        for words in data:
            stemmed_data.append(stemmer.stem(words))
        return stemmed_data
    
    def makeDictionary(self,word_list):
        Dict=defaultdict(int)
        for word in word_list:
            if word.isdecimal() or len(word)==1:
                continue
            else:
                Dict[word]+=1
        return Dict
    
    def getAllDictionary(self,word_list):
#         print("word_list",type(word_list[0]))
        word_list=self.tokenizer(' '.join(word_list))
        word_list=self.removeStopwords(word_list)
        word_list=self.doStemming(word_list)
        Dict=self.makeDictionary(word_list)
        return Dict
    
    def mergeDict(self,Dict,typeIndex):
#         print("typeIndex",typeIndex,"------------------")
#         print(Dict)
        for word in Dict:
#             print("--------word is " ,word,"-----------")
            if self.pageDictionary[word]:
#                 print("already here",word,self.pageDictionary[word])
                self.pageDictionary[word][typeIndex]+=Dict[word]
            else:
                self.pageDictionary[word]=[0,0,0,0,0,0]  
                self.pageDictionary[word][typeIndex]+=Dict[word]
#                 print("inside else")
#             print("after",word,self.pageDictionary[word])
    
    def getPageDictionary(self,titleDict,infoDict,bodyDict,categoryDict,externalLinksDict,referencesDict):
        self.mergeDict(titleDict,0)
        self.mergeDict(infoDict,1)
        self.mergeDict(bodyDict,2)
        self.mergeDict(categoryDict,3)
        self.mergeDict(externalLinksDict,4)
        self.mergeDict(referencesDict,5)
        return self.pageDictionary
        
        

