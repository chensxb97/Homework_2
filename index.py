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
from os.path import join,isfile
from nltk.stem.porter import PorterStemmer

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below

    #Initialisation
    list_punc = list(string.punctuation)
    stemmer = PorterStemmer()
    index_dict = {}
    postings = {}
    files = [f for f in listdir(in_dir) if isfile(join(in_dir,f))]
    sorted_files = sorted(files,key=lambda f: int(os.path.splitext(f)[0]))
    
    #Word_processing and tokenisation for each file
    for file in sorted_files:
    	file_path = join(in_dir,file)
    	f = open(file_path,"r")
    	tokens = []
    	for line in f:
    		new_line = ''
    		for c in line:
    			if c not in list_punc:
    				new_line+=c
    		new_line = new_line.lower()
    		for words in nltk.sent_tokenize(new_line):
    			for word in nltk.word_tokenize(words):
    				word = stemmer.stem(word)
    				tokens.append(word)
    	for t in tokens:
    		if t not in index_dict:
    			index_dict[t] = 1
    			postings[t] = [int(file)]
    		else:
    			doc_id = int(file)
    			if doc_id not in postings[t]:
    				index_dict[t]+=1
    				postings[t].append(int(file))
    #Save results to output dictionary and postings files
    output_post = open(output_file_postings,"w")
    for token in postings:
    	(posting, startPos, endPos) = add_skips(postings[token])
    	output_post.write(posting+ '\n')
    	doc_frequency = index_dict[token]
    	index_dict[token] = (doc_frequency,startPos,endPos)
    output_post.close()
    pickle.dump(index_dict,open(output_file_dictionary,"wb"))

def add_skips(posting):
	posting_list =[str(i) for i in list(posting)]
	print('Processing posting: ', posting_list)
	interval = math.floor(math.sqrt(len(posting_list)))
	print('Interval: ',interval)
	posting = ''
	i = 1
	for p in posting_list:
		if interval>0 and i%interval ==0 and i!=1:
			posting+='*{} '.format(interval)
		posting+=p
		posting+=' '
		i+=1
	return (posting, posting_list[0], posting_list[-1])

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
