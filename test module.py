#!/usr/bin/env python
# coding: utf-8

# In[32]:


import os

#this module aims to test bam file's format via ValidateSamFile (a java picard tool)
#if VSF output ERROR then break and show user the ERROR info for format correction
#otherwise it shall continue the qc process

location="/home/kechanglin/data/new_test.bam" #input a bam's directory
valinfo=os.popen("java -jar /home/kechanglin/picard.jar ValidateSamFile I="+location+" MODE=SUMMARY")


# In[33]:


import re

def validateBAM(valinfo):
    for i in valinfo:
        if not re.match('ERROR',str(i))== None:
            print(i)
    


# In[34]:


validateBAM(valinfo)


# In[170]:


import pysam
location1="/data/yangxiaoxia/bqsr.bam"
psentity=pysam.AlignmentFile(location1,'rb')


# In[119]:


# BAMheader=pysam.view("-H",location1)
a=str(re.findall(r'PL:\w+',BAMheader))[5:-2] #output platform name
print(a)


# In[117]:


print(BAMheader)


# In[213]:


BAMheader[67:76]


# In[224]:


class BAMinput(object):
    """input bam file and check format"""
    
    def __init__(self,directory):
        self.directory=directory
    
    def ValidateBAM(self,crash=False):
        self.valinfo=os.popen("java -jar /home/kechanglin/picard.jar ValidateSamFile I="+self.directory)
        for i in self.valinfo:
            if not re.match('ERROR',str(i))== None:
                print(i)
                self.crash=True
        if crash==True:
            raise ValueError('fatal error in file format!')
        
    
    def gen_identification(self):
        self.treatment=False
        self.BAMheader=pysam.view("-H",self.directory)
        self.platform=str(re.findall(r'PL:\w+',self.BAMheader))[5:-2] #output platform name
        try:
            if plat[str.upper(self.platform)]=='gen3':
                self.treatment=True #treatment arg is for furture gen3 file handling
        except KeyError as e:
            raise KeyError('no equipment info provided, thus unable to tell sequencing technology, it could be a converted file.')
        finally:
            return self.treatment
        
# @staticmethod
def check_md5(filepath, md5):
    """Check File md5."""
    filemd5 = FileMD5(filepath)
    return filemd5.md5check(md5)
        


# In[206]:


class FileMD5(object):
    """Generate md5."""

    def __init__(self, filepath):
        """Init class."""
        filepath = os.path.abspath(filepath)
        if not os.path.isfile(filepath):
            raise ValueError("Can not find file %s!" % filepath)
        self.filepath = filepath

    @property
    def md5(self):
        """Get md5 of file."""
        hash_md5 = hashlib.md5()
        with open(self.filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def write_md5(self, outfile):
        """Write md5 of file to outfile."""
        with open(outfile, 'wt') as wt:
            wt.write('%s  %s' % (self.md5, self.filepath))

    def md5check(self, md5):
        """Check md5 file."""
        if self.md5 != md5:
            return False
        else:
            return True

#maybe useless code
def md5sum(md5file):
    """Md5sum -c file."""
    md5, filename = ('',) * 2
    with open(md5file) as wt:
        for line in wt:
            if line.startswith("MD5"):
                filename, md5 = line.split('=')
                filename = filename.replace('MD5(', '').replace(')', '')
            else:
                md5, filename = line.split('  ')[:2]
            md5 = md5.strip()
            filename = filename.strip()
            filemd5 = FileMD5(filename)
            infor = 'succeed' if filemd5.md5check(md5) else 'fail'
            print('{} md5 check: {}'.format(filename, infor))


# In[222]:


import logging
import os
import re
import sys
import time
import argparse
import json
import pysam
import hashlib
import subprocess

plat={
    'PACBIO':'gen3',
    'SEQUEL':'gen3',
    'ILLUMINA':'gen2',
    'MGISEQ':'gen2'
}

qualimap_loc="/home/kechanglin/biosoft/qualimap_v2.2.1/qualimap"
qualimap_out="/home/kechanglin/data"


# In[226]:



"""Run system command."""
def run_cmd(cmd):
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = pipe.communicate()
    pipe.wait()
    if pipe.returncode != 0:
        raise ValueError("Failed to run command :%s, error mesages: %s." % (cmd, pipe.stderr.read().decode('utf-8')))
    else:
        return stdout,stderr
        # return pipe.returncode,stdout,stderr
    


# In[140]:


testinstance=BAMinput(location)
testinstance.ValidateBAM()
testinstance.gen_identification()


# In[225]:


testinstance=BAMinput(location)
testinstance.ValidateBAM()
#testinstance.gen_identification()


# In[214]:


check_md5(location1,'093dd0fec383a9d9')


# In[221]:


qc_info=os.popen(qualimap_loc+' bamqc -bam '+location+' -outdir '+qualimap_out+' -outformat PDF:HTML')
print(qc_info)


# In[251]:


qc_sub_run=run_cmd(qualimap_loc+' bamqc -bam '+location+' -outdir '+qualimap_out+' -outformat PDF:HTML')


# In[248]:


run_list=str(qc_sub_run[0]).split('\\n')


# In[250]:


for i in range(len(run_list)):
    print(run_list[i])


# In[255]:


import hashlib
#individual check on md5
def md5(filepath):
    """Get md5 of file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

md5(location)
    


# In[ ]:




