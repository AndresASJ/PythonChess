# Detailed Analysis of `board.py` Functions

## `__init__(self)`

**Purpose**: Initializes a new chess board and sets up initial game state variables.

**Parameters**: None

**Return Value**: None (constructor implicitly returns instance)

### Detailed Behavior:

- Creates `self.board` as an 8×8 grid using nested list comprehensions:
    - Outer loop creates 8 rows
    - Inner loop creates 8 columns initialized with `None`
- Sets `self.current_player` to the `BLUE` constant (representing White, who moves first)
- Initializes `self.selected_piece` to `None` (will hold tuple `(row, col)` of the selected piece)
- Creates an empty list for `self.valid_moves` to store valid move positions
- Calls `self.setup_board()` immediately to populate the board
- Note: Previous explicit king reference tracking removed in favor of dynamic `find_king()` method

**Importance**:

- Establishes the foundational game state according to chess rules
- Explicitly defines initial conditions crucial for game integrity

---

## `setup_board(self)`

**Purpose**: Sets pieces on the board in standard chess starting positions.

**Parameters**: None

**Return Value**: None

### Detailed Behavior:

- Defines `piece_order` list containing piece symbols and values for back row:
    - Order: Rook(5), Knight(3), Bishop(3), Queen(9), King(100), Bishop(3), Knight(3), Rook(5)
- Uses loops to place pieces:
    - `RED` back row at row `0`, pawns at row `1`
    - `BLUE` pawns at row `6`, back row at row `7`
- Pieces instantiated as `ChessPiece` objects with color, symbol, value, and position
- Logs positions of both kings by calling `find_king()` for debugging

**Importance**:

- Essential for initializing standard chess gameplay
- Creates initial conditions necessary for the game's progression

---

## `find_king(self, color)`

**Purpose**: Finds the specified color's king on the board.

**Parameters**:

- `color`: Either `RED` or `BLUE`

**Return Value**:

- Tuple `(row, col)` if king found, else `None`

### Detailed Behavior:

- Iterates over the entire board to find the king matching the color and symbol (`"K"`)
- Immediately returns position upon finding the king

**Importance**:

- Essential for detecting checks/checkmates
- Provides a robust and reliable method of king location

---

## `can_piece_attack_square(self, start, end)`

**Purpose**: Determines if a piece at `start` position can attack the piece at `end` position.

**Parameters**:

- `start`: `(row, col)` of attacker
- `end`: `(row, col)` of target

**Return Value**: Boolean

### Detailed Behavior:

- Retrieves attacking piece, returns `False` immediately if no piece or friendly fire attempt
- Implements attack logic per piece type (pawn, rook, knight, bishop, queen, king)
- Uses `is_clear_path` for applicable pieces (rook, bishop, queen)

**Importance**:

- Critical for accurate detection of checks
- Clarifies distinct logic for attacking versus general moves

---

## `is_valid_move(self, start, end)`

**Purpose**: Validates legality of a move from `start` to `end` positions.

**Parameters**:

- `start`: Current position `(row, col)`
- `end`: Destination position `(row, col)`

**Return Value**: Boolean

### Detailed Behavior:

- Checks piece existence, color turn order, and friendly fire prevention
- Implements detailed chess rules per piece (pawn, rook, knight, bishop, queen, king)
- Uses `is_clear_path` where applicable

**Importance**:

- Core enforcement of chess rules
- Ensures only legal moves can occur

---

## `get_valid_moves(self, row, col)`

**Purpose**: Provides list of all legal move destinations for a given piece.

**Parameters**:

- `row`: Row index (0-7)
- `col`: Column index (0-7)

**Return Value**: List of tuples `(row, col)`

### Detailed Behavior:

- Iterates over all squares, collecting moves validated by `is_valid_move`

**Importance**:

- Critical for UI interaction (highlighting moves)
- Essential for checkmate logic and move validation

---

## `is_clear_path(self, start, end)`

**Purpose**: Checks if the path between two squares is unobstructed.

**Parameters**:

- `start`: Starting position `(row, col)`
- `end`: Ending position `(row, col)`

**Return Value**: Boolean

### Detailed Behavior:

- Iteratively checks intermediate squares for obstructions based on movement direction

**Importance**:

- Prevents illegal moves involving piece teleportation
- Core to rook, bishop, queen movement logic

---

## `switch_sides(self)`

**Purpose**: Switches active player after a valid move.

**Parameters**: None

**Return Value**: None

### Detailed Behavior:

- Alternates `self.current_player` between `RED` and `BLUE`

**Importance**:

- Controls player turns
- Maintains game flow

---

## `make_move(self, start, end)`

**Purpose**: Executes a validated chess move.

**Parameters**:

- `start`: Starting position `(row, col)`
- `end`: Destination position `(row, col)`

**Return Value**: Boolean (move success)

### Detailed Behavior:

- Validates move with `is_valid_move`
- Updates board state and piece attributes upon valid move
- Checks for resulting checks, reverting if move places own king in danger
- Implements pawn promotion to queen automatically upon reaching opposite end
- Switches turns

**Importance**:

- Implements comprehensive move execution logic
- Maintains game state consistency

---

## `is_check(self, color)`

**Purpose**: Checks if king of given color is threatened.

**Parameters**:

- `color`: Either `RED` or `BLUE`

**Return Value**: Boolean

### Detailed Behavior:

- Finds king position, checks all opponent pieces for threats

**Importance**:

- Central to maintaining legality of moves
- Critical to checkmate detection

---

## `is_checkmate(self, color)`

**Purpose**: Determines if a player is checkmated.

**Parameters**:

- `color`: Player color (`RED` or `BLUE`)

**Return Value**: Boolean

### Detailed Behavior:

- Checks for check status
- Tests all possible moves to see if escape from check is possible
- Declares checkmate if no escape exists

**Importance**:

- Game-ending logic
- Most advanced chess logic component

---

Each function in `board.py` is integral, working cohesively to uphold the rules and logic of chess, ensuring an accurate and enjoyable gameplay experience.