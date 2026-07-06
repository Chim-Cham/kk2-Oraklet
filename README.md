# kk2-Oraklet
LLM-chain with FastAPI and SmolLLM


## How to install:
```bash
python -m venv .venv
source .venv/Scripts/activate        # mac: .venv/bin/activate 
pip install -r requirements.txt
```

## How to Run:
```bash
uv run uvicorn app.main:app --reload
```

Then open 'http://127.0.0.1:8000/docs'

Disclaimer: "config.py is currently not in use as the program downloads the LLM on runtime instead of calling onto HuggingsFace API"

Due to limitations of the LLM used the program has been designed to only answer simple questions such as:
- "How many rows are there?"
- "How many columns are there?"
- "What is the highest X?"
- "What is the lowest X?"
- "What is the average X?"

Asking anything outside of these question can lead to weird results.