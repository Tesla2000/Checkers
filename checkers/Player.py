from checkers.constants import FIELD_SIZE


class Player:
	def __init__(self, color_pawn):
		self.color = color_pawn

	def get_input_row_col(self, pos):
		pass

	def select(self, row, col, game):
		pass

	def _move(self, row, col, game):
		pass


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
			game.valid_moves = game.board.get_valid_moves(pawn)
			return True

		return False

	def _move(self, row, col, game):
		pawn = game.board.get_pawn(row, col)
		if game.selected and pawn == 0 and (row, col) in game.valid_moves:
			game.board.move(game.selected, row, col)
			skipped = game.valid_moves[(row, col)]
			if skipped:
				game.board.remove(skipped)
			game.change_turn()
		else:
			return False

		return True

class BotPlayer(Player):
	def get_input_row_col(self, pos):
		pass
