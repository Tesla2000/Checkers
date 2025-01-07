from collections.abc import Iterable
from collections.abc import Mapping
from collections.abc import MutableMapping
from collections.abc import Sized
from typing import Any
from typing import Union

import pygame

from checkers.constants import BLACK
from checkers.constants import COLS
from checkers.constants import DOWN
from checkers.constants import FIELD_SIZE
from checkers.constants import GREY
from checkers.constants import INIT_NUMBER_OF_KINGS
from checkers.constants import INIT_NUMBER_OF_PAWNS
from checkers.constants import LEFT
from checkers.constants import RIGHT
from checkers.constants import ROW
from checkers.constants import UP
from checkers.constants import WHITE
from checkers.Pawn import Pawn
from protocols.protocols import Board as Board_
from protocols.protocols import CurrentPlayer
from protocols.protocols import Pawn as Pawn_
from protocols.protocols import PawnsSubscript
from protocols.protocols import Player
from protocols.protocols import Window


class Board(Board_):
    def __init__(self):
        self.board = []
        self.white_left = self.black_left = INIT_NUMBER_OF_PAWNS
        self.white_kings = self.black_kings = INIT_NUMBER_OF_KINGS
        self.create_board()

    def draw_fields(self, window: Window):
        window.fill(GREY)
        for row in range(ROW):
            for col in range(row % 2, ROW, 2):  # (START POS, END COND, STRIDE LENGTH)
                pygame.draw.rect(window, WHITE, (row * FIELD_SIZE, col * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE))

    def create_board(self):
        for row in range(ROW):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Pawn(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Pawn(row, col, WHITE))
                    else:
                        self.board[row].append(0)  # blank piece
                else:
                    self.board[row].append(0)

    def draw_board(self, win):
        self.draw_fields(win)
        for row in range(ROW):
            for col in range(COLS):
                pawn = self.board[row][col]
                if pawn != 0:
                    pawn.drawPawn(win)

    def move(self, pawn: Pawn_, row, col):  # swapping
        self.board[pawn.get_row()][pawn.get_col()], self.board[row][col] = self.board[row][col], self.board[pawn.row][
            pawn.col]
        pawn.move(row, col)
        self.update_king_status(pawn, row)

    def get_pawn(self, row, col):
        return self.board[row][col]

    def update_king_status(self, pawn: Pawn_, row):
        if row == ROW - 1 or row == 0:
            pawn.change_to_king()
            if pawn.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def remove(self, pawns: Iterable[PawnsSubscript], currentPlayer: CurrentPlayer):
        for pawn in pawns:
            self.board[pawn.row][pawn.col] = 0
            currentPlayer.update_score()
            if pawn != 0:
                if pawn.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        if self.white_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return WHITE

        return None

    def get_all_valid_moves(self, player: Player):
        jump_moves = {}
        single_moves = {}
        for row in range(ROW):
            for col in range(COLS):
                if self.board[row][col] != 0 and self.board[row][col].color == player.color:
                    self.segragate_moves(self.get_valid_moves(self.board[row][col]), jump_moves, single_moves)
                    self.filter_by_longest_size(jump_moves)
        return jump_moves or single_moves

    def get_all_valid_moves_for(self, player, pawn):
        all_moves = {}
        for row in range(ROW):
            for col in range(COLS):
                if self.board[row][col] == pawn:
                    for (key, value) in self.get_valid_moves(self.board[row][col]).items():
                        if (key, value) in self.get_all_valid_moves(player).items():
                            all_moves.update({key: value})

                    return all_moves

    def segragate_moves(self, dict: Mapping[Any, Sized], double_moves: MutableMapping, single_moves: MutableMapping):
        for (key, value) in dict.items():
            if len(value) != 0:
                double_moves.update({key: value})
            else:
                single_moves.update({key: value})

    def evaluate(self, turn):  # maximize bot moves -> black_left , prioritize the king
        if turn == BLACK:
            return self.black_left - self.white_left + (self.black_kings * 0.5 - self.white_kings * 0.5)
        else:
            return self.white_left - self.black_left + (self.white_kings * 0.5 - self.black_kings * 0.5)

    def get_all_pawns(self, player: Player):
        pawns = []
        for row in range(ROW):
            for col in range(COLS):
                if self.board[row][col] != 0 and self.board[row][col].color == player.color:
                    pawns.append(self.board[row][col])
        return pawns

    def get_valid_moves(self, pawn: Pawn_):
        valid_moves = {}
        start_left_col = pawn.col - 1
        start_right_col = pawn.col + 1
        row = pawn.row
        step_up = -1
        step_down = 1

        if pawn.color == WHITE or pawn.king:
            valid_moves.update(self.check_left_diagonal(row - 1, max(row - 3, -1), step_up, pawn.color, start_left_col))
            valid_moves.update(
                self.check_right_diagonal(row - 1, max(row - 3, -1), step_up, pawn.color, start_right_col))

        if pawn.color == BLACK or pawn.king:
            valid_moves.update(
                self.check_left_diagonal(row + 1, min(row + 3, ROW), step_down, pawn.color, start_left_col))
            valid_moves.update(
                self.check_right_diagonal(row + 1, min(row + 3, ROW), step_down, pawn.color, start_right_col))



        return self.filter_by_longest_size(valid_moves)

    def check_left_diagonal(self, start, stop, step, color, left: Union[float, int], skipped=[]):
        valid_moves = {}
        last = []
        for row in range(start, stop, step):
            if left < 0:
                break

            current_pawn = self.board[row][left]
            if current_pawn == 0:
                if skipped and not last:
                    break
                elif skipped:
                    valid_moves[(row, left)] = last + skipped  # dodaje do listy pominietych ostatni pionek
                else:
                    valid_moves[(row, left)] = last  # nie ma pominietych, kolejny mozliwy ruch to najblizszy ruch

                if last:
                    if step < 0:  # step_up
                        curr_row = max(row - 3, 0)
                    else:  # step_down
                        curr_row = min(row + 3, ROW)
                    valid_moves.update(
                        self.check_left_diagonal(row + step, curr_row, step, color, left - 1, skipped=last))
                    valid_moves.update(
                        self.check_right_diagonal(row + step, curr_row, step, color, left + 1, skipped=last))

                    valid_moves.update(
                        self.check_left_diagonal(row - step, max(row - 3, 0), -step, color, left - 1, skipped=last))
                    valid_moves.update(
                        self.check_right_diagonal(row - step, max(row - 3, 0), -step, color, left + 1, skipped=last))
                break
            elif current_pawn.color == color:
                break
            else:
                last = [current_pawn]

            left -= 1

        return valid_moves

    def check_right_diagonal(self, start, stop, step_dir, color, right: Union[float, int], skipped=[]):
        valid_moves = {}
        last = []
        for row in range(start, stop, step_dir):
            if right >= COLS:
                break

            current_pawn = self.board[row][right]
            if current_pawn == 0:
                if skipped and not last:
                    break
                elif skipped:
                    valid_moves[(row, right)] = last + skipped
                else:
                    valid_moves[(row, right)] = last

                if last:
                    if step_dir < 0:
                        curr_row = max(row - 3, 0)
                    else:
                        curr_row = min(row + 3, ROW)
                    valid_moves.update(
                        self.check_left_diagonal(row + step_dir, curr_row, step_dir, color, right - 1, skipped=last))
                    valid_moves.update(
                        self.check_right_diagonal(row + step_dir, curr_row, step_dir, color, right + 1, skipped=last))
                break
            elif current_pawn.color == color:
                break
            else:
                last = [current_pawn]

            right += 1
        return valid_moves

    def filter_by_longest_size(self, dict: Mapping[Any, Sized]):
        if not all(map(lambda x: len(x) == 0, dict.values())):
            size = max(len(x) for x in dict.values())
            result = {}
            for (key, value) in dict.items():
                if len(value) == size:
                    result.update({key: value})
            return result
        else:
            return dict

    def king_move(self, row, col, horizontal_dir, vertical_dir, possible_moves: Union[MutableMapping, memoryview], color):
        next_col = col + horizontal_dir
        next_row = row + vertical_dir
        nextPawn = self.get_pawn(next_row, next_col)  # do góry w lewo
        while nextPawn == 0 and self.check_constraints(horizontal_dir, vertical_dir, next_row, next_col):
            next_row = row + vertical_dir
            next_col = col + horizontal_dir
            nextPawn = self.get_pawn(next_row, next_col)  # do góry w lewo
        if nextPawn.color != color:
            possible_moves[(next_row, next_col)] = nextPawn

    def check_constraints(self, horizontal_dir, vertical_dir, row, col):
        if horizontal_dir == LEFT and vertical_dir == UP:
            return row > 1 and col > 1
        if horizontal_dir == LEFT and vertical_dir == DOWN:
            return row < ROW - 2 and col > 1
        if horizontal_dir == RIGHT and vertical_dir == UP:
            return row > 1 and col < COLS - 2
        if horizontal_dir == RIGHT and vertical_dir == DOWN:
            return row < ROW - 2 and col < COLS - 2
