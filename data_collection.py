import requests
import sys
import re
import numpy as np
import time

"""
Use the annotations to collect corresponding RNA sequence from web
"""

# define a function to get data for mRNA and lncRNA sequences
def Chromosome_m_lnc(filename, filename1):

    f = open(filename)
    f1 = open(filename1, 'w')
    sequence = []
    count = 0
    for i in f:
        if i.startswith('Gene_name'):
            continue

        find = re.search('chr\d', i)
        count += 1
        if count % 15 == 0:
            time.sleep(1)
    # try to get appropriate data in the first 3000 RNA in the file
        if count > 3000:
            break

        if find == None:
            continue
        else:
            num = find.span()[0]
        i = i[num:]
        if i.split()[3] == '-':
            ch = ':-1?'
        else:
            ch = ':1?'
        chromosome = i.split()[0] + ':' + i.split()[1] + '..' + i.split()[2] + ch
    # the codes for getting the sequences from the website
        server = "http://rest.ensembl.org"
        ext = "/sequence/region/human/" + chromosome
        r = requests.get(server + ext, headers={"Content-Type": "text/plain"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        print(count)
        print(chromosome)

    # using .fa format to store the sequence
        #sequence.append(r.text)
        f1.write('>'+ chromosome + '\n' + r.text + '\n')

    f.close()
    f1.close()
    return sequence

# define a function to get data for circRNA which is quite similar to the above one
def Chromosome_circ(filename, filename1):

    f = open(filename)
    f1 = open(filename1, 'w')
    sequence = []
    count = 0
    for i in f:
        if i.startswith("exo_circRNA_ID"):
            continue
        count += 1
        if count % 15 == 0:
            time.sleep(1)
        if count > 3000:
            break
        if i.split()[4] == '-':
            ch = ':-1?'
        else:
            ch = ':1?'
        chromosome = i.split()[3] + ch

        server = "http://rest.ensembl.org"
        ext = "/sequence/region/human/" + chromosome
        r = requests.get(server + ext, headers={"Content-Type": "text/plain"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        sequence.append(r.text)
        print(count)
        print(chromosome)

    # using .fa format to store the sequence
        # sequence.append(r.text)
        f1.write('>' + chromosome + '\n' + r.text + '\n')

    f.close()
    f1.close()
    return sequence


## lncRNA_ann.txt, mRNA_ann.txt, and circRNA_ann.txt only contain the annotation which can be used to extract RNA sequences
## Use the annotation to obtain the RNA sequences from the website respectively
# get the raw sequences and save them
lnc_seq = Chromosome_m_lnc("anntation/lncRNA_ann.txt", "annotation/RNAseq_lnc.fa")
# np.save('raw_data/real_lnc.npy', lnc_seq)

m_seq = Chromosome_m_lnc("annotation/mRNA_ann.txt", "anntation/RNAseq_m.fa")
# np.save('raw_data/real_m.npy', m_seq)

circ_seq = Chromosome_circ("annotation/circRNA_ann.txt", "annotation/RNAseq_circ.fa")
# np.save("raw_data/real_circ.npy", circ_seq)
