# Peer-Review: Domänenmodell v0.1

Diagramm: [`domain.puml`](domain.puml)

## Begründung der Klassenwahl

- **Classroom** — das zentrale Konzept. v1 hat genau eines, das wird als
  Singleton-Aggregat modelliert, nicht als Sammlung.
- **Participant** — wer sich mit einem Namen angemeldet hat. Kein
  Rollenunterschied (Lehrperson / Schüler:in), weil die Spec keinen macht.
- **Message** — Textnachricht mit Autor:in und Zeitpunkt.

Bewusst *nicht* modelliert: System-/Beitrittshinweise ("Alice joined").
Scope v1 = minimaler Chat, keine Meta-Ereignisse.

## Bewusst ausgeschlossen (nicht Domäne, sondern Technik)

WebSocket, Lock, Deque, In-Memory-Speicher, Render.com, Flask — gehört
in das Architekturmodell (`architecture.puml`), nicht hierher.

## Bewusst ausgeschlossen (Scope v1)

Mehrere Räume, Raum-Code, private Nachrichten, Moderation, Rollen,
Editieren / Löschen, persistente Historie, Dateianhänge.

## Invarianten aus der Spec

- `Participant.name` — nach Trim 1..40 Zeichen.
- `Message.text` — nach Trim 1..1000 Zeichen.
- Eine **Message** hat genau einen Autor (Participant).
- Keine Historie: Nachrichten sind flüchtige Ereignisse, werden nach
  dem Broadcast verworfen.

## Entschiedene Review-Fragen

| # | Frage                                                        | Entscheidung                                                               |
|---|--------------------------------------------------------------|----------------------------------------------------------------------------|
| 1 | Wiederkehrende Identität für `Participant` in v1?            | **Nein.** Kein Konzept von Identität zwischen Sessions.                    |
| 2 | `historyLimit` als Domänenattribut?                          | **Nein.** Kein persistenter Speicher, keine Historie → Policy, nicht Domäne. |
| 3 | `Instant` vs. `DateTime`?                                    | **Egal.** `Instant` beibehalten.                                           |

## Review-Protokoll

| Reviewer | Datum      | Entscheidung        | Anmerkungen |
|----------|------------|---------------------|-------------|
| Marcel   | 2026-04-23 | abgenommen (v0.2)   | —           |
