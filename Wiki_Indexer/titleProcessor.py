#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import nltk
nltk.download('stopwords',quiet=True)
from nltk.corpus import stopwords 
from nltk.stem.porter import *
import sys
# from nltk.stem.snowball import SnowballStemmer
import Stemmer 
from collections import defaultdict


# In[ ]:


class TitleProcessor():
    def processData(self,data):
#         data=self.camelCase(data)
#         print(data)
        data=self.remove_Regx(data)
        data=self.tokenizer(data)
        data=self.case_fold(data)
        prev_size=len(data)
        data=self.removeStopwords(data)
        data=self.doStemming(data)
        return data,prev_size
        
#     def camelCase(self,data):
#         return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))',data)
    
    def case_fold(self,data):
        case_Folded= [w.casefold() for w in data]
        return case_Folded
    
    def tokenizer(self,data):
        tokenizedata=re.findall("\d+|[\w]+",data)
        tokenizedata=[key for key in tokenizedata]
        return tokenizedata
    
    def removeStopwords(self,data):
        stop_word = set(stopwords.words('english'))
        removedStopW=[w for w in data if w not in stop_word] 
        return removedStopW
    
    def doStemming(self,data):
#         stemmer=SnowballStemmer("english")
        stemmer=Stemmer.Stemmer('english')
        stemmed_data=[]
        for words in data:
            stemmed_data.append(stemmer.stemWord(words))
        return stemmed_data
    
    def remove_Regx(self,data):
        removReg2=re.compile(r'{\|(.*?)\|}',re.DOTALL).sub('',data)
        data=removReg2
        
        removReg3=re.compile(r'{{v?cite(.*?)}}',re.DOTALL).sub('',data)
        data=removReg3
        
        removReg4=re.compile(r'[.,;_()"/\']',re.DOTALL).sub(' ',data)
        data=removReg4
        
        removReg5=re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL).sub('',data)
        data=removReg5
        
        removReg6=re.compile(r'<(.*?)>',re.DOTALL).sub('',data)
        data=removReg6
        data=data.replace('_',' ').replace(',','')
        return data
    
    def getTitleDictionary(self,titles):
        titleDict=defaultdict(int)
        for word in titles:
            titleDict[word]+=1
        return titleDict
    


# In[ ]:





# In[ ]:




