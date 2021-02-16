import math
class postingList:

	# Constructor
	def __init__(self, posting=None):
		self.length = 0
		self.skip = False #Skip marker

		if posting == None:
			self.head = None #empty	
			self.tail = None #empty

		else: # create PostingList
			for doc_id in posting:
				node = ListNode(doc_id)
				self.add(node)
	# gets length
	def get_length(self):
		return self.length

	# add node at back of list
	def add(self, node):
		if self.length == 0:
			self.head = node
			self.tail = node
		else:
			self.tail.insert(node)
			self.tail = node
		self.length +=1

	# checks if posting list has added skips
	def is_skipped(self):
		return self.skip

	# calculate the skip interval between ids in the list
	def skip_interval(self):
		skip_interval = math.floor(math.sqrt(self.length))
		return skip_interval

	# get a specific node according to its index
	def get_node(self, idx):
		cur = self.head
		while idx > 0: # traversing nodes to reach specific node
			cur = cur.next
			idx -= 1
		return cur

	# sets skip pointer of first node to point to the second node
	def skip_to(self, idx1,idx2):
		node1 = self.get_node(idx1)
		node2 = self.get_node(idx2)
		node1.skip = node2

	# add skips to posting list
	def add_skips(self):
		if self.is_skipped():
			self.clear_skips() 
		else:
			cur_idx = 0 # first index
			target_idx = 0 + self.skip_interval() #second index
			while target_idx < self.length:
				self.skip_to(cur_idx, target_idx)
				cur_idx = target_idx
				target_idx += self.skip_interval()
			self.skip = True # set skip to true
		return self
	# prints posting list
	def printList(self):
		result = []
		cur = self.head
		while cur.next!=None:
			result.append(cur.doc_id)
			cur = cur.next
		result.append(self.tail.doc_id)
		print(result)
	# resets all skip markers to False
	def clear_skips(self):
		if self.skip == True:
			cur = self.head
			while cur.next!=None:
				if cur.skip!=None:
					cur.skip = None
				cur = cur.next
			self.skip = False
		return self

class ListNode: 
	# Constructor
	def __init__(self, doc_id=None): 
		self.doc_id = int(doc_id)
		self.next = None 
		self.skip = None

	# Append method
	def insert(self, node):
		self.next = node
