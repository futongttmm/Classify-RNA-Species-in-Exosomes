# Classify RNA Species in Exosomes

Exsomes, a membrane-enclosed microvesicles, secreted by cell from internal endosome-derived membranes. 
It can modulate the behaviors of the recipient cells and may used as biomarkers for diagnosis of human diseases. 
By using the deep-learning method, a popular approach of predication, whether it is a RNA sequence packaged in exosomes or not may be identify.

P.S.  Here, the raw data is too big to upload. The raw data can be download from this 
[Google Drive](https://drive.google.com/drive/folders/1oE7LYvUqyKaf2S5yHvpO5RZBBCu-aGha?usp=sharing).

## Introduction
Exosomes refer to small vesicles (30-150 nm) containing complex RNAs and proteins, 
which today are specifically referred to as disc-shaped vesicles having a diameter of 40-100 nm. 
A variety of cells secrete exosomes in both normal and pathological conditions, and exosomes are naturally present in body fluids, 
including blood, saliva, urine, cerebrospinal fluid, and milk. 
Exosomes are currently regarded as specifically secreted vesicles, involved in intercellular communication, 
which contain an amount of different RNA species that can relatively regulate and determine the traits of recipient cells 
and is probably used as a detector for diagnosis of specific human diseases.

Long RNA species in human blood exosomes, such as messenger RNA (mRNA), long non-coding RNA (lncRNA) and circle RNA (circRNA), 
are increasingly proven to be the useful clinical implications. For instance, androgen receptor splice variant 7 (AR-V7) 
is detectable in plasma- derived exosomal RNA of patients with castration-resistant prostate cancer (CRPC) 
and may be a predictive biomarker of resistance to hormonal therapy in CRPC. Human telomerase reverse transcriptase (TERT) mRNA 
was found to be absent in serum-derived exosomes from normal persons but was variably detected in patients with different cancer types. 
The detection of serum exosomal HOTAIR lncRNA may be a potential biomarker for diagnosing laryngeal squamous cell carcinoma (LSCC) 
or rheumatoid arthritis (Shengli Li et al., 2017). 
Therefore, identifying and analyze RNA species packaged in exosomes has realistic significance. 

Considering the data, there is a database of circRNA, lncRNA, and mRNA in human blood exosomes, named exoRBase. exoRBase 
features the integration and visualization of RNA expression profiles based on normalized RNA-seq data spanning both normal 
individuals and patients with different diseases. exoRBase aims to collect and characterize all long RNA species in human blood exosomes. 
The first release of exoRBase contains 58,330 circRNAs, 15,501 lncRNAs and 18,333 mRNAs (Shengli Li et al., 2017). 
It is appropriate to obtain the data used in the project from this database.

Recently, increasing attention has been paid to deep neural network architectures such as feed- forward neural network, 
convolutional neural network and recurrent neural network. The reason why this technique become explosively popular is 
because of the development of more optimal algorithm for training deep model, elegant and simple to use libraries for implementation, 
the capability of greater computational resources, and more raw data. The achievement of developing neural network 
generate various programing frameworks to train a feasible neural network and to validate its accuracy. 
The framework using in this project is Keras, a high-level and easy-to-use
neural network application programming interface, which is based of the TensorFlow and Theano. 
With bioinformatics, here, the application of deep learning with Keras is meaningful in prediction of RNAspecies.

## Method
First, using exoRBase to obtain the annotation of the RNA sequences, such as gene name, chromosome, start position, end position, 
the orientation and the length of those sequences. Next, extracting the useful parts from the whole information, and it is indicated in Figure 2. 
According to the annotation of the sequences, the complete raw data can be obtained from Ensembl Project which provide RNA sequence expressed 
in deoxyribonucleotide (http://rest.ensembl.org). Instead of using the whole dataset getting from exoRBase, 
I choose 6000 RNA sequences from lncRNA, mRNA and circRNA respectively, and each of them are truncated to 400 nucleotides 
(the first and last 200 nucleotides of each sequence obtaining from the website). 
That means, the sum of the data is 6000. However, it is not enough, if we prepare to know whether a RNA sequence packaged in exosomes or not, 
another set of data which is relatively irrelevant with the original data is needed.
I separated the data in to two parts, the first set is the original data getting from exoRBase and Ensembl, and the second one that I shuffled it randomly. 
Therefore, the total number of this dataset is 12000 including training set and test set.


Besides, in order to perform a better job in prediction, one-hot encoding is required, where a nucleotide is represented by a vector of length 4. 
RNA sequences are encoded as ‘one-hot’ format, showing in Figure 3 and Table 1, with a single ‘1’ at the different positions and three zero 
corresponding to nucleotides type (A, G, C and T). Therefore, the structure of input data is a 12000*1600 matrix.

After those preparatory works, I implemented three neural networks models starting from a simple feed forward neural network up 
to convolutional neural network and long short-term neural network. Figure 4 shows the simple FNN model. In order to process the data, 
firstly they need to be flattened and every single sequence becomes a one-dimensional vector. Considering to prevent overfitting, 
I use dropout mechanism to deal with data redundancy. For every training input, the output fo each hidden unit is set to zero 
with a certain probability selecting manually. Here the probability is set as 50%. There is only one output unit in the output layer, 
because the problem is a binary classification problem that means there are only two possibilities of the output. 
Hence, sigmoid function is suitable to be the activation function of this layer.

The convolutional neural network used in this project is indicating in Figure 5. The layers of it are more complex than that of FNN. 
For each sequence, 3 sets of filters are applied to extract feature values. In the first convolutional layer, the number of filters are 10, 
and the kernel size is 3. And then, the next 10 filters are set into size 5. The third convolutional layer has 20 filters setting the same kernel 
size with those in the first convolutional layer. Besides, to make a convolutional neural network to be independent of the input sequence length, 
max pooling contributes a lot. It provides an approach of reducing the input or hidden layer size by selecting only the maximally activated
neuron from a number of neighboring neurons. On the classification problem, max-pooling is equivalent to feature selection, 
and features are selected to facilitate classification. Therefore, the number of hidden neurons generated by the convolutional filter is equal 
to the number of filters and not influenced by the input sequence length.

A clear layer structure of LSTM model of the project showing in Figure 6, and by choosing the directional layer 
because it will integrate the information locally not only forward but also backward in the sequence.

## Result

The most significant thing considered here is the accuracy of validation set which shows by the orange line of each diagram. 
The accuracy of FNN model in the context fluctuates from 0.73 to 0.77, which is relatively not bad. Moreover, 
the accuracy of validation set for convolutional neural network is excellent, meanwhile it is only trained for 20 epoches. 
Additionally, the result of long short-term neural network is not ideal. 
From the diagram, we can see even though it was trained 80 epchoes, the accuracy is unstable.

## Conclusion
In this project, the result of CNN relatively better than that of feed forward neural network and long short-term neural network.
The reason why CNN performs so well s because it can be applied to an extraction of a sequence motif which is a sequence pattern that repeat 
in a set of input sequences and is frequently represented as a position weight matrix that the importance of each kind of nucleotide at every 
position in the pattern. Through training the positive and negative dataset, the filters can be learn automatically. 
Therefore, the filters will recognize features in input sequences without knowing the places they appear.


## References
1. Vanessa I. J. et.al. (2017) An introduction to deep learning on biological sequence data: examples and solutions. Bioinformatics, 33(22), 2017, 3685–3690
2. Genta A.and Yasubumi S. (2018) Convolutional neural networks for classification of alignments of non-coding RNA sequences. Bioinformatics, 34, 2018, i237–i244
3. Shengli L. et.al. (2018) exoRBase: a database of circRNA, lncRNA and mRNA in human blood exosomes. D106–D112 Nucleic Acids Research, 2018, Vol. 46, Database issue
