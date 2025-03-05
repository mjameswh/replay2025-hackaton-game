# Getting Started

1. Install uv
2. `cd backend`
   Install dependencies with `uv sync`

# Running the webserver

1. in one terminal run `uv run python src/main.py`
2. in another terminal run `uv run python -m websockets ws://localhost:8765/`
3. send messages from the second tab!
