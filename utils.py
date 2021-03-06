import collections
import csv
import numpy as np
import itertools
import matplotlib.pyplot as plt


def preprocess(X):
    X_binarized = [binary_representation(item) for item in X]
    X_binarized = np.array(X_binarized)

    # X_binarized = X_binarized.reshape((X_binarized.shape[0],X_binarized.shape[1]))

    return X_binarized


def confusion_matrix(cm,title='Confusion matrix',cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """

    print('Confusion matrix plot')

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()


    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def create_dict_words():
    kmer = 3
    nucleotides = ['A', 'T', 'G', 'C']
    words = []
    binary_words = {}
    combinations = itertools.product(*itertools.repeat(nucleotides, 3))
    for idx, j in enumerate(combinations):
        words.append(''.join(j))
        _ = np.zeros((len(nucleotides) * len(nucleotides) * len(nucleotides)))
        _[idx] = 1.0
        binary_words[''.join(j)] = _

    return binary_words


def kmers(seq, k):
    kmer = []
    # overlapping
    for i in range(len(seq) - k + 1):
        kmer.append(seq[i:i + k])
    # non-overlapping
    #for i in range(0,len(seq) - k + 1,k):
    #    kmer.append(seq[i:i + k])

    return kmer



def binary_representation(fn, k=3, limit=1):
    d = collections.defaultdict(int)
    dict_words = create_dict_words()

    seq_l = fn
    kms = kmers(seq_l, k)


    representation = []
    for idx in range(0, len(kms) - 1):
        f_ = np.array(dict_words[kms[idx]])
        s_ = np.array(dict_words[kms[idx + 1]])

        representation.append(np.stack((f_,s_)))

    representation = np.array(representation)

    return np.array(representation)

def get_words(vector_sentences):
    sentences = []
    k = 3

    for sentence in vector_sentences:
        words = []
        for i in range(0, len(sentence) - k + 1, k):
            words.append(sentence[i:i + k])

        sentences.append(words)

    return sentences


def transform_to_vectors(X, dict_words):
    new_x = []
    k = 3

    for sentence in X:
        words = [dict_words[sentence[i:i + k]] for i in range(0, len(sentence) - k + 1, k)]
        new_x.append(np.array(words).flatten())

    return np.array(new_x)

def load_csv(dataset):
    X, y = [], []
    classes = -1
    available = []
    input_file = "datasets/" + dataset
    with open(input_file) as raw_data:
        data = csv.reader(raw_data, delimiter=',')
        for idx, val in enumerate(data):
            if idx == 0:
                continue
            sequence = val[2]
            target = val[0]
            preprocessed = sequence.replace(" ", "")

            X.append(preprocessed)
            if not dataset=='splice.csv':
                y.append(int(target))
            else:
                if not target in available:
                    classes += 1
                    y.append(classes)
                    available.append(target)
                else:
                    y.append(classes)

    y=np.array(y)

    return X,y


def oneHotEncoding(y, classes=10):
    n_labels = y.shape[0]
    labels_one_hot = np.zeros((n_labels, classes))
    labels_one_hot[np.arange(n_labels), y] = 1

    return labels_one_hot


def preproc(x):
    """Convert values to range 0-1"""
    batch_normalized = x / x.max()

    return batch_normalized

def get_binary_words(vector_sentences,flatten_words=False):
    sentences = []
    k=3
    nucleotides={'a':[1,0,0,0],'t':[0,1,0,0],'c':[0,0,1,0],'g':[0,0,0,1],
                 'A': [1, 0, 0, 0], 'T': [0, 1, 0, 0], 'C': [0, 0, 1, 0], 'G': [0, 0, 0, 1]}

    sizes=[]

    for sentence in vector_sentences:
        words = []
        kms = kmers(sentence, k)
        for val in kms:

            word_rep=[]
            for symbol in val:
                rep = np.zeros(4)
                # lidando com ambiguidade
                if symbol == 'D':
                    ambig = np.random.choice((0,1,3),1,replace=False)
                    rep[ambig]=1

                elif symbol == 'N':
                    ambig = np.random.choice((0,1,2,3),1,replace=False)
                    rep[ambig]=1

                elif symbol == 'S':
                    ambig = np.random.choice((2,3),1,replace=False)
                    rep[ambig]=1

                elif symbol == 'R':
                    ambig = np.random.choice((0,3),1,replace=False)
                    rep[ambig]=1

                else:
                    rep = nucleotides[symbol]

                word_rep.append(rep)


            word_rep = np.array(word_rep)
            words.append(word_rep.flatten())
        if flatten_words:
            words=np.array(words)
            words= words.flatten()
        sentences.append(words)
    sentences = np.array(sentences)


    return sentences
