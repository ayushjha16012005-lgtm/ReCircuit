# ReCircuit Backend

Rule-based recovery decision engine and component-grading logic, exposed as
a small Flask API with SQLite-backed inventory storage.

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the API

```bash
python app.py
```

The API starts at `http://localhost:5000`. See [`../docs/API.md`](../docs/API.md)
for the full endpoint reference.

## Run the tests

```bash
python -m pytest tests/ -v
```

## Module guide

| File | Purpose |
|---|---|
| `vision_stub.py` | Placeholder for a real CV/ML component detector. Returns fixed demo detections. |
| `decision_engine.py` | Real, tested logic for recovery decisions and A/B/C/REJECT grading. |
| `database.py` | SQLite persistence for the recovered-component inventory. |
| `app.py` | Flask routes tying the above together. |
