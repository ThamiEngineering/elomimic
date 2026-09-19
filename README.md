# elomimic

[![CI](https://github.com/ThamiEngineering/elomimic/actions/workflows/ci.yml/badge.svg)](https://github.com/ThamiEngineering/elomimic/actions/workflows/ci.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

A chess engine that plays like a human at any target Elo.

Most engines answer "what is the best move?". elomimic answers a different question: "what would a 1200-rated player do here?". The goal is to learn `P(move | position, rating)` from millions of human games on Lichess, so the engine makes the same kind of choices, and the same kind of mistakes, as a real player of the requested level.

## Status

Early stage. The HTTP API and a baseline random engine are in place. No machine learning yet: the project is being built in the order of the roadmap below, and each phase ships working, tested code.

## Roadmap

- [ ] **1. Software foundations**: stateless HTTP API, rules, tests, CI *(in progress)*
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
```

See [apps/api](apps/api/README.md) for setup, endpoints and error codes.

## Getting started

Requires [uv](https://docs.astral.sh/uv/).

```bash
cd apps/api
uv sync
uv run fastapi dev
```

Then open http://127.0.0.1:8000/docs.

## Related work

[Maia Chess](https://www.maiachess.com/) is the reference research project on human-like chess engines trained on Lichess games. elomimic is an independent learning project exploring the same problem from the ground up.

## License

[GPL-3.0](LICENSE). elomimic depends on [python-chess](https://python-chess.readthedocs.io/en/stable/), which is GPL-licensed.