from constants import RED, BLUE
from pieces import ChessPiece

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]  # it's a nested list comprehension in another list comprehension where it generates None
                                                                   # we use '_' so that we because were not using a loop variable, its just generating None
        self.current_player = BLUE                                 # Games starts with blue which is essentially white and while red is black
        self.selected_piece = None                                 # Keeps track of the selected piece's tuple (row,col)
        self.valid_moves = []                                      # all the valid moves the current piece can make, starts as empty list

        self.setup_board()                                         # This is an immediate call to initialize the board
        # self.red_king = None  # (Disabled line) We used to store references to the kings here.
        # self.blue_king = None # (Disabled line) Now we find them dynamically with find_king().

    def setup_board(self):
        piece_order = [
            ("R", 5), ("N", 3), ("B", 3), ("Q", 9), ("K", 100), ("B", 3), ("N", 3), ("R", 5)
            # chess board is symmetrical so it's the correct order for both sides  # is also just the back row
            # Tuples with the symbol and then value
        ]
        for i in range(8):
            self.board[0][i] = ChessPiece(RED, piece_order[i][0], piece_order[i][1], (0, i))      # we make the object and enter it on the field   # also this is matrix
            self.board[1][i] = ChessPiece(RED, "P", 1, (1, i))                                    # implement the Pawn
            self.board[6][i] = ChessPiece(BLUE, "P", 1, (6, i))
            self.board[7][i] = ChessPiece(BLUE, piece_order[i][0], piece_order[i][1], (7, i))

        # self.red_king =  self.board[0][4]  # (Disabled line) Instead, we'll find it when needed.
        # self.blue_king = self.board[7][4]  # (Disabled line) Instead, we'll find it when needed.
        # print(f"Initial setup - Blue king at: {self.blue_king.position}, Red king at: {self.red_king.position}")  # (Disabled line)

        # Instead we can do a debug print with find_king:
        red_king_pos = self.find_king(RED)          # the board tracks the red king, better for keeping it track, havent felt the need to do it other peices
        blue_king_pos = self.find_king(BLUE)        # the board tracks the blue king, better for keeping it track, havent felt the need to do it other peices
        print(f"Initial setup - Blue king at: {blue_king_pos}, Red king at: {red_king_pos}")

    def find_king(self, color):
        for row in range(8):                 # search every row
            for col in range(8):            # search every col
                piece = self.board[row][col]    # Wherever the king piece is on the baard
                if piece and piece.symbol == "K" and piece.color == color: # once you find your piece
                    return (row, col)  # return where they are
        return None  # Should never happen if the king is always on the board

    def can_piece_attack_square(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]
        if not piece:
            return False

        # Can't capture your own piece, so if there's a piece at the end
        # if it's the same color, return False immediately.
        if self.board[end_row][end_col] and self.board[end_row][end_col].color == piece.color:
            return False

        # Use the same "movement" logic as is_valid_move, except we don't check piece.color == self.current_player
        # and we don't check empty_square = not self.board[end_row][end_col] in the same way.
        # Just a minimal re-check of each piece's actual movement capability:

        # The board is a matrix from 0 to 7 range(8).
        if piece.symbol == "P":  # Pawn
            if piece.color == RED:  # if the piece is red,pawn captures moving down
                direction = 1
            else:                   # if the piece is blue ,pawn captures moving up
                direction = -1

            # Pawns capture diagonally by exactly 1 row, 1 col
            if abs(start_col - end_col) == 1 and end_row == start_row + direction:
                return True
            return False

        elif piece.symbol == "R":  # Rook
            # we use is_clear_path to check if everything in that direction is empty
            # and we do not allow diagonal movement
            return self.is_clear_path(start, end) and (start_row == end_row or start_col == end_col)

        elif piece.symbol == "N":  # Knight
            # This makes the L movement of the knight, either the knight can move 2 rows over then one column and vice versa
            return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
                   (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)

        elif piece.symbol == "B":  # Bishop
            # this allows the bishop to ONLY move diagonally
            return abs(start_row - end_row) == abs(start_col - end_col) and self.is_clear_path(start, end)  #basically slope

        elif piece.symbol == "Q":  # Queen
            # Queen can move anywhere that is clear
            row_diff = abs(start_row - end_row)
            col_diff = abs(start_col - end_col)
            if (start_row == end_row or start_col == end_col or row_diff == col_diff):
                return self.is_clear_path(start, end)
            return False

        elif piece.symbol == "K":  # King
            # King can move any direction like the queen but limit it to just one movement
            return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

        return False

    def is_valid_move(self, start, end):
        start_row, start_col = start       # The coordinates of the starting piece are put into two separate variables
        end_row, end_col = end             # The coordinates of where you want the piece to move, separated into two variables
        piece = self.board[start_row][start_col]  # we put the start position row and col into a TEMP variable named piece

        if not piece or piece.color != self.current_player:  # if it's an empty square, or the opponent's square, you cant move it thus return false
            return False

        if self.board[end_row][end_col] and self.board[end_row][end_col].color == self.current_player:
            # This makes sure we're not capturing our own piece.
            return False

        # The board is a matrix from 0 to 7 range(8),
        # blue starts on 7 and needs to advance by substracting until 0
        # red starts on 0 and needs to advance by adding  until 7

        if piece.symbol == "P":  # Pawn
            if piece.color == RED:  # if the piece is red, pawn moves "down" (row + 1)
                direction = 1
            elif piece.color == BLUE:  # if the piece is blue , pawn moves "up" (row - 1)
                direction = -1
            empty_square = not self.board[end_row][end_col]

            # The pawn can only move forward as long as the square is empty
            if start_col == end_col and empty_square:
                if end_row == start_row + direction:  # The end row should be equal to its current start row plus 1
                    return True
                if not piece.has_moved and end_row == start_row + 2 * direction and not \
                        self.board[start_row + direction][start_col]:
                    return True

            # pawns captures diagonally so it should only shift column 1 (once)
            if abs(start_col - end_col) == 1 and end_row == start_row + direction:
                return self.board[end_row][end_col] is not None

        elif piece.symbol == "R":  # Rook
            # we use is_clear_path to check if everything in that direction is empty
            return self.is_clear_path(start, end) and (start_row == end_row or start_col == end_col)

        elif piece.symbol == "N":  # Knight
            # This makes the L movement of the knight
            return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
                (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)

        elif piece.symbol == "B":  # Bishop
            # this allows the bishop to ONLY move diagonally
            return abs(start_row - end_row) == abs(start_col - end_col) and self.is_clear_path(start, end)

        elif piece.symbol == "Q":  # Queen
            # Queen can move anywhere that is clear
            row_diff = abs(start_row - end_row)
            col_diff = abs(start_col - end_col)
            if (start_row == end_row or start_col == end_col or row_diff == col_diff):
                return self.is_clear_path(start, end)
            return False

        elif piece.symbol == "K":  # King
            # King can move any direction like the queen but we limit it to just one movement
            return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

        return False

    def get_valid_moves(self, row, col):  # Collects all legal moves for a piece
        valid_moves = []  # list of all the legal moves for that piece
        for end_row in range(8):  # iterates through all rows
            for end_col in range(8):  # iterates through all columns
                if self.is_valid_move((row, col), (end_row, end_col)):  # if move is legal
                    valid_moves.append((end_row, end_col))  # add to the list
        return valid_moves  # after checking all valid moves, return it for the piece

    def is_clear_path(self, start, end):  # Checks if the path throughout the board is clear
        start_row, start_col = start   # original coordinate
        end_row, end_col = end  # destination coordinate
        row_step = 0
        col_step = 0
        # updates the row_step to the next available free spot
        if end_row > start_row:  # check step going forward (towards red)
            row_step = 1
        elif end_row < start_row:  # check step going backwards (towards blue)
            row_step = -1
        else:
            row_step = 0

        # updates the col_step to the next available free spot
        if end_col > start_col:  # check step going right
            col_step = 1
        elif end_col < start_col:  # check step going left
            col_step = -1
        else:
            col_step = 0

        row = start_row + row_step  # update row
        col = start_col + col_step  # update col

        while (row, col) != (end_row, end_col):  # continues before reaching the final coordinate
            if self.board[row][col]:  # checks if there's something occupying that exact spot
                return False  # exit before updating the values
            row += row_step   # Keep going by adding to row
            col += col_step   # Keep going by adding to col

        return True

    def switch_sides(self):
        if self.current_player == RED:  # We start with red here because it should only trigger after blue makes a move
            self.current_player = BLUE
        else:
            self.current_player = RED

    def make_move(self, start, end):  # start is the tuple of where the piece is now, end is the chosen destination
        if self.is_valid_move(start, end):  # First need to make sure you can make that move
            start_row, start_col = start
            end_row, end_col = end
            piece = self.board[start_row][start_col]  # the tuple of the original piece's location | Helper variable
            captured_piece = self.board[end_row][end_col]

            # Move the piece
            self.board[end_row][end_col] = piece  # now we update end point with where the piece must go
            self.board[start_row][start_col] = None  # make this empty now

            piece.position = (end_row, end_col)  # update the position attribute of the current piece
            piece.has_moved = True  # toggle flag for king, rook and pawn

            # print(f" Blue king at: {self.blue_king.position}, Red king at: {self.red_king.position}")  # (Disabled line)
            # Instead we do a debug print referencing find_king:
            print(f" Blue king at: {self.find_king(BLUE)}, Red king at: {self.find_king(RED)}")

            if self.is_check(piece.color):
                # Undo the move if it puts or leaves the player in check
                self.board[start_row][start_col] = piece  #starting  point
                self.board[end_row][end_col] = captured_piece   #end point
                piece.position = (start_row, start_col)   #reset the positon
                piece.has_moved = False # used for staring pawn movement
                print("Move canceled - would put/leave king in check")  # Debug print
                return False

            # Check for pawn promotion
            if piece.symbol == "P" and (end_row == 7 or end_row == 0):
                self.board[end_row][end_col] = ChessPiece(piece.color, "Q", 9, (end_row, end_col))  # Promote to Queen

            self.switch_sides()
            self.selected_piece = None  # Move complete no need to have it selected
            return True
        return False  # doesn't execute move, cannot be done

    def is_check(self, color):
        """
        Checks if the king of the given color is in check.
        We find the king's position via find_king(color), then see if an opposing piece
        can attack that position with can_piece_attack_square.
        """
        king_pos = self.find_king(color)
        if not king_pos:
            return False  # not expected in normal chess

        if color == BLUE:  # when RED is checking BLUE
            opponent_color = RED
        else:  # when BLUE is checking RED
            opponent_color = BLUE

        for row in range(8): #checking every row
            for col in range(8): #checking every col
                piece = self.board[row][col]    #put them in a variable
                if piece and piece.color == opponent_color:   #if opponent piece
                    if self.can_piece_attack_square((row, col), king_pos):  #if opponent piece has you in check
                        return True  # returns True if oppopnent has you  in check

        return False

    def is_checkmate(self, color):
        if not self.is_check(color): #must be in check to enter here checkmate
            return False

        for row in range(8): #check every row
            for col in range(8):  #check every col
                piece = self.board[row][col]   #record every row and col
                if piece and piece.color == color:   #the current player's pieces
                    valid_moves = self.get_valid_moves(row, col) #ONLY COMPARE Valid Possible otherwise were wasting our time
                    # what were basically going to be doing is checking every possible move that can be done a piece to see if get it gets the player out of check, else try again
                    for move in valid_moves:
                        # Try the move
                        original_piece = self.board[move[0]][move[1]] # record whatever is in the position where going to update
                        self.board[move[0]][move[1]] = piece #try a new valid move with that piece / update to new coordinate
                        self.board[row][col] = None  #delete old position

                        saved_pos = piece.position #save the pieces old position (the one it holds its self)
                        piece.position = (move[0], move[1]) #update the attribute position

                        still_in_check = self.is_check(color) #check if the king is still in check

                        # Undo the move / This is only supposed to be a simulation
                        self.board[row][col] = piece #restore
                        self.board[move[0]][move[1]] = original_piece #restore the original position
                        piece.position = saved_pos # restore attribute position

                        if not still_in_check: # no longer in check so you must exit is_checkmate
                            return False
        return True
