#!/usr/bin/env python
State = {"MIN":0, "MAX":1}

class Graph(object):
	def __init__(self, start):
		self.root = Node(start, State["MAX"])

class Node(object):
	def __init__(self, board, state):
		self.board = board
		self.state = state
		self.value = 0
		self.children = []

	def insert(self, board):
		self.children.append(board)
