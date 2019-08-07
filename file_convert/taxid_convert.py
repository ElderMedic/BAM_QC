#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import re
import sys

def new_read_dmp(dmpfile):
    tmp_dict={}
    if dmpfile.endswith('.dmp'):
        with open(dmpfile) as rd:
            for line in rd:
                item=[re.sub(r'\s+\|\s+', '', x) for x in line.rstrip(os.linesep).split('\t|\t')]
                key=int(item[0])
                value=item[1].rstrip(' \t|')
                tmp_dict[key]=value
        return tmp_dict
    else:
        raise ValueError('invalid input file!')
    

def treat_value(v):
    tmpv=v.split(' ')
    tmpv.reverse()
    tmpv.append('1')
    return tmpv

def finale_process(input_dmp,output_dir):
    dict1=new_read_dmp(input_dmp)
    dict2={}
    for key in dict1.keys():
        dict2[key]=treat_value(dict1[key])
    
    list1=sorted(dict2.items(),key=lambda sort:sort[0] ,reverse=False)

    with open(output_dir,'a+') as w:
        # '/home/kechanglin/data/data_conversion/result_taxidlineage'
        for i in list1:
            result=re.sub(r'\D',' ',str(i))
            w.write(result+'\n')

if __name__ == '__main__':
    
    finale_process(*sys.argv[1:3])

    
        
        


# In[ ]:




