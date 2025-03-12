import pygame
from constants import (
    ROWS, COLS, SQUARE_SIZE, WHITE, BLACK, GRAY, RED, BLUE, GREEN, YELLOW, WIDTH, HEIGHT
)

def draw_board(screen, board):
    for row in range(ROWS): # Go through all Row
        for col in range(COLS): # Go through all Cols
            if (row + col) % 2 == 0:
                color = WHITE # must start with WHITE
            else:
                color = GRAY  # After WHITE we can do gray, might change to BLACK if I get images for the peices
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board.board[row][col]   #check for piece in this coordinate
            if piece:  #if we find a piece in this coordinate
                font = pygame.font.Font(None, 72) #Size of letter (subject to change if I get images for pieces)
                text = font.render(piece.symbol, True, piece.color) # add the letter to represent the piece and the color assigned to it
                text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)) # center the letter pieces in the square
                screen.blit(text, text_rect) #draw hte piece on the screen

    if board.selected_piece: #if the piece is selected
        seleteced_row, seleteced_col = board.selected_piece    #get the row and col for the selected piece
        pygame.draw.rect(screen, GREEN, (seleteced_col * SQUARE_SIZE, seleteced_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4) #draw a GREEN square around the selected piece

        for move in board.valid_moves:  #after you have the selected piece , demonstrate the avialable moves
            move_row, move_col = move  # get the row and col for the selected piece
            pygame.draw.circle(screen, YELLOW,(move_col * SQUARE_SIZE + SQUARE_SIZE // 2, move_row * SQUARE_SIZE + SQUARE_SIZE // 2),10) # draw circle on the board to represent the available moves you can make


def draw_status(screen, board, game_over, loser_color): # current status of board
    font = pygame.font.Font(None, 36)  # font for the text

    if game_over: # Checkmate
        # Figure out who lost and who won
        if loser_color == RED:  # if RED loses then
            loser_str = "Red" #loser is RED
            winner_str = "Blue" #winner is BLUE
        else:                    # if the LOSER is BLUE
            loser_str = "Blue"   # LOSER is BLUE
            winner_str = "Red"   # WINNER is RED

        status = f"Checkmate! {loser_str} loses, {winner_str} wins!"  #  Declare the winner via text
        text = font.render(status, True, loser_color)  # # game over color
        screen.blit(text, (10, HEIGHT - 40)) # text at the bottom right

    else:
        # Game is still going: show the usual player info
        current_player = "Red" if board.current_player == RED else "Blue"
        text = font.render(f"Current Player: {current_player}", True, BLACK) #  color of text
        screen.blit(text, (10, HEIGHT - 40))  # bottom left

        # If in check
        if board.is_check(board.current_player):  # If the player is in check
            check_str = f"{current_player} is in check!"  # declare check
            check_text = font.render(check_str, True, board.current_player) # text details
            screen.blit(check_text, (WIDTH - 300, HEIGHT - 40)) #location of text, bottom right
