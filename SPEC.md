# Classroom Messenger — Specification

Version: 1.1
Status: Draft
Author: Marcel Gloor
Date: 2026-04-23

## 0. Tooling (project-wide)

| Concern               | Tool                                      |
|-----------------------|-------------------------------------------|
| Specification         | ChatGPT.com (or equivalent LLM assistant) |
| Models / diagrams     | PlantUML.com                              |
| Source repository     | GitHub.com                                |
| Language              | Python (python.org), 3.11+                |
| Web framework         | Flask (flask.palletsprojects.com)         |
| Web server            | gunicorn (gunicorn.org)                   |
| Operation / hosting   | Render.com                                |

All other dependencies are minimised. The project shall add one and only one
additional runtime dependency beyond Flask/gunicorn: `flask-sock` for
WebSocket support, which is the idiomatic Flask extension for WebSockets and
is maintained by the Flask/Pallets ecosystem contributors.

## 1. Purpose

A minimal web-based messenger that lets a classroom (one teacher and their
students) exchange short text messages in real time. The product optimises
for simplicity of code, ease of deployment, and low operational cost. It is
explicitly not a general-purpose chat platform.

## 2. Users and usage model

- There is exactly one shared room. Every user who opens the site is in the
  same room.
- A user identifies with a free-text display name on entry. No password,
  no account, no email.
- Any user can post. All users see every message.
- Expected concurrent usage: ≤ 50 clients.

## 3. Functional requirements

FR-1  The site shall present a name-entry screen on first load. The user
      cannot post or read messages before entering a non-empty name.

FR-2  After entering a name the user enters the chat view, which shows
      (a) a scrolling list of recent messages and (b) an input box for
      posting a new message.

FR-3  When a user posts a message, all currently connected clients
      (including the sender) shall receive that message within 1 second
      under normal network conditions.

FR-4  Each received message shall display sender name, message text, and a
      client-side-formatted timestamp (HH:MM local time).

FR-5  Messages shall be trimmed and capped at 1000 characters; display
      names shall be trimmed and capped at 40 characters. Inputs exceeding
      these limits are truncated silently by the server.

FR-6  Messages shall be rendered as plain text. The client shall not execute
      HTML or scripts contained in messages.

FR-7  Messages are not retained. Only currently-connected clients receive a
      message; late joiners see only messages posted after they joined.

## 4. Non-functional requirements

NFR-1 Server: a single Python 3.11+ process running Flask behind gunicorn.

NFR-2 Real-time delivery: WebSockets via `flask-sock` on endpoint `/ws`.

NFR-3 State lives in process memory only and consists solely of the set
      of connected sockets. A server restart disconnects all clients; the
      client shall auto-reconnect within 5 seconds.

NFR-4 No database, no external services, no third-party authentication.

NFR-5 The implementation shall fit in one Python file (`app.py`) plus one
      HTML file (`templates/index.html`). Total non-comment lines of Python
      ≤ 150.

NFR-6 Deployment target is a single Render.com Web Service described by a
      committed `render.yaml` (Render Blueprint). Free-tier compatible.

NFR-7 gunicorn shall be configured with a single worker and multiple threads
      (`--workers 1 --threads 16 --worker-class gthread`) so that all
      WebSocket clients share one process and therefore the same in-memory
      state. Scaling past one process is explicitly out of scope for v1.

NFR-8 Delivery latency: under normal network conditions a posted message
      shall reach every currently-connected client within 1 second.
      (Migrated from FR-10 in REQUIREMENTS.md v1.0 after peer review.)

NFR-9 Persistence invariant: the server shall not store messages. Only
      currently-connected clients receive a given message; anyone joining
      later does not see it. (Migrated from FR-21 in REQUIREMENTS.md v1.0.)

## 5. Interface

### 5.1 HTTP

- `GET /`        returns the single-page HTML client.
- `GET /healthz` returns `200 OK` with body `ok` for Render health checks.

### 5.2 WebSocket `/ws`

Opened with query parameter `?name=<display_name>`.

Server → client frames are JSON objects with a `type` field:

    { "type": "message", "message": <message> }

where `<message>` is:

    { "name": "Alice", "text": "Hello", "ts": 1745000000.0 }

Client → server frames are JSON objects:

    { "type": "post", "text": "Hello" }

Any malformed frame is ignored by the server.

## 6. Data model

One process-global, lock-protected structure:

    state.lock:    threading.Lock
    state.clients: dict[Server, str]      # socket -> display name

Messages are not stored; they are broadcast immediately to all entries of
`state.clients` and then discarded.

## 7. Security and privacy

- No personal data is persisted. Messages are lost on restart.
- Names are user-chosen and unauthenticated; impersonation is possible and
  accepted as a known limitation of the "as simple as possible" scope.
- The client escapes all text before rendering (see FR-6).
- Transport is HTTPS/WSS in production (provided by Render).

## 8. Out of scope (v1.x)

Multiple rooms, private messages, file upload, message editing or deletion,
moderation tools, persistence across restarts, native mobile apps, i18n.

## 9. Acceptance criteria

AC-1  Two browser tabs with different names exchange messages in real time;
      each sees the other's messages within 1 second.

AC-2  A tab joining after others have already posted sees an empty log and
      from that moment on receives every newly posted message.

AC-3  Posting `<script>alert(1)</script>` renders as literal text; no
      alert executes.

AC-4  Restarting the server disconnects all clients; clients reconnect
      automatically to an empty log.

AC-5  `GET /healthz` returns HTTP 200 with body `ok`.

AC-6  Deploying the repository to Render via `render.yaml` produces a
      working public URL without manual configuration.

## 10. Repository layout

    .
    ├── SPEC.md                 # this document
    ├── README.md               # run / deploy instructions
    ├── requirements.txt        # Flask, flask-sock, gunicorn
    ├── render.yaml             # Render Blueprint
    ├── app.py                  # Flask application (single file)
    ├── templates/
    │   └── index.html          # single-page client
    ├── models/
    │   ├── architecture.puml   # component diagram (PlantUML)
    │   └── post-message.puml   # sequence diagram (PlantUML)
    └── .gitignore
