# ASJ's PythonChess

A Python chess game with GUI built using Pygame.

## Features

- Standard chess rules implementation
- Visual highlighting of selected pieces and valid moves
- Check and checkmate detection
- Game state tracking

## Requirements

- Python 3.6+
- Pygame

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/AndresASJ/PythonChess.git
   cd PythonChess
   ```

2. Install dependencies:
   ```
   pip install pygame
   ```

3. Run the game:
   ```
   python main.py
   ```

## How to Play

1. Blue (equivalent to White in traditional chess) plays first
2. Click on a piece to select it - valid moves appear as yellow circles
3. Click on a highlighted position to move
4. Game status is displayed at the bottom of the screen

## Project Structure

- `main.py` - Game initialization and main loop
- `board.py` - Chess logic and move validation
- `pieces.py` - Chess piece class definition
- `gui.py` - Board and piece rendering functions
- `constants.py` - Game constants (colors, dimensions)

## Future Improvements

- Piece images instead of letter symbols
- Castling implementation
- En passant captures
- Additional pawn promotion options
- Move history
- Improved Color for pieces and board
