from fastapi.testclient import TestClient

from elomimic_api.main import app

client = TestClient(app)


def test_starting_position_has_20_legal_moves():
    response = client.get("/moves")

    assert response.status_code == 200
    data = response.json()
    assert data["turn"] == "white"
    assert data["count"] == 20
    assert "e2e4" in data["moves"]


def test_black_to_move():
    response = client.get(
        "/moves",
        params={"fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["turn"] == "black"
    assert data["count"] == 20
    assert "e7e5" in data["moves"]


def test_invalid_fen_returns_422():
    response = client.get(
        "/moves",
        params={"fen": "invalidFen"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid FEN"
