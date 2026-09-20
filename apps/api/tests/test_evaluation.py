import chess
import pytest

from elomimic_api.evaluation import evaluate


@pytest.mark.parametrize(
    ("fen", "expected_score"),
    [
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            0,
        ),
        (
            "rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            900,
        ),
        (
            "4k3/8/8/8/8/8/8/4K3 w - - 0 1",
            0,
        ),
    ],
)
def test_evaluate_material(fen: str, expected_score: int):
    board = chess.Board(fen)

    assert evaluate(board) == expected_score


@pytest.mark.parametrize(
    "fen",
    [
        "4k3/8/8/8/8/8/8/R3K3 w - - 0 1",
        "4k3/8/8/8/8/8/6pp/4K3 w - - 0 1",
        "4k3/8/8/8/8/2B5/6p1/4K3 w - - 0 1",
    ],
)
def test_evaluate_is_symmetric(fen: str):
    board = chess.Board(fen)

    assert evaluate(board.mirror()) == -evaluate(board)
