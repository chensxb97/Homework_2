#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import sys
import string
import os
import pickle
import math
from os import listdir
from os.path import join, isfile
from nltk.stem.porter import PorterStemmer


def usage():
    print("usage: " +
          sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")


def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below

    # Initialisation
    list_punc = list(string.punctuation)
    stemmer = PorterStemmer()
    index_dict = {}
    postings = {}
    files = [f for f in listdir(in_dir) if isfile(
        join(in_dir, f))]  # all files from directory
    sorted_files = sorted(files, key=lambda f: int(
        os.path.splitext(f)[0]))  # sorted files
    # Word_processing and tokenisation for each file
    for file in sorted_files:
        file_path = join(in_dir, file)
        f = open(file_path, "r")
        tokens = []
        for line in f:
            new_line = ''
            for c in line:
                if c not in list_punc:
                    new_line += c
            new_line = new_line.lower()
            for sentence in nltk.sent_tokenize(new_line):
                for word in nltk.word_tokenize(sentence):
                    word = stemmer.stem(word)
                    tokens.append(word)

        for t in tokens:
            if t not in index_dict:
                index_dict[t] = 1
                postings[t] = [int(file)]
            else:
                if int(file) not in postings[t]:
                    index_dict[t] += 1
                    postings[t].append(int(file))

    # Sort dictionary
    temp_index_dict = sorted(index_dict.items())
    # Note temp_index_dict is are key-sorted tuples of the indexed dictionary
    sorted_index_dict = {}
    for pointer, (key, value) in enumerate(temp_index_dict):
        pointer += 1  # Pointer starts from 1
        # value:doc-frequency, pointer:line number
        sorted_index_dict[key] = (value, pointer)

    # Save results postings file
    output_post = open(out_postings, "w")
    for word in sorted_index_dict:
        posting_list = create_posting_list(postings[word])
        output_post.write(posting_list + '\n')
    output_post.close()

    # Save dictionary
    pickle.dump(sorted_index_dict, open(out_dict, "wb"))
    print('done!')


def create_posting_list(posting):
    posting_list = [str(i) for i in list(posting)]
    interval = math.floor(math.sqrt(len(posting_list)))
    posting_str = ''
    i = 1
    for p in posting_list:
        if interval > 0 and i % interval == 0 and i != 1:
            posting_str += '*{} '.format(interval)
        posting_str += p
        posting_str += ' '
        i += 1
    return posting_str


input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # input directory
        input_directory = a
    elif o == '-d':  # dictionary file
        output_file_dictionary = a
    elif o == '-p':  # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
