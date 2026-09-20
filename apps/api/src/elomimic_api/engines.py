import random

import chess

from elomimic_api.evaluation import evaluate


def random_move(board: chess.Board) -> chess.Move:
    if board.is_game_over():
        raise ValueError("Game over")

    return random.choice(list(board.legal_moves))


def greedy_move(board: chess.Board) -> chess.Move:
    if board.is_game_over():
        raise ValueError("Game over")

    best_score = float("-inf")
    best_move: chess.Move | None = None

    for move in board.legal_moves:
        board.push(move)

        score = evaluate(board)

        board.pop()

        if score > best_score:
            best_move = move
            best_score = score

    assert best_move is not None
    return best_move
