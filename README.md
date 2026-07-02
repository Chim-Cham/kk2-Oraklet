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
