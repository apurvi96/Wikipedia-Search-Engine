#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import re


# In[ ]:


class TextFieldProcessor():
    data=None
    def process(self,data):
        self.data=data
        self.data=self.data.casefold()
        self.remove_Regx()
        External_Links=self.get_external_links()
        info,bodytext,category,references=self.get_InfoBox_category()
#         print("references ",references)
#         print("body ",bodytext)
#         references=self.get_references()
        return info,bodytext,category,External_Links,references
    
    def remove_Regx(self):
        removReg1=re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL).sub('',self.data)
        self.data=removReg1
        
        removReg2=re.compile(r'{\|(.*?)\|}',re.DOTALL).sub('',self.data)
        self.data=removReg2
        
#         removReg3=re.compile(r'{{v?cite(.*?)}}',re.DOTALL).sub('',self.data)
#         self.data=removReg3
        
        removReg4=re.compile(r'[.,;_()"/\']',re.DOTALL).sub(' ',self.data)
        self.data=removReg4
        
        removReg5=re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL).sub('',self.data)
        self.data=removReg5
        
        removReg6=re.compile(r'<(.*?)>',re.DOTALL).sub('',self.data)
        self.data=removReg6
        self.data=self.data.replace('_',' ').replace(',','')
        
    def get_Refreg(self):
        Ref_regx=re.compile(r'(==\s?references\s?==(.*?)}}\n\n)', re.DOTALL)
        return Ref_regx
        
    def get_external_links(self):
        external_links=[]
        lines=self.data.split('\n')
        line_present=1
        i=0
        while i<len(lines):
            if "== external links ==" in lines[i] or "==external links ==" in lines[i] or "== external links==" in lines[i] or line_present==0 or "==external links==" in lines[i]:
                i+=1
                while i < len(lines):
                    if "*[" in lines[i] or "* [" in lines[i]:
                        external_links.extend(lines[i].split(' '))
                    i+=1
            i+=1         
        return external_links
                
    def check_bodyend(self,line):
        return "[[category:" in line or "== external links ==" in line or "==external links ==" in line or "== external links==" in line or "==external links==" in line
    
    def get_InfoBox_category(self):
        info=[]
        Text_body=[]
        Category=[]
        flag=0
        lines=self.data.split('\n')
        references=[]
        no_line=len(lines)
        i=0
        Body_flag=1
        while(i<no_line):
            if '{{infobox' in lines[i]:
                count_open=0
                split_1=lines[i].split('{{infobox')
                if(len(split_1)==2):
                    info.extend(split_1[1:])
                while True:
                    if '{{' in lines[i]:
                        openb=lines[i].count('{{')
                        flag=1
                        count_open+=openb
                    
                    if '}}' in lines[i]:
                        close=lines[i].count('}}')
                        flag=0
                        count_open-=close
                    
                    if count_open<=0:
                        break
                    i=i+1
                    
                    if(i<len(lines)) and count_open>0:
                        append_data=lines[i]
                        info.append(append_data)
                    else:
                        break
            
            elif "==references==" in lines[i] or "== references==" in lines[i] or "==references ==" in lines[i] or "== references ==" in lines[i]:
                i+=1
                flag=1
                count_open=0
                while i<len(lines):
                    if "==" in lines[i] or "[[category:" in lines[i]:
                        break
                    
                    elif "{{cite" in lines[i] or "{{vcite" in lines[i]:
                            cite_split=lines[i].split("title=")
                            if(len(cite_split)>1):
                                references.append(cite_split[1].split("|")[0])
                    
                    elif "{{ref" not in lines[i] and "{{" in lines[i]:
                        references.append(lines[i].split("{{")[1].split("}}")[0])
                    
#                     print("type reference",type(references))
                    
                    i+=1
            
            elif (Body_flag==1):
                #at start of a category or a external link body finishes
                if (self.check_bodyend(lines[i])):
                    Body_flag=0
                Text_body.append(lines[i])
            
            elif "[[category:" in lines[i]:
                category_split=lines[i].split("[[category:")
                l=len(category_split)
                if(l>1):
                    Category.extend(category_split[1:-1])
                    l=len(category_split)
                    Category.append(category_split[-1].split(']]')[0])
            i+=1
        
        return info,Text_body,Category,references
    
    def process_ref(self,Sref):
        self.data=self.data.replace(Sref.group(0), ' ')
        self.data=self.data.replace(Sref.group(2), ' ')
        return Sref.group(2)

    def get_references(self):
        references=[]
        lines=self.data.split('\n')
        line_present=1
        i=0
        while len(lines)>0 and i<len(lines):
            if "==references==" in lines[i] or "== references==" in lines[i] or "==references ==" in lines[i] or "== references ==" in lines[i]:
                i+=1
                flag=1
                count_open=0
                while i<len(lines):
                    if "==" in lines[i] or "[[category:" in lines[i]:
                        break
                    
                    elif "{{cite" in lines[i] or "{{vcite" in lines[i]:
                            cite_split=lines[i].split("title=")
                            if(len(cite_split)>1):
                                references.append(cite_split[1].split("|")[0])
                    
                    elif "{{ref" not in lines[i] and "{{" in lines[i]:
                        references.append(lines[i].split("{{")[1].split("}}"))
                    
                    
                    i+=1
            i+=1
        return references
                
        

