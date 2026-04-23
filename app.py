import eventlet
eventlet.monkey_patch()

import json
import threading
import time

from flask import Flask, render_template, request
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)


class _State:
    def __init__(self):
        self.lock = threading.Lock()
        self.clients: dict = {}  # socket -> display name


state = _State()


def _clean(value: str, limit: int) -> str:
    return value.strip()[:limit]


def _broadcast(payload: str):
    dead = []
    with state.lock:
        targets = list(state.clients.keys())
    for ws in targets:
        try:
            ws.send(payload)
        except Exception:
            dead.append(ws)
    if dead:
        with state.lock:
            for ws in dead:
                state.clients.pop(ws, None)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/healthz")
def healthz():
    return "ok", 200


@sock.route("/ws")
def ws_handler(ws):
    name = _clean(request.args.get("name", ""), 40)
    if not name:
        ws.close()
        return

    with state.lock:
        state.clients[ws] = name

    try:
        while True:
            data = ws.receive()
            if data is None:
                break
            try:
                frame = json.loads(data)
            except (ValueError, TypeError):
                continue
            if frame.get("type") != "post":
                continue
            text = _clean(str(frame.get("text", "")), 1000)
            if not text:
                continue
            msg = {"name": name, "text": text, "ts": time.time()}
            _broadcast(json.dumps({"type": "message", "message": msg}))
    finally:
        with state.lock:
            state.clients.pop(ws, None)
