# elomimic-api

HTTP API for [elomimic](../../README.md), a chess engine that plays like a human at any target Elo.

The API is stateless: the server stores no game. The client sends the position as a FEN string with every request.

## Requirements

- [uv](https://docs.astral.sh/uv/) (manages Python and dependencies)

## Setup

```bash
uv sync
```

## Run

```bash
uv run fastapi dev
```

The server starts on http://127.0.0.1:8000. Interactive documentation is available at http://127.0.0.1:8000/docs.

## Test and lint

```bash
uv run pytest -v
uv run ruff check
uv run ruff format
```

## Endpoints

| Method | Path     | Description                                              |
| ------ | -------- | -------------------------------------------------------- |
| GET    | `/health` | Liveness check                                          |
| GET    | `/moves`  | Legal moves for a position (`fen` query parameter)      |
| POST   | `/move`   | Play a move and return the new position and game state  |

### Errors

| Status | Meaning                                                  |
| ------ | -------------------------------------------------------- |
| 400    | The move is well-formed but illegal in the given position |
| 422    | Malformed input (invalid FEN, invalid move format, missing field) |

## Stack

FastAPI, Pydantic, [python-chess](https://python-chess.readthedocs.io/en/stable/), pytest, ruff.