#!/usr/bin/env python
import os, sys
from AIChessGame import AIChessGame
from AIChessGame import BoardState

# Prints the parameters at the start of a new game
def printStart(players, useHeuristicY):
	print("\n-------------------------------------------")
	print("Game started...")
	print("Test case " + str(game.testCase) + ": ", end = "")

	# Print starting positions of all pieces
	i = j = 0
	for player in players:
		for piece in player.pieces:
			print(piece.getLabel() + str(piece.position), end = "")
			if (i < len(players) - 1) or (j < len(player.pieces) - 1):
				print(", ", end = "")
			j = j + 1
		i = i + 1

	print("\nHeuristic functions used: ", end = "")
	if useHeuristicY:
		print("heuristicX, heuristicY");
	else:
		print("heuristicX")
	print("-------------------------------------------")

# Plays a game of chess
def play(game):
	printStart(game.players, game.useHeuristicY)
	game.printBoard()
	for n in range(game.n):
		for player in game.players:
			# End the game if check mate or stale mate
			game.board.calcBoardState()
			if game.board.state != BoardState["None"]:
				print("Number of moves made: " + str(n))
				if game.board.state == BoardState["Checkmate"]:
					print("Game result: Checkmate")
				else:
					print("Game result: Stalemate")
				sys.exit(0)
			# If the game is not over, make the next move and draw the board
			else:
				player.movePlayer(game)
				game.printBoard()

	print("Numer of moves made: " + str(n))
	print("Game result: None")

# Begins program execution
if __name__ == "__main__":
	game = AIChessGame()
	game.start()
	play(game)
	# game.end() if necessary
	# exit
