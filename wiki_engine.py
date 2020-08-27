#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import Files 
import xml.sax
import bz2
import sys
from collections import defaultdict
from titleProcessor import TitleProcessor
from TextParser import TextFieldProcessor
from PageProcessor import PageProcessor
import re
import timeit


# In[2]:


#global Variables 
Doc_ID=1 #to maintain total Number of pages in the dump
Doc_IDtoTitle={} # a map to maintain name of doc ids
globalDictionary={} #final invertedIndex dictionary for each batch
invertedIndexFile=1 #maintainsFile number


# In[3]:


def getGlobalDictionary(pageDictionary):
    global globalDictionary,Doc_ID
    for word in pageDictionary:
        check=checkWords(word)
        if check==True:
            continue
        pageDict={}
        if word in globalDictionary :
            pageDict=globalDictionary[word]
        pageDict[Doc_ID]=pageDictionary[word]
        globalDictionary[word]=pageDict

def writeToFile():
    global globalDictionary,invertedIndexFile,Doc_ID
    outputPath="./output"
    filePath=outputPath+"/indexfile"+str(invertedIndexFile)+".txt"
    invertedIndexFile+=1
    with open(filePath, "a") as outfile:
        for word in sorted(globalDictionary):
            invStr=word+":"
#             print("in write file ",invStr)
            tempDict=globalDictionary[word]
            for item in sorted(tempDict):
                invStr+="d"+str(item)
    #             print("add docid",invStr)
                fieldFreq=tempDict[item]
                tagDict={0:"t",1:"i",2:"b",3:"c",4:"l",5:"r"}
                for i in range(0,len(fieldFreq)):
    #                 print("i is",i,fieldFreq[i])
                    if fieldFreq[i]>0:
                        invStr+="#"+tagDict[i]+str(fieldFreq[i])
                invStr+="|"        
            invStr=invStr[:-1]
#             print("final invStr",invStr)
            outfile.write(invStr + '\n')        
    outfile.close()        


# In[4]:


def checkWords(word):
    ignoreWords=['redirect','redirect2']
    if len(word)<=2 or word in ignoreWords or re.match('^[0]+$',word) or not(re.match('^[a-zA-Z0-9]+$',word)):
        return True
    return False


# In[5]:


#content Handler code for XML parser
def storeValue(key,value,Dict):
    global Doc_IDtoTitle
    Doc_IDtoTitle[key]=value
    
class parseXML(xml.sax.ContentHandler):
    
    global Doc_ID,Doc_IDtoTitle 
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.current_tag=""
        self.title_content=""
        self.text_content=""
    
    def startElement(self,tag,attributes):
        self.current_tag=tag
        if tag=='page':
            self.title_content=""
            self.text_content=""

    def characters(self,content):
        if self.current_tag=="title":
            self.title_content+=content
        elif self.current_tag=="text":
            self.text_content+=content
            
    def endElement(self,tag):
        if tag=='page':
            global Doc_ID,globalDictionary,Doc_IDtoTitle
            print("----------------------end doc",Doc_ID,"----------------------------")
            if Doc_ID%50000==0:
                writeToFile()
                globalDictionary.clear()
                Doc_IDtoTitle.clear()
            
           
            Doc_ID+=1
        
        elif tag=='title':
#             print(self.title_content)
#             global Doc_ID,globalDictionary,Doc_IDtoTitle
            storeValue(Doc_ID,self.title_content,Doc_IDtoTitle) 
        
        elif tag=='text':
            #process title
            pr=TitleProcessor()
            processedTitle=pr.processData(self.title_content)
#             print("Processed title : ",processedTitle)
            
            #get fields from text_content
            pt=TextFieldProcessor()
            info,bodyText,category,externalLinks,references=pt.process(self.text_content)
            
            #make dictionary for each field
            titleDict=pr.getTitleDictionary(processedTitle)
            page=PageProcessor()
            infoDict=page.getAllDictionary(info)
#             print("---------info---------")
            bodyDict=page.getAllDictionary(bodyText)
#             print("---------bodyDict---------")
            categoryDict=page.getAllDictionary(category)
#             print("---------catDict---------")
            externalLinksDict=page.getAllDictionary(externalLinks)
#             print("---------exlDict---------")
#             print(referencesDict)
            referencesDict=page.getAllDictionary(references)
#             print("---------refDict---------")
            
#             print(externalLinksDict)
            
            #make final page Dictionary for each page
            pageDictionary=page.getPageDictionary(titleDict,infoDict,bodyDict,categoryDict,externalLinksDict,referencesDict)
#             print("page dictionary ",pageDictionary)
            getGlobalDictionary(pageDictionary)
        self.current_tag=""


# In[ ]:


if __name__=="__main__":
    global globalDictionary
    Wiki_input_file="./Data/input.bz2"
    source = bz2.BZ2File(Wiki_input_file, "rb")
    start = timeit.default_timer()
    #Create a parser Object
    parser= xml.sax.make_parser()
    
    #turnoff namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    
    #callHandler
    handler= parseXML()
    
    #parse data 
    parser.setContentHandler(handler)
    parser.parse(source)
    
    if bool(globalDictionary):
        writeToFile()
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    print('-----------------------------')


# In[ ]:





# In[ ]:




