#!/usr/bin/env python
from AIChessGame import AIChessGame

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
	# Disabling n for now and just using 1 move per player
	for n in range(game.n):
	#for n in range(1):
		for player in game.players:
			# player.move() (this function both makes and prints the move e.g. "Rook to (1, 1)")
			player.move(game)
			game.printBoard()
			# check for stale mate and check mate
			#   if so, print the result
			#   return
			# pause
			pass

# Begins program execution
if __name__ == "__main__":
	game = AIChessGame()
	game.start()
	play(game)
	# game.end() if necessary
	# exit
