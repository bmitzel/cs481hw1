#!/usr/bin/env python
import os, sys, random, time
import Graph

debugLegalMoves = False
debugWhiteRandom = False

Color = {"White":0, "Black":1}
BoardState = {"None":0, "Checkmate":1, "Stalemate":2} 

class AIChessGame(object):
	def __init__(self):
		self.lookahead = 4
		self.testCase = 0
		self.useHeuristicY = False
		self.n = 0
		self.players = []
		#self.board is initialized inside self.start() function

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

	# Starts a new game -- this function MUST be called before any others
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

		if self.testCase == 1:
			wkX = 5
			wkY = 6
			wrX = 8
			wrY = 5
			bkX = 6
			bkY = 8
			self.n = 35
		elif self.testCase == 2:
			wkX = 6
			wkY = 5
			wrX = 5
			wrY = 6
			bkX = 4
			bkY = 7
			self.n = 35
		elif self.testCase == 3:
			wkX = 7
			wkY = 6
			wrX = 8
			wrY = 5
			bkX = 7
			bkY = 8
			self.n = 35
		else:
			# Get the starting positions for all 3 pieces: White King, White Rook, Black King
			print("\nEnter the starting positions for each piece.")
			print("Valid values for X and Y are from 1-8.")
			wkX = self.getXY("White King X: ")
			wkY = self.getXY("White King Y: ")
			wrX = self.getXY("White Rook X: ")
			wrY = self.getXY("White Rook Y: ")
			bkX = self.getXY("Black King X: ")
			bkY = self.getXY("Black King Y: ")

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

		# Get whether or not to use heuristicY
		useHeuristicY = input("\nUse heuristicY for the Black player (Y/N)? ").upper()[:1]
		while (useHeuristicY.upper() != "Y" and useHeuristicY.upper() != "N"):
			self.printError()
			useHeuristicY = input("Use heuristicY for the Black player (Y/N)? ").upper()[:1]
		if useHeuristicY == "Y":
			self.useHeuristicY = True
		else:
			self.useHeuristicY = False

		# Create and initialize the players and the chess board
		self.players = [WhitePlayer(Position(wkX, wkY), Position(wrX, wrY)),
			BlackPlayer(Position(bkX, bkY))]
		self.board = Board(self.players[0].pieces, self.players[1].pieces)

	# Returns true if the game has ended in a check mate
	def isCheckMate(self):
		pass

	# Returns true if the game has ended in a stale mate
	def isStaleMate(self):
		pass

	def end(self):
		# Is there any cleanup to do before exiting? If not, delete this function.
		pass

class Player(object):
	# Generate the game graph from the current board state
	def makeGraph(self, currentPlayer, currentBoard, maxDepth):
		# Insert the root node
		gameGraph = Graph.Graph((currentPlayer + 1) % 2, currentBoard)
		tempNode = gameGraph.root

		# Generate the rest of the tree using iterative depth-first search algorithm
		stack = []
		discovered = []
		stack.append(tempNode)
		# Process all new, undiscovered nodes
		while (stack):
			tempNode = stack.pop()
			if tempNode not in discovered:
				# Generate all the children for the current node without exceeding maxDepth
				childBoards = []
				if tempNode.depth < maxDepth:
					# Determine which player is making the next move
					nextPlayer = (tempNode.activePlayer + 1) % 2
					for piece in tempNode.board.pieces:
						if piece.color == nextPlayer:
							childBoards.extend(piece.getLegalMoves(tempNode.board))
				for newBoard in childBoards:
					tempNode.children.append(Graph.Node(nextPlayer, tempNode.depth + 1, newBoard))
				# Add the generated child nodes to the stack for processing
				for child in tempNode.children:
					stack.append(child)
				# Add the completed node to the discovered list
				discovered.append(tempNode)
		return gameGraph

	# Finds the optimal move in the game graph using the mini-max algorithm
	def minimax(self, graph, node, depth, maximize, alpha, beta):
		# If at max depth or a leaf node, return the heuristic value
		if (depth == 0) or (not node.children):
			value = self.calculateHV(node.board)
			# print(str(value))
			return value
		# If at the root, initialize the best move to the first move
		if graph.root == node:
			graph.bestMove = node.children[0].board
			# If there is only one possible move, we're done
			if len(node.children) == 1:
				return None
		# If it's the maximizing player's turn, return the highest value
		if maximize:
			for child in node.children:
				value = self.minimax(graph, child, depth - 1, False, alpha, beta)
				if value > alpha:
					alpha = value
					if graph.root == node:
						graph.bestMove = child.board
				# Stop searching if alpha >= beta
				if alpha >= beta:
					return alpha
			return alpha
		# If it's the minimizing player's turn, return the lowest value
		else:
			for child in node.children:
				value = self.minimax(graph, child, depth - 1, True, alpha, beta)
				if value < beta:
					beta = value
					if graph.root == node:
						graph.bestMove = child.board
				# Stop searching if beta <= alpha
				if beta <= alpha:
					return beta
			return beta

class WhitePlayer(Player):
	def __init__(self, kingPos, rookPos):
		self.pieces = [King(Color["White"], kingPos), Rook(Color["White"], rookPos)]

	def __str__(self):
		return "White"

	def __repr__(self):
		return self.__str__()

	# Get best move using mini-max algorithm
	def heuristicX(self, board, lookahead):
		gameGraph = self.makeGraph(Color["White"], board, lookahead)
		self.minimax(gameGraph, gameGraph.root, lookahead, True, -9999999999, 9999999999)
		return gameGraph.bestMove

	def calculateHV(self, board):
		# If the rook has been captured, return -infinity
		if len(board.pieces) < 3:
			return -9999999999

		# If the rook is under attack and not defended by the king, return -infinity
		for piece in board.pieces:
			if str(piece) == "king" and piece.color == Color["White"]:
				wkPos = piece.position
				wkDefense = [wkPos.tl(), wkPos.t(), wkPos.tr(),
						wkPos.l(), wkPos.r(),
						wkPos.bl(), wkPos.b(), wkPos.br()]
		for piece in board.pieces:
			if str(piece) == "rook":
				rookPos = piece.position
				if piece.position in board.blackAttacks and piece.position not in wkDefense:
					return -9999999999

		# If the board is in stale mate, return -infinity
		board.calcBoardState()
		if board.state == BoardState["Stalemate"]:
			return -9999999999

		# If the board is in check mate, return +infinity
		if board.state == BoardState["Checkmate"]:
			return 9999999999

		# Count twice the number of squares on and around the Black king that are under attack
		# This is intended to give a high priority to attacking the Black king
		value = 2 * len(list(set(board.whiteAttacks).intersection(board.blackAttacks)))

		# Subtract the distance between the rook and nearest board edge in the Black king direction
		# This is because we want the rook to trap the Black king on a board edge
		# Then, subtract the distance between the White king and two squares away from that edge
		# This is to position the White king on the correct row or column for a check mate
		for piece in board.pieces:
			if str(piece) == "king" and piece.color == Color["Black"]:
				bkPos = piece.position
		rookDistance = 0
		kingDistance = 0
		# The Black king is to the right of the rook
		if bkPos.x - rookPos.x > 0:
			rookDistance = 8 - rookPos.x
			kingDistance = max(abs(6 - wkPos.x), 2)
		# The Black king is to the left of the rook
		elif bkPos.x - rookPos.x < 0:
			rookDistance = rookPos.x - 1
			kingDistance = max(abs(wkPos.x - 3), 2)
		# The Black king is above the rook
		if bkPos.y - rookPos.y > 0:
			rookDistance = min(8 - rookPos.y, rookDistance)
			kingDistance = max(abs(6 - wkPos.y), 2)
		# The Black king is below the rook
		elif bkPos.y - rookPos.y < 0:
			rookDistance = min(rookPos.y - 1, rookDistance)
			kingDistance = max(abs(wkPos.y - 3), 2)
		value = value - rookDistance - kingDistance

		# Subtract the distance between the Black king and the nearest board edge
		# This is because we can only mate the Black king while it is on a board edge
		for piece in board.pieces:
			if str(piece) == "king" and piece.color == Color["Black"]:
				bkPos = piece.position
		minDistance = abs(bkPos.x - 1)
		minDistance = min(abs(bkPos.x - 8), minDistance)
		minDistance = min(abs(bkPos.y - 1), minDistance)
		minDistance = min(abs(bkPos.y - 8), minDistance)
		value = value - minDistance

		return value

	def randomX(self, board):
		moves = []
		#include debugging of legal moves on both 
		if debugLegalMoves:
			print("Drawing all legal moves for the White player...\n")

		for piece in self.pieces:
			moves.extend(piece.getLegalMoves(board))
		# Return a randomly-selected legal board move
		return moves[random.randint(0, len(moves) - 1)]

	# Make a move for the White player
	def movePlayer(self, game):
		# Get the new board from heuristicX and update the player's pieces
		if debugWhiteRandom:
			game.board = self.randomX(game.board)
		else:
			game.board = self.heuristicX(game.board, game.lookahead)
		for player in game.players:
			player.updatePieces(game.board)

	# Update the White player's list of pieces from the current game board
	def updatePieces(self, board):
		self.pieces = []
		for piece in board.pieces:
			if piece.color == Color["White"]:
				self.pieces.append(piece)

class BlackPlayer(Player):
	def __init__(self, kingPos):
		self.pieces = [King(Color["Black"], kingPos)]

	def __str__(self):
		return "Black"

	def __repr__(self):
		return self.__str__()

	# Get best move using mini-max algorithm
	def heuristicY(self, board, lookahead):
		gameGraph = self.makeGraph(Color["Black"], board, lookahead)
		self.minimax(gameGraph, gameGraph.root, lookahead, True, -9999999999, 9999999999)
		return gameGraph.bestMove

	def calculateHV(self, board):
		# If the rook has been captured, return +infinity
		if len(board.pieces) < 3:
			return 9999999999

		# If the rook is under attack and not defended by the king, return +infinity
		for piece in board.pieces:
			if str(piece) == "king" and piece.color == Color["White"]:
				wkPos = piece.position
				wkDefense = [wkPos.tl(), wkPos.t(), wkPos.tr(),
						wkPos.l(), wkPos.r(),
						wkPos.bl(), wkPos.b(), wkPos.br()]
		for piece in board.pieces:
			if str(piece) == "rook":
				rookPos = piece.position
				if piece.position in board.blackAttacks and piece.position not in wkDefense:
					return 9999999999

		# If the board is in stale mate, return +infinity
		board.calcBoardState()
		if board.state == BoardState["Stalemate"]:
			return 9999999999

		# If the board is in check mate, return -infinity
		if board.state == BoardState["Checkmate"]:
			return -9999999999

		# Count twice the distance to the nearest board edge
		# Since we want to prioritize staying away from board edges
		for piece in board.pieces:
			if str(piece) == "king" and piece.color == Color["Black"]:
				bkPos = piece.position
		minDistance = abs(bkPos.x - 1)
		minDistance = min(abs(bkPos.x - 8), minDistance)
		minDistance = min(abs(bkPos.y - 1), minDistance)
		minDistance = min(abs(bkPos.y - 8), minDistance)
		value = 2 * minDistance

		# Add the distance to the white king by number of moves
		value = value + max(abs(bkPos.x - wkPos.x), abs(bkPos.y - wkPos.y))

		# Add 0 or 1 for the distance to the white rook by number of moves
		if bkPos.x != rookPos.x and bkPos.y != rookPos.y:
			value = value + 1

		return value

	# Get random move
	def randomY(self, board):
		moves = []
		if debugLegalMoves:
			print("Drawing all legal moves for the Black player...\n")
		for piece in self.pieces:
			moves.extend(piece.getLegalMoves(board))
		# Return a randomly-selected legal board move
		return moves[random.randint(0, len(moves) - 1)]

	# Make a move for the Black player
	def movePlayer(self, game):
		# Get the new board from heuristicY or randomY and update the player's pieces
		if game.useHeuristicY:
			game.board = self.heuristicY(game.board, game.lookahead)
		else:
			game.board = self.randomY(game.board)
		for player in game.players:
			player.updatePieces(game.board)

	def updatePieces(self, board):
		self.pieces = []
		for piece in board.pieces:
			if piece.color == Color["Black"]:
				self.pieces.append(piece)

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

	# Calculates a list of board objects corresponding to all the legal moves for the king
	# Illegal moves:
	#   - Moving into check
	#   - Moving onto a square occupied by another piece of the same color
	def getLegalMoves(self, board):
		legalMoves = []
		# Get list of positions under attack by opposing player
		attacked = board.underAttack((int(self.color) + 1) % 2)
		# Get list of occupied squares and remove itself from the list
		if self.color == Color["White"]:
			occupied = list(board.occupied)
			occupied.remove(self.position)
		else:
			occupied = [] # This is a shortcut because the Black king can capture the White rook
		# Generate all the legal moves from the current position
		# Add each new board object to the list of moves
		for y in range(min(8, self.position.y + 1), max(0, self.position.y - 2), -1):
			for x in range(max(1, self.position.x - 1), min(9, self.position.x + 2)):
				newPosition = Position(x, y)
				if ((self.position != newPosition) and (newPosition not in attacked) and
						(newPosition not in occupied)):
					newBoard = board.makeMove(Move(self, newPosition))
					legalMoves.append(newBoard)
					if debugLegalMoves:
						if self.color == Color["White"]:
							print("White ", end = "")
						else:
							print("Black ", end = "")
						print(str(self) + " to " + str(newPosition))
						newBoard.draw()
		return legalMoves

class Rook(Piece):
	def __str__(self):
		return "rook"

	def __repr__(self):
		return self.__str__()

	def getLabel(self):
		return "r"

	# Calculates a list of board objects corresponding to all the legal moves for the rook
	# Illegal moves:
	#   - Moving onto or beyond a square occupied by another piece of the same color
	#   - Capturing the opposing king
	def getLegalMoves(self, board):
		legalMoves = []
		# Get list of occupied squares and remove itself from the list
		if self.color == Color["White"]:
			occupied = list(board.occupied)
			occupied.remove(self.position)
		# The Black king doesn't care about occupied squares since it can't move there anyway
		else:
			occupied = []
		# Generate all the legal moves from the current position
		# Add each new board object to the list of moves
		legalPositions = self.calcLegalPositions(occupied)
		for position in legalPositions:
			self.addMove(legalMoves, board, position)
		return legalMoves

	# Calculates all the legal positions to which the rook can move
	def calcLegalPositions(self, occupied):
		positions = []
		# Move up
		for y in range(self.position.y + 1, 9):
			newPosition = Position(self.position.x, y)
			if newPosition in occupied:
				break
			positions.append(newPosition)
		# Move down
		for y in range(self.position.y - 1, 0, -1):
			newPosition = Position(self.position.x, y)
			if newPosition in occupied:
				break
			positions.append(newPosition)
		# Move left
		for x in range(self.position.x - 1, 0, -1):
			newPosition = Position(x, self.position.y)
			if newPosition in occupied:
				break
			positions.append(newPosition)
		# Move right
		for x in range(self.position.x + 1, 9):
			newPosition = Position(x, self.position.y)
			if newPosition in occupied:
				break
			positions.append(newPosition)
		return positions

	# Create and add a new board object to the list of legal moves
	def addMove(self, moves, board, position):
		newBoard = board.makeMove(Move(self, position))
		moves.append(newBoard)
		if debugLegalMoves:
			print("White " + str(self) + " to " + str(position))
			newBoard.draw()

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

	def __hash__(self):
		#return hash(tuple(self.__str__()))
		return hash(self.__str__())

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
		self.whiteAttacks = []
		self.blackAttacks = []
		self.occupied = []
		self.state = BoardState["None"]
		self.update()

	# Update which squares are currently under attack or occupied by both players
	def update(self):
		self.calcOccupied()
		self.calcWhiteAttacks()
		self.calcBlackAttacks()

	# Calculate which squares are under attack by the White player
	def calcWhiteAttacks(self):
		self.whiteAttacks = []
		for piece in self.pieces:
			if piece.color == Color["White"]:
				if str(piece) == "king":
					self.whiteAttacks.extend(
						[piece.position.tl(), piece.position.t(), piece.position.tr(),
						piece.position.l(), piece.position.r(),
						piece.position.bl(), piece.position.b(), piece.position.br()])
				else:
					# Get the list of positions the rook can attack
					otherOccupied = list(self.occupied)
					otherOccupied.remove(piece.position)
					for otherPiece in self.pieces:
						if str(otherPiece) == "king":
							# Allow the Black king's position and any squares beyond it
							if otherPiece.color == Color["Black"]:
								otherOccupied.remove(otherPiece.position)
							# If the White king is defended by the rook, add its position
							else:
								self.whiteAttacks.append(otherPiece.position)
					self.whiteAttacks.extend(piece.calcLegalPositions(otherOccupied))
		self.whiteAttacks.extend(self.calcBorderPositions())

	# Calculate which squares are under attack by the Black player
	def calcBlackAttacks(self):
		for piece in self.pieces:
			if piece.color == Color["Black"]:
				self.blackAttacks = [piece.position.tl(), piece.position.t(), piece.position.tr(),
					piece.position.l(), piece.position, piece.position.r(),
					piece.position.bl(), piece.position.b(), piece.position.br()]

	# List border positions as under attack
	def calcBorderPositions(self):
		borderPositions = []
		for y in range (10):
			borderPositions.append(Position(0 , y))
		for x in range (1 , 10):
			borderPositions.append(Position(x , 9))
		for y in range (8, -1, -1):
			borderPositions.append(Position(9 , y))
		for x in range (8 , 0 , -1):
			borderPositions.append(Position(x , 0))
		return borderPositions

	# Calculate which squares are occupied by both players
	def calcOccupied(self):
		self.occupied = []
		for piece in self.pieces:
			self.occupied.append(piece.position)

	# Calculates the current board state: none, checkmate, or stalemate
	def calcBoardState(self):
		for piece in self.pieces:
			if str(piece) == "king" and piece.color == Color["Black"]:
				# Test if moves list is empty
				if not piece.getLegalMoves(self):
					if piece.position in self.whiteAttacks:
						self.state = BoardState["Checkmate"]
					else:
						self.state = BoardState["Stalemate"]
				break;

	# Draw the current game board and pause
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
		wait = input("\n...Paused...")
		print("\n")

	# This function is for debugging only; prints all the pieces currently on the board
	def printPieces(self):
		for piece in self.pieces:
			if piece.color == Color["White"]:
				print("White ", end = "")
			else:
				print("Black ", end = "")
			print(str(piece) + " at " + str(piece.position))

	# Returns a list of positions that are under attack by the given colored player
	def underAttack(self, color):
		if color == Color["White"]:
			return self.whiteAttacks
		else:
			return self.blackAttacks

	# Returns a new board object updated with the given move
	def makeMove(self, move):
		origin = move.piece.position
		destination = move.position
		newWhitePieces = [] # Updated list of White pieces for the board being returned
		newBlackPieces = [] # Updated list of Black pieces for the board being returned
		# Generate the new lists of White and Black pieces
		for piece in self.pieces:
			# These pieces are not moving
			if piece.position != origin:
				# Add pieces that are not being captured to the appropriate new list
				if piece.position != destination:
					if piece.color == Color["White"]:
						newWhitePieces.append(piece)
					else:
						newBlackPieces.append(piece)
			# This piece is moving
			else:
				# Add the piece that's moving to the appropriate new list
				if piece.color == Color["White"]:
					if str(piece) == "king":
						newWhitePieces.append(King(Color["White"], destination))
					else:
						newWhitePieces.append(Rook(Color["White"], destination))
				else:
					newBlackPieces.append(King(Color["Black"], destination))
		return Board(newWhitePieces, newBlackPieces)
	