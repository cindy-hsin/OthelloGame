from player import Player
import random
from copy import deepcopy


class Computer(Player):
    """A computer player. Inherits from Player class"""
    def __init__(self, COLOR, board, BEGIN_TILE, algo):
        """
        :Int COLOR: Color of the tile. 0 for Black, 1 for White.
        :Board board: The board of the game.
        :Int BEGIN_TILE: The player's inital number of tiles on the board.
        :String algo: Name of Computer's move selection algorithm.

        Initialize Player object.
        """
        self.algo = algo
        Player.__init__(self, COLOR, board, BEGIN_TILE)

    def random_pick(self, legal_pos):
        """
        :Dictionary legal_pos:
            {(legal_row, legal_col): [(exist_row, exist_col),
                                    (exist_row, exist_col)...], ...}
            dict value: A list of all indexes of exisiting tiles that
            form a flipping condition with the legal position(dict key).

        :return Tuple of Tuples (pick_pos, exist_pos): The tuple of
        (row,column) index tuples of the picked legal position and
        its corresponding existing position.

        Random algorithm. Randomly pick a legal position.
        """

        pick_pos = random.choice(list(legal_pos.keys()))
        # In case there are more than one exist_pos that forms
        # flipping condition with pick_pos, randomly choose one:
        exist_pos = random.choice(legal_pos[pick_pos])
        return (pick_pos, exist_pos)

    def max_pick(self, legal_pos):
        """
        :Dictionary legal_pos:
            {(legal_row, legal_col): [(exist_row, exist_col),
                                    (exist_row, exist_col)...], ...}
            dict value: A list of all indexes of exisiting tiles that
            form a flipping condition with the legal position(dict key).

        :return Tuple(of Tuples): The tuple of
        (row,column) index tuples of the picked legal position and
        its corresponding existing position.

        Local maximization algorithm. Pick the legal position that can flip
        the maximum number of opponent's tiles. If there're multiple maximum
        moves that flip the same amount of opponent's tiles, randomly pick one.
        """
        # Create a dictionary, whose keys are the number of flipped tiles, and
        # values are all pairs of legal position & existing position('s index
        # tuples) that flip this number of tiles.
        pos_count_flip = {}
        # structure: {count_flip: [(new_pos, exist_pos), (new_pos, exist_pos)]}

        for new_pos in legal_pos.keys():
            # new_pos: (new_pos_row, new_pos_column)
            for exist_pos in legal_pos[new_pos]:
                # exist_pos: (exist_pos_row, exist_pos_column)
                # Simulation mode
                count_flip = self.board.place_flip_tile(new_pos, exist_pos,
                                                        self.COLOR, simu=True)
                if count_flip in pos_count_flip.keys():
                    pos_count_flip[count_flip].append((new_pos, exist_pos))
                else:
                    pos_count_flip[count_flip] = [(new_pos, exist_pos)]

        # Sort pos_count_flip by key(i.e. count_flip)
        # sort_pos[0]: (max_count_flip,
        #               [all corresponding (new_pos, exist_pos) tuples])
        sort_pos = sorted(pos_count_flip.items(),
                          key=lambda x: x[0], reverse=True)

        # max_pos: A list of (new_pos, exist_pos) tuples with max count_flip
        max_pos = sort_pos[0][1]
        return random.choice(max_pos)

    def max_weight_pick(self, legal_pos):
        """
        :Dictionary legal_pos:
            {(legal_row, legal_col): [(exist_row, exist_col),
                                    (exist_row, exist_col)...], ...}
            dict value: A list of all indexes of exisiting tiles that
            form a flipping condition with the legal position(dict key).

        :return Tuple(of Tuples): The tuple of
        (row,column) index tuples of the picked legal position and
        its corresponding existing position.

        Local weight maximization algorithm. Evaluate each legal position with
        the weighted score based on the board after making the move.
        Pick the legal position that realizes the maximum weighted score.
        """
        sort_pos = self.sort_pos_weight(legal_pos)
        # max_weight_pos: A list of (new_pos, exist_pos) tuples with max score
        max_weight_pos = sort_pos[0][1]

        # If there are more than one pair of positions that
        # have same maximum scores, randomly pick one.
        return random.choice(max_weight_pos)

    def sort_pos_weight(self, legal_pos):
        """
        :Dictionary legal_pos:
            {(legal_row, legal_col): [(exist_row, exist_col),
                                    (exist_row, exist_col)...], ...}
            dict value: A list of all indexes of exisiting positions that
            form a flipping condition with the legal position(dict key).

        :return List(of lists) sort_pos: A sorted list of tuples made up of
        score and its corresponding combinations of legal position and
        exisiting position.

        Sort "legal position-existing position" pairs by
        weighted score. (max_weight_pick()'s helper function)
        """
        pos_count_flip = {}
        # For each combination of new_pos and exist_pos in legal_pos
        for new_pos in legal_pos.keys():
            for exist_pos in legal_pos[new_pos]:
                # Create a board for simulation.
                simu_board = deepcopy(self.board)
                simu_board.place_flip_tile(new_pos, exist_pos, self.COLOR)
                # Calculate the score after placing a tile at new_pos
                # and flip the tiles between new_pos & exist_pos
                score = self.score(simu_board)
                # Append to the dictionary for sorting
                if score in pos_count_flip.keys():
                    pos_count_flip[score].append((new_pos, exist_pos))
                else:
                    pos_count_flip[score] = [(new_pos, exist_pos)]
        # Sort pos_count_flip by key(i.e. score)
        sort_pos = sorted(pos_count_flip.items(),
                          key=lambda x: x[0], reverse=True)
        return sort_pos

    def score(self, board):
        """
        :Board board:
            A new board object for moves simulation and score calculation.
        :return Int score:
            The weighted score defined by computer's score minus human's score.
            computer's score: the sum of all square's
                "number of white tile at the square * weight of the square"
            human's score: the sum of all square's
                "number of black tile at the square * weight of the square"

        Calculate the weighted score based on a heuistic set of weights.
        Corners and not-adjacent-to-corner edges are weighted more heavily,
        while positions adjacent to corners and edges(that can easily lead to
        opponent's capturing corners and edges) are given negative weights.

        This function is sort_pos_weight()'s helper function.
        """
        # Reference for values in SQUARE_WEIGHTS:
        # http://dhconnelly.com/paip-python/docs/paip/othello.html#localmax
        SQUARE_WEIGHTS = [
            [120, -20,  20,   5,   5,  20, -20, 120],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [20,   -5,  15,   3,   3,  15,  -5,  20],
            [5,    -5,   3,   3,   3,   3,  -5,   5],
            [5,    -5,   3,   3,   3,   3,  -5,   5],
            [20,   -5,  15,   3,   3,  15,  -5,  20],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [120, -20,  20,   5,   5,  20, -20, 120]
        ]
        human_score = 0
        computer_score = 0
        for i, row_list in enumerate(board.tile_table):
            for j, item in enumerate(row_list):
                if item is not None and item.color == 0:
                    human_score += SQUARE_WEIGHTS[i][j]
                elif item is not None and item.color == 1:
                    computer_score += SQUARE_WEIGHTS[i][j]
        score = computer_score - human_score
        return score
