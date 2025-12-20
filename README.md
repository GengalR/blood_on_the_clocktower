# Blood on the Clocktower - Digital Implementation

Eine digitale Implementierung des sozialen Deduktionsspiels "Blood on the Clocktower" mit FastAPI und Vanilla JavaScript.

## Features

### ✅ Implementiert

- **Spielerstellung & -verwaltung**
  - Erstelle Spiele mit verschiedenen Editionen (Trouble Brewing, Sects & Violets)
  - Spieler können Spielen beitreten
  - Storyteller-Rolle mit speziellen Berechtigungen

- **Rollenvergabe**
  - Automatische Verteilung von Rollen basierend auf Spielerzahl
  - Charaktere aus den offiziellen Editionen
  - Korrekte Setup-Verteilung (Townsfolk, Outsider, Minions, Demons)

- **Spezielle Charaktermechaniken**
  - **Drunk:** Erhält falsche Townsfolk-Rolle (glaubt Townsfolk zu sein, hat keine Fähigkeit)
  - **Baron:** Ersetzt automatisch 2 Townsfolk durch 2 Outsider beim Spielstart 🆕

- **Storyteller-Übersicht**
  - Zeigt alle Spieler mit ihren echten Rollen
  - Nachtreihenfolge (First Night & Other Nights)
  - Minion/Demon Info bei 7+ Spielern
  - Drunk-Markierung

- **Player Flags System** 🆕
  - Storyteller kann Status-Flags auf Spieler setzen
  - Verfügbare Flags:
    - 🧪 **Vergiftet** (Poisoner-Fähigkeit)
    - 👹 **Dämon** (Dämon-Markierung)
    - 🎯 **Red Herring** (Fortune Teller)
    - 💀 **Tot**
    - ✅ **Fähigkeit genutzt**
    - 🛡️ **Geschützt** (Monk)
  - Temporäre Flags können automatisch gelöscht werden
  - Visuelle Badges mit Farbcodierung

- **Spieler-Ansicht**
  - Zeigt eigene Rolle und Fähigkeit
  - Drunk sieht falsche Rolle

## Baron-Feature 🎭

Der Baron ist ein Minion aus der Trouble Brewing Edition mit einer passiven Fähigkeit:

**"Es gibt 2 zusätzliche Outsider im Spiel."**

### Wie es funktioniert

1. Wenn Baron zufällig ausgewählt wird
2. Werden automatisch 2 Townsfolk-Charaktere entfernt
3. Und durch 2 Outsider-Charaktere ersetzt
4. Dies passiert transparent während der Spielinitialisierung

### Beispiel: 5 Spieler

**Ohne Baron:**
- 3 Townsfolk, 0 Outsider, 1 Minion, 1 Dämon

**Mit Baron:**
- 1 Townsfolk, 2 Outsider, 1 Minion (Baron), 1 Dämon

📄 **Detaillierte Dokumentation:** [BARON_FEATURE.md](BARON_FEATURE.md)

## Tech Stack

- **Backend:** Python 3.13+, FastAPI, Pydantic, Uvicorn
- **Frontend:** Vanilla HTML/CSS/JavaScript
- **Daten:** JSON-basierte Speicherung (In-Memory für MVP)

## Installation & Start

### Voraussetzungen
- Python 3.13+
- pip oder uv

### Server starten
```bash
# Mit uv (empfohlen)
uv run uvicorn main:app --reload

# Oder mit pip
pip install -r requirements.txt
uvicorn main:app --reload
```

Server läuft auf: http://localhost:8000

## Tests

### Baron-Feature testen
```bash
python test_baron.py
```

### Manueller Test
1. Server starten: `uvicorn main:app --reload`
2. Browser öffnen: http://localhost:8000
3. Spiel erstellen mit "Trouble Brewing"
4. 5-10 Spieler hinzufügen
5. Spiel starten und Charaktere prüfen

## Projektstruktur

```
blood_on_the_clocktower/
├── main.py                 # FastAPI Endpoints
├── game_service.py         # Business-Logik
├── models.py               # Pydantic Modelle
├── data/
│   ├── editions.json       # Charakterdaten
│   └── rules/              # PDF Regelwerke
├── static/
│   ├── index.html          # Startseite (Spiel erstellen)
│   ├── join.html           # Spiel beitreten
│   ├── storyteller.html    # Storyteller-Ansicht
│   └── player.html         # Spieler-Ansicht
├── test_baron.py           # Baron-Feature Tests
├── BARON_FEATURE.md        # Baron-Dokumentation
└── README.md               # Diese Datei
```

## API-Übersicht

### Spielverwaltung
- `POST /api/game/create` - Spiel erstellen
- `GET /api/game/{game_id}` - Spielinformationen
- `POST /api/game/{game_id}/join` - Spiel beitreten
- `POST /api/game/{game_id}/start` - Spiel starten

### Spielansichten
- `GET /api/game/{game_id}/storyteller` - Storyteller-Übersicht
- `GET /api/game/{game_id}/player/{player_id}` - Spieler-Rolle

### Daten
- `GET /api/editions` - Verfügbare Editionen
- `GET /api/editions/{edition}/characters` - Charaktere einer Edition

## Changelog

### Version 1.1.0 - 2025-01-20
- ✅ Baron-Feature implementiert
- ✅ Automatische Outsider-Umwandlung
- ✅ `baron_active` Flag in API
- ✅ Umfassende Tests
- ✅ Dokumentation

### Version 1.0.0 - 2025-01-19
- ✅ Grundlegende Spielmechanik
- ✅ Drunk-Mechanik
- ✅ Storyteller & Spieler-Ansichten
- ✅ Nachtreihenfolge

## Nächste Schritte

- [ ] Frontend-Anzeige für Baron-Status
- [ ] Mehr Charaktermechaniken (Spy, Recluse, etc.)
- [ ] Persistente Speicherung (SQLite)
- [ ] Echtzeit-Updates (WebSockets)
- [ ] Mobile-optimierte UI

## Lizenz

Privates Projekt - Blood on the Clocktower ist ein Spiel von The Pandemonium Institute.

## Kontakt

GitHub Copilot - AI Assistant

