# 🎭 Blood on the Clocktower - Web App

## 📋 PROJEKT-ÜBERSICHT

**Projekttyp:** Web-Anwendung (Python FastAPI + Vanilla JavaScript)
**Zweck:** Digitale Umsetzung des Social-Deduction-Spiels "Blood on the Clocktower"
**Status:** MVP funktionsfähig, 2 UI-Bugs offen

### Kern-Features
- ✅ Mehrere Spieler können über Handy beitreten
- ✅ Automatische Rollenzuteilung basierend auf Spielerzahl
- ✅ Erzähler erhält Übersicht + Nachtphasen-Reihenfolge
- ✅ Spieler sehen nur ihre eigene Rolle
- ✅ Echtzeit-Updates via Polling

---

## 🏗️ ARCHITEKTUR

### Tech-Stack
```
Backend:  FastAPI + Uvicorn + Pydantic
Frontend: Vanilla HTML/CSS/JavaScript
Daten:    In-Memory (dict) + JSON (Editions)
```

### Dateistruktur
```
├── main.py              → FastAPI App, API Endpoints, Route-Handler
├── game_service.py      → Business Logic (Spiel erstellen/starten, Rollen verteilen)
├── models.py            → Pydantic Models (Game, Player, Character)
├── requirements.txt     → Python Dependencies
├── data/
│   └── editions.json    → Charaktere, Fähigkeiten, Setup pro Edition
└── static/
    ├── index.html       → Startseite: Spiel erstellen (Erzähler)
    ├── join.html        → Beitreten-Seite (Spieler)
    ├── storyteller.html → Erzähler-Dashboard
    └── player.html      → Spieler-Rollenansicht
```

---

## 🔄 SPIELFLUSS (User Journey)

### 1. Spiel erstellen (Erzähler)
```
index.html
├─ Input: Erzähler-Name, Edition
├─ API: POST /api/game/create
├─ Erhält: game_id, storyteller_id
└─ Redirect: storyteller.html?game={game_id}&storyteller={storyteller_id}
```

### 2. Spieler beitreten
```
join.html?game={game_id}
├─ Input: Spieler-Name
├─ API: POST /api/game/{game_id}/join
├─ Erhält: player_id
└─ Redirect: player.html?game={game_id}&player={player_id}
```

### 3. Spiel starten (Erzähler)
```
storyteller.html
├─ Input: Spielerzahl
├─ API: POST /api/game/{game_id}/start (mit player_count)
├─ Backend: Rollen zufällig verteilen
└─ Frontend: Zeigt Spielerliste + Nachtphasen an
```

### 4. Rolle sehen (Spieler)
```
player.html
├─ Polling: GET /api/player/{game_id}/{player_id}/role (alle 2s)
├─ Vor Start: 404 → Wartebildschirm
└─ Nach Start: 200 → Rollenanzeige
```

---

## 📡 API ENDPOINTS (main.py)

### Editions-Daten
| Endpoint | Method | Zweck |
|----------|--------|-------|
| `/api/editions` | GET | Liste aller Editionen |
| `/api/editions/{edition}/characters` | GET | Charaktere einer Edition |

### Spiel-Verwaltung
| Endpoint | Method | Body | Response |
|----------|--------|------|----------|
| `/api/game/create` | POST | `{edition, storyteller_name}` | `{game_id, storyteller_id, join_url}` |
| `/api/game/{game_id}` | GET | - | `{id, edition, started, player_count}` |
| `/api/game/{game_id}/join` | POST | `{player_name}` | `{player_id, name, game_id}` |
| `/api/game/{game_id}/start` | POST | `{player_count}` | `{game_id, started, message}` |

### Spieler-Daten
| Endpoint | Method | Zweck |
|----------|--------|-------|
| `/api/player/{game_id}/{player_id}/role` | GET | Rolle eines Spielers |
| `/api/storyteller/{game_id}/{storyteller_id}/overview` | GET | Alle Rollen + Nachtphasen |

### Static Files
```python
app.mount("/static", StaticFiles(directory="static"), name="static")
# → Macht static/*.html unter /static/*.html verfügbar
# → FileResponse("static/index.html") funktioniert auch ohne mount
# → Mount ermöglicht direkten Browser-Zugriff auf CSS/JS/Bilder
```

---

## 🎮 GAME SERVICE LOGIK (game_service.py)

### Kern-Funktionen

#### `create_game(edition, storyteller_name)`
```python
# 1. Validiert Edition existiert
# 2. Generiert game_id (UUID)
# 3. Erstellt Erzähler als Player (is_storyteller=True)
# 4. Speichert Game in self.games dict
# 5. Returned Game-Objekt
```

#### `join_game(game_id, player_name)`
```python
# 1. Prüft: Spiel existiert
# 2. Prüft: Spiel noch nicht gestartet
# 3. Erstellt Player mit UUID
# 4. Fügt zu game.players hinzu
# 5. Returned Player-Objekt
```

#### `start_game(game_id, player_count)`
```python
# 1. Lädt Setup aus editions.json (z.B. 5 Spieler = 3 Townsfolk, 0 Outsider, 1 Minion, 1 Demon)
# 2. Wählt zufällig Charaktere pro Typ
# 3. Mischt Charaktere
# 4. Weist jedem Spieler (außer Erzähler) Charakter zu
# 5. Setzt game.started = True
# 6. Returned Game-Objekt
```

#### `get_storyteller_overview(game_id, storyteller_id)`
```python
# 1. Validiert: Spieler ist Erzähler
# 2. Sammelt alle Spieler + deren Rollen
# 3. Erstellt Nachtphasen-Listen:
#    - first_night: Sortiert nach character.first_night (aufsteigend, nur > 0)
#    - other_nights: Sortiert nach character.other_nights (aufsteigend, nur > 0)
# 4. Returned {players: [...], night_order: {...}}
```

### Rollenverteilung
```json
// editions.json → setup
{
  "5": {"townsfolk": 3, "outsiders": 0, "minions": 1, "demons": 1},
  "6": {"townsfolk": 3, "outsiders": 1, "minions": 1, "demons": 1},
  ...
}
// → Bei 5 Spielern: 3 zufällige Townsfolk + 1 Minion + 1 Demon
```

---

## 🌐 FRONTEND-DETAILS

### index.html (Spiel erstellen)
**JavaScript-Ablauf:**
```javascript
// 1. DOMContentLoaded → loadEditions()
async function loadEditions() {
  const response = await fetch('/api/editions');
  const editions = await response.json();
  // Fülle <select id="editionSelect"> dynamisch
}

// 2. Form Submit
document.getElementById('gameForm').addEventListener('submit', async (e) => {
  e.preventDefault(); // Verhindert normales Submit
  const storytellerName = document.getElementById('storytellerName').value;
  const edition = document.getElementById('editionSelect').value;
  
  const response = await fetch('/api/game/create', {
    method: 'POST',
    body: JSON.stringify({edition, storyteller_name: storytellerName})
  });
  
  const data = await response.json();
  // Redirect zu Erzähler-Seite
  window.location.href = `/static/storyteller.html?game=${data.game_id}&storyteller=${data.storyteller_id}`;
});
```

**Event-Bindung:**
- `addEventListener('submit', ...)` registriert Handler
- Button `type="submit"` triggert Form-Submit
- Handler läuft OHNE explizite onClick-Attribute

---

### storyteller.html (Erzähler-Dashboard)
**URL-Parameter:**
```javascript
const params = new URLSearchParams(window.location.search);
const gameId = params.get('game');
const storytellerId = params.get('storyteller');
```

**Funktionen:**
1. **Join-URL anzeigen:** `${window.location.origin}/static/join.html?game=${gameId}`
2. **Spieler-Polling:** Alle 2s GET `/api/game/{gameId}` → Zeigt Spielerzahl
3. **Spiel starten:** 
   ```javascript
   POST /api/game/{gameId}/start
   Body: {player_count: <input value>}
   ```
4. **Übersicht laden:**
   ```javascript
   GET /api/storyteller/{gameId}/{storytellerId}/overview
   → Zeigt Spielerliste + Nachtphasen
   ```

**❌ OFFENER BUG:**
- "Neues Spiel erstellen" Box bleibt nach Start sichtbar
- **FIX:** CSS `display: none` wenn `game.started === true`

---

### player.html (Spieler-Rolle)
**Polling-Logik:**
```javascript
async function checkRole() {
  try {
    const response = await fetch(`/api/player/${gameId}/${playerId}/role`);
    
    if (response.status === 404) {
      // Spiel noch nicht gestartet
      setTimeout(checkRole, 2000); // Erneut nach 2s
      showWaiting(); // Spinner anzeigen
    } else {
      // Spiel gestartet
      const role = await response.json();
      showRole(role); // Rolle anzeigen
    }
  } catch (error) {
    console.error(error);
    setTimeout(checkRole, 2000);
  }
}
```

**Rollen-Typ Styling:**
```css
.role-type.townsfolk  { background: #e3f2fd; color: #1976d2; } /* Blau */
.role-type.outsiders  { background: #fff3e0; color: #f57c00; } /* Orange */
.role-type.minions    { background: #fce4ec; color: #c2185b; } /* Pink */
.role-type.demons     { background: #ffebee; color: #d32f2f; } /* Rot */
```

**❌ OFFENER BUG:**
- "Aktualisieren"-Button bleibt nach Start sichtbar
- **FIX:** Button ausblenden nach erfolgreicher Rolle-Ladung

---

## 🔍 JAVASCRIPT-KONZEPTE ERKLÄRT

### 1. Browser führt JavaScript aus
```html
<script>
  // Dieser Code läuft SOFORT wenn Browser ihn parst
  console.log('Hallo');
</script>

<script>
  // Wartet bis HTML fertig geladen
  document.addEventListener('DOMContentLoaded', () => {
    // Jetzt existieren alle HTML-Elemente
  });
</script>
```

### 2. Event-Bindung ohne onClick
```html
<!-- NICHT nötig: onclick="handleClick()" -->
<button id="myBtn">Klick mich</button>

<script>
  // Event Listener wird im JavaScript registriert
  document.getElementById('myBtn').addEventListener('click', () => {
    alert('Geklickt!');
  });
  // → Button und Handler sind jetzt verbunden
</script>
```

### 3. Polling Pattern
```javascript
async function poll() {
  const data = await fetch('/api/status').then(r => r.json());
  
  if (data.ready) {
    showResult(); // Fertig
  } else {
    setTimeout(poll, 2000); // Erneut nach 2s
  }
}
poll(); // Start
```

### 4. Fetch API
```javascript
// GET
const data = await fetch('/api/endpoint').then(r => r.json());

// POST
const response = await fetch('/api/endpoint', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({key: 'value'})
});
```

---

## 📚 DATENMODELLE (models.py)

### Enums
```python
class Team(str, Enum):
    GOOD = "good"
    EVIL = "evil"

class CharacterType(str, Enum):
    TOWNSFOLK = "townsfolk"
    OUTSIDER = "outsiders"
    MINION = "minions"
    DEMON = "demons"
```

### Hauptklassen
```python
class Character(BaseModel):
    id: str
    name: str
    ability: str
    first_night: int      # Reihenfolge erste Nacht (0 = nicht aufrufen)
    other_nights: int     # Reihenfolge weitere Nächte
    type: Optional[CharacterType] = None

class Player(BaseModel):
    id: str
    name: str
    character: Optional[Character] = None
    is_storyteller: bool = False

class Game(BaseModel):
    id: str
    edition: str
    players: List[Player] = []
    started: bool = False
    player_count: Optional[int] = None
```

---

## 🐛 BEKANNTE PROBLEME & LÖSUNGEN

### ✅ GELÖST: "Fehlende Parameter in URL"
**Problem:** Nach "Spiel erstellen" kam Fehler  
**Ursache:** Redirect URL hatte falsche Parameter  
**Lösung:** `window.location.href` korrigiert in index.html

### ✅ GELÖST: Weiße Seite
**Problem:** Seite blieb leer  
**Ursache:** JavaScript-Fehler oder fehlende API-Calls  
**Lösung:** Error-Handling verbessert, DOM-Ready-Events gefixt

### ✅ GELÖST: asyncio.run() Error
**Problem:** `RuntimeError: asyncio.run() cannot be called from a running event loop`  
**Ursache:** Jupyter/IPython hat bereits Event Loop  
**Lösung:** Verwende `uvicorn main:app --reload` statt `uvicorn.run()` in Code

### ❌ OFFEN: Storyteller UI nach Start
**Problem:** "Neues Spiel erstellen" Box bleibt sichtbar  
**Lösung:** 
```javascript
if (game.started) {
  document.getElementById('create-game-section').style.display = 'none';
}
```

### ❌ OFFEN: Player Update-Button
**Problem:** "Aktualisieren"-Button unnötig nach Start  
**Lösung:**
```javascript
function showRole(role) {
  // ... Rolle anzeigen ...
  const refreshBtn = document.getElementById('refresh-btn');
  if (refreshBtn) refreshBtn.style.display = 'none';
}
```

---

## ⚙️ DEPLOYMENT

### Lokaler Start
```bash
# Server starten (Empfohlen)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Dependencies installieren
pip install -r requirements.txt

# JSON validieren
python -c "import json; print(json.load(open('data/editions.json')))"
```

### Zugriff
- **Lokal:** http://localhost:8000
- **Netzwerk:** http://<lokale-ip>:8000
- Spieler verbinden sich mit Handy über selbes WLAN

### Mount vs. FileResponse
```python
# MIT Mount
app.mount("/static", StaticFiles(directory="static"), name="static")
# → Browser kann direkt /static/index.html aufrufen
# → CSS/JS/Bilder funktionieren automatisch

# OHNE Mount
@app.get("/")
async def root():
    return FileResponse("static/index.html")
# → Funktioniert für einzelne Datei
# → Aber: CSS/JS müssen eigene Endpoints haben
# → Unpraktisch für viele Dateien
```

---

## 📝 DATEN-FORMAT (editions.json)

```json
{
  "trouble-brewing": {
    "name": "Trouble Brewing",
    "characters": {
      "townsfolk": [
        {
          "id": "washerwoman",
          "name": "Waschfrau",
          "ability": "Du erfährst, dass einer von zwei Spielern ein bestimmter Townsfolk ist.",
          "first_night": 30,
          "other_nights": 0
        }
      ],
      "outsiders": [...],
      "minions": [...],
      "demons": [...]
    },
    "setup": {
      "5": {"townsfolk": 3, "outsiders": 0, "minions": 1, "demons": 1},
      "6": {"townsfolk": 3, "outsiders": 1, "minions": 1, "demons": 1}
    }
  }
}
```

**Nachtphasen-Logik:**
- Sortiere alle Charaktere nach `first_night` (aufsteigend)
- Filter: Nur Charaktere mit Wert > 0
- Zeige Erzähler in dieser Reihenfolge

---

## ✅ TODO-LISTE

### Hoch-Priorität (Bugs)
- [ ] storyteller.html: Erstellen-Box nach Start ausblenden
- [ ] player.html: Aktualisieren-Button nach Start entfernen

### Mittel-Priorität (Features)
- [ ] Persistierung: SQLite/PostgreSQL statt In-Memory
- [ ] Error-Handling: Toast-Notifications im Frontend
- [ ] Validation: Min/Max Spielerzahl prüfen

### Niedrig-Priorität (Nice-to-Have)
- [ ] Mehr Editionen: Sects & Violets, Bad Moon Rising
- [ ] Spieler-Kick-Funktion für Erzähler
- [ ] Mobile UI-Optimierung
- [ ] Dark Mode
- [ ] WebSocket statt Polling

---

## 🧠 WICHTIGE ERKENNTNISSE FÜR KI

### Wie Variablen gespeichert werden
```javascript
// IN BROWSER (JavaScript)
const storytellerName = document.getElementById('storytellerName').value;
// → Holt Wert aus HTML-Input BEIM Submit
// → Nicht vorab gespeichert, erst bei Aktion

// IN URL (nach Redirect)
window.location.href = `/static/storyteller.html?game=${gameId}&storyteller=${storytellerId}`;
// → Variablen werden in URL übergeben
// → Nächste Seite liest mit URLSearchParams

// IN SERVER (Python)
self.games[game_id] = game
// → In-Memory Dictionary
// → Geht bei Neustart verloren
```

### Event-Flow
```
1. HTML wird geladen → Browser rendert Elemente
2. <script> wird ausgeführt → Event Listener registriert
3. User klickt Button → Event gefeuert
4. Event Handler läuft → Fetch zu API
5. API antwortet → JavaScript verarbeitet Response
6. DOM wird aktualisiert → User sieht Änderung
```

### Polling-Prinzip
```
Spieler wartet → GET /api/role
├─ 404: Noch nicht gestartet → setTimeout(check, 2000)
├─ 200: Gestartet → Zeige Rolle, Stop Polling
└─ Error: Netzwerkfehler → setTimeout(check, 2000)
```

---

## 📄 CHANGELOG

### v1.0 - 2025-01-19 (Initial Release)
- ✅ FastAPI Backend mit allen Endpoints
- ✅ 4 HTML-Seiten (index, join, storyteller, player)
- ✅ Trouble Brewing Edition komplett
- ✅ Automatische Rollenzuteilung
- ✅ Nachtphasen-Reihenfolge
- ✅ Echtzeit-Updates via Polling
- ⚠️ 2 UI-Bugs bekannt (siehe TODO)

---

## 🎯 FÜR ZUKÜNFTIGE COPILOT-SESSIONS

**Bevor du Code änderst:**
1. Lies diese Datei komplett
2. Verstehe den Spielfluss (User Journey)
3. Prüfe offene TODOs
4. Teste nach Änderungen

**Code-Stil:**
- Backend: Type Hints verwenden
- Frontend: Async/Await statt Promises.then()
- Fehler: Immer HTTPException mit detail
- Docs: API-Änderungen hier dokumentieren

**Wichtige Dateien:**
- `main.py` → API-Endpoints (REST-Interface)
- `game_service.py` → Business Logic (KEINE API-Logik!)
- `storyteller.html` → Komplexeste Frontend-Datei
- `data/editions.json` → Spiel-Daten (validiere Schema!)

---

**Erstellt:** 2025-01-19  
**Letzte Aktualisierung:** 2025-01-19  
**Version:** 1.0.0

