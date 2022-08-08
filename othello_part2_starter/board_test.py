from board import Board
from tile import Tile


def test_constructor():
    # Board size: 4
    bd = Board(400, 400, 4)
    assert bd.tile_table[1][1].color == 1
    assert bd.tile_table[2][1].color == 0
    assert bd.tile_table[1][2].color == 0
    assert bd.tile_table[2][2].color == 1

    # Board size: 2
    bd = Board(400, 400, 2)
    assert bd.tile_table[0][0].color == 1
    assert bd.tile_table[0][1].color == 0
    assert bd.tile_table[1][0].color == 0
    assert bd.tile_table[1][1].color == 1

    # Board size: 0
    bd = Board(400, 400, 0)
    assert bd.tile_table == []


def test_mouse_location():
    bd = Board(400, 400, 4)
    assert bd.mouse_location(120, 367) == (1, 3)
    assert type(bd.mouse_location(120, 367)[0]) == int


def test_place_flip_tile():
    bd = Board(400, 400, 4)

    # Board 1:
    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None
    bd.tile_table[0][2] = Tile(400, 400, 4, 0, 250, 50)  # black
    bd.tile_table[1][1] = Tile(400, 400, 4, 1, 150, 150)  # white
    bd.tile_table[1][2] = Tile(400, 400, 4, 1, 250, 150)  # white
    bd.tile_table[2][1] = Tile(400, 400, 4, 0, 150, 250)  # black
    bd.tile_table[2][2] = Tile(400, 400, 4, 1, 250, 250)  # white
    # Vertical: new_row < exist_row
    count_flip = bd.place_flip_tile((0, 1), (2, 1), 0)
    assert count_flip == 1
    assert bd.tile_table[0][1].color == 0
    assert bd.tile_table[1][1].color == 0
    # Vertical: new_row > exist_row
    count_flip = bd.place_flip_tile((3, 2), (0, 2), 0)
    assert count_flip == 2
    assert bd.tile_table[1][2].color == 0
    assert bd.tile_table[2][2].color == 0
    assert bd.tile_table[3][2].color == 0

    # Board 2:
    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None
    bd.tile_table[1][1] = Tile(400, 400, 4, 1, 150, 150)  # white
    bd.tile_table[1][2] = Tile(400, 400, 4, 1, 250, 150)  # white
    bd.tile_table[1][3] = Tile(400, 400, 4, 0, 350, 150)  # black
    bd.tile_table[2][0] = Tile(400, 400, 4, 1, 50, 250)   # black
    bd.tile_table[2][1] = Tile(400, 400, 4, 1, 150, 250)  # white
    # Horizontal: new_col < exist_col
    count_flip = bd.place_flip_tile((1, 0), (1, 3), 0)
    assert count_flip == 2
    assert bd.tile_table[1][0].color == 0
    assert bd.tile_table[1][1].color == 0
    assert bd.tile_table[1][2].color == 0
    # Horizontal: new_col > exist_col
    count_flip = bd.place_flip_tile((2, 2), (2, 0), 0)
    assert count_flip == 1
    assert bd.tile_table[2][1].color == 0
    assert bd.tile_table[2][2].color == 0

    # Board 3:
    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None
    bd.tile_table[0][3] = Tile(400, 400, 4, 0, 350, 50)  # black
    bd.tile_table[1][2] = Tile(400, 400, 4, 1, 250, 150)  # white
    bd.tile_table[2][1] = Tile(400, 400, 4, 1, 150, 250)  # white
    bd.tile_table[2][2] = Tile(400, 400, 4, 1, 250, 250)  # white
    # Diagonal: new_col < exist_col, new_row < exist_row
    count_flip = bd.place_flip_tile((1, 1), (3, 3), 0)
    assert count_flip == 1
    assert bd.tile_table[1][1].color == 0
    assert bd.tile_table[2][2].color == 0
    # Diagonal: new_col < exist_col, new_row > exist_row
    count_flip = bd.place_flip_tile((3, 0), (0, 3), 0)
    assert count_flip == 2
    assert bd.tile_table[3][0].color == 0
    assert bd.tile_table[2][1].color == 0
    assert bd.tile_table[1][2].color == 0

    # Board 4:
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
    count_flip = bd.place_flip_tile((2, 2), (0, 0), 0)
    assert count_flip == 1
    assert bd.tile_table[1][1].color == 0
    assert bd.tile_table[2][2].color == 0
    # Diagonal: new_col > exist_col, new_row < exist_row
    count_flip = bd.place_flip_tile((0, 3), (3, 0), 0)
    assert count_flip == 2
    assert bd.tile_table[0][3].color == 0
    assert bd.tile_table[2][1].color == 0
    assert bd.tile_table[1][2].color == 0

    # Test the simulation process:
    bd = Board(400, 400, 4)
    # Initial Status:
    assert bd.tile_table[0][2] is None
    bd.place_flip_tile((0, 2), (2, 2), 1, simu=True)
    # When simu==True, the original board should not change.
    assert bd.tile_table[0][2] is None
