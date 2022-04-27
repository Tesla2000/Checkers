import pygame
from checkers.constants import WIDTH, HEIGHT, BORD, BLACK, FIELD_SIZE
from checkers.Board import Board
from checkers.Player import HumanPlayer, BotPlayer
from checkers.Game import Game

FPS = 60  # frame per second
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers');



def main():

    run = True

   # board = Board()
    bordPlayer = HumanPlayer(BORD)
    blackPlayer = HumanPlayer(BLACK)
    clock = pygame.time.Clock()  #constant frame rate
    game = Game(bordPlayer, blackPlayer, WINDOW)

    while run:
        clock.tick(FPS)
        position = None

        if isinstance(game.currentPlayer, BotPlayer):
            pass

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if  isinstance(game.currentPlayer, HumanPlayer) and event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = game.currentPlayer.get_input_row_col(position)
                game.currentPlayer.select(row, col, game)  #currentplayer.select

        #row, col = game.currentPlayer.get_input_row_col(position)
        #game.currentPlayer.select(row, col, game)  # currentplayer.select
        game.update(WINDOW)

    pygame.quit()


if __name__ == '__main__':
    main()


