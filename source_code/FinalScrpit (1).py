#!/usr/bin/env python
# coding: utf-8

# In[4]:


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

#input

location1="/data/yangxiaoxia/bqsr.bam"
location2="/home/kechanglin/gen3ccs_new3.ccs.bam"
location="/home/kechanglin/data/new_test.bam" #test input of bam's directory
md5_input="2cb38082d6d46d425cb7181665e38147" #md5 of the location file
qualimap_loc="/home/kechanglin/biosoft/qualimap_v2.2.1/qualimap"
qualimap_out="/home/kechanglin/data"
vsf_loc="/home/kechanglin/picard.jar"
ccs_out="/home/kechanglin/gen3ccs_new3.ccs.bam"
fastq_out="/home/kechanglin/data/newfq.fastq"
fastp_out="/home/kechanglin/data/fastp_newfq.fq"


def run_cmd(cmd):
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = pipe.communicate()
    pipe.wait()
    if pipe.returncode != 0:
        raise ValueError("Failed to run command :%s, error mesages: %s." % (cmd, pipe.stderr.read().decode('utf-8')))
    else:
        return stdout,stderr
    
def run_ccs(input_file,output_file,env_name='py27'):
    pipe1=subprocess.Popen('source activate '+env_name+' && '+'ccs '+input_file+' '+output_file+' && '+'conda deactivate',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = pipe1.communicate()
    pipe1.wait()
    #ccs=run_cmd('source activate '+env_name+' && '+'ccs '+input_file+' '+output_file+' && '+'conda deactivate')
    return pipe1.returncode,stdout,stderr


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

def check_md5(filepath, md5):
    """Check File md5. execution func"""
    filemd5 = FileMD5(filepath)
    return filemd5.md5check(md5)
        
    
    
    
class BAMinput(object):
    """input bam file and check format"""
    
    def __init__(self,directory):
        self.directory=directory
        if not os.path.isfile(self.directory):
            raise IOError("no such file %s" % self.directory)
        if not self.directory.endswith('.bam'):
            raise IOError("unable to manage file other than .bam")
    
    def ValidateBAM(self,crash=False):
        
        """format validation and if fatal error met then check md5"""
        self.valinfo=os.popen("java -jar "+vsf_loc+" ValidateSamFile I="+self.directory+" MODE=SUMMARY")
        for i in self.valinfo:
            if not re.match('ERROR',str(i))== None:
                print(i)
                self.crash=True
        if self.crash==True:
            self.md5_result=check_md5(self.directory,md5_input)
            if self.md5_result:
                print('md5 check ok but found fatal error in file format!') #格式有问题，md5无误
            else: 
                raise ValueError('fatal error in file due to failed md5 check!') #格式有问题，md5改变
        
        
    
    def gen_identification(self):
        self.treatment=False
        self.BAMheader=pysam.view("-H",self.directory)
        self.platform=str(re.findall(r'PL:\w+',self.BAMheader))[5:-2] #output platform name
        # print(self.platform)
        if self.platform == ''or self.platform is None:
            print('no equipment info provided, thus unable to tell sequencing technology, it could be a converted file')
        elif plat[str.upper(self.platform)]=='gen3':
            self.treatment=True #treatment arg is for furture gen3 file handling
            print('gen3 seq bam detected')
        elif plat[str.upper(self.platform)]=='gen2':
            print('gen2 seq bam detected')
        else: 
            print('no recognizable equipment info detected, thus unable to tell sequencing technology, it could be a converted file')
        return self.treatment
    
    
    def gen2_qc(self):
        self.qc_sub_run=run_cmd(qualimap_loc+' bamqc -bam '+self.directory+' -outdir '+qualimap_out+' -outformat PDF:HTML')
        self.run_list=str(self.qc_sub_run[0]).split('\\n')
        self.show_run= self.run_list[20:42]
        return self.show_run
        
    
    def gen3_qc(self):
        self.gen3_run=run_ccs(self.directory,ccs_out)
        self.gen3_run_log=self.gen3_run[2]
        self.fq_log=os.system('samtools fastq '+ccs_out+' > '+fastq_out)
        self.fp_log=run_cmd('fastp -i '+fastq_out+' -o '+fastp_out)
        self.fastp_report_dir=os.getcwd()
        return self.gen3_run_log,self.fq_log,self.fp_log,self.fastp_report_dir


        

if __name__ == '__main__':
#test command    
    testinstance=BAMinput(location2) #change this arg to run test
    id_treatment=testinstance.gen_identification()
    if id_treatment==True:
        ccs_result=testinstance.gen3_qc()
        # output gen3 result to json
    else:
        testinstance.ValidateBAM()
        gen2_reslut=testinstance.gen2_qc()
        # output gen2_result to json
    
    
    
    
    #for i in range(len(self.show_run)):
         #   print(self.show_run[i])
    # check_md5(location,md5_input)
    


# In[ ]:





# In[ ]:





# In[ ]:




