This is the README file for A0228375X-A0228420N's submission 
Email: 
e0673208@u.nus.edu (A0228375X)
e0673253@u.nus.edu (A0228420N)

== Python Version ==

I'm using Python Version 3.7.4 for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general. A few paragraphs 
are usually sufficient.

= Indexing =

The index dictionary is built by processing terms from text files in the Reuters Training data. After removing all punctuation, case-folding all words to lower case and stemming, terms are stored in a set (to ensure no duplicates), and are saved in the dictionary, sorted by term in ascending order, with the 
following format: {term: [termID, termFrequency, charOffset, stringLength]}.

- term(string) refers to the processed and stemmed word
- termID(int) is a unique ID associated with each word after the words have all been sorted in ascending order
- termFrequency(int) is the number of unique documents each term exists in
- charOffset(int) are character offset values which point to the start of the posting list in the postings file for that term.
- stringLength(int) states the length of the posting list generated for that term.

Secondly, we build the posting list index using BSBI. We split the directory of files into 11 blocks. 
For each block, we process the tokens as what we've done in previously (removing punctuation, case-folding). A postings dictionary is created with the following format: {termID: [array of docIDs]}. We then process each array of docIds, converting them into strings prior to writing each of them to a posting file at specific
line numbers(corresponding to their termId).

After all blocks have been processed, we proceed to merge the 11 generated posting list files.
We loop through every termId and obtain the term's posting lists from every block postings file using linecache.
We merge the docIds from the block files, and write the merged posting list onto the finalised postings file.
During the merging process, charOffset and stringLength values for each term are updated in the main dictionary. 

Lastly, we save the finalised output postings file consisting of all merged posting lists.
We also save the finalised dictionary as a pickled file so that they could be easily re-loaded in memory to be used in search.py.
We also delete all unnecessary files (such as the block posting files for each block as they have already been merged).

= Searching =

The search algorithm takes in the pickled dictionary, postings file, queries file as input arguments.
The objective is to process each query and arrive at its list of docIds.

Before reading the query, we first implement the Shunting Yard algorithm to transform each query to a processable format.
After running through the algorithm, each query will be stored in an output queue, using the Reverse Polish notation as shown below.

Before: peter AND (john OR NOT jane)
After: peter john jane NOT OR AND

As shown, the algorithm ensures that the order of precedence '() -> NOT -> AND -> OR' is taken care of.

To read the query, we read the values from the output queue. Then process the following in a loop.

1. If a token is read, we use it as a key to look up the dictionary for its relevant posting list, using seek(charOffset,0) and read(stringLength). We then convert the posting list(string) into a postingList object(linked list with skip pointers). 
We then push the result back into the stack.
2. If an operator(NOT, AND, OR) is read, we pop 1 postingList(NOT) or 2 postingLists(AND, OR) from the stack 
and process them with the corresponding operator functions.
3. Push the result back into the stack.

At the end of the loop, the final result in the stack is the answer to the query, which is written to the output results file.

The basic operator functions can be described as follows:
NOT: Returns the inverse of 1 posting list by comparing the input posting list with a global posting list.
AND: Returns the intersection of 2 posting lists, where only docIds that exist in both lists are
inserted into the result posting list. Skip pointers are implemented to jump ahead redundant nodes to speed up the traversal process.
OR: Returns the union of 2 posting lists. 

To improve the speed and efficiency of the search algorithm, we added logic to optimise complex queries such as the following:
NOT NOT: If two NOTs are read, we do nothing since the inverse of the inverse gives the original posting list.
AND AND: If two ANDs are read, it means we are performing an AND operation on 3 posting lists, therefore, we can optimise the query by performing AND on the two shortest posting lists first, then perform the second AND operation on the result + longest posting list.

Complex operator functions:
AND NOT: Returns the intersection of a posting list and an inverted posting list directly, without having to process 2 separate operations (NOT, then AND).

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

> index.py
Builds the index necessary for searching - both the dictionary and postings files
> search.py
Processes a list of boolean queries and returns the search results
> postingList.py
Defines ListNode and postingList class to utilise skip pointers
> dictionary.txt
Pickled dictionary containing the keys(terms) and values(termIDs, termFrequency, charOffsets, stringLengths)
> postings.txt
Returns a single line of all posting documentIDs for all terms(arranged in ascending order of terms)
> README.txt
Information file for documentation(this)

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0228375X-A0228420N, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[] I, A0228375X-A0228420N, did not follow the class rules regarding homework
assignment, because of the following reason:

NIL

I suggest that I should be graded as follows:

NIL

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

File operations
https://www.zframez.com/tutorials/python-tutorial-file-operations.html

Using linecache to grab a specific line from a text file
https://www.geeksforgeeks.org/linecache-getline-in-python/

Using pickle to save dictionary
https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict

Theory of BSBI
https://nlp.stanford.edu/IR-book/html/htmledition/blocked-sort-based-indexing-1.html

Shunting yard algorithm
https://www.youtube.com/watch?v=Jd71l0cHZL0

Faster postings list intersection with skip pointers algorithm
https://nlp.stanford.edu/IR-book/html/htmledition/faster-postings-list-intersection-via-skip-pointers-1.html
