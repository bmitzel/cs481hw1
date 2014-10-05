#!/usr/bin/env python
import os, sys, random
from enum import Enum

class Color(Enum):
	white = 1
	black = 2

class AIChessGame(object):
	def printError(self):
		print("Invalid input. Try again.\n")

	def getXY(self, prompt):
		try:
			value = int(input(prompt))
		except ValueError:
			value = 0
		while (value < 1 or value > 8):
			self.printError()
			try:
				value = int(input(prompt))
			except ValueError:
				pass
		return value

	def printBoard(self):
		self.board.draw()

	def start(self):
		print("Starting AIChessGame...\n")

		# Get the test case number
		try:
			self.testCase = int(input("Enter the test case number: "))
		except ValueError:
			self.testCase = 0
		while (self.testCase < 1 ):
			self.printError()
			try:
				self.testCase = int(input("Enter the test case number: "))
			except ValueError:
				pass
		
		# Get the starting positions for all 3 pieces: White King, White Rook, Black King
		print("\nEnter the starting positions for each piece.")
		print("Valid values for X and Y are from 1-8.")
		wkX = self.getXY("White King X: ")
		wkY = self.getXY("White King Y: ")
		wrX = self.getXY("White Rook X: ")
		wrY = self.getXY("White Rook Y: ")
		bkX = self.getXY("Black King X: ")
		bkY = self.getXY("Black King Y: ")

		# Get whether or not to use heuristicY
		useHeuristicY = input("\nUse heuristicY for the Black player (Y/N)? ").upper()[:1]
		while (useHeuristicY.upper() != "Y" and useHeuristicY.upper() != "N"):
			self.printError()
			useHeuristicY = input("Use heuristicY for the Black player (Y/N)? ").upper()[:1]
		if useHeuristicY == "Y":
			self.useHeuristicY = True
		else:
			self.useHeuristicY = False

		# Get the max number of moves for each player
		try:
			self.n = int(input("\nEnter the max number of moves per player: "))
		except ValueError:
			self.n = 0
		while (self.n < 1):
			self.printError()
			try:
				self.n = int(input("Enter the max number of moves per player: "))
			except ValueError:
				pass

		# Create and initialize the players and the chess board
		self.players = [WhitePlayer(Position(wkX, wkY), Position(wrX, wrY)),
			BlackPlayer(Position(bkX, bkY))]
		self.board = Board(self.players[0], self.players[1])
		
	def end(self):
		# Is there any cleanup to do before exiting? If not, delete this function.
		pass

class Player(object):
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
		self.pieces = [King(Color.white, kingPos), Rook(Color.white, rookPos)]

	def __str__(self):
		return "White"

	def __repr__(self):
		return self.__str__()

	# Get best move using mini-max algorithm
	def heuristicX(self):
		pass

	# Make a move for the White player
	def move(self):
		pass

class BlackPlayer(Player):
	def __init__(self, kingPos):
		self.pieces = [King(Color.black, kingPos)]

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

	# Make a move for the Black player
	def move(self):
		pass

class Piece(object):
	def __init__(self, color, position):
		self.color = color
		self.position = position

class King(Piece):
	def __str__(self):
			return "king"

	def __repr__(self):
		return self.__str__()

	def getLabel(self):
		if self.color == Color.white:
			return "w"
		else:
			return "b"

class Rook(Piece):
	def __str__(self):
		return "rook"

	def __repr__(self):
		return self.__str__()

	def getLabel(self):
		return "r"

class Position(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

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
	def __init__(self, white, black):
		self.squares = [[None for x in range(10)] for x in range(10)]
		# add white pieces to squares table
		for piece in white.pieces:
			self.squares[piece.position.x][piece.position.y] = piece
		# add black piece to squares table
		for piece in black.pieces:
			self.squares[piece.position.x][piece.position.y] = piece

	def draw(self):
		for row in range(8, 0, -1):
			print("   +---+---+---+---+---+---+---+---+")
			print(" " + str(row) + " ", end = "")
			for col in range(1, 9):
				print("| ", end = "")
				if self.squares[col][row] == None:
					print(" ", end = "")
				else:
					print(self.squares[col][row].getLabel(), end = "")
				print(" ", end = "")
			print("|")
		print("   +---+---+---+---+---+---+---+---+")
		print("     1   2   3   4   5   6   7   8")
