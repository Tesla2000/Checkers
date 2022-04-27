import pygame
from .Board import Board
from .constants import BORD, BLACK, BLUE, FIELD_SIZE


class Game:
	def __init__(self, bordPlayer, blackPlayer, win):
		self.bordPlayer = bordPlayer
		self.blackPlayer = blackPlayer
		self.currentPlayer = bordPlayer
		self.reset()
		self.win = win

	def update(self, win):
		self.board.draw_board(win)
		self.show_valid_moves(self.valid_moves)
		pygame.display.update()


	def reset(self):
		self.selected = None
		self.board = Board()
		self.turn = self.currentPlayer.color
		self.valid_moves = {}

	def winner(self):
		return self.board.winner()


	def change_turn(self):
		self.valid_moves = {}
		if self.turn == BORD:
			self.currentPlayer = self.blackPlayer
		else:
			self.currentPlayer = self.bordPlayer

		self.turn = self.currentPlayer.color

	def show_valid_moves(self, valid_moves):
		for move in valid_moves:
			row, col = move
			pygame.draw.rect(self.win, BLUE, (col * FIELD_SIZE, row * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE))









