# 以农为本 - FastAPI app

This folder contains the FastAPI application that serves the static frontend and exposes the agent API and WebSocket endpoints. Place your static frontend files into the `static/` folder.

Key commands:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create DB tables:
   ```
   python create_tables.py
   ```

3. Run app (from `src`):
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
