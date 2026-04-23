# Funktionale Anforderungen — Gesamtliste

Version: 1.1
Stand: 2026-04-23
Abgeleitet aus [`USECASES.md`](USECASES.md) v0.2; ersetzt die
eingebetteten `FR-…` aus [`SPEC.md`](SPEC.md) Abschnitt 3.

Jede Anforderung ist auf einen Use-Case-Schritt oder eine Abweichung
zurückgeführt. Abkürzungen: UC-n.m = Schritt m des Use Case n;
UC-n.ma = Abweichung "a" bei Schritt m.

**Migrationshinweis v1.0 → v1.1.** Im Peer-Review wurden zwei
Anforderungen als nicht-funktional umklassifiziert und in
[`SPEC.md`](SPEC.md) Abschnitt 4 verschoben:

- Zustellzeit ≤ 1 s (ehemals FR-10) → NFR in `SPEC.md`.
- Keine Nachrichten-Persistenz (ehemals FR-21) → NFR/Invariante in
  `SPEC.md`.

## Liste

| ID    | Anforderung                                                                                                         | Herkunft             |
|-------|---------------------------------------------------------------------------------------------------------------------|----------------------|
| FR-01 | Vor der Chat-Ansicht wird ein Namenseingabe-Formular gezeigt.                                                       | UC-1.2               |
| FR-02 | Ein leerer Name wird nicht akzeptiert.                                                                              | UC-1.3a              |
| FR-03 | Der Name wird getrimmt und auf 40 Zeichen gekürzt.                                                                  | UC-1.3b              |
| FR-04 | Nach erfolgreicher Eingabe wechselt die Anwendung in die Chat-Ansicht mit Eingabefeld und leerem Nachrichtenbereich. | UC-1.5               |
| FR-05 | In der Chat-Ansicht steht ein Eingabefeld für neue Nachrichten bereit.                                              | UC-2.1               |
| FR-06 | Der Client sendet eine Nachricht als JSON-Frame `{type:"post", text:…}` über die offene WebSocket.                  | UC-2.3               |
| FR-07 | Der Server trimmt den Nachrichtentext und kürzt ihn auf 1000 Zeichen.                                               | UC-2.4, UC-2.4a      |
| FR-08 | Leere Nachrichten werden weder vom Client gesendet noch vom Server zugestellt.                                      | UC-2.2a              |
| FR-09 | Der Server ergänzt jede Nachricht um Absendername und Zeitstempel und verteilt sie an alle aktuell verbundenen Clients (inkl. Absender:in). | UC-2.5, UC-2.6, UC-2.7 |
| FR-10 | Empfangene Nachrichten werden mit Absendername, Text und lokal formatiertem Zeitstempel (HH:MM) angezeigt.          | UC-3.3               |
| FR-11 | Der Client rendert Nachrichten als reinen Text; enthaltenes HTML oder Script wird nicht ausgeführt.                 | UC-3.3a              |
| FR-12 | Der Client scrollt die Nachrichtenliste nach jedem Eintrag ans Ende, sofern die Liste zuvor am Ende war; andernfalls bleibt die Scroll-Position unverändert. | UC-3.4 |
| FR-13 | Malformierte Frames werden vom Empfänger (Client wie Server) stillschweigend ignoriert.                             | UC-3.2a              |
| FR-14 | Beim Schließen eines Browser-Tabs wird der betroffene Socket aus der Empfängermenge entfernt.                       | UC-4.3               |
| FR-15 | Wird ein Zielsocket beim Broadcast ungültig, entfernt der Server ihn und fährt mit den übrigen fort.                | UC-2.6a              |
| FR-16 | Bei unerwartetem WebSocket-Schließen zeigt der Client sichtbar einen "reconnecting"-Status.                         | UC-5.2               |
| FR-17 | Der Client versucht spätestens 5 Sekunden nach Abbruch automatisch einen neuen Verbindungsaufbau (Retry-Schleife).   | UC-5.3, UC-5.3a      |
| FR-18 | Nach 10 erfolglosen Reconnect-Versuchen beendet der Client die Retry-Schleife und zeigt "offline — bitte Seite neu laden". | UC-5.3b          |
| FR-19 | Bereits angezeigte Nachrichten bleiben während Abbruch und Reconnect sichtbar.                                       | UC-5 Nachbedingung   |
| FR-20 | `GET /healthz` antwortet mit HTTP 200 und Body `ok`.                                                                 | UC-6.2               |

## Rückverfolgbarkeit zum bisherigen Spec-Block

| Neu       | Alt (SPEC §3)                 |
|-----------|-------------------------------|
| FR-01, FR-04 | FR-1                      |
| FR-05     | FR-2                          |
| FR-09     | FR-3 (ohne 1-s-Klausel, siehe NFR) |
| FR-10     | FR-4                          |
| FR-03, FR-07 | FR-5                      |
| FR-11     | FR-6                          |
| —         | FR-7 (jetzt NFR, siehe oben)  |
| FR-02, FR-06, FR-08, FR-12–FR-19 | neu (durch Use-Case-Analyse explizit gemacht) |
| FR-20     | NFR-6 / AC-5 (jetzt als FR geführt) |

## Peer-Review

| Reviewer | Datum      | Entscheidung          | Anmerkungen                                  |
|----------|------------|-----------------------|----------------------------------------------|
| Marcel   | 2026-04-23 | abgenommen (v1.1)     | FR-10 + FR-21 → NFR, UC-2 Schritt 4 gesplittet, XSS nach UC-3, Offline-Fallback nach 10 Retries |
