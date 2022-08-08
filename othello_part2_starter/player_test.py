from player import Player
from board import Board
from tile import Tile


def test_constructor():
    bd = Board(400, 400, 4)
    py = Player(0, bd, 2)
    assert py.COLOR == 0
    assert py.board is bd
    assert py.tile_number == 2


def test_str():
    bd = Board(400, 400, 4)
    py = Player(0, bd, 2)
    assert str(py) == "Black"


def test_neighbor_oppo():
    bd = Board(400, 400, 4)
    py = Player(0, bd, 2)

    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None  # Reset the board
    bd.tile_table[0][0] = Tile(400, 400, 4, 0, 50, 50)  # black
    bd.tile_table[0][1] = Tile(400, 400, 4, 1, 150, 50)  # white
    bd.tile_table[0][2] = Tile(400, 400, 4, 1, 250, 50)  # white
    bd.tile_table[1][0] = Tile(400, 400, 4, 1, 50, 150)  # white
    bd.tile_table[1][1] = Tile(400, 400, 4, 0, 150, 150)  # black
    bd.tile_table[1][2] = Tile(400, 400, 4, 0, 250, 150)  # black
    bd.tile_table[1][3] = Tile(400, 400, 4, 1, 350, 150)  # white
    bd.tile_table[2][1] = Tile(400, 400, 4, 1, 150, 250)  # white

    # [0][0]: On the board's corner.
    # Test if the function works well for index out of board.
    assert len(py.neighbor_oppo(0, 0)) == 2
    assert (0, 1) in py.neighbor_oppo(0, 0)
    assert (1, 0) in py.neighbor_oppo(0, 0)
    # tile of player's own color should not be counted
    assert (1, 1) not in py.neighbor_oppo(0, 0)

    # [1][2]: In the board center.
    assert len(py.neighbor_oppo(1, 2)) == 4
    assert (0, 2) in py.neighbor_oppo(1, 2)
    assert (1, 3) in py.neighbor_oppo(1, 2)
    # tile of player's own color should not be counted
    assert (1, 1) not in py.neighbor_oppo(1, 2)
    # Diagonal
    assert (0, 1) in py.neighbor_oppo(1, 2)
    assert (2, 1) in py.neighbor_oppo(1, 2)


def test_legal_positions():
    bd = Board(400, 400, 4)
    py = Player(0, bd, 2)

    # Board 1: includes cases like:
    # 1. No legal_positions:
    #    There are opponent's tile on the extended line, but out of range.
    # or There are player's own tile on the extended line.
    # 2. Have legal_position:
    #    Only one opponent's tile in the middle
    #    Two opponent's tiles in the middle

    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None  # Reset the board
    bd.tile_table[0][0] = Tile(400, 400, 4, 0, 50, 50)  # black
    bd.tile_table[0][2] = Tile(400, 400, 4, 1, 250, 50)  # white
    bd.tile_table[0][3] = Tile(400, 400, 4, 0, 350, 50)
    bd.tile_table[1][0] = Tile(400, 400, 4, 1, 50, 150)  # white
    bd.tile_table[1][1] = Tile(400, 400, 4, 1, 150, 150)  # white
    bd.tile_table[1][2] = Tile(400, 400, 4, 0, 250, 150)  # black
    bd.tile_table[2][0] = Tile(400, 400, 4, 0, 50, 250)  # black
    bd.tile_table[2][2] = Tile(400, 400, 4, 1, 250, 250)  # white

    legal_pos = py.legal_positions()
    assert len(legal_pos) == 3
    assert legal_pos[(3, 3)] == [(0, 0)]
    assert legal_pos[(3, 2)] == [(1, 2)]
    assert legal_pos[(0, 1)] == [(0, 3)]

    # Board 2: check if the coordinate translation part works well.
    # Check different directions:
    # (+- vertical, +- horizontal, +- diagonal)
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None  # Reset the board
    bd.tile_table[0][2] = Tile(400, 400, 4, 0, 250, 50)  # b
    bd.tile_table[1][0] = Tile(400, 400, 4, 1, 50, 150)  # white
    bd.tile_table[1][1] = Tile(400, 400, 4, 1, 150, 150)  # white
    bd.tile_table[1][2] = Tile(400, 400, 4, 1, 250, 150)  # w
    bd.tile_table[2][1] = Tile(400, 400, 4, 0, 150, 250)  # black
    bd.tile_table[2][2] = Tile(400, 400, 4, 1, 250, 250)  # white
    bd.tile_table[3][3] = Tile(400, 400, 4, 0, 350, 350)  # b

    legal_pos = py.legal_positions()
    assert len(legal_pos) == 6
    # Direction from existing tile to legal positions:
    assert (0, 0) in legal_pos.keys()
    assert legal_pos[(0, 0)] == [(3, 3)]    # left-up
    assert legal_pos[(0, 1)] == [(2, 1)]    # up
    assert legal_pos[(0, 3)] == [(2, 1)]    # right-up
    assert legal_pos[(2, 0)] == [(0, 2)]    # left-down
    assert legal_pos[(2, 3)] == [(2, 1)]    # right
    assert legal_pos[(3, 2)] == [(0, 2)]    # down

    # Board2: Change player.
    py = Player(1, bd, 2)    # white
    legal_pos = py.legal_positions()
    assert len(legal_pos) == 4
    assert legal_pos[(2, 0)] == [(2, 2)]
    assert legal_pos[(3, 0)] == [(1, 2)]
    assert legal_pos[(3, 1)] == [(1, 1)]
    assert legal_pos[(3, 2)] == [(1, 0)]

    # Board3: One legal position form flipping condition with more than one
    # existing tile
    py = Player(0, bd, 2)    # black

    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None  # Reset the board
    bd.tile_table[0][1] = Tile(400, 400, 4, 1, 150, 50)
    bd.tile_table[0][2] = Tile(400, 400, 4, 0, 250, 50)
    bd.tile_table[1][0] = Tile(400, 400, 4, 1, 50, 150)
    bd.tile_table[1][1] = Tile(400, 400, 4, 1, 150, 150)
    bd.tile_table[2][0] = Tile(400, 400, 4, 0, 50, 250)
    bd.tile_table[2][2] = Tile(400, 400, 4, 0, 250, 250)

    legal_pos = py.legal_positions()
    assert len(legal_pos) == 1
    assert len(legal_pos[(0, 0)]) == 3
    assert (0, 2) in legal_pos[(0, 0)]
    assert (2, 0) in legal_pos[(0, 0)]
    assert (2, 2) in legal_pos[(0, 0)]


def test_place_flip_tile():
    bd = Board(400, 400, 4)
    py = Player(0, bd, 2)    # black

    # Board 4: One of the test case of board's place_flip_tile method.
    # Only that the current player's color is passed in automatically.
    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None
    bd.tile_table[0][0] = Tile(400, 400, 4, 0, 50, 50)    # black
    bd.tile_table[1][1] = Tile(400, 400, 4, 1, 150, 150)  # white
    bd.tile_table[1][2] = Tile(400, 400, 4, 1, 250, 150)  # white
    bd.tile_table[2][1] = Tile(400, 400, 4, 1, 150, 250)  # white
    bd.tile_table[3][0] = Tile(400, 400, 4, 0, 50, 350)  # black

    # Diagonal: new_col > exist_col, new_row > exist_row
    count_flip = py.place_flip_tile((2, 2), (0, 0))
    assert count_flip == 1
    assert bd.tile_table[1][1].color == 0
    assert bd.tile_table[2][2].color == 0
    # Diagonal: new_col > exist_col, new_row < exist_row
    count_flip = py.place_flip_tile((0, 3), (3, 0))
    assert count_flip == 2
    assert bd.tile_table[0][3].color == 0
    assert bd.tile_table[2][1].color == 0
    assert bd.tile_table[1][2].color == 0

    # Test the simulation process:
    bd = Board(400, 400, 4)
    py = Player(1, bd, 2)    # white
    # Initial Status:
    assert py.board.tile_table[0][2] is None
    py.place_flip_tile((0, 2), (2, 2), simu=True)
    # When simu==True, the original board should not change.
    assert py.board.tile_table[0][2] is None


def test_update_tile_count():
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)     # black
    computer = Player(1, bd, 2)

    human.update_tile_count(1, True)
    assert human.tile_number == 4

    computer.update_tile_count(1, False)
    assert computer.tile_number == 1
