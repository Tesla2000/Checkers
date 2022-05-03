from copy import deepcopy

from checkers.constants import FIELD_SIZE, ROW, COLS
from checkers.Game import Game
import pygame
from math import inf
class Player:
	def __init__(self, color_pawn):
		self.color = color_pawn
		self.score = 0

	def get_input_row_col(self, pos):
		pass

	def select(self, row, col, game):
		pass

	def _move(self, row, col, game):
		pass

	def update_score(self):
		self.score+=1





class HumanPlayer(Player):
	def get_input_row_col(self, pos):
		x, y = pos
		row = y // FIELD_SIZE
		col = x // FIELD_SIZE
		return row, col

	def select(self, row, col, game):
		if game.selected:
			result = self._move(row, col, game)
			if not result:
				game.selected = None
				self.select(row, col, game)

		pawn = game.board.get_pawn(row, col)
		if pawn != 0 and pawn.color == game.turn:
			game.selected = pawn
			canGoInside = False
			for move in game.board.get_valid_moves(pawn).items():
				if move in game.board.get_all_valid_moves(self).items():
					canGoInside = True
			if canGoInside:
				game.valid_moves = game.board.get_valid_moves(pawn)
			return canGoInside
		return False

	def _move(self, row, col, game):
		pawn = game.board.get_pawn(row, col)
		if game.selected and pawn == 0 and (row, col) in game.valid_moves:
			game.board.move(game.selected, row, col)
			skipped = game.valid_moves[(row, col)]
			if skipped:
				game.board.remove(skipped, self)
			game.change_turn()
		else:
			return False

		return True


class BotPlayer(Player):

	def min_max(self, board, depth, max_player, game):
		if depth == 0 or board.winner() != None:
			return board.evaluate(), board

		if max_player:  #maksymalizuje
			maxEval = -inf
			best_move = None
			for move in self.get_all_moves(board, self.color, game):
				evaluation = self.min_max(move, depth - 1, False, game)[0]
				maxEval = max(maxEval, evaluation)
				if maxEval == evaluation:
					best_move = move
			return maxEval, best_move
		else:
			minEval = inf
			best_move = None
			for move in self.get_all_moves(board, self.color, game):
				evaluation = self.min_max(move, depth - 1, True, game)[0]
				minEval = min(minEval, evaluation)
				if minEval == evaluation:
					best_move = move
			return minEval, best_move

	def get_input_row_col(self, pos):
		pass

	def select(self, row, col, game):
		pass

	def _move(self, row, col, game):
		pass

	def get_all_moves(self, board, color, game):
	    moves = []
	    for pawn in board.get_all_pawns(self):
	        valid_moves = board.get_all_valid_moves_for(self, pawn)
	        for move, skip in valid_moves.items():
	            temp_board = deepcopy(board)
	            temp_pawn = temp_board.get_pawn(pawn.row, pawn.col)
	            new_board = self.simulate_move(temp_pawn, move, temp_board, game, skip)
	            moves.append(new_board)
	    return moves

	def simulate_move(self, pawn, move, board, game, skip):
		board.move(pawn, move[0], move[1])
		if skip:
			board.remove(skip, self)

		return board