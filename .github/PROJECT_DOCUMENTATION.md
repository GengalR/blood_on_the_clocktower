# 🎭 Blood on the Clocktower - Web App

## 📋 PROJECT OVERVIEW

**Project Type:** Web Application (Python FastAPI + Vanilla JavaScript)
**Purpose:** Digital implementation of the social deduction game "Blood on the Clocktower"
**Status:** MVP functional, 2 UI bugs open

### Core Features
- ✅ Multiple players can join via mobile
- ✅ Automatic role assignment based on player count
- ✅ Storyteller receives overview + night phase order
- ✅ Players only see their own role
- ✅ Real-time updates via polling
- ✅ Quick Rules Modal (in-game help for players & storyteller)

---

## 🏗️ ARCHITECTURE

### Tech Stack
```
Backend:  FastAPI + Uvicorn + Pydantic
Frontend: Vanilla HTML/CSS/JavaScript
Data:     In-Memory (dict) + JSON (Editions)
```

### File Structure
```
├── main.py              → FastAPI App, API Endpoints, Route Handler
├── game_service.py      → Business Logic (create/start game, distribute roles)
├── models.py            → Pydantic Models (Game, Player, Character)
├── requirements.txt     → Python Dependencies
├── data/
│   └── editions.json    → Characters, abilities, setup per edition
└── static/
    ├── index.html       → Home page: Create game (Storyteller)
    ├── join.html        → Join page (Players)
    ├── storyteller.html → Storyteller dashboard
    └── player.html      → Player role view
```

---

## 🔄 GAME FLOW (User Journey)

### 1. Create Game (Storyteller)
```
index.html
├─ Input: Storyteller name, edition
├─ API: POST /api/game/create
├─ Receives: game_id, storyteller_id
└─ Redirect: storyteller.html?game={game_id}&storyteller={storyteller_id}
```

### 2. Players Join
```
join.html?game={game_id}
├─ Input: Player name
├─ API: POST /api/game/{game_id}/join
├─ Receives: player_id
└─ Redirect: player.html?game={game_id}&player={player_id}
```

### 3. Start Game (Storyteller)
```
storyteller.html
├─ Input: Player count
├─ API: POST /api/game/{game_id}/start (with player_count)
├─ Backend: Randomly distribute roles
└─ Frontend: Shows player list + night phases
```

### 4. View Role (Player)
```
player.html
├─ Polling: GET /api/player/{game_id}/{player_id}/role (every 2s)
├─ Before Start: 404 → Waiting screen
└─ After Start: 200 → Role display
```

---

## 📡 API ENDPOINTS (main.py)

### Edition Data
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/editions` | GET | List of all editions |
| `/api/editions/{edition}/characters` | GET | Characters of an edition |

### Game Management
| Endpoint | Method | Body | Response |
|----------|--------|------|----------|
| `/api/game/create` | POST | `{edition, storyteller_name}` | `{game_id, storyteller_id, join_url}` |
| `/api/game/{game_id}` | GET | - | `{id, edition, started, player_count}` |
| `/api/game/{game_id}/join` | POST | `{player_name}` | `{player_id, name, game_id}` |
| `/api/game/{game_id}/start` | POST | `{player_count}` | `{game_id, started, message}` |

### Player Data
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/player/{game_id}/{player_id}/role` | GET | Role of a player |
| `/api/storyteller/{game_id}/{storyteller_id}/overview` | GET | All roles + night phases |

### Static Files
```python
app.mount("/static", StaticFiles(directory="static"), name="static")
# → Makes static/*.html available under /static/*.html
# → FileResponse("static/index.html") also works without mount
# → Mount enables direct browser access to CSS/JS/images
```

---

## 🎮 GAME SERVICE LOGIC (game_service.py)

### Core Functions

#### `create_game(edition, storyteller_name)`
```python
# 1. Validates edition exists
# 2. Generates game_id (UUID)
# 3. Creates storyteller as Player (is_storyteller=True)
# 4. Stores Game in self.games dict
# 5. Returns Game object
```

#### `join_game(game_id, player_name)`
```python
# 1. Checks: Game exists
# 2. Checks: Game not yet started
# 3. Creates Player with UUID
# 4. Adds to game.players
# 5. Returns Player object
```

#### `start_game(game_id, player_count)`
```python
# 1. Loads setup from editions.json (e.g. 5 players = 3 Townsfolk, 0 Outsider, 1 Minion, 1 Demon)
# 2. Randomly selects characters per type
# 3. Shuffles characters
# 4. Assigns character to each player (except storyteller)
# 5. Sets game.started = True
# 6. Returns Game object
```

#### `get_storyteller_overview(game_id, storyteller_id)`
```python
# 1. Validates: Player is storyteller
# 2. Collects all players + their roles
# 3. Creates night phase lists:
#    - first_night: Sorted by character.first_night (ascending, only > 0)
#    - other_nights: Sorted by character.other_nights (ascending, only > 0)
# 4. Returns {players: [...], night_order: {...}}
```

#### 🌙 `get_night_order(game_id)` - Night Order Generation (v1.2.0+)

**Zweck:** Generiert die Nachtreihenfolge mit automatischer Integration von Minion/Dämon-Info.

**Erste Nacht bei 7+ Spielern:**
```python
# ZUERST werden diese Info-Schritte hinzugefügt:
first_night_actions = [
    {
        "name": "👿 Minion Info",
        "ability": "Wenn 7+ Spieler: Zeige den Minions, wer ihr Dämon ist.",
        "order": 0.1
    },
    {
        "name": "😈 Dämon Info", 
        "ability": "Wenn 7+ Spieler: Zeige dem Dämon, wer seine Minions sind. Außerdem zeige ihm 3 gute Charaktere, die nicht im Spiel sind.",
        "order": 0.2
    }
]
# DANN folgen alle Charakterfähigkeiten (order >= 1)
```

**Sortierung:**
1. Order 0.1: Minion Info *(nur bei 7+ Spielern)*
2. Order 0.2: Dämon Info *(nur bei 7+ Spielern)*
3. Order 1+: Charakterfähigkeiten nach `first_night` Wert aus editions.json

**Wichtig:** 
- Änderung wirkt nur für **neue Spiele** (In-Memory-Storage)
- Bei < 7 Spielern: Keine Info-Schritte, direkt Charaktere

**Frontend-Darstellung:**
- Storyteller-Dashboard → "🌙 Nachtreihenfolge → Erste Nacht"
- Zeigt: Order-Nummer (roter Kreis) + Name + Fähigkeitsbeschreibung

### Role Distribution
```json
// editions.json → setup
{
  "5": {"townsfolk": 3, "outsiders": 0, "minions": 1, "demons": 1},
  "6": {"townsfolk": 3, "outsiders": 1, "minions": 1, "demons": 1},
  ...
}
// → With 5 players: 3 random Townsfolk + 1 Minion + 1 Demon
```

---

## 🌐 FRONTEND DETAILS

### index.html (Create Game)
**JavaScript Flow:**

```javascript
// 1. DOMContentLoaded → loadEditions()
async function loadEditions() {
    const response = await fetch('/api/editions');
    const editions = await response.json();
    // Dynamically populate <select id="editionSelect">
}

// 2. Form Submit
document.getElementById('gameForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevents normal submit
    const storytellerName = document.getElementById('storytellerName').value;
    const edition = document.getElementById('editionSelect').value;

    const response = await fetch('/api/game/create', {
        method: 'POST',
        body: JSON.stringify({edition, storyteller_name: storytellerName})
    });

    const data = await response.json();
    // Redirect to storyteller page
    window.location.href = `../static/storyteller.html`;
});
```

**Event Binding:**
- `addEventListener('submit', ...)` registers handler
- Button `type="submit"` triggers form submit
- Handler runs WITHOUT explicit onClick attributes

---

### storyteller.html (Storyteller Dashboard)
**URL Parameters:**
```javascript
const params = new URLSearchParams(window.location.search);
const gameId = params.get('game');
const storytellerId = params.get('storyteller');
```

**Functions:**
1. **Show Join URL:** `${window.location.origin}/static/join.html?game=${gameId}`
2. **Player Polling:** Every 2s GET `/api/game/{gameId}` → Shows player count
3. **Start Game:** 
   ```javascript
   POST /api/game/{gameId}/start
   Body: {player_count: <input value>}
   ```
4. **Load Overview:**
   ```javascript
   GET /api/storyteller/{gameId}/{storytellerId}/overview
   → Shows player list + night phases
   ```

**❌ OPEN BUG:**
- "Create New Game" box remains visible after start
- **FIX:** CSS `display: none` when `game.started === true`

---

### player.html (Player Role)
**Polling Logic:**
```javascript
async function checkRole() {
  try {
    const response = await fetch(`/api/player/${gameId}/${playerId}/role`);
    
    if (response.status === 404) {
      // Game not yet started
      setTimeout(checkRole, 2000); // Try again after 2s
      showWaiting(); // Show spinner
    } else {
      // Game started
      const role = await response.json();
      showRole(role); // Display role
    }
  } catch (error) {
    console.error(error);
    setTimeout(checkRole, 2000);
  }
}
```

**Role Type Styling:**
```css
.role-type.townsfolk  { background: #e3f2fd; color: #1976d2; } /* Blue */
.role-type.outsiders  { background: #fff3e0; color: #f57c00; } /* Orange */
.role-type.minions    { background: #fce4ec; color: #c2185b; } /* Pink */
.role-type.demons     { background: #ffebee; color: #d32f2f; } /* Red */
```

**❌ OPEN BUG:**
- "Refresh" button remains visible after start
- **FIX:** Hide button after successful role load

---

## 🔍 JAVASCRIPT CONCEPTS EXPLAINED

### 1. Browser Executes JavaScript
```html
<script>
  // This code runs IMMEDIATELY when browser parses it
  console.log('Hello');
</script>

<script>
  // Waits until HTML is fully loaded
  document.addEventListener('DOMContentLoaded', () => {
    // Now all HTML elements exist
  });
</script>
```

### 2. Event Binding Without onClick
```html
<!-- NOT needed: onclick="handleClick()" -->
<button id="myBtn">Click me</button>

<script>
  // Event listener is registered in JavaScript
  document.getElementById('myBtn').addEventListener('click', () => {
    alert('Clicked!');
  });
  // → Button and handler are now connected
</script>
```

### 3. Polling Pattern
```javascript
async function poll() {
  const data = await fetch('/api/status').then(r => r.json());
  
  if (data.ready) {
    showResult(); // Done
  } else {
    setTimeout(poll, 2000); // Try again after 2s
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

## 📚 DATA MODELS (models.py)

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

### Main Classes
```python
class Character(BaseModel):
    id: str
    name: str
    ability: str
    first_night: int      # Order first night (0 = don't call)
    other_nights: int     # Order other nights
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

## 🐛 KNOWN ISSUES & SOLUTIONS

### ✅ SOLVED: "Missing Parameters in URL"
**Problem:** Error after "Create Game"  
**Cause:** Redirect URL had wrong parameters  
**Solution:** Fixed `window.location.href` in index.html

### ✅ SOLVED: White Page
**Problem:** Page remained blank  
**Cause:** JavaScript error or missing API calls  
**Solution:** Improved error handling, fixed DOM-ready events

### ✅ SOLVED: asyncio.run() Error
**Problem:** `RuntimeError: asyncio.run() cannot be called from a running event loop`  
**Cause:** Jupyter/IPython already has event loop  
**Solution:** Use `uvicorn main:app --reload` instead of `uvicorn.run()` in code

### ❌ OPEN: Storyteller UI After Start
**Problem:** "Create New Game" box stays visible  
**Solution:** 
```javascript
if (game.started) {
  document.getElementById('create-game-section').style.display = 'none';
}
```

### ❌ OPEN: Player Update Button
**Problem:** "Refresh" button unnecessary after start  
**Solution:**
```javascript
function showRole(role) {
  // ... display role ...
  const refreshBtn = document.getElementById('refresh-btn');
  if (refreshBtn) refreshBtn.style.display = 'none';
}
```

---

## ⚙️ DEPLOYMENT

### Local Start
```bash
# Start server (Recommended)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Install dependencies
pip install -r requirements.txt

# Validate JSON
python -c "import json; print(json.load(open('data/editions.json')))"
```

### Access
- **Local:** http://localhost:8000
- **Network:** http://<local-ip>:8000
- Players connect with mobile via same WiFi

### Mount vs. FileResponse
```python
# WITH Mount
app.mount("/static", StaticFiles(directory="static"), name="static")
# → Browser can directly call /static/index.html
# → CSS/JS/images work automatically

# WITHOUT Mount
@app.get("/")
async def root():
    return FileResponse("static/index.html")
# → Works for single file
# → But: CSS/JS need their own endpoints
# → Impractical for many files
```

---

## 📝 DATA FORMAT (editions.json)

```json
{
  "trouble-brewing": {
    "name": "Trouble Brewing",
    "characters": {
      "townsfolk": [
        {
          "id": "washerwoman",
          "name": "Washerwoman",
          "ability": "You learn that one of two players is a specific Townsfolk.",
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

**Night Phase Logic:**
- Sort all characters by `first_night` (ascending)
- Filter: Only characters with value > 0
- Show storyteller in this order

---

## ✅ TODO LIST

### High Priority (Bugs)
- [ ] storyteller.html: Hide create box after start
- [ ] player.html: Remove refresh button after start

### Medium Priority (Features)
- [ ] Persistence: SQLite/PostgreSQL instead of in-memory
- [ ] Error handling: Toast notifications in frontend
- [ ] Validation: Check min/max player count

### Low Priority (Nice-to-Have)
- [ ] More editions: Sects & Violets, Bad Moon Rising
- [ ] Player kick function for storyteller
- [ ] Mobile UI optimization
- [ ] Dark mode
- [ ] WebSocket instead of polling

---

## 🧠 IMPORTANT INSIGHTS FOR AI

### How Variables Are Stored
```javascript
// IN BROWSER (JavaScript)
const storytellerName = document.getElementById('storytellerName').value;
// → Gets value from HTML input ON submit
// → Not stored beforehand, only on action

// IN URL (after redirect)
window.location.href = `/static/storyteller.html?game=${gameId}&storyteller=${storytellerId}`;
// → Variables are passed in URL
// → Next page reads with URLSearchParams

// IN SERVER (Python)
self.games[game_id] = game
// → In-memory dictionary
// → Lost on restart
```

### Event Flow
```
1. HTML is loaded → Browser renders elements
2. <script> is executed → Event listeners registered
3. User clicks button → Event fired
4. Event handler runs → Fetch to API
5. API responds → JavaScript processes response
6. DOM is updated → User sees change
```

### Polling Principle
```
Player waits → GET /api/role
├─ 404: Not yet started → setTimeout(check, 2000)
├─ 200: Started → Show role, stop polling
└─ Error: Network error → setTimeout(check, 2000)
```

---

## 📄 CHANGELOG

### v1.2.0 - 2025-12-20 (Minion & Dämon Info)
- ✅ **New Feature:** Minion & Dämon Info in Nachtreihenfolge
  - Fügt zwei neue Info-Schritte am Anfang der ersten Nacht hinzu (nur bei 7+ Spielern)
  - 👿 **Minion Info** (Order 0.1): "Zeige den Minions, wer ihr Dämon ist"
  - 😈 **Dämon Info** (Order 0.2): "Zeige dem Dämon, wer seine Minions sind + 3 gute Charaktere die nicht im Spiel sind"
  - Automatische Sortierung in der Nachtreihenfolge vor allen Charakterfähigkeiten
  - Sichtbar im Storyteller-Dashboard unter "🌙 Nachtreihenfolge → Erste Nacht"
  - Implementiert in: `game_service.py` → `get_night_order()` Funktion
  - **Wichtig:** Nur für neue Spiele wirksam (In-Memory-Storage)
- 🔧 **Verbesserung:** Prompt-Organisation
  - `.github/prompts/docs/` - Dokumentations-Prompts (6 Dateien)
  - `.github/prompts/features/` - Feature-Planungs-Prompts (3 Dateien)
- 📝 **Dokumentation:** Changelog aktualisiert mit v1.2.0

### v1.1 - 2025-01-19 (Quick Rules Feature)
- ✅ **New Feature:** Quick Rules Modal
  - Zugänglich über Button "📜 Regeln" (oben rechts)
  - 4 Kernregeln auf Deutsch (Siegbedingungen, Tag, Nacht, Tod & Abstimmen)
  - Modal mit ESC, Click-outside und X-Button schließbar
  - Keyboard-Navigation und Screen-Reader kompatibel (ARIA)
  - Responsive Design für Mobile (< 600px)
  - Implementiert in: `player.html` und `storyteller.html`
  - Keine Backend-Änderungen notwendig (Pure Frontend)
- 📝 **Dokumentation:** `.github/QUICK_RULES_TESTING.md` hinzugefügt

### v1.0 - 2025-01-19 (Initial Release)
- ✅ FastAPI backend with all endpoints
- ✅ 4 HTML pages (index, join, storyteller, player)
- ✅ Trouble Brewing edition complete
- ✅ Automatic role assignment
- ✅ Night phase order
- ✅ Real-time updates via polling
- ⚠️ 2 UI bugs known (see TODO)

---

## 🎯 FOR FUTURE COPILOT SESSIONS

**Before changing code:**
1. Read this file completely
2. Understand the game flow (user journey)
3. Check open TODOs
4. Test after changes

**Code Style:**
- Backend: Use type hints
- Frontend: Async/await instead of Promises.then()
- Errors: Always HTTPException with detail
- Docs: Document API changes here

**Important Files:**
- `main.py` → API endpoints (REST interface)
- `game_service.py` → Business logic (NO API logic!)
- `storyteller.html` → Most complex frontend file
- `data/editions.json` → Game data (validate schema!)

---

**Created:** 2025-01-19  
**Last Updated:** 2025-12-20  
**Version:** 1.2.0 (Minion & Dämon Info Feature)

