#!/usr/bin/env python
# coding: utf-8

# In[ ]:





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
totalDumpTokens=0
invertedIndexTokens=0


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
#     filePath="indexfile"+str(invertedIndexFile)+".txt"
    folderPath=sys.argv[2]
    filePath=folderPath+"indexfile"+str(invertedIndexFile)+".txt"
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
#             print(invStr)
            outfile.write(invStr + '\n')        
    outfile.close()        


# In[4]:


def checkWords(word):
    ignoreWords=['redirect','redirect2']
    if len(word)<=2 or word in ignoreWords or re.match('^[0]+$',word) or not(re.match('^[a-zA-Z0-9]+$',word)) or (word.isdecimal() and len(word)>4):
        return True
    return False


# In[5]:


def writeStatFile():
    global globalDictionary,totalDumpTokens
    filePath=sys.argv[3]
#     filePath="stat.txt"
    with open(filePath, "w") as outfile:
#         print("final totalDumpTokens ",totalDumpTokens)
        outfile.write(str(totalDumpTokens)+ '\n')
#         print("final global ",len(globalDictionary))
        outfile.write(str(len(globalDictionary)))
    outfile.close()


# In[6]:


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
#             print("----------------------end doc",Doc_ID,"----------------------------")
            if Doc_ID%50000==0:
#             if Doc_ID==10:
                writeToFile()
                globalDictionary.clear()
                Doc_IDtoTitle.clear()
#                 sys.exit()
           
            Doc_ID+=1
        
        elif tag=='title':
#             print(self.title_content)
#             global Doc_ID,globalDictionary,Doc_IDtoTitle
            storeValue(Doc_ID,self.title_content,Doc_IDtoTitle) 
        
        elif tag=='text':
            global totalDumpTokens
            #process title
            pr=TitleProcessor()
            processedTitle,prevTitle=pr.processData(self.title_content)
            
            #get fields from text_content
            pt=TextFieldProcessor()
            info,bodyText,category,externalLinks,references=pt.process(self.text_content)
            
            #make dictionary for each field
            titleDict=pr.getTitleDictionary(processedTitle)
            page=PageProcessor()
            infoDict,prevInfo=page.getAllDictionary(info)
#             print("---------info---------")
            bodyDict,prevBody=page.getAllDictionary(bodyText)
#             print("---------bodyDict---------")
            categoryDict,prevCat=page.getAllDictionary(category)
#             print("---------catDict---------")
            externalLinksDict,prevLinks=page.getAllDictionary(externalLinks)
#             print("---------exlDict---------")
#             print(referencesDict)
            referencesDict,prevRef=page.getAllDictionary(references)
            
            totalDumpTokens+=(prevTitle+prevLinks+prevCat+prevBody+prevInfo+prevTitle)
            #make final page Dictionary for each page
            pageDictionary=page.getPageDictionary(titleDict,infoDict,bodyDict,categoryDict,externalLinksDict,referencesDict)
#             print("page dictionary ",pageDictionary)
            getGlobalDictionary(pageDictionary)
        self.current_tag=""


# In[7]:


if __name__=="__main__":
    source=sys.argv[1]
#     Wiki_input_file="./Data/input.bz2"
#     source = bz2.BZ2File(Wiki_input_file, "rb")
#     source="/home/apurvi/Desktop/SEM-3/IRE/Mini Project/Wikipedia Search Engine/multistream2.xml-p1p30303"
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
    writeStatFile()
    
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    print('-----------------------------')


# In[ ]:





# In[ ]:




