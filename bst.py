#binary tree
import Assign1

class Node:
	left, right, data = None, None, 0
	def __init__(self, data):
		self.left = None
		self.right = None
		self.data = data 

class BTree:
	def __init__(self):
		self.root = None


	def addNode(self, data):
		return Node(data)

	def insert(self, root, data):
		if root == None:
			#Inserts at root if no data.
			return self.addNode(data)
		else:
			if data <= root.data:
				root.left = self.insert(root.left, data)
			else:
				root.right = self.insert(root.right,data)
			return root

	def query(self, root, target):
		if root == None:
			return 0
		else:
			if target == root.data:
				return 1
			else:
				if target < root.data:
					return self.query(root.left, target)
				else:
					return self.query(root.right, target)

	def minValue(self, root):
		while(root.left != None):
			root = root.left
		return root.data

	def maxDepth(self, root):
		if root == None:
			return 0
		else: 
			ldepth = self.maxDepth(root.left)
			rdepth = self.maxDepth(root.right)
			return max(ldepth, rdepth) + 1

	def size(self, root):
		if root == None:
			return 0;
		else:
			return self.size(root.left) + 1 + self.size(root.right)

	def printTree(self, root):
		if root == None:
			pass
		else:
			self.printTree(root.left)
			print(root.data),
			self.printTree(root.right)

if __name__ == "__main__":
	#create binary tree
	BTree = BTree()
	root = BTree.addNode(10)

	for i in range(0,5):
		data = int(raw_input("insert the node value nr %d: " % i))
		BTree.insert(root, data)
	print

	BTree.printTree(root)
	print

	data = int(raw_input("Insert a value to find: "))
	if BTree.query(root,data):
		print "found"
	else:
		print "not found"

	print "MV: " , BTree.minValue(root)
	print "MD: " , BTree.maxDepth(root)
	print "SZ: " , BTree.size(root)
