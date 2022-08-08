from board import Board
import random
import re


class GameController:
    "A game controller that monitors the game flow."
    def __init__(self, board, human, computer):
        """
        :Board board: The board of the game.
        :Player human: The human player of the game.
        :Player computer: The computer player of the game.

        Initialize GameController object.
        """
        self.board = board
        self.human = human
        self.computer = computer

        # Assign human player to go first
        self.human_turn = True
        self.game_end = False

    def computer_move(self):
        """Control the flow of moves when it's computer's turn."""
        legal_pos = self.computer.legal_positions()
        # If computer has legal positions
        if legal_pos:
            # Pick positions according to required algorithm
            if self.computer.algo == "random":
                p_e = self.computer.random_pick(legal_pos)
            elif self.computer.algo == "local_max":
                p_e = self.computer.max_pick(legal_pos)
            elif self.computer.algo == "local_max_weight":
                p_e = self.computer.max_weight_pick(legal_pos)
            pick_pos = p_e[0]
            exist_pos = p_e[1]

            # Place and flip tiles
            count_flip = self.computer.place_flip_tile(pick_pos, exist_pos)
            # Update tile number
            self.computer.update_tile_count(count_flip, True)
            self.human.update_tile_count(count_flip, False)

            # Go one step ahead: check if human has legal moves.
            # Otherwise, if human has no legal moves, game controller wouldn't
            # know it until human clicks the mouse once
            # (and triggers the checking in human_move() method).

            if self.human.legal_positions():
                # Change turn
                self.human_turn = True
                self.announce_turn()
            else:
                if self.computer.legal_positions():
                    print("User has no legal moves.")
                    self.announce_turn()   # Still Computer's turn.
                else:
                    # ENDING SITUATION: Computer places the last tile.
                    print("Both players have no legal moves. Game Over!")
                    # End the game
                    self.game_end = True

    def human_move(self, mouse_x, mouse_y):
        """
        :Float mouse_x: The x coordinate of mouse press.
        :Float mouse_y: The y coordinate of mouse press.

        Control the flow of moves when it's human's turn."""
        legal_pos = self.human.legal_positions()
        # If human has legal positions
        if legal_pos:
            # Convert mouse press to indexes
            pick_pos = self.board.mouse_location(mouse_x, mouse_y)
            # If mouse press is a legal move
            if pick_pos in legal_pos.keys():
                # Human Move Principle:
                # Pick the existing position with which pick_pos flips
                # the maximum number of tiles.
                # If there are more than one such exisiting positions,
                # randomly pick one.

                exist_pos = random.choice(legal_pos[pick_pos])  # initial pick
                base_count_flip = self.human.place_flip_tile(pick_pos,
                                                             exist_pos,
                                                             simu=True)
                # Pick the existing position that flips the most
                for ep in legal_pos[pick_pos]:
                    count_flip = self.human.place_flip_tile(pick_pos, ep,
                                                            simu=True)
                    if count_flip > base_count_flip:
                        base_count_flip = count_flip
                        exist_pos = ep

                # Place and flip tiles
                count_flip = self.human.place_flip_tile(pick_pos, exist_pos)
                # Update tile number
                self.human.update_tile_count(count_flip, True)
                self.computer.update_tile_count(count_flip, False)

                if self.computer.legal_positions():
                    self.human_turn = False
                    self.announce_turn()
                else:
                    if self.human.legal_positions():
                        print("Computer has no legal moves.")
                        self.announce_turn()         # Still human's turn.
                    else:
                        # ENDING SITUATION: Human places the last tile.
                        print("Both players have no legal moves. Game Over!")
                        # End the game
                        self.game_end = True

    def announce_turn(self):
        """Print to the terminal whose turn it is"""
        if self.human_turn:
            print("****USER'S TURN!****")
            return "announce user's turn"
        else:
            print("****COMPUTER'S TURN!****")
            return "announce computer's turn"  # return value for testing

    @property
    def result(self):
        """
        :return String: The string of game result.

        Returns a string that shows the number of tiles of each player.
        """
        return (str(self.human) + ": "
                + str(self.human.tile_number)
                + " v.s. "
                + str(self.computer) + ": "
                + str(self.computer.tile_number))

    def print_result(self):
        """Print results to the terminal"""
        if self.human.tile_number > self.computer.tile_number:
            print(str(self.human) + " Wins! " + self.result)
        elif self.human.tile_number < self.computer.tile_number:
            print(str(self.computer) + " Wins! " + self.result)
        else:
            print("TIE! " + self.result)

    def display_result(self):
        """Show result on Processing window"""
        TEXT_COLOR = (1, 0.5, 0)
        TEXT_SIZE = 20

        if self.game_end:
            fill(TEXT_COLOR[0], TEXT_COLOR[1], TEXT_COLOR[2])
            textSize(TEXT_SIZE)
            textAlign(CENTER)
            if self.human.tile_number > self.computer.tile_number:
                text(str(self.human)+" Wins!\n"+self.result,
                     self.board.WIDTH/2, self.board.HEIGHT/2)
            elif self.human.tile_number < self.computer.tile_number:
                text(str(self.computer)+" Wins!\n"+self.result,
                     self.board.WIDTH/2, self.board.HEIGHT/2)
            else:
                text("TIE!\n"+self.result,
                     self.board.WIDTH/2, self.board.HEIGHT/2)

    def save_score(self, name):
        """
        :String name: The name of human player entered by user.
        :return String history: History records in the text file
                                (for testing purpose).

        Save human player's number of tiles and name in scores.txt,
        where the highest user score is always the first entry in the file.
        """
        new_score = self.human.tile_number
        new_line = name + " " + str(new_score) + "\n"

        try:
            f = open("scores.txt", "r+")
        except:     # nopep8
            f = open("scores.txt", "w+")

        history = f.readlines()  # Cannot be f.read()!
        # Otherwise the following for loop won't work

        max_score = 0
        for line in history:
            score = int(re.findall(r"\s([0-9]+)", line)[0])
            if score > max_score:
                max_score = score

        if new_score > max_score:
            f.seek(0, 0)
            f.write(new_line)
            f.writelines(history)   # correspond to history = f.realines()
        else:
            f.write(new_line)
        f.close()
        return history      # return value for testing
