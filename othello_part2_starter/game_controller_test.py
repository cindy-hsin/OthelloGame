from board import Board
from player import Player
from computer import Computer
from game_controller import GameController
from tile import Tile

STRATEGY = ["random", "local_max", "local_max_weight"]
# Tests in this module should pass for any algo in STRATEGY.
algo = STRATEGY[1]  # STRATEGY[0], STRATEGY[1], or STRATEGY[2]


def test_constructor():
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)

    assert gc.board is bd
    assert gc.human is human
    assert gc.computer is computer

    assert gc.human_turn
    assert not gc.game_end


def test_computer_move():
    # Case1:
    # Computer has legal moves-> Computer places a tile
    # -> Human has legal moves.
    # Result: Alternates the turn to Human.
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)

    # Simulate that human places the 1st tile at row 1 column 0.
    gc.board.tile_table[1][0] = Tile(400, 400, 4, 0, 150, 50)
    gc.board.tile_table[1][1] = Tile(400, 400, 4, 0, 150, 150)
    gc.human.tile_number = 4
    gc.computer.tile_number = 1
    gc.human_turn = False
    assert not gc.game_end  # Check the initial status

    # Computer makes move:
    gc.computer_move()
    # Check tile number updated
    assert gc.computer.tile_number == 3
    assert gc.human.tile_number == 3
    # Check turn alternated
    assert gc.human_turn
    assert not gc.game_end

    # Case2:
    # Computer has legal moves-> Computer places a tile
    # -> Human has no legal moves. -> Computer has legal moves.
    # Result: It should still be Computer's turn.
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)
    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None
    gc.board.tile_table[0][0] = Tile(400, 400, 4, 0, 50, 50)
    gc.board.tile_table[0][1] = Tile(400, 400, 4, 1, 50, 150)
    gc.board.tile_table[0][2] = Tile(400, 400, 4, 0, 50, 250)
    gc.board.tile_table[1][0] = Tile(400, 400, 4, 1, 150, 50)
    gc.board.tile_table[1][1] = Tile(400, 400, 4, 0, 150, 150)
    gc.board.tile_table[1][2] = Tile(400, 400, 4, 0, 150, 250)
    gc.board.tile_table[1][3] = Tile(400, 400, 4, 1, 150, 250)
    gc.board.tile_table[2][0] = Tile(400, 400, 4, 0, 250, 50)
    gc.board.tile_table[2][1] = Tile(400, 400, 4, 0, 250, 150)
    gc.board.tile_table[2][2] = Tile(400, 400, 4, 0, 250, 250)
    gc.board.tile_table[3][0] = Tile(400, 400, 4, 1, 350, 50)
    gc.board.tile_table[3][1] = Tile(400, 400, 4, 1, 350, 150)
    gc.board.tile_table[3][2] = Tile(400, 400, 4, 1, 350, 250)
    gc.human.tile_number = 7
    gc.computer.tile_number = 6
    gc.human_turn = False
    assert not gc.game_end  # Check the initial status

    # Computer has two legal positions. Makes move:
    gc.computer_move()

    # If computer's last move leads to Case2
    check_tile1 = gc.board.tile_table[0][3]
    check_flip_tile = gc.board.tile_table[0][2]
    if check_tile1 is not None and check_tile1.color == 1:
        if check_flip_tile is not None and check_flip_tile.color == 1:
            # Check tile number updated: only 1 tile is flipped
            assert gc.computer.tile_number == 8
            assert gc.human.tile_number == 6
        elif check_flip_tile is not None and check_flip_tile.color == 0:
            # 2 tiles are flipped.
            assert gc.computer.tile_number == 9
            assert gc.human.tile_number == 5
        # Since human has no legal moves, check it's still computer's turn
        assert not gc.human_turn
        # Since computer still has legal move, game isn't over.
        assert not gc.game_end

    # Elif computer's last move leads to Case1
    check_tile2 = gc.board.tile_table[2][3]
    if check_tile2 is not None and check_tile2.color == 1:
        # Check tile number updated
        assert gc.computer.tile_number == 8
        assert gc.human.tile_number == 6
        # Since human has legal moves, alternates the turn.
        assert gc.human_turn
        assert not gc.game_end

    # Case3:
    # Computer has legal moves-> Computer places a tile
    # -> Human has no legal moves. -> Computer has no legal moves either.
    # Result: End the game.

    # Case3 is the next step after Case2(computer places a tile at row 0 col 3)
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)
    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None
    bd.tile_table[0][0] = Tile(400, 400, 4, 0, 50, 50)
    bd.tile_table[0][1] = Tile(400, 400, 4, 1, 50, 150)
    bd.tile_table[0][2] = Tile(400, 400, 4, 1, 50, 250)
    bd.tile_table[0][3] = Tile(400, 400, 4, 1, 50, 350)
    bd.tile_table[1][0] = Tile(400, 400, 4, 1, 150, 50)
    bd.tile_table[1][1] = Tile(400, 400, 4, 0, 150, 150)
    bd.tile_table[1][2] = Tile(400, 400, 4, 0, 150, 250)
    bd.tile_table[1][3] = Tile(400, 400, 4, 1, 150, 350)
    bd.tile_table[2][0] = Tile(400, 400, 4, 0, 250, 50)
    bd.tile_table[2][1] = Tile(400, 400, 4, 0, 250, 150)
    bd.tile_table[2][2] = Tile(400, 400, 4, 0, 250, 250)
    bd.tile_table[3][0] = Tile(400, 400, 4, 1, 350, 50)
    bd.tile_table[3][1] = Tile(400, 400, 4, 1, 350, 150)
    bd.tile_table[3][2] = Tile(400, 400, 4, 1, 350, 250)
    gc.human.tile_number = 6
    gc.computer.tile_number = 8
    gc.human_turn = False
    assert not gc.game_end  # Check the initial status

    # Computer has only one legal position. Makes move:
    gc.computer_move()
    # Check tile number updated
    assert gc.computer.tile_number == 10
    assert gc.human.tile_number == 5
    # Check it's still computer's turn
    assert not gc.human_turn
    # Since both player have no legal moves, the game should end.
    assert gc.game_end


def test_human_move():
    # Case1:
    # Human has legal moves-> Human places a tile
    # -> Computer has legal moves.
    # Result: Alternates the turn to Human.
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)

    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None
    gc.board.tile_table[0][1] = Tile(400, 400, 4, 0, 50, 150)
    gc.board.tile_table[1][1] = Tile(400, 400, 4, 0, 150, 150)
    gc.board.tile_table[2][1] = Tile(400, 400, 4, 0, 250, 150)
    gc.board.tile_table[0][2] = Tile(400, 400, 4, 1, 50, 250)
    gc.board.tile_table[1][2] = Tile(400, 400, 4, 1, 150, 250)
    gc.board.tile_table[2][2] = Tile(400, 400, 4, 1, 250, 250)
    gc.human.tile_number = 3
    gc.computer.tile_number = 3

    gc.human_turn = True     # Appoint human's turn
    assert not gc.game_end   # Check initial status
    # Human makes move:
    gc.human_move(125, 367)
    # Check tile number updated
    assert gc.computer.tile_number == 2
    assert gc.human.tile_number == 5
    # Check turn alternated
    assert not gc.human_turn
    assert not gc.game_end

    # Case2
    # Human has legal moves-> Human places a tile
    # -> Computer has no legal moves. -> Human has legal moves.
    # Result: It should still be Human's turn.
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)
    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None
    gc.board.tile_table[2][0] = Tile(400, 400, 4, 1, 250, 50)
    gc.board.tile_table[3][0] = Tile(400, 400, 4, 0, 350, 50)
    gc.board.tile_table[0][1] = Tile(400, 400, 4, 0, 50, 150)
    gc.board.tile_table[1][1] = Tile(400, 400, 4, 1, 150, 150)
    gc.board.tile_table[2][1] = Tile(400, 400, 4, 0, 250, 150)
    gc.board.tile_table[3][1] = Tile(400, 400, 4, 0, 350, 150)
    gc.board.tile_table[0][2] = Tile(400, 400, 4, 0, 50, 250)
    gc.board.tile_table[1][2] = Tile(400, 400, 4, 0, 150, 250)
    gc.board.tile_table[2][2] = Tile(400, 400, 4, 1, 250, 250)
    gc.board.tile_table[3][2] = Tile(400, 400, 4, 0, 350, 250)
    gc.board.tile_table[0][3] = Tile(400, 400, 4, 0, 50, 350)
    gc.board.tile_table[1][3] = Tile(400, 400, 4, 1, 150, 350)
    gc.board.tile_table[2][3] = Tile(400, 400, 4, 1, 250, 350)
    gc.human.tile_number = 8
    gc.computer.tile_number = 5
    gc.human_turn = True
    assert not gc.game_end  # Check the initial status

    # Human makes move:s
    gc.human_move(310, 367)
    assert gc.human.tile_number == 11
    assert gc.computer.tile_number == 3
    # Check it's still Human's turn:
    assert gc.human_turn
    assert not gc.game_end

    # Case3:
    # Human has legal moves-> Human places a tile
    # -> Computer has no legal moves. -> Human has no legal moves.
    # Result: End the game.
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)
    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None
    gc.board.tile_table[0][0] = Tile(400, 400, 4, 1, 50, 50)
    gc.board.tile_table[1][0] = Tile(400, 400, 4, 0, 150, 50)
    gc.board.tile_table[2][0] = Tile(400, 400, 4, 0, 250, 50)
    gc.board.tile_table[3][0] = Tile(400, 400, 4, 0, 350, 50)
    gc.board.tile_table[0][1] = Tile(400, 400, 4, 1, 50, 150)
    gc.board.tile_table[1][1] = Tile(400, 400, 4, 1, 150, 150)
    gc.board.tile_table[2][1] = Tile(400, 400, 4, 0, 250, 150)
    gc.board.tile_table[3][1] = Tile(400, 400, 4, 0, 350, 150)
    gc.board.tile_table[0][2] = Tile(400, 400, 4, 1, 50, 250)
    gc.board.tile_table[1][2] = Tile(400, 400, 4, 0, 150, 250)
    gc.board.tile_table[2][2] = Tile(400, 400, 4, 1, 250, 250)
    gc.board.tile_table[1][3] = Tile(400, 400, 4, 1, 150, 350)
    gc.board.tile_table[2][3] = Tile(400, 400, 4, 1, 250, 350)
    gc.board.tile_table[3][3] = Tile(400, 400, 4, 1, 350, 350)

    gc.human.tile_number = 6
    gc.computer.tile_number = 8
    gc.human_turn = True
    assert not gc.game_end  # Check the initial status

    # Human makes move:s
    gc.human_move(310, 267)
    assert gc.human.tile_number == 8
    assert gc.computer.tile_number == 7
    # Check it's still Human's turn:
    assert gc.human_turn
    # Since both players have no legal moves, the game should end.
    assert gc.game_end

    # Case4: When one new_pos can flip different number of tiles,
    # it should always flip as many as possible.
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)
    # Reset the board for testing
    for i in range(len(bd.tile_table)):
        for j in range(len(bd.tile_table[i])):
            bd.tile_table[i][j] = None

    gc.board.tile_table[3][0] = Tile(400, 400, 4, 0, 50, 50)
    gc.board.tile_table[3][1] = Tile(400, 400, 4, 1, 50, 150)
    gc.board.tile_table[0][2] = Tile(400, 400, 4, 0, 50, 250)
    gc.board.tile_table[1][2] = Tile(400, 400, 4, 1, 150, 250)
    gc.board.tile_table[2][2] = Tile(400, 400, 4, 1, 250, 250)
    gc.human.tile_number = 2
    gc.computer.tile_number = 3
    gc.human_turn = True

    # Human makes moves
    gc.human_move(310, 267)
    # This move can flip 1 or 2 white tiles. It should choose to flip 2.
    assert gc.human.tile_number == 5
    assert gc.computer.tile_number == 1
    assert gc.board.tile_table[1][2].color == 0  # Flipped the 2-tile line.
    assert gc.board.tile_table[3][1].color == 1  # The 1-tile line stays still.
    assert not gc.human_turn
    assert not gc.game_end


def test_announce_turn():
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)
    assert gc.announce_turn() == "announce user's turn"
    gc.human_turn = False
    assert gc.announce_turn() == "announce computer's turn"


def test_result():
    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)
    assert gc.result == "Black: 2 v.s. White: 2"


def test_save_score():
    """NOTE: save_score() should be tested when "scores.txt" file
    has not been created in the directory."""
    def count_line(file):
        count = 0
        for line in file:
            count += 1
        return count

    bd = Board(400, 400, 4)
    human = Player(0, bd, 2)
    computer = Computer(1, bd, 2, algo)
    gc = GameController(bd, human, computer)

    # 1st round: no history.
    # There's no "scores.txt" in the directory.
    gc.human.tile_number = 15
    gc.save_score("Amy")
    f = open("scores.txt", "r")
    assert count_line(f) == 1
    f.seek(0, 0)
    assert f.readline() == "Amy 15\n"

    # 2nd round: break record.
    gc.human.tile_number = 40
    assert gc.save_score("Will James") is not None  # Name with space in it
    f = open("scores.txt", "r")
    assert count_line(f) == 2
    f.seek(0, 0)
    assert f.readline() == "Will James 40\n"
    assert f.readline() == "Amy 15\n"

    # 3rd round: Does not break record, but higher than some previous score.
    # Duplicate name.
    gc.human.tile_number = 26
    gc.save_score("Amy")
    f = open("scores.txt", "r")
    assert count_line(f) == 3
    f.seek(0, 0)
    assert f.readline() == "Will James 40\n"
    assert f.readline() == "Amy 15\n"
    assert f.readline() == "Amy 26\n"

    # 4th round: tie with highest score -> Is not written on the top.
    gc.human.tile_number = 40
    gc.save_score("C jr.")      # Name with space and dot in it
    f = open("scores.txt", "r")
    assert count_line(f) == 4
    f.seek(0, 0)
    assert f.readline() == "Will James 40\n"
    assert f.readline() == "Amy 15\n"
    assert f.readline() == "Amy 26\n"
    assert f.readline() == "C jr. 40\n"
