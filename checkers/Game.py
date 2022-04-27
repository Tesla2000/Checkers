import pygame
from .Board import Board
from .constants import BORD, BLACK, BLUE, FIELD_SIZE
from .Player import Player


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


	def select(self, row, col):
		if self.selected:
			result = self._move(row, col)
			if not result:
				self.selected = None
				self.select(row, col)

		pawn = self.board.get_pawn(row, col)
		if pawn != 0 and pawn.color == self.turn:
			self.selected = pawn
			self.valid_moves = self.board.get_valid_moves(pawn)
			return True

		return False



	def _move(self, row, col):
		pawn = self.board.get_pawn(row, col)
		if self.selected and pawn == 0 and (row, col) in self.valid_moves:
			self.board.move(self.selected, row, col)
			skipped = self.valid_moves[(row, col)]
			if skipped:
				self.board.remove(skipped)
			self.turn = self.change_turn().color
		else:
			return False

		return True


	def change_turn(self):
		self.valid_moves = {}
		if self.turn == BORD:
			currentPlayer = self.blackPlayer
		else:
			currentPlayer = self.bordPlayer
		return currentPlayer



	def show_valid_moves(self, valid_moves):
		for move in valid_moves:
			row, col = move
			pygame.draw.rect(self.win, BLUE, (col * FIELD_SIZE, row * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE))









