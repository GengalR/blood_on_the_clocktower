# 🧪 Test-Script: Automatisches Spieler-Hinzufügen

## 📋 Übersicht

Dieses Script automatisiert das Hinzufügen von Spielern zu einem Blood on the Clocktower Spiel, um das Testing zu vereinfachen.

**Vorher:** Manuell viele Browser-Fenster öffnen und Join-Links kopieren  
**Nachher:** Ein Befehl erstellt und startet ein komplettes Testspiel! ✨

---

## 🚀 Installation

Das Script benötigt nur die `requests` Bibliothek:

```bash
pip install requests
```

---

## 💡 Verwendung

### Quick Mode (Empfohlen)

Erstellt automatisch ein neues Spiel, fügt Spieler hinzu und startet es:

```bash
# 6 Spieler (enthält 1 Outsider - Drunk möglich!)
python test_add_players.py --quick 6

# 7 Spieler (enthält 0 Outsider - Drunk NICHT möglich)
python test_add_players.py -q 7

# 10 Spieler mit Sects & Violets Edition
python test_add_players.py -q 10 -e SectsAndViolets
```

**Output:**
- ✅ Game ID und Storyteller ID
- ✅ Liste aller hinzugefügten Spieler
- ✅ Vollständige Rollenzuteilung
- ✅ Nachtreihenfolge (erste Nacht)
- ✅ Direktlinks zur Storyteller-Ansicht

---

### Manueller Modus

Für mehr Kontrolle:

```bash
# Zu bestehendem Spiel 5 Spieler hinzufügen
python test_add_players.py --game abc123 --count 5

# Spieler hinzufügen UND Spiel starten
python test_add_players.py -g abc123 -c 7 --start

# Spieler mit eigenem Präfix
python test_add_players.py -g abc123 -c 5 --prefix "Test"
# Erstellt: Test1, Test2, Test3, Test4, Test5
```

---

## 📚 Alle Optionen

| Option | Kurzform | Beschreibung | Standard |
|--------|----------|--------------|----------|
| `--quick COUNT` | `-q COUNT` | Quick Mode: Erstellt Spiel mit COUNT Spielern | - |
| `--game ID` | `-g ID` | Game ID für manuellen Modus | - |
| `--count N` | `-c N` | Anzahl der Spieler | 5 |
| `--start` | `-s` | Spiel automatisch starten | false |
| `--edition NAME` | `-e NAME` | Edition (TroubleBrewing/SectsAndViolets) | TroubleBrewing |
| `--url URL` | - | Server URL | http://localhost:8000 |
| `--prefix TEXT` | - | Präfix für Spielernamen | Player |
| `--help` | `-h` | Zeige Hilfe | - |

---

## 🎯 Beispiele

### Drunk-Mechanik testen

```bash
# 6 Spieler = 3 Townsfolk + 1 Outsider + 1 Minion + 1 Demon
python test_add_players.py -q 6

# Drunk erscheint als Outsider
# Wenn Drunk gezogen wird, erscheint er als Townsfolk mit 🥴 DRUNK Badge!
```

### Minion/Dämon Info testen (7+ Spieler)

```bash
# 7 Spieler = Minion Info + Dämon Info in Nachtreihenfolge
python test_add_players.py -q 7

# Nachtreihenfolge zeigt:
# 0.1 👿 Minion Info
# 0.2 😈 Dämon Info
# 1.0 Washerwoman
# ...
```

### Großes Spiel testen

```bash
# 15 Spieler (Maximum)
python test_add_players.py -q 15

# Setup: 9 Townsfolk + 2 Outsider + 3 Minions + 1 Demon
```

### Mehrere Runden schnell testen

```bash
# Mehrmals ausführen für verschiedene Rollenzuteilungen
python test_add_players.py -q 6
python test_add_players.py -q 6
python test_add_players.py -q 6

# Jedes Mal neue zufällige Rollen!
```

---

## 📊 Output-Beispiel

```
============================================================
🚀 QUICK TEST MODE
============================================================
📝 Erstelle neues Spiel...
✅ Spiel erstellt!
   Game ID: beef24bd
   Storyteller ID: 3139f7c9

👥 Füge 6 Spieler hinzu...
   ✅ Player1 hinzugefügt (ID: 46907842)
   ✅ Player2 hinzugefügt (ID: 166bcbf2)
   ✅ Player3 hinzugefügt (ID: ea801e80)
   ✅ Player4 hinzugefügt (ID: be0909f0)
   ✅ Player5 hinzugefügt (ID: 0dc5fb65)
   ✅ Player6 hinzugefügt (ID: 75b597b8)

✅ 6 von 6 Spielern erfolgreich hinzugefügt!

🎮 Starte Spiel mit 6 Spielern...
✅ Spiel gestartet! Rollen wurden verteilt!

============================================================
🎭 SPIELÜBERSICHT
============================================================
Spiel-ID: beef24bd
Edition: TroubleBrewing
Status: ✅ Gestartet

👥 Spieler (6):
------------------------------------------------------------
  Player1          Imp                  (demons    )
      🔗 http://localhost:8000/player.html?game=beef24bd&player=46907842
  Player2          Librarian            (townsfolk )
      🔗 http://localhost:8000/player.html?game=beef24bd&player=166bcbf2
  Player3          Washerwoman          (townsfolk ) 🥴 DRUNK
      🔗 http://localhost:8000/player.html?game=beef24bd&player=ea801e80
  Player4          Spy                  (minions   )
      🔗 http://localhost:8000/player.html?game=beef24bd&player=be0909f0
  Player5          Slayer               (townsfolk )
      🔗 http://localhost:8000/player.html?game=beef24bd&player=0dc5fb65
  Player6          Empath               (townsfolk )
      🔗 http://localhost:8000/player.html?game=beef24bd&player=75b597b8

🌙 Nachtreihenfolge - Erste Nacht:
------------------------------------------------------------
    1.0  Washerwoman
    2.0  Librarian
    5.0  Empath
    9.0  Spy
============================================================

============================================================
📋 STORYTELLER LINKS:
============================================================
🎭 Storyteller-Ansicht: http://localhost:8000/storyteller.html?game=beef24bd&storyteller=3139f7c9
👥 Spieler-Join-URL: http://localhost:8000/join.html?game=beef24bd
============================================================
```

---

## 🎭 Features

### ✅ Was das Script macht:

1. **Spiel erstellen** - Automatisch mit Storyteller
2. **Spieler hinzufügen** - So viele wie gewünscht (5-15)
3. **Spiel starten** - Rollen werden verteilt
4. **Übersicht anzeigen** - Alle Rollen + Nachtreihenfolge
5. **Links generieren** - Direkt zur Storyteller-Ansicht
6. **Spieler-Links** - 🔗 Direktlinks zu jeder Spieler-Ansicht! ⬅️ **NEU**

### 🥴 Drunk-Erkennung:

- Zeigt 🥴 DRUNK Badge bei betroffenen Spielern
- Zeigt die **falsche Townsfolk-Rolle** (z.B. "Washerwoman")
- Drunk erscheint in **Nachtreihenfolge** als falsche Rolle!

### 🌙 Nachtreihenfolge:

- Zeigt erste Nacht mit Order-Nummern
- Inklusive Minion/Dämon Info (bei 7+ Spielern)
- Drunk erscheint als seine falsche Rolle

### 🔗 Spieler-Links: ⬅️ **NEU**

- **Jeder Spieler** erhält einen Direktlink zur Spieler-Ansicht
- Format: `http://localhost:8000/player.html?game={game_id}&player={player_id}`
- **Einfach im Browser öffnen** - kein manuelles Kopieren mehr!
- **Perfekt für Multi-Browser-Testing** - öffnen Sie Links in verschiedenen Tabs

---

## 🔧 Erweiterte Nutzung

### Eigener Server

```bash
# Verbinde zu Remote-Server
python test_add_players.py -q 6 --url http://192.168.1.100:8000
```

### Integration in Test-Suite

```python
from test_add_players import GameTester

tester = GameTester()

# Erstelle Testspiel
game_data = tester.create_game()
game_id = game_data['game_id']

# Füge 10 Spieler hinzu
tester.add_players(game_id, 10)

# Starte Spiel
tester.start_game(game_id, 10)

# Hole Übersicht
overview = tester.get_game_overview(game_id, game_data['storyteller_id'])
```

---

## 💡 Tipps

### Drunk testen

Führe das Script mehrmals aus, bis ein Drunk erscheint:

```bash
# Bash/Linux
while ! python test_add_players.py -q 6 | grep -q "DRUNK"; do echo "Kein Drunk, nochmal..."; done

# PowerShell (Windows)
do { python test_add_players.py -q 6 } while ($LASTEXITCODE -eq 0)
```

### Schnell mehrere Spiele testen

```bash
# 5 Spiele mit je 6 Spielern
for i in {1..5}; do python test_add_players.py -q 6; sleep 2; done
```

---

## 🐛 Troubleshooting

### "Connection refused"

**Problem:** Server läuft nicht  
**Lösung:** 
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### "requests module not found"

**Problem:** Requests nicht installiert  
**Lösung:**
```bash
pip install requests
```

### "Game ID not found"

**Problem:** Spiel existiert nicht mehr (In-Memory-Storage)  
**Lösung:** Erstelle neues Spiel mit Quick Mode

---

## 📝 Changelog

### v1.0.0 (2025-12-20)
- ✅ Initial Release
- ✅ Quick Mode
- ✅ Manueller Modus
- ✅ Drunk-Erkennung mit 🥴 Badge
- ✅ Nachtreihenfolge-Anzeige
- ✅ Beide Editionen (Trouble Brewing, Sects & Violets)

---

**Erstellt:** 2025-12-20  
**Version:** 1.0.0  
**Autor:** GitHub Copilot  
**Lizenz:** MIT

