# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
from checkers.constants import WIDTH, HEIGHT, BORD, BLACK, FIELD_SIZE
from checkers.Board import Board
from checkers.Player import HumanPlayer
from checkers.Game import Game

FPS = 60  # frame per second
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers');


def get_input_row_col(pos):
    x, y = pos
    row = y // FIELD_SIZE
    col = x // FIELD_SIZE
    return row, col


def main():

    run = True

   # board = Board()
    bordPlayer = HumanPlayer(BORD)
    blackPlayer = HumanPlayer(BLACK)
    clock = pygame.time.Clock()  #constant frame rate
    game = Game(bordPlayer, blackPlayer, WINDOW)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_input_row_col(pos)
                game.select(row, col)      #currentplayer.select

        game.update(WINDOW)

    pygame.quit()


if __name__ == '__main__':
    main()


