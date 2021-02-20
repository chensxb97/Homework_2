#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import math
import pickle
import os
from nltk.stem.porter import PorterStemmer
from postingList import postingList

# python search.py -d dictionary.txt -p postings.txt  -q queries.txt -o results.txt


def usage():
    print("usage: " +
          sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")


def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # Initialise stemmer
    stemmer = PorterStemmer()

    # dictionary
    in_dict = open(dict_file, 'rb')
    sorted_dict = pickle.load(in_dict)
    number_of_terms = len(sorted_dict.keys())
    globalSet = set(range(1, number_of_terms))
    # print(sorted_dict)

    # posting lists
    postings = open(postings_file, 'r')

    # queries
    queries = open(queries_file, 'r')

    # implement shunting-yard algorithm in increasing order of precedence - OR least impt
    operators = ['OR', 'AND', 'NOT']
    i = 1
    for q in queries:
        stack = []  # output stack
        queue = []  # output queue
        values = q.split()
        print('Processing query {}'.format(i))
        for val in values:
            if val not in operators and '(' not in val and ')' not in val:
                # Tokens will be processed to lower case and stemmed for comparision with dictionary
                val = val.lower()
                val = stemmer.stem(val)
                queue.append(val)  # queue tokens
            elif val == 'NOT':
                stack.append(val)  # push 'NOT' to stack
            elif val == 'AND' or val == 'OR':
                while (len(stack) != 0 and stack[-1] != '(' and (operators.index(val) < operators.index(stack[-1])
                                                                 or operators.index(val) == operators.index(stack[-1]))):
                    # pop operators with greater precedence from stack into queue
                    queue.append(stack.pop())
                else:
                    stack.append(val)  # push the operator to stack
            elif '(' in val:
                queue.append(val[1:])  # queue token
                stack.append(val[0])  # push paranthesis to stack
            elif ')' in val:
                queue.append(val[:-1])  # queue token
                while stack[-1] != '(':
                    queue.append(stack.pop())
                stack.pop()  # remove left paranthesis
                # do not push right parantheseis to stack

        while len(stack) > 0:
            # queue now contains tokens and operands in the right order
            queue.append(stack.pop())
        print('Queue: ', queue)
        print('Stack: ', stack)

        # process query (STACK IMPLEMENTATION FIRST)
        for item in queue:
            # obtain posting lists from tokens
            if item not in operators:
                stack.append(item)
            elif item == 'OR':
                item1 = stack.pop()
                item2 = stack.pop()
                if type(item1) is not set:
                    if item1 in sorted_dict.keys():
                        postings.seek(sorted_dict[item1][2], 0)
                        tokenSet1 = set(postings.read(sorted_dict[item1][3]))
                    else:
                        tokenSet1 = set()
                if type(item2) is not set:
                    if item2 in sorted_dict.keys():
                        postings.seek(sorted_dict[item2][2], 0)
                        tokenSet2 = set(postings.read(sorted_dict[item2][3]))
                    else:
                        tokenSet2 = set()
                stack.append(OR(tokenSet1, tokenSet2))
            elif item == 'AND':
                item1 = stack.pop()
                item2 = stack.pop()
                if type(item1) is not set:
                    if item1 in sorted_dict.keys():
                        postings.seek(sorted_dict[item1][2], 0)
                        tokenSet1 = set(postings.read(
                            sorted_dict[item1][3]).split())
                    else:
                        tokenSet1 = set()
                if type(item2) is not set:
                    if item2 in sorted_dict.keys():
                        postings.seek(sorted_dict[item2][2], 0)
                        tokenSet2 = set(postings.read(
                            sorted_dict[item2][3]).split())
                    else:
                        tokenSet2 = set()
                stack.append(AND(tokenSet1, tokenSet2))
            elif item == 'NOT':
                item1 = stack.pop()
                if type(item1) is not set:
                    if item1 in sorted_dict.keys():
                        postings.seek(sorted_dict[item1][2], 0)
                        tokenSet1 = set(postings.read(
                            sorted_dict[item1][3]).split())
                    else:
                        tokenSet1 = set()
                stack.append(NOT(tokenSet1, globalSet))
        print('Final Stack: ', stack)


def OR(tokenSet1, tokenSet2):
    return tokenSet1 | tokenSet2


def NOT(tokenSet1, globalSet):
    return globalSet - tokenSet1


def AND(tokenSet1, tokenSet2):
    return tokenSet1 & tokenSet2


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None:
    usage()
    sys.exit(2)


run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
