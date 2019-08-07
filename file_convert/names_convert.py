#!/usr/bin/env python
# coding: utf-8

# In[9]:


import os
import re
import sys


# In[34]:


def read_name_dmp(dmpfile):
    dict1={}
    if dmpfile.endswith('.dmp'):
        with open(dmpfile) as rd:
            for line in rd:
                text=line.rstrip('\t|\n').split('\t|\t')
                if int(text[0]) in dict1.keys():
                    dict1[int(text[0])]=dict1[int(text[0])]+' | '+text[1]+' * '+text[3]
                else:
                    dict1[int(text[0])]=text[1]+' * '+text[3]
        return dict1
    else:
        raise ValueError('invalid input file!')
            


def out_file(dic,out_dir):
    if not os.path.exists(out_dir):
        for i in dic.keys():
            with open(out_dir,'a+') as w:
                result=str(i)+' | '+dic[i]+' | \n'
            
                w.write(result)
    else:
        raise ValueError('pls delete existing file!')
            
    


if __name__=='__main__':
    dict2=read_name_dmp('/home/kechanglin/data/data_conversion/names.dmp')
    out_file(dict2,'/home/kechanglin/data/data_conversion/name_result')


# In[28]:





# In[ ]:




