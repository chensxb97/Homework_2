import math

class ListNode: 
	# Initilisation
	def __init__(self, doc_id=None): 
		self.doc_id = int(doc_id)
		self.next = None 
		self.skip_to = None

class postingList:
	# Initilisation
	def __init__(self, postingStr=None):
		self.has_skips = False # whether list contains skips
		self.length = 0 # length of list
		self.head = None # first node
		self.tail = None # last node

		if postingStr != None:
			for doc_id in postingStr:
				self.insert(ListNode(doc_id)) # populate postingList

	# insertion at back of list
	def insert(self, node):
		if self.head ==None:
			self.head = node
			self.tail = node
		else:
			self.tail.next = node
			self.tail = node
		self.length +=1

	# returns length of list
	def getLength(self):
		return self.length

	# prints posting list
	def printList(self):
		cur = self.head
		while cur.next!=None:
			print(cur.doc_id)
			print('->')
			cur = cur.next
		print('None')

	# get node via search index
	def getNode(self, index):
		cur = self.head
		while index > 0:
			cur = cur.next
			index -= 1
		return cur

	# checks if posting list has added skips
	def isSkipped(self):
		return self.has_skips()
	
	# calculate skip interval
	def skipInterval(self):
		skip_interval = math.floor(math.sqrt(self.getLength()))
		return skip_interval

	# sets the skip pointer of node1 to node2
	def skip(self, idx1,idx2):
		node1 = self.getNode(idx1)
		node2 = self.getNode(idx2)
		node1.skip_to = node2

	# add skips to posting list
	def addSkips(self):
		if !self.isSkipped():
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

