import pygame
import sys
from constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, RED, BLUE
from board import ChessBoard
from gui import draw_board, draw_status

# Initialize Pygame
pygame.init()

def main():
    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # when starting the game it makes the screen 800x800 large
    pygame.display.set_caption("ASJ's Ultimate Chess")  # Names the application ASJ's Chess
    
    clock = pygame.time.Clock()  #controls the game speed
    board = ChessBoard()  # generate chess board

    # Track whether checkmate has happened
    game_over = False
    loser_color = None  # We can store who just got checkmated

    while True: #runs until player exits turn
        for event in pygame.event.get():  # Process all user inputs
            if event.type == pygame.QUIT: # if user presses the exit button on the window top right
                pygame.quit()
                sys.exit()

            # Only allow moves if the game is NOT over
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN: # <-- refers to button press
                col = event.pos[0] // SQUARE_SIZE  #Convert pixel to col
                row = event.pos[1] // SQUARE_SIZE  # convert pixel to row

                if board.selected_piece: # if a piece is selected
                    start = board.selected_piece # current starting position
                    end = (row, col)             # selected destination
                    if board.make_move(start, end): #  try to make the move
                        pass  # Move made successfully
                    else:
                        #move failed
                        board.selected_piece = None # deselect
                        board.valid_moves = []
                else: # No piece is selected
                    piece = board.board[row][col]  # current clicked position
                    if piece and piece.color == board.current_player: # if its the current players piece
                        board.selected_piece = (row, col) # selected piece
                        board.valid_moves = board.get_valid_moves(row, col)  # get the valid move that can be done for that piece

        # After any move, check if the CURRENT player is in checkmate.
        if not game_over:
            cur_color = board.current_player
            if board.is_check(cur_color) and board.is_checkmate(cur_color): # if both in check and checkmate
                game_over = True
                loser_color = cur_color
                # Or you could store winner_color if you prefer:
                # winner_color = (RED if cur_color == BLUE else BLUE)

        # Draw everything
        screen.fill(WHITE)  # make the screen WHITE
        draw_board(screen, board)
        draw_status(screen, board, game_over, loser_color)
        pygame.display.flip() #update the display
        clock.tick(60) #maintain 60 frames  per second


if __name__ == "__main__":
    main()
