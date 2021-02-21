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
    using the input dict_file and postings_file,
    perform searching on the given queries_file and output the results to results_file
    """
    print('running search on the queries...')

    # Initialise stemmer
    stemmer = PorterStemmer()

    # Open and load dictionary
    in_dict = open(dict_file, 'rb')
    sorted_dict = pickle.load(in_dict)
    number_of_terms = len(sorted_dict.keys())

    # Create global postingList with all termIDs [1, 2, 3 ..., number_of_terms]
    globalPostingList = postingList(list(range(1, number_of_terms))).addSkips()

    # Open posting lists, but not loaded into memory
    postings = open(postings_file, 'r')

    # Open queries file
    queries = open(queries_file, 'r')

    # Implement shunting-yard algorithm in increasing order of precedence - OR least precedence, followed by AND, then NOT
    operators = ['OR', 'AND', 'NOT']
    results_array = []
    for i, q in enumerate(queries):
        stack = []  # Output stack
        queue = []  # Output queue
        values = q.split()
        print('Processing query {}'.format(i+1))
        for val in values:
            if val not in operators and '(' not in val and ')' not in val:
                # Tokens will be processed to lower case and stemmed for comparision with dictionary
                val = val.lower()
                val = stemmer.stem(val)
                queue.append(val)  # Queue tokens
            elif val == 'NOT':
                stack.append(val)  # Push 'NOT' to stack
            elif val == 'AND' or val == 'OR':
                while (len(stack) != 0 and stack[-1] != '(' and (operators.index(val) < operators.index(stack[-1])
                                                                 or operators.index(val) == operators.index(stack[-1]))):
                    # Pop operators with greater precedence from stack into queue
                    queue.append(stack.pop())
                else:
                    stack.append(val)  # Push the operator to stack
            elif '(' in val:
                queue.append(val[1:])  # Queue token to the right of '('
                stack.append(val[0])  # Push paranthesis to stack
            elif ')' in val:
                queue.append(val[:-1])  # Queue token to the left of ')'
                while stack[-1] != '(':
                    queue.append(stack.pop())
                stack.pop()  # Remove left paranthesis
                # Do not push right parantheseis to stack

        while len(stack) > 0:
            # Pop all values from stack into queue
            # Queue now contains tokens and operands in the right order
            queue.append(stack.pop())

        # Process query in queue
        for item in queue:
            if item not in operators:
                # Extract posting lists and store them as 'postingList' objects
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
        # Convert postingLists to strings for output
        results_array.append(stack[0].convertToString())

    # Write results into given results_file
    with open(results_file, 'w') as results_file:
        for r in results_array:
            results_file.write(r + '\n')


def processItem(item, sorted_dict, postings):
    """
    Given a term, construct the term's postingList using dictionary in memory
    """
    if item == None:
        print('Item is empty')
        return None
    else:
        if item in sorted_dict.keys():
            postings.seek(sorted_dict[item][2], 0)
            posting_str = (postings.read(sorted_dict[item][3]))
            posting_l = postingList(posting_str).addSkips()
        else:
            posting_l = postingList(None)
    return posting_l


def NOT(list1, globalPostingList):
    """
    Given postingList1, return a postingList of all docIDs not found in postingList1
    """
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
    """
    Return intersection of postingList1 and postingList2 as a postingList
    """
    result = postingList()
    cur1 = list1.head
    cur2 = list2.head
    while cur1 != None and cur2 != None:
        # Skip to next node if the id of skipped node is less than the id of the compared node
        while cur1.skip_to != None and cur1.skip_to.doc_id < cur2.doc_id and cur1.doc_id != cur2.doc_id:
            cur1 = cur1.skip_to
        while cur2.skip_to != None and cur2.skip_to.doc_id < cur1.doc_id and cur1.doc_id != cur2.doc_id:
            cur2 = cur2.skip_to
        # Insert ids if they are the same
        if cur1.doc_id == cur2.doc_id:
            result.insert(ListNode(cur1.doc_id))
            cur1 = cur1.next
            cur2 = cur2.next
        # Traverse through the first list if id of first list is less than that of the second
        elif cur1.doc_id < cur2.doc_id:
            cur1 = cur1.next
        else:
            cur2 = cur2.next
    return result.addSkips()


def OR(list1, list2):
    """
    Return union of postingList1 and postingList2 as a postingList
    """
    result = postingList()
    cur1 = list1.head
    cur2 = list2.head
    while cur1 != None and cur2 != None:
        # Insert id if ids are the same
        if cur1.doc_id == cur2.doc_id:
            result.insert(ListNode(cur1.doc_id))
            cur1 = cur1.next
            cur2 = cur2.next
        else:
            # Traverse through the first list if the doc-ids are less than the second list's second doc-id
            while cur1 != None and cur2 != None and cur1.doc_id < cur2.doc_id:
                result.insert(ListNode(cur1.doc_id))
                cur1 = cur1.next
            while cur2 != None and cur1 != None and cur2.doc_id < cur1.doc_id:
                result.insert(ListNode(cur2.doc_id))
                cur2 = cur2.next

    # Traverse the remaining elements of the other list
    if cur1 == None:
        while cur2 != None:
            result.insert(ListNode(cur2.doc_id))
            cur2 = cur2.next
    if cur2 == None:
        while cur1 != None:
            result.insert(ListNode(cur1.doc_id))
            cur1 = cur1.next
    return result.addSkips()


# For terminal commands and I/O handling
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
