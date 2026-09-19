import { useEffect, useState } from "react";
import { Chessboard } from "react-chessboard";

import { ApiError, getLegalMoves, playBotMove, playMove } from "./api";
import type { GameState } from "./api";
import "./App.css";

type DropArgs = { sourceSquare: string; targetSquare: string | null };

function resolveMove(legalMoves: string[], from: string, to: string): string | null {
  const uci = `${from}${to}`;
  if (legalMoves.includes(uci)) return uci;

  const promotion = `${uci}q`;
  return legalMoves.includes(promotion) ? promotion : null;
}

function describeError(error: unknown): string {
  return error instanceof ApiError ? error.message : "The API is unreachable.";
}

function statusText(fen: string | null, state: GameState | null, busy: boolean): string {
  if (fen === null) return "Connecting to the API…";
  if (state?.is_checkmate) {
    return state.turn === "white" ? "Checkmate. Black wins." : "Checkmate. White wins.";
  }
  if (state?.is_stalemate) return "Stalemate. Draw.";
  if (state?.is_game_over) return "Game over. Draw.";
  if (busy) return "The engine is thinking…";
  if (state?.is_check) return "Check. Your move.";
  return "Your move.";
}

export default function App() {
  const [fen, setFen] = useState<string | null>(null);
  const [legalMoves, setLegalMoves] = useState<string[]>([]);
  const [state, setState] = useState<GameState | null>(null);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    getLegalMoves()
      .then((start) => {
        if (cancelled) return;
        setFen(start.fen);
        setLegalMoves(start.moves);
      })
      .catch((caught: unknown) => {
        if (!cancelled) setError(describeError(caught));
      })
      .finally(() => {
        if (!cancelled) setBusy(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  async function startNewGame() {
    setBusy(true);
    setError(null);

    try {
      const start = await getLegalMoves();
      setFen(start.fen);
      setLegalMoves(start.moves);
      setState(null);
    } catch (caught) {
      setError(describeError(caught));
    } finally {
      setBusy(false);
    }
  }

  async function playTurn(currentFen: string, move: string) {
    setBusy(true);
    setError(null);
    setLegalMoves([]);

    try {
      const afterPlayer = await playMove(currentFen, move);
      setFen(afterPlayer.fen);
      setState(afterPlayer);
      if (afterPlayer.is_game_over) return;

      const afterBot = await playBotMove(afterPlayer.fen);
      setFen(afterBot.fen);
      setState(afterBot);
      if (afterBot.is_game_over) return;

      const next = await getLegalMoves(afterBot.fen);
      setLegalMoves(next.moves);
    } catch (caught) {
      setError(describeError(caught));
    } finally {
      setBusy(false);
    }
  }

  function handlePieceDrop({ sourceSquare, targetSquare }: DropArgs): boolean {
    if (fen === null || targetSquare === null) return false;

    const move = resolveMove(legalMoves, sourceSquare, targetSquare);
    if (move === null) return false;

    void playTurn(fen, move);
    return true;
  }

  const gameOver = state?.is_game_over ?? false;

  return (
    <main className="app">
      <h1>elomimic</h1>

      <p className={error ? "status status--error" : "status"}>
        {error ?? statusText(fen, state, busy)}
      </p>

      {fen !== null && (
        <Chessboard
          options={{
            position: fen,
            boardOrientation: "white",
            allowDragging: !busy && !gameOver,
            onPieceDrop: handlePieceDrop,
          }}
        />
      )}

      <button type="button" disabled={busy} onClick={() => void startNewGame()}>
        New game
      </button>
    </main>
  );
}
