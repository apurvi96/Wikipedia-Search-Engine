# -*- coding: utf-8 -*-
"""Wiki_indexer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A10r_peDVpbccPrWavLx9YWiE6zExgFD
"""

import sys
sys.path.append('/content/drive/My Drive')

#import Files 
import xml.sax
import bz2
import sys
from collections import defaultdict
from titleProcessor import TitleProcessor
from TextParser import TextFieldProcessor
from PageProcessor import PageProcessor
import re
import glob
import timeit

#global Variables 
Doc_ID=1 #to maintain total Number of pages in the dump
Doc_IDtoTitle={} # a map to maintain name of doc ids
globalDictionary={} #final invertedIndex dictionary for each batch
invertedIndexFile=1 #maintainsFile number
totalDumpTokens=0
invertedIndexTokens=0

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
    folderPath="/content/drive/My Drive/Index/"
    # folderPath=sys.argv[2]
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



def checkWords(word):
    ignoreWords=['redirect','redirect2']
    if len(word)<=2 or word in ignoreWords or re.match('^[0]+$',word) or not(re.match('^[a-zA-Z0-9]+$',word)) or (word.isdecimal() and len(word)>4):
        return True
    return False

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

def writeTitlefile():
    global Doc_IDtoTitle
    filePath="/content/drive/My Drive/Index/Titles.txt"
    with open(filePath, "a") as outfile:
        for doc in sorted(Doc_IDtoTitle):
            toWrite=str(doc)+":"+Doc_IDtoTitle[doc]
            outfile.write(toWrite + '\n')   
        outfile.close()

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
            # print("----------------------end doc",Doc_ID,"----------------------------")
            if Doc_ID%50000==0:
            # if Doc_ID==10:
                writeToFile()
                writeTitlefile()
                globalDictionary.clear()
                Doc_IDtoTitle.clear()
                # sys.exit()
           
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



if __name__=="__main__":
    # source=sys.argv[1]
    Wiki_input_folder="/content/drive/My Drive/Wiki_Data/Phase2/*"
    file_names = glob.glob(Wiki_input_folder)
    global globalDictionary
    for i in range(len(file_names)):
      print(file_names[i])
      source = bz2.BZ2File(file_names[i], "rb")
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
          print("here")
          writeTitlefile()
          writeToFile()
          globalDictionary.clear()
          Doc_IDtoTitle.clear()
      # writeStatFile()
      
      stop = timeit.default_timer()
      print('Time: ', stop - start)

print(Doc_ID)
print(invertedIndexFile)

