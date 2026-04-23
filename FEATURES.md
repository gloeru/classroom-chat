# MVP Feature-Katalog (DDD Schritt 2)

Version: 0.1
Stand: 2026-04-23
Bezug: [`SPEC.md`](SPEC.md) v1.1, [`models/domain.puml`](models/domain.puml) v0.2

Jedes Feature bündelt Anforderungen aus der Spec zu einer abnehmbaren
Einheit. Alle fünf sind für das MVP notwendig — ohne eines davon ist
der Chat nicht klassenzimmertauglich.

---

## F1 — Raum betreten

**Zweck.** Eine Person identifiziert sich im Klassenzimmer mit einem
frei wählbaren Namen und gelangt in die Chat-Ansicht.

**Anforderungen.**
- FR-1 Name-Eingabe vor dem Chat
- FR-6 Name wird getrimmt und auf 40 Zeichen gekürzt
- Keine Authentifizierung, kein Konto (SPEC §2)

**Umsetzungsidee.** Start-Seite mit einem `<input>` und einem Button;
nach Absenden ruft der Client die WebSocket-URL `/ws?name=…` auf. Die
Kürzung/Trim übernimmt sowohl der Client (`maxlength=40`) als auch der
Server (`_clean`), damit der Server autoritativ bleibt.

---

## F2 — Nachricht senden

**Zweck.** Eine im Raum befindliche Person sendet eine Textnachricht
an alle Anwesenden.

**Anforderungen.**
- FR-3 Live-Zustellung innerhalb 1 s
- FR-6 Text getrimmt, max. 1000 Zeichen
- Leere Nachrichten werden nicht zugestellt

**Umsetzungsidee.** Formular schickt `{type:"post", text:…}` über den
bestehenden WebSocket. Server prüft/kürzt, packt in `Message`, hängt an
Ring-Puffer, ruft `_broadcast`.

---

## F3 — Nachrichten empfangen

**Zweck.** Alle verbundenen Personen sehen ankommende Nachrichten
in Echtzeit mit Absender:in, Text und Zeitstempel.

**Anforderungen.**
- FR-2 Chat-Ansicht mit Nachrichtenliste
- FR-3 Live-Zustellung an alle Clients
- FR-4 Anzeige von Name, Text, lokalem Zeitstempel (HH:MM)
- FR-7 Rendering als reiner Text, kein HTML-/Script-Exec

**Umsetzungsidee.** Server sendet `{type:"message", message:{…}}` an
jeden offenen Socket. Client-DOM-Insertion ausschließlich über
`textContent`, niemals `innerHTML` (sichert FR-7).

---

## F4 — Automatisches Reconnect

**Zweck.** Wenn die Verbindung abbricht (Server-Neustart, WLAN-Aussetzer,
Render-Idle-Spin-up), baut der Client selbständig neu auf.

**Anforderungen.**
- NFR-3 Reconnect innerhalb 5 s
- Kein manueller Reload durch Nutzende

**Umsetzungsidee.** `ws.onclose`-Handler ruft nach 2 s erneut
`connect()` auf; Status-Zeile zeigt "reconnecting (k/10)…". Nach zehn
erfolglosen Versuchen stoppt die Schleife und zeigt "offline — please
reload the page".

---

## F5 — Betriebsbereitschaft prüfbar (Health-Check)

**Zweck.** Die Hosting-Plattform (Render) kann die Laufzeit überwachen
und bei Fehlstart erkennen.

**Anforderungen.**
- NFR-6 Blueprint-gesteuerter Render-Deploy
- AC-5 `GET /healthz` → `200 ok`

**Umsetzungsidee.** Eine triviale Flask-Route, die eine statische
Antwort zurückgibt. In `render.yaml` als `healthCheckPath: /healthz`
eingetragen.

---

## Was bewusst *nicht* im MVP ist

Mehrere Räume / Raum-Codes, Rollen (Lehrperson / Schüler:in), private
Nachrichten, Moderation, Editieren / Löschen, Dateianhänge, persistenter
Verlauf über Neustarts hinweg, Push-Benachrichtigungen, native Mobile-
Apps. Siehe SPEC §8.

## Peer-Review dieses Katalogs

| Reviewer | Datum | Entscheidung | Anmerkungen |
|----------|-------|--------------|-------------|
|          |       |              |             |
