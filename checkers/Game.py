import pygame
from .Board import Board
from .constants import WHITE, BLACK, BLUE, FIELD_SIZE, LIMIT_OF_ONLY_KINGS_MOVE


class Game:
	def __init__(self, whitePlayer, blackPlayer, win):
		self.whitePlayer = whitePlayer
		self.blackPlayer = blackPlayer
		self.currentPlayer = whitePlayer
		self.reset()
		self.win = win

	def update(self, win):
		self.board.draw_board(win)
		self.show_valid_moves(self.valid_moves)
		pygame.display.update()


	def reset(self):
		self.last_kings_moves = 0;
		self.selected = None
		self.board = Board()
		self.turn = self.currentPlayer.color
		self.valid_moves = {}

	def winner(self):
		return self.board.winner()


	def loser(self):
		if not self.currentPlayer.get_all_valid_moves(self.board):
			return self.currentPlayer
		else:
			return None

	def tie(self):
		if self.last_kings_moves >= LIMIT_OF_ONLY_KINGS_MOVE:
			return True
		else:
			return False


	def count_last_kings_moves(self):
		if(self.board.white_left == self.board.white_kings) and (self.board.black_left == self.board.black_kings):
			self.last_kings_moves += 1

	def change_turn(self):
		self.count_last_kings_moves()
		self.valid_moves = {}
		if self.turn == WHITE:
			self.currentPlayer = self.blackPlayer
		else:
			self.currentPlayer = self.whitePlayer

		self.turn = self.currentPlayer.color

	def show_valid_moves(self, valid_moves):
		for move in valid_moves:
			row, col = move
			pygame.draw.rect(self.win, BLUE, (col * FIELD_SIZE, row * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE))









