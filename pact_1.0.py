import os
import sys
import argparse
import textwrap
import subprocess
import pickle
import re
import concurrent.futures
import numpy as np
import pandas as pd
from Bio import SeqIO


def inParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help = "Input file")
    parser.add_argument("-o", "--output", default='output' , help = "Output directory path")
    parser.add_argument("-t", "--threshold", default=-236 , help = "Energy threshold")
    args = parser.parse_args()
    
    return(args)


def temlateSeq(fasta, template):

    record = SeqIO.parse(fasta, 'fasta')  

    for i in record:
        if template == i.name:
            return(str(i.seq))


def add_tails(seq1, seq2, t_seq):
    
    lseq1 = len(seq1)
    lseq2 = len(seq2)
    ltseq = len(t_seq)

    # Seq1 is the longest
    if lseq1 >= lseq2 and lseq1 >= ltseq:

        #Align template seq to seq1
        ldiff = len(seq1)-len(t_seq)
        tail = int(ldiff/2) * '-'
        t_seq = tail + t_seq + tail

        #Align seq2 to seq1
        ldiff = len(seq1)-len(seq2)
        tail = int(ldiff/2) * '-'
        seq2 = tail + seq2 + tail
    
    elif lseq2 >= lseq1 and lseq2 >= ltseq:
        #Align template seq to seq2
        ldiff = len(seq2)-len(t_seq)
        tail = int(ldiff/2) * '-'
        t_seq = tail + t_seq + tail

        #Align seq1 to seq2
        ldiff = len(seq2)-len(seq1)
        tail = int(ldiff/2) * '-'
        seq1 = tail + seq1 + tail

    else:
        #Align seq1 to template
        ldiff = len(t_seq)-len(seq1)
        tail = int(ldiff/2) * '-'
        seq1 = tail + seq1 + tail

        #Align seq2 to template
        ldiff = len(t_seq)-len(seq2)
        tail = int(ldiff/2) * '-'
        seq2 = tail + seq2 + tail


    return(seq1, seq2, t_seq)


def cross_infile(seq1, seq2, structure, fasta):

    t_seq = temlateSeq(fasta, structure)

    print(seq1 + '+' + seq2)
    f = open('alignment.pir', 'w')

    seq1, seq2, t_seq = add_tails(seq1, seq2, t_seq)

    print(">P1;template", file = f)
    print("Structure:%s:FIRST:A:LAST:L::-1.00:-1.00:" % structure, file = f)
    for i in range(1,4):
        print(textwrap.fill(t_seq, width = 80) + '/', file = f)
    print(textwrap.fill(t_seq, width = 80) + '*\n', file = f)

    print(">P1;sequence", file = f)
    print("sequence:target::::::-1.00:-1.00:", file = f)
    #print(textwrap.fill(t_seq, width = 80), file = f)
    for i in range(1,3):
        print(textwrap.fill(seq1, width = 80) + '/', file = f)
    print(textwrap.fill(seq2, width = 80) + '/', file = f)
    print(textwrap.fill(seq2, width = 80) + '*\n', file = f)
    
    f.close()


def runScript(script):
    
    p = subprocess.Popen(script, stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()


def cross_model(seq1, seq2, name, output_path):
    dir_path = output_path+'/'+name
            
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

        #for template in ['2e8d', '2nnt', 'iapp']:
        for template in ['iapp']:

            models_path = output_path+'/'+name+'/'+template
            os.mkdir(models_path)

            template_path = './templates/'+template+'.pdb'
            os.link(template_path, models_path+'/'+template+'.pdb') 
            os.link('scripts/runMod.py', models_path+'/runMod.py') 
                    
            os.chdir(models_path)

            cross_infile(seq1, seq2, template, template_fasta)
            
            # To be version agnostic use mod runMod.py
            # This requires soft link to version downloaded inside docker
            #runScript("mod runMod.py")
            runScript("mod9.24 runMod.py")

            os.chdir('../../../')


def check_if_fasta(seq):
    for i in seq:
        if not i in ['A','C','D','E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']:
            return False
    return True


def check_input(input_path):

    data = pd.read_csv(input_path)
    #print(data.columns)
    if not (data.columns == ['interactor', 'seq1', 'interactee', 'seq2']).all(): 
        sys.exit("Invalid header in input file, should be: \ninteractor,seq1,interactee,seq2")

    seq_list1 = data['seq1']
    seq_list2 = data['seq2']

    n = 0
    for seq1, seq2 in zip(seq_list1, seq_list2):
        if len(seq1) > 45:
            sys.exit("Error in pair %d: seq1 is too long!" % n)
        if len(seq2) > 45:
            sys.exit("Error in pair %d: seq2 is too long!" % n)
        if len(seq1) < 14:
            sys.exit("Error in pair %d: seq1 is too short!" % n)
        if len(seq1) < 14:
            sys.exit("Error in pair %d: seq2 is too short!" % n)
        
        if not check_if_fasta(seq1):
            sys.exit("Error in pair %d: non FASTA chracters in seq1!" % n)
        
        if not check_if_fasta(seq2):
            sys.exit("Error in pair %d: non FASTA chracters in seq2!" % n)

        n+=1



if __name__ == '__main__':
  
    args = inParser()

    input_path = args.input
    output_path = args.output
    
    check_input(input_path)

    # Modeling
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    else:
        sys.exit('Output directory already exist!')

    data = pd.read_csv(input_path)

    template_fasta = '../../../templates.fasta'

    proteins = []
    prot_names = []
    
    names_list1 = data['interactor']
    names_list2 = data['interactee']
    seq_list1 = data['seq1']
    seq_list2 = data['seq2']
    
    f = open(output_path+'/meta.csv', 'w')
    print("seq,length", file=f)
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i in range(len(seq_list1)):
                
                name1 = names_list1[i]
                name2 = names_list2[i]
                name = "pair_" + str(i)
                length = (len(seq_list1[i])+len(seq_list2[i]))/2
                print("%s,%f" % (name, length), file=f)
                
                seq1 = str(seq_list1[i])
                seq2 = str(seq_list2[i])
                
                future = executor.submit(cross_model, seq1, seq2, name, output_path)

      
    f.close()
        
    # Scoring
    os.chdir(output_path)

    os.link('../scripts/data.sh', 'data.sh') 
    
    runScript("bash data.sh > energy.csv")

    data = pd.read_csv("energy.csv")
    meta = pd.read_csv("meta.csv")
    data = pd.merge(data, meta, on='seq')

    min_e = data.loc[data.groupby('seq')['dope'].idxmin()]
    min_e['ndope'] = min_e['dope']/min_e['length']
    min_e['prediction'] = np.where(min_e['ndope'] < args.threshold, 1, 0)

    results = min_e.values

    f = open('results.csv', 'w')
    print('pair,interactor,interactee,score,classification', file=f)
    for i in  range(len(results)):
        #print("%d,%s,%s,%s,%s,%3.2f,%d" % (i, names_list1[i], seq_list1[i], names_list2[i], seq_list2[i],  results[i,-2],results[i,-1]))
        print("%d,%s,%s,%3.2f,%d" % (i, names_list1[i], names_list2[i],  results[i,-2],results[i,-1]), file=f)

    f.close()
    