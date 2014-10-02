#!/usr/bin/env python
import os, sys, random

class Player(object):

	def __init__(self, color):
		self.color = color

	def getPieces(self, board):
		return [pos for pos in board if board[pos].color is self.color]

	def isCheckmate():
		return False

	def underAttack(self, position, playerBlack, playerWhite):
		return 1
	
	def isCheckMate(self, board):
		return True

	def isChecked(self, board):
		return True

	def move(self, board, start, end):
		return 0

	def legalMoves(self, board, start, end):

		return 0

	def checkRook(self, start, end):
		return True

	def rookMoves(self, start, end):
		return True

	def kingMoves(self, start, end):
		return True

	def getMove(self, board):
		return True


class Board():
	def __init__(self, black, white):
		
		# 0-10, squares 0 and 9 are used for underAttack calculations. 
		# Board is limited 1-8

		self.board = [[(x,y) for x in xrange(1,9)] for y in xrange(1,9)]
		self.white = white
		self.black = black
		black.rook = Piece('r', (8,5), black)
		black.king = Piece('k', (6,8), black)
		white.king = Piece('k', (5,6), white)


		#8 = 	56 57 58 59 60 61 62 63  |8
		#7 = 	48 49 50 51 52 53 55 55  |7
		#6 = 	40 41 42 43 44 45 46 47  |6
		#5 = 	32 33 34 35 36 37 38 39  |5
		#4 = 	24 25 26 27 28 29 30 31  |4
		#3 = 	16 17 18 19 20 21 22 23  |3
		#2 = 	8  9  10 11 12 13 14 15  |2
		#1 = 	0  1   2  3  4  5  6  7  |1 
		#line	--------------------------
		#0 =    A   B  C  D  E  F  G  H  0


	def boardState(self):
		print self.board[7]
		print self.board[6]
		print self.board[5]
		print self.board[4]
		print self.board[3]
		print self.board[2]
		print self.board[1]
		print self.board[0]


class Piece(object):

	def __init__(self, pieceName, position, player):

		self.color = player.color
		self.position = position
		self.pieceName = pieceName


	def __str__(self):
		return self.color + " " + self.pieceName

	def __repr__(self):
		return self.__str__()



class Play(object):

	def __init__(self, black, white):
		#self.board = dict()
		self.board = Board(black, white)

		#self.board = [((8,5), Piece('R', (8,5), black)), ((6,8), Piece('K', (6,8), black)), ((5,6), Piece('K', (5,6), white))]
		#self.board = [((6,8), Piece('King', (6,8), black))]
		#self.board = [((5,6), Piece('King', (5,6), white))]


	def run(self, player):
		return True

	def printBoard(self):
		self.board.boardState()

if __name__ == "__main__":
	#w = {5,6}
	#b = {6,8}
	#r = {8,5}
	white = Player('white')
	black = Player('black')
	#white.getPieces()
	newGame = Play(black, white)
	newGame.printBoard()
	#newGame.run(black)

	w, b, r = Piece('king', (5,6), white), Piece('king', (6,8), black), Piece('rook', (8,5), black)

	my_board = Board(white, black)
	#my_board.printBoard()

#	w.printPosition()

	#my_board.moveWhite()

