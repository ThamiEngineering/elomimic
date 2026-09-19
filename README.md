# elomimic

[![CI](https://github.com/ThamiEngineering/elomimic/actions/workflows/ci.yml/badge.svg)](https://github.com/ThamiEngineering/elomimic/actions/workflows/ci.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

A chess engine that plays like a human at any target Elo.

Most engines answer "what is the best move?". elomimic answers a different question: "what would a 1200-rated player do here?". The goal is to learn `P(move | position, rating)` from millions of human games on Lichess, so the engine makes the same kind of choices, and the same kind of mistakes, as a real player of the requested level.

## Status

Early stage. The HTTP API, a baseline random engine and a playable web client are in place. No machine learning yet: the project is being built in the order of the roadmap below, and each phase ships working, tested code.

## Roadmap

- [x] **1. Software foundations**: stateless HTTP API, rules, tests, CI, playable web client
- [ ] **2. Classical engine**: evaluation function, minimax, alpha-beta pruning
- [ ] **3. Benchmarking**: tournament runner to measure engines against each other
- [ ] **4. Dataset**: Lichess game dumps, filtering and encoding by rating
- [ ] **5. PyTorch**: first neural move predictor
- [ ] **6. Elo-conditioned model**: one model, any target rating
- [ ] **7. Validation**: requested Elo vs measured Elo
- [ ] **8. Policy/value networks**, MCTS and self-play
- [ ] **9. Inference and serving**
- [ ] **10. LLM coach**: natural-language feedback on games

## Repository layout

```
apps/
  api/        FastAPI service: legal moves, move validation, bot moves
  web/        React client: playable chessboard backed by the API
```

See [apps/api](apps/api/README.md) and [apps/web](apps/web/README.md) for setup and details.

## Getting started

Requires [uv](https://docs.astral.sh/uv/), [Node.js](https://nodejs.org/) and [pnpm](https://pnpm.io/).

Start the API:

```bash
cd apps/api
uv sync
uv run fastapi dev
```

Then, in a second terminal, start the web client:

```bash
cd apps/web
pnpm install
pnpm dev
```

Open http://localhost:5173 and play against the engine.

## Related work

[Maia Chess](https://www.maiachess.com/) is the reference research project on human-like chess engines trained on Lichess games. elomimic is an independent learning project exploring the same problem from the ground up.

## License

[GPL-3.0](LICENSE). elomimic depends on [python-chess](https://python-chess.readthedocs.io/en/stable/), which is GPL-licensed.
