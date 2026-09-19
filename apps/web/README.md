# elomimic-web

Web client for [elomimic](../../README.md), a chess engine that plays like a human at any target Elo.

A playable chessboard backed by the [elomimic API](../api/README.md). The client holds no chess logic: legal moves, move validation and engine replies all come from the API.

## Requirements

- [Node.js](https://nodejs.org/) 20.19+ or 22.12+ (required by Vite)
- [pnpm](https://pnpm.io/)
- The API running locally, see [apps/api](../api/README.md)

## Setup

```bash
pnpm install
```

## Run

```bash
pnpm dev
```

The app starts on http://localhost:5173 and expects the API on http://127.0.0.1:8000.

## Lint and build

```bash
pnpm lint
pnpm build
```

`pnpm build` type-checks the project with TypeScript before bundling.

## Configuration

| Variable       | Default                 | Description          |
| -------------- | ----------------------- | -------------------- |
| `VITE_API_URL` | `http://127.0.0.1:8000` | Base URL of the API  |

## How a turn works

1. The client loads the legal moves of the current position with `GET /moves`.
2. When a piece is dropped, the move is checked instantly against that list. An illegal drop never reaches the network.
3. A legal move is sent to `POST /move`, then the engine replies through `POST /bot/move`.
4. The legal moves of the new position are loaded, and the player moves again.

Pawn promotion currently always promotes to a queen.

## Stack

React, TypeScript, Vite, [react-chessboard](https://github.com/Clariity/react-chessboard), Oxlint.
