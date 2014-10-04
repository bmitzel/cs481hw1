from AIChessGame import AIChessGame

# Plays a game of chess
def play():
	pass

# Begins program execution
if __name__ == "__main__":
	game = AIChessGame()
	game.start()
	# Pseudocode:
	#
	# play a game where n is the max number of moves for each player
	#   starting with the white player (heuristicX)
	#	make the next move for the current player
	#   display the board after each move along with the move that was made (piece to position)
	#   check for check mate or stale mate and print as appropriate
	#      if so, end the game and exit the program
	#   pause for the user to continue

	#w = {5,6}
	#b = {6,8}
	#r = {8,5}
	#white = Player('white')
	#black = Player('black')
	#white.getPieces()
	#newGame = Play(black, white)
	#newGame.printBoard()
	#newGame.run(black)

	#w, b, r = Piece('king', (5,6), white), Piece('king', (6,8), black), Piece('rook', (8,5), black)

	#my_board = Board(white, black)
	#my_board.printBoard()

#	w.printPosition()

	#my_board.moveWhite()
