const API_URL: string = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export type Turn = "white" | "black";

export interface GameState {
  fen: string;
  turn: Turn;
  is_check: boolean;
  is_checkmate: boolean;
  is_stalemate: boolean;
  is_game_over: boolean;
}

export interface LegalMoves {
  fen: string;
  turn: Turn;
  count: number;
  moves: string[];
}

export interface BotMove extends GameState {
  move: string;
}

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, init);

  if (!response.ok) {
    const body: unknown = await response.json().catch(() => null);
    const detail =
      typeof body === "object" && body !== null && "detail" in body && typeof body.detail === "string"
        ? body.detail
        : response.statusText;
    throw new ApiError(response.status, detail);
  }

  return (await response.json()) as T;
}

function postJson(body: unknown): RequestInit {
  return {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  };
}

export function getLegalMoves(fen?: string): Promise<LegalMoves> {
  const query = fen ? `?${new URLSearchParams({ fen })}` : "";
  return request<LegalMoves>(`/moves${query}`);
}

export function playMove(fen: string, move: string): Promise<GameState> {
  return request<GameState>("/move", postJson({ fen, move }));
}

export function playBotMove(fen: string): Promise<BotMove> {
  return request<BotMove>("/bot/move", postJson({ fen }));
}
