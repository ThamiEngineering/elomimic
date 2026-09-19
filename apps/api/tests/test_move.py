from fastapi.testclient import TestClient

from elomimic_api.main import app

client = TestClient(app)


def test_e2e4_returns_black_turn():
    response = client.post(
        "/move",
        json={"move": "e2e4"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["turn"] == "black"
    assert data["is_check"] is False


def test_illegal_move_returns_400():
    response = client.post(
        "/move",
        json={"move": "e2e5"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Illegal move"


def test_invalid_move_format_returns_422():
    response = client.post(
        "/move",
        json={"move": "zzz"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid move format"


def test_missing_move_field_returns_422():
    response = client.post(
        "/move",
        json={},
    )

    assert response.status_code == 422


def test_fools_mate():
    response = client.post(
        "/move",
        json={
            "fen": "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2",
            "move": "d8h4",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["is_check"] is True
    assert data["is_checkmate"] is True
    assert data["is_game_over"] is True
    assert data["is_stalemate"] is False
