class Tile:
    """A tile."""
    def __init__(self, WIDTH, HEIGHT, BOARD_SIZE, COLOR, x, y):
        """
        :Int WIDTH: Width of the board.
        :Int HEIGHT: Height of the board.
        :Int BOARD_SIZE: Number of squares on each edge of the board.
        :Int COLOR: Color of the tile. 0 for Black, 1 for White.
        :Int x: The x-coordinate of the tile.
        :Int y: The y-coordinate of the tile.

        Initialzie Tile object.
        """
        self.RADIUS = 0.9 * WIDTH/BOARD_SIZE

        # Tile color should not be constant. It can change when flipped.
        self.color = COLOR      # 0 for Black, 1 for White

        self.x = x
        self.y = y

    def display(self):
        """Display the tile."""
        fill(self.color)
        ellipse(self.x, self.y, self.RADIUS, self.RADIUS)
