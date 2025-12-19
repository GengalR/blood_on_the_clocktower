# 🤖 Copilot Instructions - Blood on the Clocktower Project

## 🎯 Projekt-Kontext

**Projekttyp:** Web-Anwendung (FastAPI + Vanilla JavaScript)  
**Zweck:** Digitale Umsetzung des Spiels "Blood on the Clocktower"  
**Tech-Stack:** Python 3.13+, FastAPI, Pydantic, Uvicorn, Vanilla HTML/CSS/JS

---

## 📋 GRUNDPRINZIPIEN

### 1. **Ehrlichkeit vor allem**
- ✅ Sage klar, wenn du etwas **nicht weißt**
- ✅ Gib zu, wenn eine Lösung **unsicher** ist
- ✅ Verweise auf Dokumentation statt zu raten
- ❌ Erfinde KEINE Funktionen oder APIs
- ❌ Gib keine Antwort, wenn du nicht sicher bist

**Beispiel:**
```
❌ "Diese Funktion existiert in FastAPI 0.104.0"
✅ "Ich bin nicht sicher ob diese Funktion existiert. Lass mich die Dokumentation prüfen oder wir testen es."
```

### 2. **Step-by-Step Approach**
Jede Aufgabe wird in kleine, testbare Schritte zerlegt:

```
Aufgabe: "Füge Spieler-Kick-Funktion hinzu"

Schritt 1: API-Endpoint erstellen
├─ Test: curl-Request zum neuen Endpoint
└─ Erwartung: 404 wenn Spieler nicht existiert

Schritt 2: Service-Logik implementieren
├─ Test: Unit-Test für kick_player()
└─ Erwartung: Spieler wird aus Liste entfernt

Schritt 3: Frontend-Button hinzufügen
├─ Test: Button erscheint in UI
└─ Erwartung: Fetch zu API bei Click

Schritt 4: Integration testen
├─ Test: E2E - Spieler wird gekickt und verschwindet
└─ Erwartung: Andere Spieler bleiben unberührt
```

### 3. **Testbarkeit ist Pflicht**
- Jede Änderung muss **testbar** sein
- Schreibe **vor** der Implementierung wie getestet wird
- Nutze konkrete Test-Szenarien

---

## 🏗️ CODE-STANDARDS

### Python (Backend)

#### Type Hints immer verwenden
```python
# ✅ GUT
def create_game(edition: str, storyteller_name: str) -> Game:
    game_id: str = str(uuid.uuid4())[:8]
    return Game(id=game_id, edition=edition)

# ❌ SCHLECHT
def create_game(edition, storyteller_name):
    game_id = str(uuid.uuid4())[:8]
    return Game(id=game_id, edition=edition)
```

#### Error Handling mit aussagekräftigen Messages
```python
# ✅ GUT
if game_id not in self.games:
    raise HTTPException(
        status_code=404, 
        detail=f"Spiel mit ID '{game_id}' nicht gefunden. Prüfe ob die URL korrekt ist."
    )

# ❌ SCHLECHT
if game_id not in self.games:
    raise HTTPException(status_code=404, detail="Not found")
```

#### Pydantic Models für alle Datenstrukturen
```python
# ✅ GUT
class CreateGameRequest(BaseModel):
    edition: str
    storyteller_name: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "edition": "trouble-brewing",
                "storyteller_name": "Alex"
            }
        }
    )

# ❌ SCHLECHT - Rohe Dicts verwenden
@app.post("/game/create")
async def create_game(data: dict):
    edition = data.get("edition")  # Keine Validation!
```

#### Docstrings für alle öffentlichen Funktionen
```python
def start_game(self, game_id: str, player_count: int) -> Game:
    """
    Startet das Spiel und verteilt Rollen an Spieler.
    
    Args:
        game_id: Eindeutige Spiel-ID
        player_count: Anzahl der Spieler (ohne Erzähler)
        
    Returns:
        Game-Objekt mit gestarteten Spiel und verteilten Rollen
        
    Raises:
        ValueError: Wenn Spiel nicht existiert oder ungültige Spielerzahl
        
    Example:
        >>> game = service.start_game("abc123", 5)
        >>> assert game.started == True
        >>> assert len([p for p in game.players if p.character]) == 5
    """
```

### JavaScript (Frontend)

#### Async/Await statt Promises
```javascript
// ✅ GUT
async function loadEditions() {
    try {
        const response = await fetch('/api/editions');
        if (!response.ok) throw new Error('Failed to load editions');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading editions:', error);
        showError('Editionen konnten nicht geladen werden');
    }
}

// ❌ SCHLECHT
function loadEditions() {
    fetch('/api/editions')
        .then(r => r.json())
        .then(data => { /* ... */ })
        .catch(err => console.log(err));
}
```

#### Error Handling immer einbauen
```javascript
// ✅ GUT
async function createGame(edition, name) {
    try {
        const response = await fetch('/api/game/create', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({edition, storyteller_name: name})
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Unbekannter Fehler');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Create game failed:', error);
        alert(`Fehler: ${error.message}`);
        throw error; // Re-throw für Aufrufer
    }
}

// ❌ SCHLECHT - Kein Error Handling
async function createGame(edition, name) {
    const response = await fetch('/api/game/create', {
        method: 'POST',
        body: JSON.stringify({edition, storyteller_name: name})
    });
    return await response.json(); // Was wenn 404?
}
```

#### Konstanten für Magic Numbers
```javascript
// ✅ GUT
const POLLING_INTERVAL_MS = 2000;
const MAX_RETRIES = 5;

function startPolling() {
    setTimeout(checkStatus, POLLING_INTERVAL_MS);
}

// ❌ SCHLECHT
function startPolling() {
    setTimeout(checkStatus, 2000); // Was bedeutet 2000?
}
```

---

## 🧪 TESTING-RICHTLINIEN

### 1. Vor jeder Implementierung Test-Plan schreiben

**Beispiel:**
```markdown
## Test-Plan: Spieler kicken

### API-Test
- [ ] POST /api/game/{game_id}/kick mit player_id
- [ ] Erwartung: 200 OK, Spieler entfernt
- [ ] Test: GET /api/game/{game_id} → player_count reduziert

### Edge Cases
- [ ] Erzähler kicken → 400 Bad Request
- [ ] Nicht-existierender Spieler → 404 Not Found
- [ ] Spiel bereits gestartet → 400 Bad Request

### Frontend-Test
- [ ] Button erscheint nur bei Erzähler
- [ ] Kick-Bestätigung via Confirm-Dialog
- [ ] Spielerliste aktualisiert sich nach Kick
```

### 2. Manueller Test nach Änderung

Nach **jeder** Code-Änderung:
```bash
# 1. Server starten
uvicorn main:app --reload

# 2. Browser öffnen
# 3. Feature testen
# 4. Browser-Konsole auf Fehler prüfen
# 5. Network-Tab für API-Calls prüfen
```

### 3. Test-Befehle dokumentieren

```markdown
## Test: Spiel erstellen und starten

1. Server starten: `uvicorn main:app --reload`
2. Browser: http://localhost:8000
3. Erzähler-Name eingeben: "TestErzähler"
4. Edition wählen: "Trouble Brewing"
5. "Spiel erstellen" klicken
6. Erwartung: Redirect zu storyteller.html mit game_id in URL
7. Join-URL kopieren
8. Neues Inkognito-Fenster öffnen
9. Join-URL einfügen
10. Spieler-Name: "TestSpieler"
11. "Beitreten" klicken
12. Zurück zu Erzähler-Tab
13. Spielerzahl: 5 eingeben
14. "Spiel starten" klicken
15. Erwartung: Spielerliste mit Rollen erscheint
16. Zu Spieler-Tab wechseln
17. Erwartung: Rolle wird angezeigt
```

---

## 🔍 CODE-REVIEW-CHECKLISTE

Vor jedem Commit prüfen:

### Backend
- [ ] Type Hints bei allen Funktionen
- [ ] Docstrings bei öffentlichen Funktionen
- [ ] HTTPException mit aussagekräftiger `detail`
- [ ] Pydantic Models statt rohe Dicts
- [ ] Error Handling für alle Edge Cases
- [ ] Keine Magic Numbers (nutze Konstanten)

### Frontend
- [ ] Async/Await statt .then()
- [ ] Try-Catch um alle fetch() Calls
- [ ] `response.ok` prüfen vor `.json()`
- [ ] User-freundliche Fehlermeldungen
- [ ] Konsole-Logs für Debugging
- [ ] Konstanten für Timeouts/Intervalle

### Allgemein
- [ ] Code ist selbsterklärend (gute Variablennamen)
- [ ] Keine Duplikate (DRY-Prinzip)
- [ ] Funktionen machen nur eine Sache
- [ ] Test-Plan dokumentiert
- [ ] Manueller Test durchgeführt

---

## 🚨 HÄUFIGE FEHLER VERMEIDEN

### 1. Fehlende URL-Parameter-Validierung
```javascript
// ❌ SCHLECHT
const gameId = params.get('game');
fetch(`/api/game/${gameId}/start`); // Was wenn gameId null?

// ✅ GUT
const gameId = params.get('game');
if (!gameId) {
    alert('Fehler: Keine Spiel-ID in URL gefunden');
    window.location.href = '/';
    return;
}
```

### 2. Polling ohne Stop-Bedingung
```javascript
// ❌ SCHLECHT
async function poll() {
    const data = await fetch('/api/status');
    setTimeout(poll, 2000); // Läuft ewig!
}

// ✅ GUT
let pollCount = 0;
const MAX_POLLS = 60; // 2 Minuten

async function poll() {
    if (pollCount++ > MAX_POLLS) {
        showError('Timeout: Spiel wurde nicht gestartet');
        return;
    }
    
    const data = await fetch('/api/status');
    if (data.ready) {
        showResult(); // Stop
    } else {
        setTimeout(poll, 2000);
    }
}
```

### 3. Fehlende In-Memory-Daten-Validierung
```python
# ❌ SCHLECHT
def get_game(self, game_id: str) -> Game:
    return self.games[game_id]  # KeyError wenn nicht existiert!

# ✅ GUT
def get_game(self, game_id: str) -> Optional[Game]:
    return self.games.get(game_id)
    
# Oder mit Exception
def get_game(self, game_id: str) -> Game:
    if game_id not in self.games:
        raise ValueError(f"Spiel {game_id} existiert nicht")
    return self.games[game_id]
```

---

## 📁 DATEI-ORGANISATION

### Wann neue Datei erstellen?
- **models.py:** Alle Pydantic Models
- **game_service.py:** Business Logic (KEINE API-Logik!)
- **main.py:** NUR API-Endpoints
- **utils.py:** Hilfsfunktionen (z.B. UUID-Generator)
- **config.py:** Konfiguration (z.B. Ports, Paths)

### Was gehört NICHT in main.py?
```python
# ❌ SCHLECHT - Business Logic in main.py
@app.post("/api/game/create")
async def create_game(request: CreateGameRequest):
    game_id = str(uuid.uuid4())[:8]
    game = Game(id=game_id, edition=request.edition)
    games[game_id] = game  # Direkter Zugriff auf globales Dict!
    return {"game_id": game_id}

# ✅ GUT - Delegation an Service
@app.post("/api/game/create")
async def create_game(request: CreateGameRequest):
    try:
        game = game_service.create_game(request.edition, request.storyteller_name)
        return {"game_id": game.id, "storyteller_id": game.players[0].id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## 🔄 CHANGE-WORKFLOW

### 1. Verstehe die Anforderung
```
User: "Spieler sollen gekickt werden können"

Fragen klären:
- Wer darf kicken? → Nur Erzähler
- Wann kicken? → Nur vor Spielstart
- Was passiert mit Rolle? → N/A (keine Rolle zugeteilt)
- UI-Feedback? → Bestätigung + Liste-Update
```

### 2. Erstelle Task-Liste
```markdown
- [ ] API-Endpoint: POST /api/game/{game_id}/kick
- [ ] Service-Methode: kick_player(game_id, player_id, requester_id)
- [ ] Validierung: Nur Erzähler, nur vor Start
- [ ] Frontend: Kick-Button bei jedem Spieler
- [ ] Frontend: Bestätigungs-Dialog
- [ ] Frontend: Liste aktualisieren nach Kick
- [ ] Test: Kompletter Flow durchspielen
```

### 3. Implementiere Step-by-Step
Implementiere **einen** Punkt, teste, dann nächster.

### 4. Dokumentiere Änderungen
```markdown
## Changelog-Eintrag

### v1.1 - 2025-01-19
- ✅ Feature: Spieler können vor Spielstart gekickt werden
  - API: POST /api/game/{game_id}/kick
  - Nur Erzähler-Berechtigung
  - Bestätigungs-Dialog im Frontend
```

---

## 🔧 VERFÜGBARE TOOLS

### Built-in Tools (PyCharm IDE)

Als Copilot in PyCharm habe ich Zugriff auf folgende Tools:

#### 📁 Dateiverwaltung
- **`read_file`** - Dateiinhalte lesen (mit Zeilenbereich)
- **`create_file`** - Neue Dateien erstellen
- **`insert_edit_into_file`** - Code in existierende Dateien einfügen/ändern
- **`replace_string_in_file`** - Präzise String-Ersetzungen
- **`open_file`** - Datei im Editor öffnen
- **`list_dir`** - Verzeichnisinhalte auflisten
- **`file_search`** - Dateien nach Glob-Pattern suchen (z.B. `**/*.py`)
- **`grep_search`** - Text-Suche im gesamten Workspace

#### 🔍 Code-Analyse
- **`get_errors`** - Compile/Lint-Fehler einer Datei abrufen
  - **WICHTIG:** Nach jeder Datei-Änderung verwenden!
  - Zeigt TypeErrors, SyntaxErrors, Lint-Warnungen

#### 💻 Terminal
- **`run_in_terminal`** - Shell-Befehle ausführen
  - PowerShell unter Windows
  - Mit `;` mehrere Befehle verketten
  - `isBackground=true` für Server/Long-Running Tasks
- **`get_terminal_output`** - Output von Background-Prozessen abrufen

#### 🛡️ Sicherheit
- **`validate_cves`** - Dependencies auf Sicherheitslücken prüfen
  - Ecosystem: pip, npm, maven, etc.

#### 🤖 Delegation
- **`run_subagent`** - Spezialisierte Agents für komplexe Tasks
  - **Plan Agent:** Recherchiert und erstellt Multi-Step-Pläne

---

### 🌐 MCP Server (Model Context Protocol)

Zusätzliche Fähigkeiten durch MCP-Server in `mcp.json`:

#### 1. Context7
```json
"context7": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@upstatement/context7-mcp-server"]
}
```
**Zweck:** Persistenter Konversationskontext zwischen Sessions  
**Use Cases:**
- Projekt-Notizen speichern
- Wichtige Entscheidungen dokumentieren
- Zwischen Chat-Sessions Kontext behalten

**Beispiel:**
```
User: "Speichere: Wir verwenden In-Memory Storage für MVP, später SQLite"
Copilot: [Nutzt Context7 zum Speichern]

--- Neue Session ---
User: "Warum nutzen wir kein echtes DB?"
Copilot: [Liest aus Context7] "Wir haben entschieden In-Memory für MVP zu nutzen..."
```

#### 2. Brave Search
```json
"brave-search": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
        "BRAVE_API_KEY": "YOUR_API_KEY"
    }
}
```
**Zweck:** Internet-Suche für aktuelle Informationen  
**Use Cases:**
- Aktuelle Library-Versionen suchen
- Best Practices recherchieren
- Error-Messages googeln
- Dokumentation finden

**Beispiel:**
```
User: "Wie macht man WebSockets in FastAPI?"
Copilot: [Nutzt Brave Search]
"Laut aktueller FastAPI-Docs (v0.109.0) wird WebSocket so implementiert..."
```

#### 3. Puppeteer
```json
"puppeteer": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
}
```
**Zweck:** Browser-Automatisierung & Web-Scraping  
**Use Cases:**
- Webseiten-Inhalte extrahieren
- Screenshots erstellen
- JavaScript auf Webseiten ausführen
- API-Dokumentation scrapen

**Beispiel:**
```
User: "Lade die FastAPI-Docs zu WebSockets"
Copilot: [Nutzt Puppeteer]
"Ich habe die Seite geladen und hier ist der relevante Abschnitt..."
```

---

### 🎯 Tool-Usage Best Practices

#### 1. Nach Code-Änderungen immer Fehler prüfen
```python
# Nach insert_edit_into_file oder replace_string_in_file:
# → IMMER get_errors aufrufen!

# Beispiel-Workflow:
1. replace_string_in_file("main.py", ...)
2. get_errors(["main.py"])
3. Falls Fehler: Korrigieren und erneut prüfen
```

#### 2. Terminal für Tests nutzen
```bash
# Server starten (Background)
run_in_terminal("uvicorn main:app --reload", isBackground=True)

# Tests ausführen (Foreground)
run_in_terminal("pytest tests/", isBackground=False)

# Dependencies installieren
run_in_terminal("pip install fastapi uvicorn", isBackground=False)
```

#### 3. Brave Search für Unsicherheiten
```
Wenn unsicher über API/Feature:
1. NICHT raten oder erfinden
2. Brave Search nutzen
3. Offizielle Docs finden
4. Antwort mit Quelle geben
```

#### 4. Context7 für Projekt-Memory
```
Bei wichtigen Entscheidungen:
- Speichere Architektur-Entscheidungen
- Speichere bekannte Bugs + Workarounds
- Speichere Team-Präferenzen
```

#### 5. grep_search vor Änderungen
```python
# Bevor du eine Funktion änderst:
# 1. Suche wo sie verwendet wird
grep_search("def create_game", includePattern="**/*.py")

# 2. Verstehe Impact
# 3. Ändere alle Verwendungsstellen
```

---

### 🚫 Tool-Limitierungen

#### Was Tools NICHT können:
- ❌ **read_file:** Kann nicht ganze große Dateien auf einmal lesen
  - Lösung: Zeilenbereich angeben oder grep_search nutzen
- ❌ **run_in_terminal:** Kein interaktiver Input möglich
  - Lösung: Flags nutzen (z.B. `pip install -y`)
- ❌ **Brave Search:** Begrenzte API-Calls (2000/Monat kostenlos)
  - Lösung: Sparsam einsetzen, erst lokale Docs prüfen
- ❌ **Puppeteer:** JavaScript-Heavy-Apps können langsam sein
  - Lösung: Direkte API-Calls bevorzugen wenn verfügbar

---

### 📊 Tool-Auswahl-Entscheidungsbaum

```
Frage: "Wie mache ich X in FastAPI?"
├─ Habe ich sichere Antwort? → Direkt antworten
├─ Steht in Projekt-Docs? → read_file(".github/PROJEKT_DOKUMENTATION.md")
├─ Ist im Code-Beispiel? → grep_search("X")
└─ Keine Ahnung? → Brave Search "FastAPI X documentation"

Aufgabe: "Füge Feature Y hinzu"
├─ Komplex? → run_subagent("Plan", "Erstelle Step-by-Step Plan für Y")
├─ Einfach? → Direkt implementieren
└─ Nach Implementierung:
    ├─ get_errors(["geänderte_datei.py"])
    ├─ run_in_terminal("pytest tests/")
    └─ Dokumentation aktualisieren

User meldet Fehler: "Z funktioniert nicht"
├─ Fehler reproduzieren → run_in_terminal("python test_z.py")
├─ Logs prüfen → read_file("logs/error.log")
├─ Im Internet suchen → Brave Search "FastAPI error message Z"
└─ Fix implementieren → replace_string_in_file(...)
```

---

### 💡 Tool-Kombination Beispiele

#### Beispiel 1: Neue Funktion hinzufügen
```
1. grep_search("create_game") 
   → Verstehe existierende Patterns

2. insert_edit_into_file("game_service.py")
   → Füge neue Funktion hinzu

3. get_errors(["game_service.py"])
   → Prüfe auf Syntax-/Type-Fehler

4. grep_search("test_create_game")
   → Finde Test-Patterns

5. create_file("tests/test_new_feature.py")
   → Erstelle Tests

6. run_in_terminal("pytest tests/test_new_feature.py")
   → Führe Tests aus

7. replace_string_in_file(".github/PROJEKT_DOKUMENTATION.md")
   → Dokumentiere Feature
```

#### Beispiel 2: Bug fixen mit unbekannter Error-Message
```
1. User: "Fehler: 'NoneType' has no attribute 'id'"

2. grep_search(".id", includePattern="**/*.py")
   → Finde alle Stellen mit .id

3. read_file("main.py", zeilen_mit_fehler)
   → Verstehe Kontext

4. Brave Search "Python NoneType has no attribute best practices"
   → Lerne über Guard-Clauses

5. replace_string_in_file("main.py")
   → Füge None-Check hinzu

6. get_errors(["main.py"])
   → Validiere Fix

7. run_in_terminal("uvicorn main:app --reload", isBackground=True)
   → Starte Server

8. User testet manuell → Erfolg!
```

#### Beispiel 3: Research vor Implementierung
```
User: "Sollen wir WebSockets statt Polling nutzen?"

1. Context7: Lade bisherige Diskussionen
   → Gab es schon Überlegungen?

2. Brave Search "FastAPI WebSocket vs Polling performance"
   → Recherchiere Pros/Cons

3. Brave Search "WebSocket browser support 2025"
   → Prüfe Kompatibilität

4. run_subagent("Plan", "Erstelle Migrations-Plan von Polling zu WebSocket")
   → Plane Umsetzung

5. Präsentiere Ergebnis mit Quellen
   → User entscheidet informiert

6. Context7: Speichere Entscheidung
   → Für zukünftige Sessions
```

---

## 🎓 LERN-RESSOURCEN

### Wenn du nicht weiter weißt:

1. **Projekt-Dokumentation:** `.github/PROJEKT_DOKUMENTATION.md` (IMMER ZUERST!)
2. **Copilot Instructions:** `.github/copilot-instructions.md` (Diese Datei)
3. **FastAPI Docs:** https://fastapi.tiangolo.com/ (via Brave Search)
4. **Pydantic Docs:** https://docs.pydantic.dev/ (via Brave Search)
5. **MDN Web Docs:** https://developer.mozilla.org/ (JavaScript, via Brave Search)

### Reihenfolge bei Unsicherheit:
```
1. Projekt-Docs lesen (read_file)
   ↓ Keine Antwort?
2. Code durchsuchen (grep_search)
   ↓ Keine Antwort?
3. Internet-Recherche (Brave Search)
   ↓ Keine Antwort?
4. EHRLICH sagen: "Ich weiß es nicht, lass uns gemeinsam testen"
```

### Beispiel-Antwort bei Unsicherheit:
```
"Ich bin mir nicht sicher, ob FastAPI einen eingebauten WebSocket-Support hat. 

Lass mich das prüfen:
1. [Brave Search] Schaue in FastAPI-Docs nach WebSocket
2. [read_file] Prüfe ob es bereits im Projekt verwendet wird
3. [run_in_terminal] Teste mit kleinem Beispiel

Einen Moment..."

[Nutzt Brave Search]

"✅ Ja, FastAPI hat WebSocket-Support ab Version 0.45.0. 
Quelle: https://fastapi.tiangolo.com/advanced/websockets/

Soll ich ein Beispiel implementieren?"
```

---

## ✅ ERFOLGS-METRIKEN

Ein Feature ist fertig, wenn:
- [ ] Code geschrieben und funktioniert
- [ ] Manuell getestet (happy path + edge cases)
- [ ] Error Handling implementiert
- [ ] Dokumentation aktualisiert (PROJEKT_DOKUMENTATION.md)
- [ ] Changelog-Eintrag geschrieben
- [ ] Keine Fehler in Browser-Konsole
- [ ] Keine Python-Exceptions im Terminal

---

## 🚀 DEPLOYMENT-CHECKLISTE

Vor Production-Deployment:
- [ ] Alle TODOs aus Dokumentation abgearbeitet
- [ ] Error Messages sind user-freundlich (keine Stacktraces)
- [ ] Logging implementiert (für Debugging)
- [ ] Secrets in Environment Variables (.env)
- [ ] CORS konfiguriert (falls Frontend separate Domain)
- [ ] Rate Limiting erwägen (gegen Spam)

---

## 💡 PHILOSOPHIE

### DRY - Don't Repeat Yourself
Wenn Code 2x vorkommt → Funktion extrahieren

### KISS - Keep It Simple, Stupid
Einfache Lösung > komplexe Lösung

### YAGNI - You Ain't Gonna Need It
Keine Features implementieren "für später"

### Testbarkeit über Perfektion
Lieber simpler Code der getestet werden kann, als komplexer "perfekter" Code

---

**Zusammenfassung:**
1. ✅ Ehrlich sein wenn du etwas nicht weißt
2. ✅ Step-by-Step vorgehen
3. ✅ Alles muss testbar sein
4. ✅ Type Hints, Error Handling, Docstrings
5. ✅ Test-Plan vor Implementierung
6. ✅ Dokumentation aktualisieren
7. ✅ Tools richtig einsetzen (get_errors, Brave Search, Context7)
8. ✅ Nach Änderungen immer validieren

**Diese Prinzipien gelten für JEDE Code-Änderung im Projekt.**

---

## 🛠️ QUICK REFERENCE: Tool-Cheat-Sheet

| Situation | Tool | Befehl |
|-----------|------|--------|
| Datei lesen | `read_file` | read_file("path/to/file", start, end) |
| Code ändern | `replace_string_in_file` | Präzise String-Ersetzung |
| Neue Datei | `create_file` | create_file("path", content) |
| Fehler prüfen | `get_errors` | get_errors(["file.py"]) ⚠️ NACH JEDER ÄNDERUNG |
| Text suchen | `grep_search` | grep_search("pattern") |
| Dateien finden | `file_search` | file_search("**/*.py") |
| Server starten | `run_in_terminal` | isBackground=True |
| Tests laufen | `run_in_terminal` | isBackground=False |
| Unsicher? | `Brave Search` | Internet-Recherche |
| Komplex? | `run_subagent` | Plan-Agent für Multi-Step |
| Merken! | `Context7` | Persistente Notizen |

---

**Erstellt:** 2025-01-19  
**Letzte Aktualisierung:** 2025-01-19  
**Version:** 1.1.0 (Tools & MCP Server hinzugefügt)

