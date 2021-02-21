This is the README file for A0228375X and A0228420N's submission 
Email: e0673208@u.nus.edu AND e0673253@u.nus.edu

== Python Version ==

I'm using Python Version 3.7.4 for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general. A few paragraphs 
are usually sufficient.

= Indexing =

Firstly, we build a dictionary index for all files within the Reuters Training data. 
We process all terms by removing all punctuation marks, case-folding all words to lower case and stemming with PorterStemmer (imported from nltk.stem.porter)
Terms are stored in a set (to ensure no duplicates), and is saved in the dictionary in this format: {term: [termID, termFrequency, charOffset, stringLength]}
The dictionary is also sorted in ascending 'term' order - 'sorted_dict'
- term (string) refers to the processed and stemmed word
- termID (int) is a unique ID associated with each word after the words have all been sorted in ascending order
- termFrequency (int) is the number of unique documents each term exists in
- charOffset (int) will be initialised at the end of index.py, where these will be the pointers to access the posting list efficiently for each term
- stringLength (int) will be initialised at the end of index.py, which states the length of the posting list for that particular term

Secondly, we build the posting list index with a BSBI approach. We split files into 11 blocks before processing each block into its own individual index.
For each block, we process the words the same - removing all punctuation, case-folding to lower case and stemming. 
A dictionary 'posting_dict' is created - {termID: [array of docIDs]}. 
The posting_dict will take termIDs as a key, and the list of documentIDs the term appears in as the value.
In our algorithm, this posting_dict will be processed into a list of docID strings in the 'create_posting_lists' function
Following which, each block's posting lists will be written to separate posting list files.
After all blocks have been processed, we use line cache and write the posting lists to the final output postings file with linecache
We also update the charOffset and stringLength value for each term in the dictionary while processing these posting lists 

Lastly, we obtain the finalised output postings file consisting of all posting lists of all terms.
We also obtain the finalised dictionary where we pickle it such that we will be able to store it in memory for easy use in search.py
We also delete all unnecessary files (such as the new posting list files for each block, which are no longer necessary as they have been merged.)

= Searching =

<Please fill in>

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

> index.py
Builds the index necessary for searching - both the dictionary and postings files
> search.py
Processes a list of boolean queries and returns the search results
> postingList.py
Defines ListNode and postingList class for skip pointers
> dictionary.txt
Pickled dictionary containing a dictionary of terms and their relevant termIDs, term frequencies and pointers to each term's posting list
> postings.txt
Returns a single line of all posting documentIDs for all terms (arranged in ascending order of terms)
> README.txt
Information file for documentation

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0228375X and A0228420N, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[] I, A0228375X, did not follow the class rules regarding homework
assignment, because of the following reason:

NIL

I suggest that I should be graded as follows:

NIL

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

NIL
