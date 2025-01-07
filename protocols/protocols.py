from collections.abc import Mapping
from typing import Any
from typing import Protocol as ProtocolistProtocol
from typing import runtime_checkable
from typing import Union

@runtime_checkable
class Board(ProtocolistProtocol):
	
	def draw_board(self, arg0):
		...
	def evaluate(self, arg0):
		...
	def get_all_pawns(self, arg0: BotPlayer):
		...
	def get_all_valid_moves(self, arg0: HumanPlayer):
		...
	def get_all_valid_moves_for(self, arg0: BotPlayer, arg1):
		...
	def get_pawn(self, arg0, arg1):
		...
	def get_valid_moves(self, arg0):
		...
	def move(self, arg0: Any, arg2, arg3):
		...
	def remove(self, arg0: Union[Any, str], arg1: Union[BotPlayer, HumanPlayer]):
		...
	def winner(self):
		...
@runtime_checkable
class CurrentPlayer(ProtocolistProtocol):
	
	def update_score(self):
		...
@runtime_checkable
class Game(ProtocolistProtocol):
	board: "Board"
	selected: Any
	tester: "Tester"
	turn: Any
	valid_moves: Union[Any, Mapping]
	win: Any
	def change_turn(self):
		...
	def show_valid_moves(self, arg0):
		...
@runtime_checkable
class Pawn(ProtocolistProtocol):
	col: Union[Any, Union[complex, float, int]]
	color: Any
	king: Any
	row: Union[Any, Union[complex, float, int]]
	x: Any
	y: Any
	def change_to_king(self):
		...
	def get_col(self):
		...
	def get_row(self):
		...
	def move(self, arg0, arg1):
		...
@runtime_checkable
class PawnsSubscript(ProtocolistProtocol):
	col: Any
	color: Any
	row: Any
	
@runtime_checkable
class Player(ProtocolistProtocol):
	color: Any
	score: Any
	
@runtime_checkable
class Tester(ProtocolistProtocol):
	
	def incrementCounter(self):
		...
@runtime_checkable
class Win(ProtocolistProtocol):
	
	def blit(self, arg0, arg1: Union[tuple[Any, Any], tuple[int, int]]):
		...
@runtime_checkable
class Window(ProtocolistProtocol):
	
	def blit(self, arg0, arg1: tuple[Any, Any]):
		...
	def fill(self, arg0: tuple[int, int, int]):
		...
