import math

class ListNode:
    # Initialisation
    def __init__(self, doc_id=None):
        self.doc_id = int(doc_id)
        self.next = None
        self.skip_to = None

class postingList:
    # Initialisation
    def __init__(self, postingStr=None):
        self.has_skips = False
        self.length = 0
        self.head = None
        self.tail = None

        # Populate postingList
        if postingStr != None:
            if type(postingStr) == str: # Input argument of type: string
                doc_ids = [int(i) for i in postingStr.split()]
                doc_ids.sort()
                for doc_id in doc_ids:
                    self.insert(ListNode(doc_id))
            elif type(postingStr) == list or type(postingStr) == set: # Input argument of type: list or set
                for doc_id in postingStr:
                    self.insert(ListNode(doc_id))

    # Insertion at back of list
    def insert(self, node):
        if self.head == None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1

    # Convert object to string
    def convertToString(self):
        result = ''
        cur = self.head
        while cur != None:
            result += str(cur.doc_id) + ' '
            cur = cur.next
        result = result.rstrip()
        return result

    # Gets node via search index
    def getNode(self, index):
        cur = self.head
        while index > 0:
            cur = cur.next
            index -= 1
        return cur

    # Calculates skip interval based on the postingList length
    def skipInterval(self):
        skip_interval = math.floor(math.sqrt(self.length))
        return skip_interval

    # Sets the skip pointer of node1 to node2
    def skip(self, idx1, idx2):
        node1 = self.getNode(idx1)
        node2 = self.getNode(idx2)
        node1.skip_to = node2

    # Adds skips
    def addSkips(self):
        if self.has_skips == False:
            node1 = 0
            skips = self.skipInterval()
            node2 = skips
            while node2 < self.length:
                self.skip(node1, node2)
                node1 = node2
                node2 += skips
            self.has_skips = True
        else:
            print('Posting list already added skips')
        return self
