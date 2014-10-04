#!/usr/bin/env python
import os, sys, random

class AIChessGame(object):
	def __init__(self):
		self.board = Board()
		self.n = 0

	def printError(self):
		print("Invalid input. Try again.\n")

	def start(self):
		# Print welcome message
		print("Starting AIChessGame...\n")
		print("Enter the starting positions for each piece.")
		print("Valid values for X and Y are from 1-8.")
		
		# Get the starting positions for all 3 pieces: White King, White Rook, Black King
		wkX = int(input("White King X: "))
		while (wkX < 1 or wkX > 8):
			self.printError()
			wkX = int(input("White King X: "))
		wkY = int(input("White King Y: "))
		while (wkY < 1 or wkY > 8):
			self.printError()
			wkY = int(input("White King Y: "))
		wrX = int(input("White Rook X: "))
		while (wrX < 1 or wrX > 8):
			self.printError()
			wrX = int(input("White Rook X: "))
		wrY = int(input("White Rook Y: "))
		while (wrY < 1 or wrY > 8):
			self.printError()
			wrY = int(input("White Rook Y: "))
		bkX = int(input("Black King X: "))
		while (bkX < 1 or bkX > 8):
			self.printError()
			bkX = int(input("Black King X: "))
		bkY = int(input("Black King Y: "))
		while (bkY < 1 or bkY > 8):
			self.printError()
			bkY = int(input("Black King Y: "))
		self.players = [WhitePlayer(Position(wkX, wkY), Position(wrX, wrY)), 
			BlackPlayer(Position(bkX, bkY))]
		
		# Get whether or not to use heuristicY
		useHeuristicY = input("Use heuristicY for the Black player (Y/N)? ").upper()
		while (useHeuristicY.upper() != "Y" and useHeuristicY.upper() != "N"):
			self.printError()
			useHeuristicY = input("Use heuristicY for the Black player (Y/N)? ").upper()
		if useHeuristicY == "Y":
			self.useHeuristicY = True
		else:
			self.useHeuristicY = False

		# Get the max number of moves for each player
		self.n = int(input("Enter the max number of moves per player: "))
		while (self.n < 1):
			self.printError()
			self.n = int(input("Enter the max number of moves per player: "))

		# DEBUG: Print the players and their pieces
		print("\n" + self.players[0] + self.players[0].pieces[0])
		print(self.players[0] + self.players[0].pieces[1])
		print(self.players[1] + self.players[1].pieces[0])

	def end(self):
		# Is there any cleanup to do before exiting? If not, delete this function.
		pass

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

class WhitePlayer(Player):
	def __init__(self, kingPos, rookPos):
		self.pieces = [King(kingPos), Rook(rookPos)]

	def __str__(self):
		return "White"

	def __repr__(self):
		return self.__str__()

	# Get best move using mini-max algorithm
	def heuristicX(self):
		pass

class BlackPlayer(Player):
	def __init__(self, kingPos):
		self.pieces = [King(kingPos)]

	def __str__(self):
		return "Black"

	def __repr__(self):
		return self.__str__()

	# Get best move using mini-max algorithm
	def heuristicY(self):
		pass

	# Get random move
	def randomY(self):
		pass

class Piece(object):
	def __init__(self, position):
		self.position = position

class King(Piece):
	def __str__(self):
		return "King at" + self.position

	def __repr__(self):
		return self.__str__()

class Rook(Piece):
	def __str__(self):
		return "Rook at" + self.position

	def __repr__(self):
		return self.__str__()

class Position(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "(" + x + ", " + y + ")"

	def __repr__(self):
		return self.__str__()

	# The following 8 functions are for returning each of the 8 squares around the current position.
	# These will be useful for determining check mate and stale mate.

	# Returns position to the top-left
	def tl(self):
		return Position(x - 1, y + 1)

	# Returns position to the top
	def t(self):
		return Position(x, y + 1)

	# Returns position to the top-right
	def tr(self):
		return Position(x + 1, y + 1)

	# Returns position to the left
	def l(self):
		return Position(x - 1, y)

	# Returns position to the right
	def r(self):
		return Position(x + 1, y)

	# Returns position to the bottom-left
	def bl(self):
		return Position(x - 1, y - 1)

	# Returns position to the bottom
	def b(self):
		return Position(x, y - 1)

	# Returns position to the bottom-right
	def br(self):
		return Position(x + 1, y - 1)

class Board(object):
	def __init__(self):
		pass
		
		# 0-10, squares 0 and 9 are used for underAttack calculations. 
		# Board is limited 1-8

		# self.board = [[(x,y) for x in xrange(1,9)] for y in xrange(1,9)]
		# self.white = white
		# self.black = black
		# black.rook = Piece('r', (8,5), black)
		# black.king = Piece('k', (6,8), black)
		# white.king = Piece('k', (5,6), white)

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

	# def boardState(self):
	# 	print self.board[7]
	# 	print self.board[6]
	# 	print self.board[5]
	# 	print self.board[4]
	# 	print self.board[3]
	# 	print self.board[2]
	# 	print self.board[1]
	# 	print self.board[0]

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
