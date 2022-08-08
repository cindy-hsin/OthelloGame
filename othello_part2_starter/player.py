from board import Board
from tile import Tile


class Player:
    "A player of the game."
    def __init__(self, COLOR, board, BEGIN_TILE):
        """
        :Int COLOR: Color of the tile. 0 for Black, 1 for White.
        :Board board: The board of the game.
        :Int BEGIN_TILE: The player's inital number of tiles on the board.

        Initialize Player object.
        """
        self.COLOR = COLOR
        if self.COLOR == 0:
            self.COLOR_STR = "Black"
        elif self.COLOR == 1:
            self.COLOR_STR = "White"
        self.board = board
        self.tile_number = BEGIN_TILE   # Number of player's tiles on the board

    def __str__(self):
        """
        :return String: Player's color.
        Set player's color as its string representation"""
        return self.COLOR_STR

    def neighbor_oppo(self, i, j):
        """
        :Int i: Row index of the tile to be checked.
        :Int j: Column index of the tile to be checked.
        :return List neighbor_oppo_list: A list of (i,j)'s adjacent
                                         opponent's tiles.

        For a tile(index: i,j) of player's color,
        check if there exist adjacent tiles(index: m,n) of opponent's color.
        If yes, return their indexes in a list.
        """
        table = self.board.tile_table
        board_size = self.board.BOARD_SIZE

        neighbor_oppo_list = []
        neighbor_square = [(m, n)
                           for m in (i-1, i, i+1)
                           for n in (j-1, j, j+1)]
        neighbor_square.remove((i, j))
        for square in neighbor_square:
            m = square[0]
            n = square[1]
            if (m < board_size) and (m >= 0) and \
               (n < board_size) and (n >= 0):
                if (table[m][n] is not None) and \
                   (table[m][n].color == (1 - self.COLOR)):  # opponent's color
                    neighbor_oppo_list.append((m, n))
        return neighbor_oppo_list

    def legal_positions(self):
        """
        :return Dictionary legal_pos:
            {(legal_row, legal_col): [(exist_row, exist_col),
                                    (exist_row, exist_col)...], ...}

        Return a dictionary, whose keys are the (row, column) index tuple
        of legal positions, and values are corresonding (row, column) index
        tuples of all existing tiles that forms a flipping condition with
        the legal position.
        """
        table = self.board.tile_table
        board_size = self.board.BOARD_SIZE
        legal_pos = {}  # dictionary

        # Find legal positions and exisitng tile:

        # For each existing tile of the player's color(index: i,j):
        for i, row_list in enumerate(table):
            for j, item in enumerate(row_list):
                if (item is not None) and item.color == self.COLOR:

                    # For each tile of such, find the corresponding
                    # legal position, by finding the first empty position
                    # on the extension line. Return it as legal position.
                    for neigh_oppo in self.neighbor_oppo(i, j):
                        # m, n: the neighboring opponent's tile
                        m = neigh_oppo[0]
                        n = neigh_oppo[1]
                        diff_x = m - i
                        diff_y = n - j
                        # p, q: the square on the extended line of
                        #   player's (i,j) and opponent's (m,n)
                        p = m + diff_x
                        q = n + diff_y
                        while ((p < board_size) and (p >= 0) and
                               (q < board_size) and (q >= 0)) and \
                              (table[p][q] is not None) and \
                              (table[p][q].color == (1 - self.COLOR)):
                            p = p + diff_x
                            q = q + diff_y

                        # while stop condition:
                        # no legal position: (p,q out of range) or
                        #   (p,q has a tile AND is self.color)
                        # find legal position:
                        #   (p,q not out of range and has no tile)

                        if (p < board_size) and (p >= 0) and \
                           (q < board_size) and (q >= 0):
                            # If there is a tile in p,q:
                            if table[p][q] is None:
                                if (p, q) in legal_pos.keys():
                                    legal_pos[(p, q)].append((i, j))
                                else:
                                    legal_pos[(p, q)] = [(i, j)]
        return legal_pos

    def place_flip_tile(self, new_pos, exist_pos, simu=False):
        """
        :Tuple new_pos: row, column index of the square to place new tile
        :Tuple exist_pos: row, column index of the square with which
                          new_pos forms a flipping condition
        :Boolean simu: True if the function runs in simulation mode (for
                computer algorithm to predict result after the move).
        :return Int count_flip: The numbe of tiles being flipped.

        Place a tile of the player's color at new_pos in the board's
        tile_table, and increments the number of player's tiles on the board.

        Flip the tiles between new_pos and exist_pos.

        Return the number of tiles flipped
        """
        count_flip = self.board.place_flip_tile(new_pos, exist_pos,
                                                self.COLOR, simu)
        return count_flip

    def update_tile_count(self, count_flip, add):
        """
        :Int count_flip: The numbe of tiles being flipped.
        :Boolean add: True if this player's tile increase, False otherwise.
        """
        if add:
            self.tile_number += count_flip + 1
        else:
            self.tile_number -= count_flip
