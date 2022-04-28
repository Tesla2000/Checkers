from checkers.constants import ROW, COLS, FIELD_SIZE, GREY, RED, WHITE, BLACK, WHITE,\
	INIT_NUMBER_OF_PAWNS, INIT_NUMBER_OF_KINGS
import pygame
from checkers.Pawn import Pawn


class Board:
	def __init__(self):
		self.board = []
		self.white_left = self.black_left = INIT_NUMBER_OF_PAWNS
		self.white_kings = self.black_kings = INIT_NUMBER_OF_KINGS
		self.create_board()

	def draw_fields(self, window):
		window.fill(GREY)
		for row in range(ROW):
			for col in range(row % 2, ROW, 2):  # (START POS, END COND, STRIDE LENGTH)
				pygame.draw.rect(window, WHITE, (row * FIELD_SIZE, col * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE))

	def create_board(self):
		for row in range(ROW):
			self.board.append([])
			for col in range(COLS):
				if col % 2 == ((row + 1) % 2):
					if row < 3:
						self.board[row].append(Pawn(row, col, BLACK))
					elif row > 4:
						self.board[row].append(Pawn(row, col, WHITE))
					else:
						self.board[row].append(0)  # blank piece
				else:
					self.board[row].append(0)

	def draw_board(self, win):
		self.draw_fields(win)
		for row in range(ROW):
			for col in range(COLS):
				pawn = self.board[row][col]
				if pawn != 0:
					pawn.drawPawn(win)

	def move(self, pawn, row, col):  # swapping
		self.board[pawn.get_row()][pawn.get_col()], self.board[row][col] = self.board[row][col], self.board[pawn.row][
			pawn.col]
		pawn.move(row, col)
		self.update_king_status(pawn, row)

	def get_pawn(self, row, col):
		return self.board[row][col]

	def update_king_status(self, pawn, row):
		if row == ROW - 1 or row == 0:
			pawn.change_to_king()
			if pawn.color == WHITE:
				self.white_kings += 1
			else:
				self.black_kings += 1

	def remove(self, pawns, currentPlayer):
		for pawn in pawns:
			self.board[pawn.row][pawn.col] = 0
			currentPlayer.update_score()
			if pawn != 0:
				if pawn.color == WHITE:
					self.white_left -= 1
				else:
					self.black_left -= 1

	def winner(self):
		if self.white_left <= 0:
			return BLACK
		elif self.black_left <= 0:
			return WHITE

		return None

	def get_valid_moves(self, pawn):
		valid_moves = {}
		start_left_col = pawn.col - 1
		start_right_col = pawn.col + 1
		row = pawn.row
		step_up = -1
		step_down = 1

		if pawn.color == WHITE or pawn.king:
			valid_moves.update(self.check_left_diagonal(row - 1, max(row - 3, -1), step_up, pawn.color, start_left_col))
			valid_moves.update(self.check_right_diagonal(row - 1, max(row - 3, -1), step_up, pawn.color, start_right_col))

		if pawn.color == BLACK or pawn.king:
			valid_moves.update(self.check_left_diagonal(row + 1, min(row + 3, ROW), step_down, pawn.color, start_left_col))
			valid_moves.update(self.check_right_diagonal(row + 1, min(row + 3, ROW), step_down, pawn.color, start_right_col))

		return self.filter_by_longest_size(valid_moves)




	def check_left_diagonal(self, start, stop, step, color, left, skipped=[]):
		valid_moves = {}
		last = []
		for row in range(start, stop, step):
			if left < 0:
				break

			current_pawn = self.board[row][left]
			if current_pawn == 0:
				if skipped and not last:
					break
				elif skipped:
					valid_moves[(row, left)] = last + skipped
				else:
					valid_moves[(row, left)] = last

				if last:
					if step < 0:
						curr_row = max(row - 3, 0)
					else:
						curr_row = min(row + 3, ROW)
					valid_moves.update(
						self.check_left_diagonal(row + step, curr_row, step, color, left - 1, skipped=last))
					valid_moves.update(
						self.check_right_diagonal(row + step, curr_row, step, color, left + 1, skipped=last))
				break
			elif current_pawn.color == color:
				break
			else:
				last = [current_pawn]

			left -= 1

		return valid_moves

	def check_right_diagonal(self, start, stop, step_dir, color, right, skipped=[]):
		valid_moves = {}
		last = []
		for row in range(start, stop, step_dir):
			if right >= COLS:
				break

			current_pawn = self.board[row][right]
			if current_pawn == 0:
				if skipped and not last:
					break
				elif skipped:
					valid_moves[(row, right)] = last + skipped
				else:
					valid_moves[(row, right)] = last

				if last:
					if step_dir < 0:
						curr_row = max(row - 3, 0)
					else:
						curr_row = min(row + 3, ROW)
					valid_moves.update(
						self.check_left_diagonal(row + step_dir, curr_row, step_dir, color, right - 1, skipped=last))
					valid_moves.update(
						self.check_right_diagonal(row + step_dir, curr_row, step_dir, color, right + 1, skipped=last))
				break
			elif current_pawn.color == color:
				break
			else:
				last = [current_pawn]

			right += 1
		return valid_moves

	def filter_by_longest_size(self, dict):
		if not all(map(lambda x: len(x) == 0, dict.values())):
			size = max(len(x) for x in dict.values())
			result = {}
			for (key, value) in dict.items():
				if len(value) == size:
					result.update({key: value})
			return result
		else:
			return dict







###################################################################################################################################
	def check_right_diagonal_king(self, start, stop, step_dir, color, right, skipped=[]):
		curr_row = start
		for row in range(start, stop, step_dir):
			if right >= COLS:
				break
			current_pawn = self.board[curr_row][right]
			if current_pawn != 0:
				return self.check_right_diagonal(start, stop, step_dir, color, right, skipped)
			else:
				if step_dir < 0:
					curr_row = max(row - 3, 0)
				else:
					curr_row = min(row + 3, ROW)
					right += step_dir

	def check_left_diagonal_king(self, start, stop, step_dir, color, left, skipped=[]):
		curr_row = start
		for row in range(start, stop, step_dir):
			if left >= COLS:
				break
			current_pawn = self.board[curr_row][left]
			if current_pawn != 0:
				return self.check_left_diagonal(start, stop, step_dir, color, left, skipped)
			else:
				if step_dir < 0:
					curr_row = max(row - 3, 0)
				else:
					curr_row = min(row + 3, ROW)
					left += step_dir






