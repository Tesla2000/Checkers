import pygame

from checkers.constants import BLACK, BORD, FIELD_SIZE, BLUE, KING


class Pawn:
	OUTLINE = 2
	PADDING = 20

	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.king = False
		self.dir = self.setDirection

		self.x = 0
		self.y = 0
		self.calculate_pos()

	@property
	def setDirection(self):
		if self.color == BLACK:
			return 1  # going down
		if self.color == BORD:
			return -1  # going up

	def calculate_pos(self):
		self.x = FIELD_SIZE * self.col + FIELD_SIZE // 2
		self.y = FIELD_SIZE * self.row + FIELD_SIZE // 2

	def get_row(self):
		return self.row

	def get_col(self):
		return self.col


	def change_to_king(self):
		self.king = True

	def move(self, row, col):
		self.row = row
		self.col = col
		self.calculate_pos()

	def drawPawn(self, window):
		radius = FIELD_SIZE // 2 - self.PADDING
		pygame.draw.circle(window, BLUE, (self.x, self.y), radius)
		pygame.draw.circle(window, self.color, (self.x, self.y), radius - self.OUTLINE)

		if self.king:
			window.blit(KING, (self.x - KING.get_width()//2, self.y - KING.get_height() //2))

	def __repres__(self):
		return str(self.color)