import chess
import pytest

from elomimic_api.engines import greedy_move, random_move


@pytest.mark.parametrize(
    "engine",
    [
        random_move,
        greedy_move,
    ],
)
@pytest.mark.parametrize(
    "fen",
    [
        pytest.param(
            "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1",
            id="stalemate",
        ),
        pytest.param(
            "7k/6Q1/6K1/8/8/8/8/8 b - - 0 1",
            id="checkmate",
        ),
    ],
)
def test_engine_on_game_over(engine, fen):
    board = chess.Board(fen)

    with pytest.raises(ValueError, match="Game over"):
        engine(board)


def test_greedy_move_captures_hanging_queen():
    board = chess.Board("q6k/8/8/8/8/8/8/R3K3 w - - 0 1")

    move = greedy_move(board)

    assert move == chess.Move.from_uci("a1a8")


def test_greedy_move_black_captures_hanging_queen():
    board = chess.Board("r5k1/8/8/8/8/8/8/Q3K3 b - - 0 1")

    move = greedy_move(board)

    assert move == chess.Move.from_uci("a8a1")


def test_greedy_move_does_not_modify_board():
    board = chess.Board("q6k/8/8/8/8/8/8/R3K3 w - - 0 1")
    fen_before = board.fen()

    greedy_move(board)

    assert board.fen() == fen_before
