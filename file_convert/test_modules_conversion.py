#!/usr/bin/env python
# coding: utf-8

# In[2]:


from copy import deepcopy
import json
import os
import re
import sys


# In[49]:


test='251315	|	131567 2157 28890 2290931 183963 2235 2236 2239 	|'
item = [re.sub(r'\s+\|\s+', '', x) for x in test.rstrip(os.linesep).split('\t|\t')]


# In[50]:


item_new=item[1].rstrip(' \t|')
kk=item[0]


# In[84]:


nn=item_new.split(' ')
nn.reverse()


# In[55]:


nn


# In[105]:


def new_read_dmp(dmpfile):
    tmp_dict={}
    with open(dmpfile) as rd:
        for line in rd:
            item=[re.sub(r'\s+\|\s+', '', x) for x in line.rstrip(os.linesep).split('\t|\t')]
            key=int(item[0])
            value=item[1].rstrip(' \t|')
            tmp_dict[key]=value
    return tmp_dict

def treat_value(v):
    tmpv=v.split(' ')
    tmpv.reverse()
    tmpv.append('1')
    return tmpv

dict1=new_read_dmp("/home/kechanglin/data/data_conversion/taxidlineage.dmp")
    
dict2={}
for key in dict1.keys():
    dict2[key]=treat_value(dict1[key])
    
list1=sorted(dict2.items(),key=lambda sort:sort[0] ,reverse=False)


# In[25]:


dict1=new_read_dmp("/home/kechanglin/data/data_conversion/taxidlineage.dmp")


# In[86]:


dict2={}
for key in dict1.keys():
    dict2[key]=treat_value(dict1[key])


# In[100]:


# print(re.sub(r'\D',' ',str(list1[1])))


# In[98]:


# str(list1[1])


# In[107]:


with open('/home/kechanglin/data/data_conversion/result_taxidlineage','a+') as w:
    for i in list1:
        result=re.sub(r'\D',' ',str(i))
        w.write(result+'\n')


# In[ ]:




