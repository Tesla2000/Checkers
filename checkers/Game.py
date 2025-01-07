from collections.abc import Iterable

import pygame
from webcolors import rgb_to_name

from .Board import Board
from .constants import BLACK
from .constants import BLUE
from .constants import FIELD_SIZE
from .constants import GREY
from .constants import HEIGHT
from .constants import LIMIT_OF_ONLY_KINGS_MOVE
from .constants import WHITE
from .Tester import Tester
from protocols.protocols import Player
from protocols.protocols import Win


class Game:

    def display_counters(self, player: Player, x, y):
        font = pygame.font.SysFont(None, 35)
        text = font.render(str(rgb_to_name(player.color, spec='css3')) + ' player: ' + str(player.score), True, GREY)
        self.win.blit(text, (x, y))

    def display_msg(self, msg, x, y):
        font = pygame.font.SysFont(None, 35)
        text = font.render(str(msg), True, WHITE)
        self.win.blit(text, (x, y))



    def display_whose_turn(self):
        font = pygame.font.SysFont(None, 35)
        self.currentPlayer
        text = font.render(str(rgb_to_name(self.currentPlayer.color, spec='css3')) + ' player turn ', True, GREY)
        self.win.blit(text, (820, 80))

    def __init__(self, whitePlayer: Player, blackPlayer, win: Win):
        self.whitePlayer = whitePlayer
        self.blackPlayer = blackPlayer
        self.tester = Tester()
        self.currentPlayer = whitePlayer
        self.reset()
        self.win = win

    def update(self, win, time, counter):
        self.board.draw_board(win)
        self.show_valid_moves(self.valid_moves)
        pygame.draw.line(win, BLACK, (800, 0), (800, HEIGHT))
        pygame.draw.rect(win, WHITE, (810, 10, 380, 150))
        self.display_counters(self.whitePlayer, 820, 20)
        self.display_counters(self.blackPlayer, 820, 50)
        self.display_whose_turn()
        self.display_msg(time, 820, 180)
        self.display_msg(counter, 820, 210)
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
        if not self.board.get_all_valid_moves(self.currentPlayer):
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

    def show_valid_moves(self, valid_moves: Iterable):
        for move in valid_moves:
            row, col = move
            pygame.draw.rect(self.win, BLUE, (col * FIELD_SIZE, row * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE))

    def ai_move(self, board):
        self.board = board
        self.change_turn()
