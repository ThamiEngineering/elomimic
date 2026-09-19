from fastapi.testclient import TestClient

from elomimic_api.main import app

client = TestClient(app)


def test_bot_move_is_legal():
    legal = client.get("/moves").json()["moves"]

    response = client.post(
        "/bot/move",
        json={},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["move"] in legal


def test_bot_move_changes_turn_to_black():
    response = client.post(
        "/bot/move",
        json={},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["turn"] == "black"


def test_bot_move_on_game_over_returns_400():
    response = client.post(
        "/bot/move",
        json={"fen": "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Game over"


def test_bot_move_invalid_fen_returns_422():
    response = client.post(
        "/bot/move",
        json={"fen": "invalidFen"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid FEN"
