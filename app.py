from __future__ import annotations

import json
import time
from threading import Lock
from typing import Any

from flask import Flask, render_template, request
from flask_sock import Sock

MAX_TEXT_LEN = 1000
MAX_NAME_LEN = 40


class State:
    def __init__(self) -> None:
        self.lock = Lock()
        self.clients: dict[Any, str] = {}


state = State()

app = Flask(__name__)
sock = Sock(app)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/healthz")
def healthz():
    return "ok", 200


def _clean(value: str, limit: int) -> str:
    return (value or "").strip()[:limit]


def _broadcast(payload: dict[str, Any]) -> None:
    data = json.dumps(payload)
    dead = []

    with state.lock:
        targets = list(state.clients.keys())

    for ws in targets:
        try:
            ws.send(data)
        except Exception:
            dead.append(ws)

    if dead:
        with state.lock:
            for ws in dead:
                state.clients.pop(ws, None)


@sock.route("/ws")
def ws_handler(ws):
    name = _clean(request.args.get("name", ""), MAX_NAME_LEN)
    if not name:
        try:
            ws.close()
        except Exception:
            pass
        return

    with state.lock:
        state.clients[ws] = name

    try:
        while True:
            raw = ws.receive()
            if raw is None:
                break

            try:
                frame = json.loads(raw)
            except (TypeError, ValueError):
                continue

            if not isinstance(frame, dict):
                continue

            frame_type = frame.get("type")
            if frame_type == "ping":
                try:
                    ws.send(json.dumps({"type": "pong", "ts": time.time()}))
                except Exception:
                    break
                continue

            if frame_type != "post":
                continue

            text = _clean(str(frame.get("text", "")), MAX_TEXT_LEN)
            if not text:
                continue

            msg = {"name": name, "text": text, "ts": time.time()}
            _broadcast({"type": "message", "message": msg})
    finally:
        with state.lock:
            state.clients.pop(ws, None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
