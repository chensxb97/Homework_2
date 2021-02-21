#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import math
import pickle
import os
from nltk.stem.porter import PorterStemmer
from postingList import postingList, ListNode

# python3 search.py -d dictionary.txt -p postings.txt  -q queries.txt -o results.txt


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
    # print(sorted_dict)

    # Global postingList
    globalPostingList = postingList(list(range(1, number_of_terms))).addSkips()

    # posting lists
    postings = open(postings_file, 'r')

    # queries
    queries = open(queries_file, 'r')

    # implement shunting-yard algorithm in increasing order of precedence - OR least impt
    operators = ['OR', 'AND', 'NOT']
    i = 1
    results_array = []
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
        # print('Queue: ', queue)
        # print('Stack: ', stack)

        # process query (postingListClass IMPLEMENTATION)
        for item in queue:
            if item not in operators:
                # convert items to corresponding postingLists
                stack.append(processItem(item, sorted_dict, postings))
            elif item == 'NOT':
                list1 = stack.pop()
                stack.append(NOT(list1, globalPostingList))  # NOT
            elif item == 'OR' or item == 'AND':
                list1 = stack.pop()
                list2 = stack.pop()
                if item == 'OR':
                    stack.append(OR(list1, list2))  # OR
                else:
                    stack.append(AND(list1, list2))  # AND
        i += 1
        # Convert postingLists to strings for output
        results_array.append(stack[0].convertToString())

    # Write results into given results_file
    with open(results_file, 'w') as results_file:
        for r in results_array:
            results_file.write(r + '\n')

    # extract postingList from dictionary


def processItem(item, sorted_dict, postings):
    if item == None:
        print('Item is empty')
        return None
    else:
        if item in sorted_dict.keys():
            postings.seek(sorted_dict[item][2], 0)
            posting_str = (postings.read(sorted_dict[item][3]))
            posting_l = postingList(posting_str).addSkips()
    return posting_l


def NOT(list1, globalPostingList):
    result = postingList()
    cur1 = list1.head
    curGlobal = globalPostingList.head
    while cur1 != None:
        # traverse global list if the global ids are less than list id
        while cur1 != None and curGlobal.doc_id < cur1.doc_id:
            result.insert(ListNode(curGlobal.doc_id))
            curGlobal = curGlobal.next
        # Insert ids if ids are not the same
        if curGlobal.doc_id != cur1.doc_id:
            result.insert(ListNode(curGlobal.doc_id))
        # Do nothing if ids are the same
        curGlobal = curGlobal.next
        cur1 = cur1.next
    # traverse the remaining elements of the global list
    while curGlobal != None:
        result.insert(ListNode(curGlobal.doc_id))
        curGlobal = curGlobal.next
    return result.addSkips()


def AND(list1, list2):
    result = postingList()
    cur1 = list1.head
    cur2 = list2.head
    while cur1 != None and cur2 != None:
        # skip to next node if the id of skipped node is less than the id of the compared node
        while cur1.skip_to != None and cur1.skip_to.doc_id < cur2.doc_id and cur1.doc_id != cur2.doc_id:
            cur1 = cur1.skip_to
        while cur2.skip_to != None and cur2.skip_to.doc_id < cur1.doc_id and cur1.doc_id != cur2.doc_id:
            cur2 = cur2.skip_to
        # insert ids if they are the same
        if cur1.doc_id == cur2.doc_id:
            result.insert(ListNode(cur1.doc_id))
            cur1 = cur1.next
            cur2 = cur2.next
        # traversal
        elif cur1.doc_id < cur2.doc_id:
            cur1 = cur1.next
        else:
            cur2 = cur2.next
    return result.addSkips()


def OR(list1, list2):
    result = postingList()
    cur1 = list1.head
    cur2 = list2.head
    while cur1 != None and cur2 != None:
        # insert id if ids are the same
        if cur1.doc_id == cur2.doc_id:
            result.insert(ListNode(cur1.doc_id))
            cur1 = cur1.next
            cur2 = cur2.next
        else:
            # traverse through the first list if the doc-ids are less than the second list's second doc-id
            while cur1 != None and cur2 != None and cur1.doc_id < cur2.doc_id:
                result.insert(ListNode(cur1.doc_id))
                cur1 = cur1.next
            while cur2 != None and cur1 != None and cur2.doc_id < cur1.doc_id:
                result.insert(ListNode(cur2.doc_id))
                cur2 = cur2.next

    # traverse the remaining elements of the other list
    if cur1 == None:
        while cur2 != None:
            result.insert(ListNode(cur2.doc_id))
            cur2 = cur2.next
    if cur2 == None:
        while cur1 != None:
            result.insert(ListNode(cur1.doc_id))
            cur1 = cur1.next
    return result.addSkips()


'''
        # process query (SET IMPLEMENTATION)
        for item in queue:
            # obtain posting lists from tokens
            if item not in operators:
                stack.append(item)
            elif item == 'OR':
                item1 = stack.pop()
                item2 = stack.pop()
                tokenSet1 = turnIntoSet(item1, sorted_dict, postings)
                tokenSet2 = turnIntoSet(item2, sorted_dict, postings)
                stack.append(OR(tokenSet1, tokenSet2))
            elif item == 'AND':
                item1 = stack.pop()
                item2 = stack.pop()
                tokenSet1 = turnIntoSet(item1, sorted_dict, postings)
                tokenSet2 = turnIntoSet(item2, sorted_dict, postings)
                stack.append(AND(tokenSet1, tokenSet2))
            elif item == 'NOT':
                item1 = stack.pop()
                tokenSet1 = turnIntoSet(item1, sorted_dict, postings)
                stack.append(NOT(tokenSet1, globalSet))
        i += 1
        print('Final Stack: ', sorted(stack[0]))

def turnIntoSet(item, sorted_dict, postings):
    if type(item) is not set:
        if item in sorted_dict.keys():
            postings.seek(sorted_dict[item][2], 0)
            tokenSet = set(postings.read(
                sorted_dict[item][3]).split())
            tokenSet = set(int(token) for token in tokenSet)
        else:
            tokenSet = set()
    else:
        tokenSet = item
    return tokenSet

def NOT(tokenSet1, globalSet):
    return (globalSet - tokenSet1)

def AND(tokenSet1, tokenSet2):
    return tokenSet1 & tokenSet2

def OR(tokenSet1, tokenSet2):
    return tokenSet1 | tokenSet2
'''

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
