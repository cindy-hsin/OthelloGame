from computer import Computer
from board import Board
from tile import Tile


def test_constructor():
    bd = Board(400, 400, 4)
    computer = Computer(1, bd, 2, "local_max")
    assert computer.algo == "local_max"


def test_random_pick():
    bd = Board(400, 400, 4)
    computer = Computer(1, bd, 2, "random")

    # Board: One legal position form flipping condition with more than one
    # existing tile
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None  # Reset the board
    bd.tile_table[0][1] = Tile(400, 400, 4, 0, 150, 50)
    bd.tile_table[0][2] = Tile(400, 400, 4, 1, 250, 50)
    bd.tile_table[1][0] = Tile(400, 400, 4, 0, 50, 150)
    bd.tile_table[1][2] = Tile(400, 400, 4, 0, 250, 150)
    bd.tile_table[2][0] = Tile(400, 400, 4, 1, 50, 250)
    bd.tile_table[2][2] = Tile(400, 400, 4, 1, 250, 250)
    bd.tile_table[3][1] = Tile(400, 400, 4, 1, 150, 350)
    bd.tile_table[3][2] = Tile(400, 400, 4, 0, 250, 350)

    legal_pos = computer.legal_positions()
    p_e = computer.random_pick(legal_pos)
    pick_pos, exist_pos = p_e[0], p_e[1]
    assert type(pick_pos) == tuple
    assert type(exist_pos) == tuple
    assert pick_pos in legal_pos.keys()
    assert exist_pos in legal_pos[pick_pos]


def test_max_pick():
    # When one new_pos can flip different number of tiles,
    # it should always flip as many as possible.
    bd = Board(400, 400, 4)
    computer = Computer(1, bd, 2, "local_max")
    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None
    bd.tile_table[3][0] = Tile(400, 400, 4, 1, 50, 50)
    bd.tile_table[3][1] = Tile(400, 400, 4, 0, 50, 150)
    bd.tile_table[0][2] = Tile(400, 400, 4, 1, 50, 250)
    bd.tile_table[1][2] = Tile(400, 400, 4, 0, 150, 250)
    bd.tile_table[2][2] = Tile(400, 400, 4, 0, 250, 250)

    legal_pos = computer.legal_positions()
    p_e = computer.max_pick(legal_pos)
    pick_pos, exist_pos = p_e[0], p_e[1]

    assert pick_pos == (3, 2)
    assert exist_pos == (0, 2)  # but not (3, 0)


# The follwing section are a set of common variables used in
# test_max_weight_pick(), test_sort_pos_weight(), and test_score():
bd_w = Board(400, 400, 8)
computer_w = Computer(1, bd_w, 2, "local_max_weight")
# Reset the board for testing
for i in range(len(bd_w.tile_table)):
    for j in range(len(bd_w.tile_table[i])):
        bd_w.tile_table[i][j] = None
    bd_w.tile_table[1][1] = Tile(400, 400, 4, 0, 150, 150)
    bd_w.tile_table[3][1] = Tile(400, 400, 4, 0, 350, 150)
    bd_w.tile_table[2][2] = Tile(400, 400, 4, 0, 250, 250)
    bd_w.tile_table[3][2] = Tile(400, 400, 4, 0, 350, 250)
    bd_w.tile_table[3][3] = Tile(400, 400, 4, 1, 350, 350)
    bd_w.tile_table[4][3] = Tile(400, 400, 4, 0, 450, 350)
legal_pos_w = computer_w.legal_positions()


def test_score():
    assert computer_w.score(bd_w) == 27


def test_max_weight_pick():
    p_e = computer_w.max_weight_pick(legal_pos_w)
    pick_pos, exist_pos = p_e[0], p_e[1]
    assert pick_pos == (0, 0)  # but not (3, 0) or (5, 3)


def test_sort_pos_weight():
    sort_pos = computer_w.sort_pos_weight(legal_pos_w)
    # Each element in sort_pos: a key-value pair.
    # key: score.
    # value: a list of (new-pos, exist_pos) pairs with corresponding score
    assert sort_pos[0] == (97, [((0, 0), (3, 3))])
    assert sort_pos[1] == (36, [((5, 3), (3, 3))])
    assert sort_pos[2] == (28, [((3, 0), (3, 3))])
