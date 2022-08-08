from tile import Tile


class Board:
    "A board."
    def __init__(self, WIDTH, HEIGHT, BOARD_SIZE):
        """
        :Int WIDTH: Width of the board.
        :Int HEIGHT: Height of the board.
        :Int BOARD_SIZE: Number of squares on each edge of the board.

        Initialize Board object.
        """
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.BOARD_SIZE = BOARD_SIZE

        if BOARD_SIZE == 0:
            self.tile_table = []
        else:
            self.SPACING = WIDTH / BOARD_SIZE
            # x,y coordinates of lines
            self.LINE_COORD = [i * self.SPACING
                               for i in range(1, self.BOARD_SIZE)]

            # Center tiles parameters
            CENTER_X = (self.WIDTH/2 - self.SPACING/2,
                        self.WIDTH/2 + self.SPACING/2)
            CENTER_Y = (self.HEIGHT/2 - self.SPACING/2,
                        self.HEIGHT/2 + self.SPACING/2)

            CENTER_ROW = (self.BOARD_SIZE // 2 - 1,
                          self.BOARD_SIZE // 2)
            CENTER_COL = (self.BOARD_SIZE // 2 - 1,
                          self.BOARD_SIZE // 2)

            # Container of TILE_TABLE objects
            self.tile_table = [[None] * self.BOARD_SIZE
                               for i in range(self.BOARD_SIZE)]

            # Create and Place center tiles
            for i, x in enumerate(CENTER_X):
                for j, y in enumerate(CENTER_Y):
                    if i == j:
                        t = Tile(WIDTH, HEIGHT, BOARD_SIZE, 1, x, y)
                    else:
                        t = Tile(WIDTH, HEIGHT, BOARD_SIZE, 0, x, y)
                    self.tile_table[CENTER_ROW[i]][CENTER_COL[j]] = t

    def display(self):
        """Display the board with lines and tiles."""
        # Draw the lines
        for x in self.LINE_COORD:
            line(x, 0, x, self.HEIGHT)
        for y in self.LINE_COORD:
            line(0, y, self.WIDTH, y)
        # Display tiles
        for row_list in self.tile_table:
            for item in row_list:
                if item:            # If item is a tile object (not None)
                    item.display()

    def mouse_location(self, mouse_x, mouse_y):
        """
        :Float mouse_x: The x coordinate of mouse press.
        :Float mouse_y: The y coordinate of mouse press.
        :return Tuple(of Ints) (row, col): The row and column index
        of the square on which the mouse pressed.

        Return the row index, column index of the mouse pressed square.
        """
        row = int(mouse_x//self.SPACING)     # int casting needed to run pytest
        column = int(mouse_y//self.SPACING)
        return (row, column)

    def place_flip_tile(self, new_pos, exist_pos, color, simu=False):
        """
        :Tuple new_pos: row, column index of the square to place the new tile
        :Tuple exist_pos: row, column index of the square with which new_pos
                          form a flipping condition
        :Int color: The color of the tile to be placed.
        :Boolean simu: True if the function runs in simulation mode (for
                       computer algorithm to predict result after the move).

        :return Int count_flip: The numbe of tiles being flipped.

        Create a tile with required x,y coordinate and color,
        and place it at the required indexes in tile_table.

        Then flip the tiles between new_pos and exist_pos.

        Return the number of flipped tiles.
        """
        # Place the new tile.
        new_row = new_pos[0]
        new_col = new_pos[1]
        new_x = new_row * self.SPACING + self.SPACING / 2
        new_y = new_col * self.SPACING + self.SPACING / 2
        if not simu:
            self.tile_table[new_row][new_col] = Tile(self.WIDTH, self.HEIGHT,
                                                     self.BOARD_SIZE, color,
                                                     new_x, new_y)

        # Flip the tile between new_pos and exist_pos.
        exist_row = exist_pos[0]
        exist_col = exist_pos[1]
        count_flip = 0
        # Horizontal:
        if new_row == exist_row:
            flip_row = new_row
            for dif_col in range(1, abs(new_col - exist_col)):
                if new_col > exist_col:
                    flip_col = exist_col + dif_col
                else:
                    flip_col = exist_col - dif_col
                if not simu:
                    # Change color
                    old_color = self.tile_table[flip_row][flip_col].color
                    self.tile_table[flip_row][flip_col].color = 1 - old_color
                # Change tile number
                count_flip += 1
        # Vertical:
        elif new_col == exist_col:
            flip_col = new_col
            for dif_row in range(1, abs(new_row - exist_row)):
                if new_row > exist_row:
                    flip_row = exist_row + dif_row
                else:
                    flip_row = exist_row - dif_row
                if not simu:
                    # Change color
                    old_color = self.tile_table[flip_row][flip_col].color
                    self.tile_table[flip_row][flip_col].color = 1 - old_color
                # Change tile number
                count_flip += 1
        # Diagonal:
        else:
            for dif in range(1, abs(new_row - exist_row)):
                # For Diagonal: dif_row = dif_col
                if new_col > exist_col:
                    flip_col = exist_col + dif
                else:
                    flip_col = exist_col - dif

                if new_row > exist_row:
                    flip_row = exist_row + dif
                else:
                    flip_row = exist_row - dif
                if not simu:
                    # Change color
                    old_color = self.tile_table[flip_row][flip_col].color
                    self.tile_table[flip_row][flip_col].color = 1 - old_color
                # Change tile number
                count_flip += 1
        return count_flip
