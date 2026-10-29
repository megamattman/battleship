from lib.battleship import BattleShip
from lib.game_board import GameBoard
import pytest


def test_board_constructor()-> None:
    game_board = GameBoard(8,12,'O','X')
    assert game_board.rows == 8
    assert game_board.cols == 12
    assert game_board.empty_char == 'O'
    assert game_board.filled_char == 'X'
    for row in range(8):
        for col in range(12):
            assert game_board.board[row][col] == 'O'

def test_fill_space_in_bounds()-> None:
    game_board = GameBoard(8,12,'O','X')
    game_board.fill_space(1,2)
    assert game_board.board[1][2] == 'X'

def test_fill_space_oob()->None:
    game_board = GameBoard(8,12,'O','X')
    assert not game_board.fill_space(11,0)
    assert not game_board.fill_space(0, 22)
    assert not game_board.fill_space(22,22)

def test_add_boat_to_board()-> None:
    game_board = GameBoard(4,4,'O','X')
    ship = BattleShip("boat1", 2, 'b')
    game_board.place_ship_on_board(0,0,ship, "North")
    assert game_board.board[0][0] == 'b'
    assert game_board.board[1][0] == 'b'
    expected_grid = """
   b O O O
   b O O O
   O O O O
   O O O O
"""
    # print(game_board.get_board_visual())
    assert game_board.get_board_visual() == expected_grid

def test_add_ship_to_board_failure()-> None:
    game_board = GameBoard(4,4,'O','X')
    ship = BattleShip("boat1", 2, 'b')
    assert game_board.place_ship_on_board(0,0,ship, "North")
    assert not game_board.place_ship_on_board(0,0,ship, "North")


def test_hit_on_game_board():
    game_board = GameBoard(8,12,'O','X')
