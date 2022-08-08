from board import Board
from player import Player
from computer import Computer
from game_controller import GameController

"""
NOTES: In this program, "row" refers to the index in x direction,
"column" refers to the index in y directino.

A board's tile_table data structure like this:
[[None, None, 1, None],
 [None, None, None, None],
 [None, None, None, None],
 [None, None, None, None]]

refers to a board display(in Processing) like this:
    -> row
    |   Empty, Empty, Empty, Empty
    V   Empty, Empty, Empty, Empty
   col  Black, Empty, Empty, Empty
        Empty, Empty, Empty, Empty
where tile_table[0][3] refers to the black tile.
"""

WIDTH = 400
HEIGHT = 400
BOARD_SIZE = 8     # BOARD_SIZE rows * BOARD_SIZE columns
BEGIN_TILE = 2     # The start number of tiles for each player

DELAY = 100

STRATEGY = ["random", "local_max", "local_max_weight"]

BACK_COLOR = (0, 0.3, 0.1)

algo = STRATEGY[1]
board = Board(WIDTH, HEIGHT, BOARD_SIZE)
human = Player(0, board, BEGIN_TILE)
computer = Computer(1, board, BEGIN_TILE, algo)
gc = GameController(board, human, computer)

computer_count_down = DELAY
result_count_down = DELAY


def setup():
    """Set up Processing window"""
    size(WIDTH, HEIGHT)
    colorMode(RGB, 1)
    gc.announce_turn()  # Initially announce it's user's turn


def input(message=''):
    """Prompt for user's name for saving game result."""
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)


def draw():
    """Update Processing window"""
    global computer_count_down, result_count_down
    background(BACK_COLOR[0], BACK_COLOR[1], BACK_COLOR[2])

    if not gc.human_turn:
        if computer_count_down > 0:
            computer_count_down -= 1
        else:
            gc.computer_move()
            computer_count_down = DELAY

    board.display()

    if gc.game_end:
        gc.display_result()

        if result_count_down > 0:
            result_count_down -= 1
        else:
            gc.print_result()
            # Prompt for user's name until getting non-empty string
            human_name = input("Enter your name: ")
            while not human_name:
                human_name = input("Enter your name: ")
            gc.save_score(human_name)
            noLoop()
            # Use noLoop() to avoid non-stop looping of
            # printing result to the terminal
            # and prompting for input


def mousePressed():
    """Control the flow after each mouse press."""
    if gc.human_turn:
        gc.human_move(mouseX, mouseY)
