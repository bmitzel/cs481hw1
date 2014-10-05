#!/usr/bin/env python
import os, sys, random
from enum import Enum

class Color(Enum):
	white = 1
	black = 2

class AIChessGame(object):
	def __init__(self):
		self.n = 0

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

	def start(self):
		# Print welcome message
		print("Starting AIChessGame...\n")
		print("Enter the starting positions for each piece.")
		print("Valid values for X and Y are from 1-8.")
		
		# Get the starting positions for all 3 pieces: White King, White Rook, Black King
		wkX = self.getXY("White King X: ")
		wkY = self.getXY("White King Y: ")
		wrX = self.getXY("White Rook X: ")
		wrY = self.getXY("White Rook Y: ")
		bkX = self.getXY("Black King X: ")
		bkY = self.getXY("Black King Y: ")

		# Get whether or not to use heuristicY
		useHeuristicY = input("Use heuristicY for the Black player (Y/N)? ").upper()[:1]
		while (useHeuristicY.upper() != "Y" and useHeuristicY.upper() != "N"):
			self.printError()
			useHeuristicY = input("Use heuristicY for the Black player (Y/N)? ").upper()[:1]
		if useHeuristicY == "Y":
			self.useHeuristicY = True
		else:
			self.useHeuristicY = False

		# Get the max number of moves for each player
		try:
			self.n = int(input("Enter the max number of moves per player: "))
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
		
		# DEBUG: Print the players and their pieces
		print("\n" + str(self.players[0]) + " " + str(self.players[0].pieces[0]) + " at " + str(self.players[0].pieces[0].position))
		print(str(self.players[0]) + " " + str(self.players[0].pieces[1]) + " at " + str(self.players[0].pieces[1].position))
		print(str(self.players[1]) + " " + str(self.players[1].pieces[0]) + " at " + str(self.players[1].pieces[0].position))

		# DEBUG: Draw the chess board
		print("\n")
		self.board.draw()

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

class Piece(object):
	def __init__(self, color, position):
		self.color = color
		self.position = position

class King(Piece):
	def __str__(self):
			return "King"

	def __repr__(self):
		return self.__str__()

class Rook(Piece):
	def __str__(self):
		return "Rook"

	def __repr__(self):
		return self.__str__()

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
			print("   +----+----+----+----+----+----+----+----+")
			print(" " + str(row) + " ", end = "")
			for col in range(1, 9):
				print("| ", end = "")
				if self.squares[col][row] == None:
					print("  ", end = "")
				elif self.squares[col][row].color == Color.white:
					if str(self.squares[col][row]) == "King":
						print("WK", end = "")
					else:
						print("WR", end = "")
					#print("| " + self.squares[row][col].label + " ")
				else:
					print("BK", end = "")
				print(" ", end = "")
			print("|")
		print("   +----+----+----+----+----+----+----+----+")
		print("     1    2    3    4    5    6    7    8")
		
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
