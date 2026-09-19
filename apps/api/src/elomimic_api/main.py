import chess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="elomimic API")


class MoveRequest(BaseModel):
    fen: str = chess.STARTING_FEN
    move: str


class MoveResponse(BaseModel):
    fen: str
    turn: str
    is_check: bool
    is_checkmate: bool
    is_stalemate: bool
    is_game_over: bool


def parse_board(fen: str) -> chess.Board:
    try:
        return chess.Board(fen)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid FEN")


def parse_move(uci: str) -> chess.Move:
    try:
        return chess.Move.from_uci(uci)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid move format")


def turn_name(board: chess.Board) -> str:
    return "white" if board.turn == chess.WHITE else "black"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/moves")
def legal_moves(fen: str = chess.STARTING_FEN):
    board = parse_board(fen)
    moves = [move.uci() for move in board.legal_moves]

    return {
        "fen": board.fen(),
        "turn": turn_name(board),
        "count": len(moves),
        "moves": moves,
    }


@app.post("/move")
def play_move(request: MoveRequest) -> MoveResponse:
    board = parse_board(request.fen)
    move = parse_move(request.move)

    if move not in board.legal_moves:
        raise HTTPException(status_code=400, detail="Illegal move")

    board.push(move)

    return MoveResponse(
        fen=board.fen(),
        turn=turn_name(board),
        is_check=board.is_check(),
        is_checkmate=board.is_checkmate(),
        is_stalemate=board.is_stalemate(),
        is_game_over=board.is_game_over(),
    )
