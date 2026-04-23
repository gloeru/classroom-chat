# Classroom Messenger

Minimaler Classroom-Chat mit Flask und WebSocket.

## Endpoints

- `GET /` Chat-Seite
- `GET /healthz` Health-Check (`200 ok`)
- `GET /ws?name=...` WebSocket-Verbindung

## Stack

- Python
- Flask
- flask-sock
- Gunicorn
- HTML/CSS/Vanilla JS
- Render Web Service

## Lokal starten

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Dann `http://localhost:5000` öffnen.

## Render Deployment

- `render.yaml` ist bereits enthalten (Blueprint-Deployment).
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn --workers 1 --threads 64 --worker-class gthread --timeout 0 -b 0.0.0.0:$PORT app:app`
- Health check: `/healthz`
- Python-Version: siehe `runtime.txt`

## GitHub + Render End-to-End

Die vollständige Schritt-für-Schritt-Anleitung inkl. Nutzertest steht in `DEPLOYMENT.md`.

## Limitation

Nachrichten werden nicht persistent gespeichert und gehen bei Neustart verloren.
