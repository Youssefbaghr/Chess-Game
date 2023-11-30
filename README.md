# Chess Game

This is a simple Chess Game created using Python and Tkinter.

## How to Run

1. Clone the repository.
2. Install necessary dependencies using `pip install -r requirements.txt`.
3. Download the Stockfish chess engine from [Stockfish Official Website](https://stockfishchess.org/download/).
4. Place the Stockfish executable in the appropriate directory or update the path in `ChessGUI` class (`ai_move` method) to point to the Stockfish executable.
5. Run the game using `python src/main.py`.

## Rules

-   Players take turns to move pieces on the board.
-   The game ends when a player wins by checkmate or it ends in a draw.

## Features

-   GUI implemented using Tkinter.
-   Player can play against an AI powered by Stockfish engine.
-   Highlighting legal moves and capturing pieces.
-   Displaying captured pieces of the AI.

## File Structure

-   `main.py`: Initializes the game.
-   `chess_gui.py`: Contains the ChessGUI class.
-   `requirements.txt`: Contains necessary dependencies.

## Future Improvements

-   Implement castling and en passant moves.
-   Add a timer for each player.
-   Improve AI strategy.

**Note:** You need to download the Stockfish chess engine separately and configure the game to use it as the AI opponent.

Feel free to contribute or suggest improvements!
