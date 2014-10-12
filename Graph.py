#!/usr/bin/env python
MinMax = {"MIN":0, "MAX":1}

class Graph(object):
	def __init__(self, start):
		#self.root = Node(start, MinMax["MAX"])

class Node(object):
	def __init__(self, nodeType, text, board, value):
		self.type = nodeType
		self.description = text
		self.board = board
		self.value = value
		self.children = []

	def insert(self, board):
		self.children.append(board)
