import pygame
from checkers.constants import WIDTH, HEIGHT, BORD, BLACK, FIELD_SIZE, WHITE
from checkers.Board import Board
from checkers.Player import HumanPlayer, BotPlayer
from checkers.Game import Game
from webcolors import rgb_to_name
import time


pygame.init()
FPS = 60  # frame per second
not_from_console = True
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers');

def display_counters(player, x, y):
    font = pygame.font.SysFont(None, 25)
    text = font.render(str(rgb_to_name(player.color,spec='css3')) + ' player: ' + str(player.score),True, WHITE)
    WINDOW.blit(text,(x,y))

def win_message(player):
    font = pygame.font.SysFont(None, 50)
    text = font.render(str(rgb_to_name(player, spec='css3')) + ' player WIN ', True, WHITE)
    WINDOW.blit(text, (800, 50))


def tie_message():
    font = pygame.font.SysFont(None, 25)
    text = font.render('TIE!', True, WHITE)
    WINDOW.blit(text, (WIDTH // 2, HEIGHT // 2))


def main():
    '''
    print("Do You want to type next move from console? Y/N")
    answer = input()
    if(answer =='Y'):
        not_from_console= False
        '''


    run = True

   # board = Board()
    bordPlayer = HumanPlayer(BORD)
    blackPlayer = HumanPlayer(BLACK)
    clock = pygame.time.Clock()  #constant frame rate
    game = Game(bordPlayer, blackPlayer, WINDOW)

    while run:
        clock.tick(FPS)
        position = None
        display_counters(game.bordPlayer, 800, 10)
        display_counters(game.blackPlayer, 800, 30)
        pygame.display.update()

        if isinstance(game.currentPlayer, BotPlayer):
            pass

        if game.winner() != None:
            win_message(game.winner())
            pygame.display.update()
            time.sleep(10)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not_from_console and isinstance(game.currentPlayer, HumanPlayer) and event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = game.currentPlayer.get_input_row_col(position)
                game.currentPlayer.select(row, col, game)  #currentplayer.select

        #row, col = game.currentPlayer.get_input_row_col(position)
        #game.currentPlayer.select(row, col, game)  # currentplayer.select
        '''
        if not not_from_console and isinstance(game.currentPlayer, HumanPlayer):
            print('Get start row')
            start_row =int(input())
            print('Get start col')
            start_col = int(input())
            game.currentPlayer.select(start_row, start_col, game)
            
            print('Get end row')
            end_row = int(input())
            print('Get end col')
            end_col = int(input())
            game.currentPlayer.select(end_row, end_col, game)
            '''


        game.update(WINDOW)

    pygame.quit()


if __name__ == '__main__':
    main()


