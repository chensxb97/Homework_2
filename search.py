#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import math
import pickle
import os
from postingList import postingList

# python search.py -d dictionary.txt -p postings.txt  -q queries.txt -o results.txt

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # This is an empty method
    # Pls implement your code in below

    # dictionary
    in_dict = open(dict_file,'rb')
    sorted_dict = pickle.load(in_dict)
    #print(sorted_dict)

    # queries
    queries = open(queries_file,'r')

    # implement shunting-yard algorithm
    operators = ['OR','AND','NOT']
    i = 1
    for q in queries:
        stack = [] # output stack
        queue = [] # output queue
        values = q.split()
        print('Processing query {}'.format(i))
        for val in values:
            if val not in operators and '(' not in val and ')' not in val:
                queue.append(val) # queue tokens
            elif val =='NOT': 
                stack.append(val) # push 'NOT' to stack
            elif val =='AND' or val =='OR':
                while (len(stack)!=0 and stack[-1] !='(' and (operators.index(val)<operators.index(stack[-1])
                    or operators.index(val) == operators.index(stack[-1]))):
                    queue.append(stack.pop()) # pop operators with greater precedence from stack into queue
                else:
                    stack.append(val) # push the operator to stack
            elif '(' in val:
                queue.append(val[1:]) # queue token
                stack.append(val[0]) # push paranthesis to stack
            elif ')' in val:
                queue.append(val[:-1]) # queue token
                while stack[-1]!='(':
                    queue.append(stack.pop())
                stack.pop() # remove left paranthesis
                # do not push right parantheseis to stack

        while len(stack)>0:
            queue.append(stack.pop()) # queue now contains tokens and operands in the right order 
        print('Queue: ',queue)
        print('Stack: ', stack)

        # process query
        for item in queue:
            # obtain posting lists from tokens
            if item not in operators:
                pass # continue from here
def OR():
    pass
def NOT():
    pass
def AND():
    pass


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)


run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
