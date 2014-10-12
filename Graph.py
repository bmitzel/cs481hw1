#!/usr/bin/env python
MinMax = {"MIN":0, "MAX":1}

class Graph(object):
	def __init__(self, startingBoardState):
		self.root = Node(MinMax["MIN"], 0, startingBoardState)

class Node(object):
	def __init__(self, nodeType, level, board):
		self.type = nodeType
		self.depth = level
		self.board = board
		self.value = 0
		self.children = []
