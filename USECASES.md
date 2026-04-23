# Use Cases (DDD Schritt 3)

Version: 0.2
Stand: 2026-04-23
Bezug: [`SPEC.md`](SPEC.md), [`FEATURES.md`](FEATURES.md),
       [`models/user-actions.puml`](models/user-actions.puml)

## Akteure

| Akteur            | Rolle                  | Hinweis                                     |
|-------------------|------------------------|---------------------------------------------|
| Teilnehmende:r    | Primär (menschlich)    | Einzige Rolle — v1 unterscheidet nicht      |
| Render-Plattform  | Sekundär (Maschine)    | Ruft den Health-Endpoint periodisch auf     |

## Übersicht

| ID   | Name                             | Primärakteur       | Auslöser                |
|------|----------------------------------|--------------------|-------------------------|
| UC-1 | Raum betreten                    | Teilnehmende:r     | URL wird geöffnet       |
| UC-2 | Nachricht senden                 | Teilnehmende:r     | Enter / Klick           |
| UC-3 | Nachricht empfangen              | Teilnehmende:r     | Andere:r führt UC-2 aus |
| UC-4 | Raum verlassen                   | Teilnehmende:r     | Tab schließen           |
| UC-5 | Verbindung wiederherstellen      | Teilnehmende:r     | Leitungsabbruch         |
| UC-6 | Betriebsbereitschaft prüfen      | Render-Plattform   | Timer                   |

**Hinweis zu UC-4 vs. UC-5.** Beide UCs werden vom WebSocket-`onclose`
ausgelöst; der Client unterscheidet technisch nicht, ob der Abbruch
gewollt (Tab schließen) oder ungewollt (Netz weg) war. UC-5 wird daher
immer angestoßen und verliert lediglich seine Sichtbarkeit, wenn das Tab
gleichzeitig geschlossen wurde.

---

## UC-1 Raum betreten

- **Primärakteur.** Teilnehmende:r.
- **Ziel.** In den Chatraum kommen und mitlesen/mitreden können.
- **Vorbedingung.** Browser offen, URL des Dienstes bekannt.
- **Nachbedingung (Erfolg).** Der Client ist via WebSocket verbunden; die
  Chat-Ansicht ist sichtbar; der gewählte Name ist dem Server bekannt.
- **Nachbedingung (Misserfolg).** Die Chat-Ansicht wird nicht angezeigt.

### Hauptszenario

1. Teilnehmende:r ruft die Seite auf.
2. System zeigt das Namenseingabe-Formular.
3. Teilnehmende:r tippt einen Namen und bestätigt.
4. System öffnet eine WebSocket-Verbindung mit diesem Namen.
5. System wechselt in die Chat-Ansicht und zeigt Eingabefeld und leeren
   Nachrichten-Bereich.

### Abweichungen

- **3a Leerer Name.** System akzeptiert die Eingabe nicht; Teilnehmende:r
  kann erneut eingeben.
- **3b Name zu lang.** System kürzt auf 40 Zeichen und fährt mit Schritt 4
  fort.
- **4a Verbindung scheitert.** System zeigt Status "disconnected" und
  startet automatisch UC-5.

---

## UC-2 Nachricht senden

- **Primärakteur.** Teilnehmende:r.
- **Ziel.** Eine Textnachricht an alle Anwesenden verteilen.
- **Vorbedingung.** UC-1 abgeschlossen, WebSocket offen.
- **Nachbedingung (Erfolg).** Die Nachricht wird bei allen verbundenen
  Clients (inkl. Absender:in) angezeigt.

### Hauptszenario

1. Teilnehmende:r tippt Text in das Nachrichtenfeld.
2. Teilnehmende:r bestätigt (Enter oder Klick).
3. Client sendet `{type:"post", text:…}` an den Server.
4. Server trimmt und kürzt den Text.
5. Server ergänzt Absendername und Zeitstempel.
6. Server verteilt die Nachricht an alle aktuell verbundenen Clients.
7. Alle Clients, auch der absendende, zeigen die Nachricht an (siehe UC-3).

### Abweichungen

- **2a Leerer Text.** Client sendet nicht; Server würde den Post ebenfalls
  ignorieren.
- **4a Text zu lang.** Server kürzt auf 1000 Zeichen, fährt mit Schritt 5
  weiter.
- **6a Zielsocket bricht ab.** Server entfernt ihn aus der Client-Menge
  und fährt mit den übrigen Empfängern fort.

---

## UC-3 Nachricht empfangen

- **Primärakteur.** Teilnehmende:r (passiv).
- **Trigger.** Ein:e andere:r Teilnehmende:r hat UC-2 erfolgreich
  ausgeführt (Schritt 6 des dortigen Hauptszenarios).
- **Ziel.** Beiträge anderer sehen.
- **Vorbedingung.** UC-1 abgeschlossen.
- **Nachbedingung.** Die empfangene Nachricht ist in der Liste sichtbar.

### Hauptszenario

1. Server liefert einen `message`-Frame über die offene WebSocket.
2. Client parst den Frame und erzeugt eine neue Zeile.
3. Client rendert Absender, Text und lokal formatierten Zeitstempel (HH:MM).
4. War die Liste vor dem Empfang ans Ende gescrollt, scrollt der Client
   auch jetzt ans Ende; andernfalls bleibt die aktuelle Scroll-Position.

### Abweichungen

- **2a Malformed Frame.** Client ignoriert.
- **3a Enthält HTML oder Script.** Client setzt den Text via
  `textContent`; kein Markup wird interpretiert, kein Skript ausgeführt.

---

## UC-4 Raum verlassen

- **Primärakteur.** Teilnehmende:r.
- **Ziel.** Den Chat verlassen.
- **Vorbedingung.** UC-1 abgeschlossen.
- **Nachbedingung.** Der Server führt den Client nicht mehr in der
  Empfängermenge.

### Hauptszenario

1. Teilnehmende:r schließt Tab oder Browser.
2. WebSocket wird vom Browser geschlossen.
3. Server entfernt den Socket aus der Client-Menge.

---

## UC-5 Verbindung wiederherstellen

- **Primärakteur.** Teilnehmende:r (passiv).
- **Auslöser.** WebSocket feuert `onclose`, unabhängig davon, ob gewollt
  oder nicht (siehe Übersichtshinweis).
- **Ziel.** Ohne Zutun der Person weiter chatten können.
- **Vorbedingung.** Vorher bestand eine Verbindung.
- **Nachbedingung (Erfolg).** Neue Verbindung steht; bisher empfangene
  Nachrichten bleiben angezeigt.
- **Nachbedingung (dauerhafter Misserfolg).** Der Client zeigt einen
  Offline-Zustand mit Aufforderung "bitte Seite neu laden"; die
  Retry-Schleife ist beendet.

### Hauptszenario

1. WebSocket feuert `onclose`.
2. Client zeigt Status "reconnecting…".
3. Client wartet 2 Sekunden und versucht erneut `connect()`.
4. Verbindung steht, Status wechselt auf "connected as <Name>".

### Abweichungen

- **3a Verbindung kommt nicht zustande, unter N Versuchen.** Schritt 2–3
  wiederholen, Versuchszähler inkrementieren.
- **3b Nach N = 10 erfolglosen Versuchen.** Client zeigt
  "offline — bitte Seite neu laden" und bricht die Retry-Schleife ab.

---

## UC-6 Betriebsbereitschaft prüfen

- **Primärakteur.** Render-Plattform.
- **Ziel.** Feststellen, ob der Dienst läuft.
- **Vorbedingung.** Dienst ist gestartet.
- **Nachbedingung.** Render hält den Dienst für gesund oder startet ihn neu.

### Hauptszenario

1. Render sendet periodisch `GET /healthz`.
2. System antwortet mit HTTP 200 und Body `ok`.
