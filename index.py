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
import linecache
from os import listdir
from os.path import join, isfile
from nltk.stem.porter import PorterStemmer

# python index.py -i '<INSERT_PATH>\sample_data' -d dictionary.txt -p postings.txt


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
    files = [f for f in listdir(in_dir) if isfile(
        join(in_dir, f))]  # all files from directory
    sorted_files = sorted(files, key=lambda f: int(
        os.path.splitext(f)[0]))  # sorted files

    # Word_processing and tokenisation for each file
    for file in sorted_files:
        file_path = join(in_dir, file)
        f = open(file_path, "r")
        # Set data structure is used to account for repeated words in the same file
        terms = set()
        for line in f:
            new_line = ''
            for c in line:
                if c not in list_punc:
                    new_line += c
            new_line = new_line.lower()
            for sentence in nltk.sent_tokenize(new_line):
                for word in nltk.word_tokenize(sentence):
                    word = stemmer.stem(word)
                    terms.add(word)
        # Populate the index_dict and postings 'dictionaries'
        # index_dict = {token: token frequency}
        # postings = {token: [list of files token exists in]}
        for term in terms:
            if term in index_dict.keys():
                freq = index_dict[term][1]
                freq += 1
                index_dict[term][1] = freq
            else:
                index_dict[term] = [0, 1, 0]

    # Sort dictionary
    sorted_index_dict_array = sorted(index_dict.items())
    sorted_dict = {}
    for termID, (term, value) in enumerate(sorted_index_dict_array):
        # addition of 1 to ensure termID starts of from value 1
        value[0] = termID+1
        sorted_dict[term] = value
    # print(sorted_dict)
    # note sorted_dict is now a dictionary of {term : [termID, termFrequency, charrOffset]}

    # Divide list of files to 10 batches(BSBI)
    count = count_files(in_dir)
    n = count//2  # Tested with 2 blocks
    blocks = [sorted_files[x:x+n] for x in range(0, count, n)]
    print('Batches: \n', blocks)

    # Processing block
    batch_number = 1
    for block in blocks:
        posting_dict = {}
        for file in block:
            file_path = join(in_dir, file)
            f = open(file_path, "r")
            terms = set()
            for line in f:
                new_line = ''
                for c in line:
                    if c not in list_punc:
                        new_line += c
                new_line = new_line.lower()
                for sentence in nltk.sent_tokenize(new_line):
                    for word in nltk.word_tokenize(sentence):
                        word = stemmer.stem(word)
                        terms.add(word)
            for term in terms:
                termID = sorted_dict[term][0]
                if termID in posting_dict.keys():
                    posting_dict[termID].append(int(file))
                else:
                    posting_dict[termID] = [int(file)]
        # Create and save postings
        postings = create_posting_lists(posting_dict)
        file_name = out_postings+'_{}.txt'.format(batch_number)
        postings_out = open(file_name, 'w')
        for posting in postings:
            postings_out.write(posting)
        postings_out.close()
        batch_number += 1

    # Merge posting lists - BSBI

    '''To FILL IN'''
    final_posting = {}
    number_of_terms = len(sorted_dict.keys())
    print(number_of_terms)
    open(out_postings, 'w').close()
    # For each term, read the relevant line from all blocks
    for i in range(1, number_of_terms+1):
        combined_lines = []
        for j in range(1, batch_number):
            line = linecache.getline(out_postings+'_{}.txt'.format(j), i)
            split_line = line.split()
            if (len(split_line)) > 0:
                new_line = split_line[1:]
                for k in range(0, len(new_line)):
                    combined_lines.append(int(new_line[k]))
        combined_lines_str = ""
        # Turn array into string to be written into postings_file
        for l in combined_lines:
            combined_lines_str += str(l)
            combined_lines_str += ' '
        combined_lines_str += '\n'
        with open(out_postings, 'a') as postings_file:
            postings_file.write(combined_lines_str)
    # print(sorted_dict)

    # Add charOffset to dictionary
    char_offset = 0
    for i in range(1, number_of_terms+1):
        line = linecache.getline(out_postings, i)
        for key in sorted_dict.keys():
            if sorted_dict[key][0] == i:
                tempArray = sorted_dict[key]
                tempArray[2] = char_offset
                sorted_dict[key] = tempArray
        char_offset += len(line)
    print(sorted_dict)

    # HOW WE'RE GOING TO DO SEARCH - SEEK THE CHAR OFFSET - IT WORKS
    # temp = open(out_postings, "r")
    # temp.seek(9)
    # print(temp.readline())

    # Save dictionary
    pickle.dump(sorted_dict, open(out_dict, "wb"))
    print('done!')


''''
OLD CODE

    # Save results postings file
    output_post = open(out_postings, "w")
    for token in sorted_index_dict:
        posting_list = create_posting_lists(postings[word])
        output_post.write(posting_list + '\n')
    output_post.close()

    # Save dictionary
    pickle.dump(sorted_index_dict, open(out_dict, "wb"))
    print('done!')

'''


# def create_final_dict(dictionary):
#     sorted_dict = {}
#     start = 0
#     for termId, (key, value) in enumerate(dictionary):
#         # termId: termId, key: token, value: postings-array, (start, length): for reading posting lists using seek() function
#         doc_freq = len(value)
#         posting_str = ''
#         for file in value:
#             posting_str += str(file)
#             posting_str += ' '
#         sorted_dict[key] = (termId, doc_freq, start, len(posting_str))
#         start += len(posting_str)
#     return sorted_dict


def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])


def create_posting_lists(posting_dict):
    sorted_postings = sorted(posting_dict.items())
    posting_lists = []
    prev = 1
    for (termID, postingArr) in sorted_postings:
        posting_str = ''
        posting_str += '\n' * (termID - prev)
        posting_str += str(termID)
        posting_str += ' '
        for i in postingArr:
            posting_str += str(i)
            posting_str += ' '
        posting_lists.append((posting_str))
        prev = termID
    return posting_lists


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
