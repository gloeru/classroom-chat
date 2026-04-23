We would like to write a classroom messenger.
- As simple and basic as possible.
- Uses a simple, basic, commodity cloud service.
- Realised with simple Python code.
Software Engineering Methodology:
- We follow specification-driven development
- We use render.com


# Architecture

## Purpose
Simple web-based messenger with one page and one endpoint.

## Components
- Browser UI
- Flask app
- In-memory message store

## Endpoint
- `GET /` show page
- `POST /` send message

## Stack
- Python
- Flask
- Gunicorn
- HTML/CSS
- Render Web Service

## Files
- `app.py`
- `templates/index.html`
- `static/style.css`
- `requirements.txt`
- `render.yaml`
- `README.md`

## Deployment
Render Web Service with:
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

## Limitation
Messages are lost on restart or redeploy.

