import chess

PIECE_VALUES: dict[chess.PieceType, int] = {
    chess.KING: 0,
    chess.QUEEN: 900,
    chess.ROOK: 500,
    chess.BISHOP: 330,
    chess.KNIGHT: 320,
    chess.PAWN: 100,
}


def evaluate(board: chess.Board) -> int:
    score = 0

    for piece_type, value in PIECE_VALUES.items():
        white_count = len(board.pieces(piece_type, chess.WHITE))
        black_count = len(board.pieces(piece_type, chess.BLACK))

        score += (white_count - black_count) * value

    return score
