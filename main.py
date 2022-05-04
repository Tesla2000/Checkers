import pygame
from checkers.constants import WIDTH, HEIGHT, WHITE, BLACK, FIELD_SIZE, WHITE, GREY, BLUE
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



def win_message(player_color):
    font = pygame.font.SysFont(None, 35)
    text = font.render(str(rgb_to_name(player_color, spec='css3')) + ' player WIN ', True, GREY)
    WINDOW.blit(text, (820, 110))

def lose_message(player):
    font = pygame.font.SysFont(None, 35)
    text = font.render(str(rgb_to_name(player.color, spec='css3')) + ' player LOSE ', True, GREY)
    WINDOW.blit(text, (820, 110))

def tie_message():
    font = pygame.font.SysFont(None, 35)
    text = font.render('TIE!', True, GREY)
    WINDOW.blit(text, (820, 110))



def main():

    run = True


    #SETTING PLAYER
    #bordPlayer = HumanPlayer(WHITE)
    bordPlayer = BotPlayer(WHITE)
    blackPlayer = BotPlayer(BLACK)
    clock = pygame.time.Clock()  #constant frame rate
    game = Game(bordPlayer, blackPlayer, WINDOW)


    while run:
        clock.tick(FPS)
        position = None

        if isinstance(game.currentPlayer, BotPlayer):
            game.tester.restCounter()
            startTime = time.time()
            value, new_board = game.currentPlayer.min_max(game.board, 4, True, game)
            game.ai_move(new_board)
            timer = game.tester.measureTimeSince(startTime)
            counter = game.tester.counter


        if game.loser() != None:
              lose_message(game.loser())
              pygame.display.update()
              time.sleep(7)
              run = False

        if game.tie():
            tie_message()
            pygame.display.update()
            time.sleep(7)
            run = False

        if game.winner() != None:
            win_message(game.winner())
            pygame.display.update()
            time.sleep(7)
            run = False



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if isinstance(game.currentPlayer, HumanPlayer) and event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = game.currentPlayer.get_input_row_col(position)
                game.currentPlayer.select(row, col, game)  #currentplayer.select

        #row, col = game.currentPlayer.get_input_row_col(position)
        #game.currentPlayer.select(row, col, game)  # currentplayer.select


        game.update(WINDOW, timer, counter)

    pygame.quit()


if __name__ == '__main__':
    main()


