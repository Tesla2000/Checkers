import pygame
WIDTH, HEIGHT = 1200, 800
ROW, COLS = 8, 8
FIELD_SIZE = 800 // COLS

#game constants
INIT_NUMBER_OF_PAWNS = 12
INIT_NUMBER_OF_KINGS = 0
LIMIT_OF_ONLY_KINGS_MOVE = 15

#color
RED = (255, 0, 0)
GREY = (105, 105, 105)
BLUE = (0, 191, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORD = (255,122,0)

#img
KING = pygame.transform.scale(pygame.image.load('assets/crown.png'), (54,35))
