#!/usr/bin/env python
import os, sys, random
from Graph import Graph

Color = {"White":0, "Black":1}

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
		self.board = Board(self.players[0].pieces, self.players[1].pieces)
		
	def end(self):
		# Is there any cleanup to do before exiting? If not, delete this function.
		pass

class Player(object):
	def getPieces(self, board):
		return [pos for pos in board if board[pos].color is self.color]

	def isCheckmate():
		return False

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
		self.pieces = [King(Color["White"], kingPos), Rook(Color["White"], rookPos)]

	def __str__(self):
		return "White"

	def __repr__(self):
		return self.__str__()

	# Get best move using mini-max algorithm
	def heuristicX(self, game):
		graph = Graph(game.board)
		moves = []
		for piece in self.pieces:
			moves.extend(piece.getLegalMoves(game.board))
		graph.root.insert(moves)

	# Make a move for the White player
	def move(self, game):
		# Get the new board from heuristicX and update the player's pieces
		self.heuristicX(game)

class BlackPlayer(Player):
	def __init__(self, kingPos):
		self.pieces = [King(Color["Black"], kingPos)]

	def __str__(self):
		return "Black"

	def __repr__(self):
		return self.__str__()

	# Get best move using mini-max algorithm
	def heuristicY(self, game):
		pass

	# Get random move
	def randomY(self, game):
		moves = []
		for piece in self.pieces:
			moves.extend(piece.getLegalMoves(game.board))

	# Make a move for the Black player
	def move(self, game):
		# Get the new board from heuristicY or randomY and update the player's pieces
		self.randomY(game)

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
		if self.color == Color["White"]:
			return "w"
		else:
			return "b"

	# Returns a list of boards corresponding to all the legal moves for the king
	# Keep in mind that the king cannot move into check
	def getLegalMoves(self, board):
		moves = []
		attacked = board.underAttack((int(self.color) + 1) % 2)
		for y in range(max(1, self.position.y + 1), min(8, self.position.y - 2), -1):
			for x in range(max(1, self.position.x - 1), min(8, self.position.x + 2)):
				if (self.position != Position(x, y)) and (Position(x, y) not in attacked):
					if self.color == Color["White"]:
						print("White ", end = "")
					else:
						print("Black ", end = "")
					print(str(self) + " to " + str(Position(x, y)))
					newMove = Move(self, Position(x, y))
					newBoard = board.move(newMove)
					moves.append(newBoard)
					newBoard.draw()
		return moves

class Rook(Piece):
	def __str__(self):
		return "rook"

	def __repr__(self):
		return self.__str__()

	def getLabel(self):
		return "r"

	# Returns a list of boards corresponding to all the legal moves for the rook
	def getLegalMoves(self, board):
		moves = []
		# Vertical moves
		for y in range(1, 9):
			if (self.position != Position(self.position.x, y)):
				print("White " + str(self) + " to " + str(Position(self.position.x, y)))
				newMove = Move(self, Position(self.position.x, y))
				newBoard = board.move(newMove)
				moves.append(newBoard)
				newBoard.draw()
		# Horizontal moves
		for x in range(1, 9):
			if (self.position != Position(x, self.position.y)):
				print("White " + str(self) + " to " + str(Position(x, self.position.y)))
				newMove = Move(self, Position(x, self.position.y))
				newBoard = board.move(newMove)
				moves.append(newBoard)
				newBoard.draw()
		return moves

class Position(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return (self.x == other.x) and (self.y == other.y)

	# The following 8 functions are for returning each of the 8 squares around the current position.
	# These will be useful for determining check mate and stale mate.

	# Returns position to the top-left
	def tl(self):
		return Position(self.x - 1, self.y + 1)

	# Returns position to the top
	def t(self):
		return Position(self.x, self.y + 1)

	# Returns position to the top-right
	def tr(self):
		return Position(self.x + 1, self.y + 1)

	# Returns position to the left
	def l(self):
		return Position(self.x - 1, self.y)

	# Returns position to the right
	def r(self):
		return Position(self.x + 1, self.y)

	# Returns position to the bottom-left
	def bl(self):
		return Position(self.x - 1, self.y - 1)

	# Returns position to the bottom
	def b(self):
		return Position(self.x, self.y - 1)

	# Returns position to the bottom-right
	def br(self):
		return Position(self.x + 1, self.y - 1)

class Move(object):
	def __init__(self, piece, position):
		self.piece = piece
		self.position = position

class Board(object):
	def __init__(self, whitePieces, blackPieces):
		self.pieces = whitePieces + blackPieces
		self.squares = [[None for x in range(10)] for x in range(10)]
		# add pieces to squares table
		for piece in self.pieces:
			self.squares[piece.position.x][piece.position.y] = piece
		self.calcWhiteAttacks(self.pieces)
		self.calcBlackAttacks(self.pieces)

	def calcWhiteAttacks(self, white):
		self.whiteAttacks = []
		for piece in self.pieces:
			if piece.color == Color["White"]:
				if str(piece) == "king":
					self.whiteAttacks.extend(
						[piece.position.tl(), piece.position.t(), piece.position.tr(),
						piece.position.l(), piece.position.r(),
						piece.position.bl(), piece.position.b(), piece.position.br()])
				else:
					for x in range(10):
						if x != piece.position.x:
							self.whiteAttacks.append(Position(x, piece.position.y))
					for y in range(10):
						if y != piece.position.y:
							self.whiteAttacks.append(Position(piece.position.x, y))

	def calcBlackAttacks(self, black):
		for piece in self.pieces:
			if piece.color == Color["Black"]:
				self.blackAttacks = [piece.position.tl(), piece.position.t(), piece.position.tr(),
					piece.position.l(), piece.position.r(),
					piece.position.bl(), piece.position.b(), piece.position.br()]

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
		wait = input("...Paused...")

	# This function is for debugging only; prints all the pieces currently on the board
	def printPieces(self):
		for piece in self.pieces:
			if piece.color == Color["White"]:
				print("White ", end = "")
			else:
				print("Black ", end = "")
			print(str(piece) + " at " + str(piece.position))

	def underAttack(self, color):
		if color == Color["White"]:
			return self.whiteAttacks
		else:
			return self.blackAttacks

	# Makes the given move and returns a new board object
	def move(self, move):
		origin = move.piece.position
		destination = move.position
		newWhitePieces = []
		newBlackPieces = []
		# Generate the new lists of white and black pieces for the board object being returned
		for piece in self.pieces:
			# These pieces are not moving
			if piece.position != origin:
				# Check for a piece being captured at the move's destination
				if piece.position != destination:
					if piece.color == Color["White"]:
						newWhitePieces.append(piece)
					else:
						newBlackPieces.append(piece)
			# This piece is moving
			else:
				if piece.color == Color["White"]:
					if str(piece) == "king":
						newWhitePieces.append(King(Color["White"], destination))
					else:
						newWhitePieces.append(Rook(Color["White"], destination))
				else:
					newBlackPieces.append(King(Color["Black"], destination))
		return Board(newWhitePieces, newBlackPieces)
	