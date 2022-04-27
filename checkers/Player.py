from checkers.constants import FIELD_SIZE


class Player:
	def __init__(self, color_pawn):
		self.color = color_pawn

	def get_input_row_col(self, pos):
		pass


class HumanPlayer(Player):
	def get_input_row_col(self, pos):
		x, y = pos
		row = y // FIELD_SIZE
		col = x // FIELD_SIZE
		return row, col


class BotPlayer(Player):
	def get_input_row_col(self, pos):
		pass
