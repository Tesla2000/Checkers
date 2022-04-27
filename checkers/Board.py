from checkers.constants import ROW, COLS, FIELD_SIZE, GREY, RED, WHITE, BLACK, BORD
import pygame
from checkers.Pawn import Pawn


class Board:
	def __init__(self):
		self.board = []
		self.bord_left = self.black_left = 12
		self.bord_kings = self.black_kings = 0
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
						self.board[row].append(Pawn(row, col, BORD))
					else:
						self.board[row].append(0) #blank piece
				else:
					self.board[row].append(0)

	def draw_board(self, win):
		self.draw_fields(win)
		for row in range(ROW):
			for col in range(COLS):
				pawn = self.board[row][col]
				if pawn != 0:
					pawn.drawPawn(win)

	def move(self, pawn, row, col): #swapping
		self.board[pawn.get_row()][pawn.get_col()], self.board[row][col] = self.board[row][col], self.board[pawn.row][pawn.col]
		pawn.move(row, col)
		self.update_king_status(pawn, row)

	def get_pawn(self, row, col):
		return self.board[row][col]

	def update_king_status(self, pawn, row):
		if row == ROW - 1 or row == 0:
			pawn.change_to_king()
			if pawn.color == BORD:
				self.bord_kings += 1
			else:
				self.black_kings += 1

	def remove(self, pawns):
		for pawn in pawns:
			self.board[pawn.row][pawn.col] = 0
			if pawn != 0:
				if pawn.color == BORD:
					self.bord_left -= 1
				else:
					self.black_left -= 1

	def winner(self):
		if self.bord_left <= 0:
			return BLACK
		elif self.black_left <= 0:
			return BORD

		return None

	def get_valid_moves(self, pawn):
		valid_moves = {}
		start_left_col = pawn.col - 1
		start_right_col = pawn.col + 1
		row = pawn.row

		if pawn.color == BORD or pawn.king:
			valid_moves.update(self.check_left_diagonal(row - 1, max(row - 3, -1), -1, pawn.color, start_left_col))
			valid_moves.update(self.check_right_diagonal(row - 1, max(row - 3, -1), -1, pawn.color, start_right_col))
		if pawn.color == BLACK or pawn.king:
			valid_moves.update(self.check_left_diagonal(row + 1, min(row + 3, ROW), 1, pawn.color, start_left_col))
			valid_moves.update(self.check_right_diagonal(row + 1, min(row + 3, ROW), 1, pawn.color, start_right_col))

		return valid_moves

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
					if step == -1:
						curr_row = max(row - 3, 0)
					else:
						curr_row = min(row + 3, ROW)
					valid_moves.update(self.check_left_diagonal(row + step, curr_row, step, color, left - 1, skipped=last))
					valid_moves.update(self.check_right_diagonal(row + step, curr_row, step, color, left + 1, skipped=last))
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
					if step_dir == -1:
						curr_row = max(row - 3, 0)
					else:
						curr_row = min(row + 3, ROW)
					valid_moves.update(self.check_left_diagonal(row + step_dir, curr_row, step_dir, color, right - 1, skipped=last))
					valid_moves.update(self.check_right_diagonal(row + step_dir, curr_row, step_dir, color, right + 1, skipped=last))
				break
			elif current_pawn.color == color:
				break
			else:
				last = [current_pawn]

			right += 1

		return valid_moves



'''
	def get_valid_moves(self, pawn):
		valid_moves = {}
		start_left_col = pawn.col - 1
		start_right_col = pawn.col + 1
		current_row = pawn.row

		if pawn.color == BORD or pawn.king: #do gory  # I am only looking to above where I am
			valid_moves.update(self.check_diagonal(start_left_col < 0, current_row - 1 , max(current_row-3, -1), -1, pawn.color, start_left_col)) # left side
			valid_moves.update(self.check_diagonal(start_right_col >= COLS, current_row - 1, max(current_row - 3, -1), -1, pawn.color, start_right_col)) #right side
		if pawn.color == BLACK or pawn.king:
			valid_moves.update(self.check_diagonal(start_left_col < 0, current_row + 1, min(current_row + 3, ROW), 1, pawn.color, start_left_col))
			valid_moves.update(self.check_diagonal(start_right_col >= COLS, current_row + 1, min(current_row + 3, ROW), 1, pawn.color, start_right_col))

		return valid_moves

	def check_diagonal(self, condition, start_row_pos, stop_row_pos, dir, color, col_on_dir, skipped=[]):
		valid_moves = {}
		last = []
		for row in range(start_row_pos, stop_row_pos, dir):
			if condition: # no in range of columns    col_on_left < 0
				break
			current_pawn = self.board[row][col_on_dir]
			if current_pawn == 0:
				if skipped and not last:
					break
				elif skipped: #double skip
					valid_moves[(row, col_on_dir)] = last + skipped  #combining previous with the last
				else:
					valid_moves[row, col_on_dir] = last

				if last:       # if we skipped some pawns on the road
					if dir == -1: #going up
						current_row = max(row-3, 0)
					else: #going down
						current_row = min(row+3, ROW)
					valid_moves.update(self.check_diagonal(col_on_dir - 1 < 0, row + dir, current_row , dir, color, col_on_dir-1 , skipped= last))
					valid_moves.update(self.check_diagonal(col_on_dir + 1 >= ROW, row + dir, current_row, dir, color, col_on_dir+1, skipped=last))
				break			#no more valid moves in current iteration
			elif current_pawn.color == color:
				break
			else:
				last = [current_pawn] ###

			col_on_dir += dir

		return valid_moves '''




