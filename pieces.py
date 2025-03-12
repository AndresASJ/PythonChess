class ChessPiece:
    def __init__(self, color, symbol, value, position=None):
        self.color = color   # The color of the piece
        self.symbol = symbol # the rank of the piece | (P=Pawn, R=Rook, N=Knight, B=Bishop, Q=Queen, K=King)
        self.value = value   # The value of the piece | (Pawn=1, Knight/Bishop=3, Rook=5, Queen=9, King=100)
        self.has_moved = False # Flag Tracking, tells us if the piece moved from its original position.
                               # This is only important for pawns first move so it can move 2 places and castling king and rook
        self.position = position # attribute to make pieces keep track of their own position, mostly used to quickly reference where they are
