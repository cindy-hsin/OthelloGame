# OthelloGame

* A graphical game of Othello that allows human players to play against computer opponent. Written in Python/Processing. 

## Project Highlights:
1. Implemented DFS algorithm to validate player’s moves; applied greedy algorithm and corner-edge strategy to optimize computer’s moves, reaching a winning rate of 80%.
2. Created GUI with a clickable chessboard and real-time scoreboard with Processing and Java Swing; conducted unit testing with Pytest that achieved a line coverage of 95%.

## Game Rules and UI Instructions: 
The game is played with black-and-white tiles on an 8x8 board. The object of the game is to have more tiles of your color than your opponent has of theirs. Play begins with 4 tiles in the middle, two white and two black, like this:

<img src="https://user-images.githubusercontent.com/66403829/183505434-cf3267ed-8d6a-43b4-b198-bd7a9dba4e91.png" alt="drawing" width="400"/>

Black(human player) goes first. The player clicks a square to lay down a tile, which must be in a legal position. Any white tiles in between the new black tile and an existing black tile get flipped. Here’s what happens if I put a black tile above the northwest white tile -- it flips and becomes a black tile, so now I’m winning:

<img src="https://user-images.githubusercontent.com/66403829/183505474-d098a66b-5848-4f92-b0bd-b3025a1b5f7a.png" alt="drawing" width="400"/>


White(computer player) and black continue to take turns until eventually the board fills up and there are no more legal moves. In the finished game below the computer has won 42 to 22:

<img src="https://user-images.githubusercontent.com/66403829/183505514-65879a7b-ab11-4972-aab2-6a275e5a2257.png" alt="drawing" width="400"/>


### Legal moves
For a move to be legal, a tile must be placed such that at least one opposing tile will be flipped. Suppose I’m playing the white tiles, and I have the board depicted above, right after that first move. Here are the legal moves (any other square would be illegal and the game will not allow me to place a tile in such square):

<img src="https://user-images.githubusercontent.com/66403829/183505553-40d8c4b5-4a01-4a49-b442-9e40696c7372.png" alt="drawing" width="400"/>


### Ending the game
When the board is completely covered in tiles, or there are no more legal moves, then the game is over. Whichever player has more tiles of their color on the board wins. Ties can happen, too. The game will announce the winner with the number of tiles they have on the board, and prompt the user for their name to save their name and score in the "scores.txt" file. The highest user score will always be on the top in "scores.txt".

<img src="https://user-images.githubusercontent.com/66403829/183506820-9c4483b4-3bb1-43a1-9383-36cb6feb3873.png" alt="drawing" width="400"/>

