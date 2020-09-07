# -*- coding: utf-8 -*-
"""Merger

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ztsjqlqfKb4szyM7fccOtLTIbG6egacq
"""

import glob
import sys
from heapq import heappush,heappop
import os
import pickle

#Global variables 
filePointers=[]
fileStatus=[] # 0 means file closed 1 means file is open
fileData=[]
fileCount=0 #total files to merge
globalDict={}
fileHeap=[]
wordLimit=150000
invertedIndexFile=1 #count the number of inverted files 
secondaryIndex={} # dict to write secondaryIndex
outputPath="/content/drive/My Drive/InvertedIndexFiles/"

def get_filePointers(fileNames):
  global filePointers,fileStatus,fileData,fileCount,globalDict,fileHeap,wordLimit,invertedIndexFile,secondaryIndex
  for i in range(len(fileNames)):
    filePointers.append(open(fileNames[i], 'r'))
    line=filePointers[i].readline()
    if line:
      fileData[i]=line
      fileStatus[i]=1
      word=line.split(":")
      if word[0] not in fileHeap:
        heappush(fileHeap,str(word[0]))

def get_Files(folderPath):
  global filePointers,fileStatus,fileData,fileCount,globalDict,fileHeap,wordLimit,invertedIndexFile,secondaryIndex
  fileNames = glob.glob(folderPath)
  print("Not sorted: ",fileNames)
  fileCount=len(fileNames)
  fileStatus=[0]*fileCount
  fileData=[""]*fileCount
  get_filePointers(fileNames)
  # print(filePointers)
  # print(fileStatus)
  # print(fileData)
  # print(fileHeap)

def writeIndexFile():
  global filePointers,fileStatus,fileData,fileCount,globalDict,fileHeap,wordLimit,invertedIndexFile,secondaryIndex,outputPath
  if bool(globalDict)==False:
    return
  firstWord=True
  print("wrote file: ",invertedIndexFile)
  print(len(globalDict))
  filePath=outputPath+str(invertedIndexFile)+".txt"
  fileptr=open(filePath,"w")
  # pickler = pickle.Pickler(fileptr)
  for word in sorted(globalDict):
    if firstWord==True:
      firstWord=False
      secondaryIndex[word]=invertedIndexFile
    toWrite=word+":"+str(globalDict[word])
    # print("wrote: ",toWrite)
    fileptr.write(toWrite+"\n")
    # pickler.dump(toWrite)
  invertedIndexFile+=1
  fileptr.close()

def checkConvergence():
  global fileStatus,fileCount
  return (fileStatus.count(0)==fileCount)

def mergeDump():
  global filePointers,fileStatus,fileData,fileCount,globalDict,fileHeap,wordLimit,invertedIndexFile
  wordCount=0
  while True:
    if checkConvergence()==1:
      break
    heapWord=str(heappop(fileHeap))
    # print("heapWord: ",heapWord)
    wordCount+=1
    for i in range(fileCount):
      currWord=fileData[i].split(":")
      if fileStatus[i]==1 and currWord[0]==heapWord:
        # print("currWord: ",currWord)
        postList=currWord[1][:-1]
        # print("postList: ",postList)
        if heapWord in globalDict:
          globalDict[heapWord]+="|"+str(postList)
        else:
          globalDict[heapWord]=str(postList)
        
        line=filePointers[i].readline()
        if line:
          fileData[i]=line
          fileStatus[i]=1
          word=line.split(":")
          if word[0] not in fileHeap:
            heappush(fileHeap,str(word[0]))
        else:
          filePointers[i].close()
          fileStatus[i]=0
    if wordCount>=wordLimit:
      writeIndexFile()
      wordCount=0
      globalDict.clear()

def writeSecondaryIndex():
  global secondaryIndex,outputPath
  filePath=outputPath+"secondaryIndex.txt"
  # pickle.dump( sorted(secondaryIndex), open( filePath, "wb" ) )
  fileptr=open(filePath,"w")
  for word in sorted(secondaryIndex):
    toWrite=word+":"+str(secondaryIndex[word])+"\n"
    # pickler.dump(toWrite)
    fileptr.write(toWrite)
  fileptr.close()

if __name__=="__main__":
  folderPath="/content/drive/My Drive/IndexFiles/indexfile_*"
  get_Files(folderPath)
  mergeDump()
  writeIndexFile()
  writeSecondaryIndex()