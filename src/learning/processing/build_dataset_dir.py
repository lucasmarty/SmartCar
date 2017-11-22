import numpy as np
from scipy.misc import imread, imresize
from sklearn import svm
from random import shuffle

import filters
import parse

NPY_DATA_NAME = "dataset"
NPY_LABELS_NAME = "labels"

def min(a, b) : return a if a < b else b

def dump_npy():
    FOLDER = "client/dataset01/"
    DEBUG = True

    files = []
    dataset = []
    labels = []

    files_l1 = parse.get_filenames(FOLDER + "forward")
    min_len = len(files_l1)

    files_l2 = parse.get_filenames(FOLDER + "left")
    min_len = min(min_len, len(files_l2))

    files_l3 = parse.get_filenames(FOLDER + "right")
    min_len = min(min_len, len(files_l3))

    print(min_len)

    shuffle(files_l1)
    shuffle(files_l2)
    shuffle(files_l3)

    files += files_l1[:min_len]
    files += files_l2[:min_len]
    files += files_l3[:min_len]

    print(len(files))

    for i, f in enumerate(files):
        dataset.append(f)
        labels.append(parse.labelize_dir(f))

    np.save(NPY_DATA_NAME, dataset)
    np.save(NPY_LABELS_NAME, labels)

def readNshape(img):
    file = imread(img)
    file = imresize(file, (224, 224))
    return file

def gen_data(f_dataset, f_labels, batch_size):
    '''
    f_dataset : nom du fichier .npy où sont les noms des fichiers
    f_labels : nom du fichier .npy où se trouvent les labels
    batch_size : le nombre de fichiers à envoyer par batch
    '''
    dump_npy()
    dataset = np.load(f_dataset)
    labels = np.load(f_labels)
    j = 0
    grappe_data = []
    grappe_labels = []

    max_size = len(dataset)
    for i in range(max_size):

        if j == batch_size or i == max_size:
            yield np.array(grappe_data), np.array(grappe_labels)

            grappe_data = []
            grappe_labels = []
            j = 0

        grappe_data.append(readNshape(dataset[i]))
        grappe_labels.append(labels[i])
        j += 1
