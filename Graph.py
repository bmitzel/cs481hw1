#!/usr/bin/env python
class Graph(object):
	def __init__(self, previousPlayer, startingBoardState):
		self.root = Node(previousPlayer, 0, startingBoardState)

class Node(object):
	def __init__(self, playerColor, level, board):
		self.activePlayer = playerColor
		self.depth = level
		self.board = board
		self.value = 0
		self.children = []
