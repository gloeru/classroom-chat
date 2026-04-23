# Deployment Guide (GitHub + Render)

## 1) GitHub vorbereiten

```bash
git init
git add .
git commit -m "Initial deploy-ready Flask chat app"
git branch -M main
git remote add origin https://github.com/<USER>/<REPO>.git
git push -u origin main
```

## 2) Render mit GitHub verknüpfen

1. In Render anmelden.
2. `New +` -> `Blueprint`.
3. GitHub Repository auswählen.
4. `render.yaml` automatisch erkennen lassen.
5. Deploy starten.

Render verwendet:
- Build: `pip install -r requirements.txt`
- Start: `gunicorn -w 1 -k gevent --worker-connections 1000 --timeout 0 -b 0.0.0.0:$PORT app:app`
- Health Check: `/healthz`

## 3) Build und Start validieren

Nach dem Deploy in Render prüfen:
1. Build-Log ohne Fehler.
2. Service-Status `Live`.
3. `GET /healthz` liefert HTTP 200 mit `ok`.
4. App-URL lädt Join-Screen.

## 4) Qualitätssicherung: Nutzertest

### Testziel
Stabiler Mehrbenutzer-Chat im Browser.

### Testfall 1: Einstieg
1. App öffnen.
2. Leeren Namen eingeben -> Fehlermeldung erwartet.
3. Gültigen Namen eingeben -> Chat-Ansicht erwartet.

### Testfall 2: Messaging
1. Browser A: User `Lea`.
2. Browser B: User `Noah`.
3. A sendet Nachricht.
4. Nachricht erscheint bei A und B mit Name und Uhrzeit.

### Testfall 3: Reconnect
1. In DevTools kurz `Offline` simulieren (oder Netzwerk trennen).
2. Status zeigt Reconnect-Versuche.
3. Nach Netzwerk-Wiederherstellung wieder `connected`.

### Abnahmekriterium
Alle 3 Testfälle ohne Fehlverhalten bestanden.
