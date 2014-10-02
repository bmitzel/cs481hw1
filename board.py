#!/usr/bin/env python
import os, sys, random

class Board(object):
	axis_y = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
	axis_x = tuple(range(1,9)) 

	def __init__(self, black, white):
		self.board = [(x, y) for x in range(1,9) for y in range(1, 9)]
		
	
	def printBoard(self):
		print(self.board)
		return self.board

	def moveWhite(self, position, role):
		
		direction = str(raw_input("Choose Direction (U, D, L, R): "))
		if direction == "U" or direction == "u":
			space = int(raw_input("Choose spaces to move (1-8): "))
			print "Current Position: (" , axis_x , "," , axis_y , ")"

		if direction == "D" or direction == "d":
			space = int(raw_input("Choose spaces to move (1-8): "))

		if direction == "L" or direction == "l":
			space = int(raw_input("Choose spaces to move (1-8): "))

		if direction == "R" or direction == "r":	
			space = int(raw_input("Choose spaces to move (1-8): "))

		return 0

	def moveBlack(self, position, role):
		if role == "rook":
			return 0
		return 0

	def play(self):

		return 0

class Piece(object):

	def __init__(self, role, position, player):
		self.role = role
		self.position = position
		self.color = player.color


class Player(object):

	def __init__(self, color):
		self.color = color
		self.pieces = pieces


	def getPieces(self, board):
		


	def isCheckmate():
		return false


class Play(object):

	def __init__(self, playerBlack, playerWhite):
		self.board = dict()






if __name__ == "__main__":
	my_board = Board()

	my_board.printBoard()

