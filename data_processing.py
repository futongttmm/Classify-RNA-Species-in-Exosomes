import numpy as np
import random

"""
Create label and features
Convert them into one-hot vectors
Use 400 processed sequences for training and 400 sequences for testing 
"""

# getting positive sample and negative sample of sequences
def get_seq(filename, real_seq):
    f = open(filename)
    for i in f:
        count = -1
        if i.startswith('>'):
            real_seq.append('')
            count += 1
            continue
        else:
            real_seq[count] += i.replace('\n', '')


def get_400(filename, seq_400):
    real_seq = np.load(filename)
    seq = []
    # exclude the sequences shorter than 400
    for i in real_seq:
        if len(i) >= 400:
            seq.append(i)
    # get 2000 randomly for each RNA
    random.seed(10)
    rand_seq = np.array(random.sample(seq, 2000))
    # get 200 Nucleotides in the beginning of original RNA and 200 in the end
    for i in rand_seq:
        seq_400.append(i[0:200] + i[len(i) - 200:len(i)])


real_lnc = []
real_m = []
real_circ = []

get_seq("real_lnc_negative", real_lnc)
np.save("real_lnc_negative.npy", real_lnc)
get_seq('RNAseq_m_negative', real_m)
np.save("real_m_negative.npy", real_m)
get_seq('RNAseq_circ_negative', real_circ)
np.save("real_circ_negative.npy", real_circ)

m_400 = []
lnc_400 = []
circ_400 = []
get_400("data/real_lnc_negative.npy", lnc_400)
get_400("data/real_m_negative.npy", m_400)
get_400("data/real_circ_negative.npy", circ_400)

# stack all the sequences together with labels : 0 for mRNA, 1 for the lncRNA, 2 for the circRNA
x = np.hstack((m_400, lnc_400, circ_400))
y = np.hstack((np.zeros(2000), np.ones(2000), np.ones(2000) + 1))

# shuffle all the data with labels
index = [i for i in range(len(x))]
random.shuffle(index)
x = x[index]
y = y[index]
# x_all = np.zeros((6000, 400, 4))
# y_all = np.zeros((6000, 3))
x_all_negative = np.zeros((6000, 400, 4))
y_all_negative = np.zeros((6000, 3))

# one-hot for y : 0 = [1,0,0] 1 = [0,1,0] 2 = [0,0,1]
for i in np.arange(6000):
    if y[i] == 0:
        y_all_negative[i] = [1, 0, 0]
    if y[i] == 1:
        y_all_negative[i] = [0, 1, 0]
    if y[i] == 2:
        y_all_negative[i] = [0, 0, 1]

# one-hot for x : 'A' = [1,0,0,0], 'G' = [0,1,0,0], 'C' = [0,0,1,0], 'T' = [0,0,0,1]
for i in np.arange(6000):
    for k in np.arange(400):
        if x[i][k] == 'A':
            x_all_negative[i][k][0] = 1
        if x[i][k] == 'G':
            x_all_negative[i][k][1] = 1
        if x[i][k] == 'C':
            x_all_negative[i][k][2] = 1
        if x[i][k] == 'T':
            x_all_negative[i][k][3] = 1

# save data
# np.savez("200x_y200.npz", x_all=x_all, y_all=y_all)
np.savez("200x_y200_negative.npz", x_all_negative = x_all_negative, y_all_negative = y_all_negative)
