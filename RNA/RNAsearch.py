#!/usr/bin/python3

from subprocess import Popen, PIPE

import re

'''Infernal detects ncRNA from Rfam'''

def INFERNAL2GFF3(INFERNAL_output):
    INFERNAL_output_gff = INFERNAL_output + '.gff'
    f = open(INFERNAL_output_gff,'w')
   process = Popen(args=['awk', r'BEGIN {print "##gff-version 3"} NR>2{if($8 < $9 && $8 > 0) printf "%s\tinfernal\tmisc_RNA\t%d\t%d\t.\t%s\t.\tID=%s_infernal_%s_%s;Name=%s\n" ,$3,$8,$9,$10,$3,$8,$9,$1}',INFERNAL_output], 
                   stdout = f, stderr = PIPE)
    stdout, stderr = process.communicate()
    del stdout,stderr

def INFERNAL (input_file,database_path,output_file,cpu_cores):
    process = Popen(args = ['cmscan',
                            '-E','1e-06',
                            '--rfam',               # set heuristic filters at Rfam-level (fast)
                            '--cpu', cpu_cores,     # number of parallel CPU workers to use for multithreads
                            '--tblout',output_file, # save parseable table of hits to file <s>
                            '--noali',              # don't output alignments, so output is smaller
                            database_path,          # Using the Rfam 12.0 bacteria databases
                            input_file],            # Input raw genome assembly file
                            stdout = PIPE, stderr = PIPE)

    stdout, stderr = process.communicate()
    del stdout,stderr

    INFERNAL2GFF3(output_file)
    return stdout

''' ARAGORN detects tRNA, mtRNA, and tmRNA genes
    By default, all RNA gene types above will be searched'''

def ARAGORN2GFF3(ARAGORN_output):
    # For robust use, the path should be specified
    ARAGRON_output_gff = ARAGORN_output[-28:] + '.gff'
    f = open(ARAGRON_output_gff,'w')
    
    process = Popen(args = ['perl',                 # It's a perl script that use perl to run   
                            'cnv_aragorn2gff.pl',   # The script needs to be in current directory or we can add path for it
                            '-i', ARAGORN_output,   # Input file name          
                            '-gff-ver=3'],           # Print out in batch mode, which can be applied for gff convertation
                            stdout = f, stderr = PIPE)

    stdout, stderr = process.communicate()
    del stdout,stderr

def ARAGORN (input_file,output_file):
    process = Popen(args = ['aragorn',              
                            '-l',                   # Assume that each sequence has a linear topology.
                            '-gc1',                 # Use the GenBank transl_table = <num> genetic code.
                            '-w',                   # Print out in batch mode.
                            input_file,
                            '-o',output_file],
                            stdout = PIPE, stderr = PIPE)
    stdout, stderr = process.communicate()
    del stdout,stderr

    ARAGORN2GFF3(output_file)

''' 
    RNAmmer can also detects rRNA, but only have perl version
'''

def RNAMMER (input_file,output_file):
    # For RNAMMER, the primary programs need to be modified
    f = open(output_file,'w')
    process = Popen(args = ['rnammer',
                            '-S', 'bac'     # Kingdom us bacteria
                            '-gff', 
                            input_file],
                            stdout = f, stderr = PIPE)
    stdout, stderr = process.communicate()
    del stdout,stderr

    
def RNAmerge(file_1,file_2):
    list_f1 = []
    list_f2 = []
    list_merge = ["##gff-version 3\n"]
    merge_file = 'rna_merge.gff'
    with open(file_1,'r') as f1:
        for line in f1:
            if not re.match("##",line):
                list_f1.append(line)
    f1.close()
    with open(file_2,'r') as f2:
        for line in f2:
            if not re.match("##",line):
                list_f2.append(line)
    f2.close()
    k = 0
    for i in range(len(list_f1)):
        for j in range(len(k,list_f2)):
            if list_f1[i].split()[3] < list_f2[j].split()[3]:
                list_merge.append(list_f1[i]);break
            else:
                list_merge.append(list_f2[j]);k += 1
    with open(merge_file,'w') as f3:
        for line in list_merge:
            f3.write(line)
    f3.close()  

def main():
    pass
    # Parameters need to specified
    input_file = 'xxx.fna'          # From other's job
    database_path = './db/bacteria' # Rfam is a essential reference to infernal

    output_file_ncRNA = 'ncRNA.gff'
    output_file_tRNA = 'tRNA.gff' 
    output_file_rRNA = 'rRNA.gff'

    cpu_cores = '4'  # Get options to change the number of cores, should be string

    doncRNA = True # Get options to ensure if fo this
    dotRNA  = True # Get options to ensure if fo this
    dorRNA  = True # Get options to ensure if fo this

    if doncRNA == True:
        INFERNAL(input_file,database_path,output_file_ncRNA,cpu_cores)
    if dotRNA  == True:
        ARAGORN(input_file,output_file_tRNA)
    if dorRNA  == True:
        RNAMMER(input_file,output_file_rRNA)
    
    if doncRNA and dotRNA and dorRNA:
        RNAmerge(output_file_ncRNA,output_file_tRNA)
        RNAmerge('rna_merge.gff',output_file_rRNA)
    elif doncRNA and dotRNA:
        RNAmerge(output_file_ncRNA,output_file_tRNA)
    elif doncRNA and dorRNA:
        RNAmerge(output_file_ncRNA,output_file_rRNA)
    elif dotRNA and dorRNA:
        RNAmerge(output_file_tRNA,output_file_rRNA)

if __name__ == '__main__':
    main()
