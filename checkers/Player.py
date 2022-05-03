from checkers.constants import FIELD_SIZE, ROW, COLS
from checkers.Game import Game
import pygame

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
	def get_input_row_col(self, pos):
		pass
