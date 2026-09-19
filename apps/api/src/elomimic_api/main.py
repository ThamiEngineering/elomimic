import chess
from fastapi import FastAPI, HTTPException

app = FastAPI(title="elomimic API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/moves")
def legal_moves(fen: str = chess.STARTING_FEN):
    try:
        board = chess.Board(fen)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid FEN")

    moves = [move.uci() for move in board.legal_moves]

    return {
        "fen": board.fen(),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "count": len(moves),
        "moves": moves,
    }
