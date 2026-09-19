import random

import chess


def random_move(board: chess.Board) -> chess.Move:
    return random.choice(list(board.legal_moves))
