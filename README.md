# kk2-Oraklet
LLM-chain with FastAPI and SmolLLM


## How to install:
Open up git bash and navigate to the folder for where you clone to git to and then do the following:
```bash
python -m venv .venv
source .venv/Scripts/activate        # mac: .venv/bin/activate 
pip install -r requirements.txt
```

## How to Run:
```bash
uv run uvicorn app.main:app --reload
```

## How to run test examples:
```bash
uv run pytest app/tests/ -v
```


Then open 'http://127.0.0.1:8000/docs'

Disclaimer: "config.py is currently not in use as the program downloads the LLM on runtime instead of calling onto HuggingsFace API"

Due to limitations of the LLM used the program has been designed to only answer simple questions such as:
- "How many rows are there?"
- "How many columns are there?"
- "What is the highest X?"
- "What is the lowest X?"
- "What is the average X?"
- "Who/What had the highest X?"
- "Who/What had the lowest X?"

Where X is the information you want to find, such as age, salary, height, etc.

Asking anything outside of these question can lead to weird results.

Note: Sometimes the LLM will only return the answer and not a generated line of text to go along with it. Seems like this happens at random and only way to fix this is to restart the program.