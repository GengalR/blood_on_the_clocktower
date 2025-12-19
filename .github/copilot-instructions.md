# 🤖 Copilot Instructions - Blood on the Clocktower Project

## 🎯 Project Context

**Project Type:** Web Application (FastAPI + Vanilla JavaScript)  
**Purpose:** Digital implementation of the game "Blood on the Clocktower"  
**Tech Stack:** Python 3.13+, FastAPI, Pydantic, Uvicorn, Vanilla HTML/CSS/JS

---

## 📋 CORE PRINCIPLES

### 1. **Honesty Above All**
- ✅ Clearly state when you **don't know** something
- ✅ Admit when a solution is **uncertain**
- ✅ Refer to documentation instead of guessing
- ❌ NEVER invent functions or APIs
- ❌ Don't provide answers if you're not sure

**Example:**
```
❌ "This function exists in FastAPI 0.104.0"
✅ "I'm not sure if this function exists. Let me check the documentation or we can test it."
```

### 2. **Step-by-Step Approach**
Every task is broken down into small, testable steps:

```
Task: "Add player kick function"

Step 1: Create API endpoint
├─ Test: curl request to new endpoint
└─ Expectation: 404 when player doesn't exist

Step 2: Implement service logic
├─ Test: Unit test for kick_player()
└─ Expectation: Player is removed from list

Step 3: Add frontend button
├─ Test: Button appears in UI
└─ Expectation: Fetch to API on click

Step 4: Integration test
├─ Test: E2E - Player is kicked and disappears
└─ Expectation: Other players remain untouched
```

### 3. **Testability is Mandatory**
- Every change must be **testable**
- Write **before** implementation how it will be tested
- Use concrete test scenarios

---

## 🏗️ CODE STANDARDS

### Python (Backend)

#### Always Use Type Hints
```python
# ✅ GOOD
def create_game(edition: str, storyteller_name: str) -> Game:
    game_id: str = str(uuid.uuid4())[:8]
    return Game(id=game_id, edition=edition)

# ❌ BAD
def create_game(edition, storyteller_name):
    game_id = str(uuid.uuid4())[:8]
    return Game(id=game_id, edition=edition)
```

#### Error Handling with Descriptive Messages
```python
# ✅ GOOD
if game_id not in self.games:
    raise HTTPException(
        status_code=404, 
        detail=f"Game with ID '{game_id}' not found. Check if the URL is correct."
    )

# ❌ BAD
if game_id not in self.games:
    raise HTTPException(status_code=404, detail="Not found")
```

#### Pydantic Models for All Data Structures
```python
# ✅ GOOD
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

# ❌ BAD - Using raw dicts
@app.post("/game/create")
async def create_game(data: dict):
    edition = data.get("edition")  # No validation!
```

#### Docstrings for All Public Functions
```python
def start_game(self, game_id: str, player_count: int) -> Game:
    """
    Starts the game and distributes roles to players.
    
    Args:
        game_id: Unique game ID
        player_count: Number of players (excluding storyteller)
        
    Returns:
        Game object with started game and distributed roles
        
    Raises:
        ValueError: If game doesn't exist or invalid player count
        
    Example:
        >>> game = service.start_game("abc123", 5)
        >>> assert game.started == True
        >>> assert len([p for p in game.players if p.character]) == 5
    """
```

### JavaScript (Frontend)

#### Async/Await Instead of Promises
```javascript
// ✅ GOOD
async function loadEditions() {
    try {
        const response = await fetch('/api/editions');
        if (!response.ok) throw new Error('Failed to load editions');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading editions:', error);
        showError('Editions could not be loaded');
    }
}

// ❌ BAD
function loadEditions() {
    fetch('/api/editions')
        .then(r => r.json())
        .then(data => { /* ... */ })
        .catch(err => console.log(err));
}
```

#### Always Include Error Handling
```javascript
// ✅ GOOD
async function createGame(edition, name) {
    try {
        const response = await fetch('/api/game/create', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({edition, storyteller_name: name})
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Unknown error');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Create game failed:', error);
        alert(`Error: ${error.message}`);
        throw error; // Re-throw for caller
    }
}

// ❌ BAD - No error handling
async function createGame(edition, name) {
    const response = await fetch('/api/game/create', {
        method: 'POST',
        body: JSON.stringify({edition, storyteller_name: name})
    });
    return await response.json(); // What if 404?
}
```

#### Constants for Magic Numbers
```javascript
// ✅ GOOD
const POLLING_INTERVAL_MS = 2000;
const MAX_RETRIES = 5;

function startPolling() {
    setTimeout(checkStatus, POLLING_INTERVAL_MS);
}

// ❌ BAD
function startPolling() {
    setTimeout(checkStatus, 2000); // What does 2000 mean?
}
```

---

## 🧪 TESTING GUIDELINES

### 1. Write Test Plan Before Implementation

**Example:**
```markdown
## Test Plan: Kick Player

### API Test
- [ ] POST /api/game/{game_id}/kick with player_id
- [ ] Expectation: 200 OK, player removed
- [ ] Test: GET /api/game/{game_id} → player_count reduced

### Edge Cases
- [ ] Kick storyteller → 400 Bad Request
- [ ] Non-existent player → 404 Not Found
- [ ] Game already started → 400 Bad Request

### Frontend Test
- [ ] Button appears only for storyteller
- [ ] Kick confirmation via confirm dialog
- [ ] Player list updates after kick
```

### 2. Manual Test After Changes

After **every** code change:
```bash
# 1. Start server
uvicorn main:app --reload

# 2. Open browser
# 3. Test feature
# 4. Check browser console for errors
# 5. Check network tab for API calls
```

### 3. Document Test Commands

```markdown
## Test: Create and Start Game

1. Start server: `uvicorn main:app --reload`
2. Browser: http://localhost:8000
3. Enter storyteller name: "TestStoryteller"
4. Select edition: "Trouble Brewing"
5. Click "Create Game"
6. Expectation: Redirect to storyteller.html with game_id in URL
7. Copy join URL
8. Open new incognito window
9. Paste join URL
10. Player name: "TestPlayer"
11. Click "Join"
12. Switch back to storyteller tab
13. Player count: Enter 5
14. Click "Start Game"
15. Expectation: Player list with roles appears
16. Switch to player tab
17. Expectation: Role is displayed
```

---

## 🔍 CODE REVIEW CHECKLIST

Check before each commit:

### Backend
- [ ] Type hints on all functions
- [ ] Docstrings on public functions
- [ ] HTTPException with descriptive `detail`
- [ ] Pydantic models instead of raw dicts
- [ ] Error handling for all edge cases
- [ ] No magic numbers (use constants)

### Frontend
- [ ] Async/await instead of .then()
- [ ] Try-catch around all fetch() calls
- [ ] Check `response.ok` before `.json()`
- [ ] User-friendly error messages
- [ ] Console logs for debugging
- [ ] Constants for timeouts/intervals

### General
- [ ] Code is self-explanatory (good variable names)
- [ ] No duplicates (DRY principle)
- [ ] Functions do only one thing
- [ ] Test plan documented
- [ ] Manual test performed

---

## 🚨 AVOID COMMON MISTAKES

### 1. Missing URL Parameter Validation
```javascript
// ❌ BAD
const gameId = params.get('game');
fetch(`/api/game/${gameId}/start`); // What if gameId is null?

// ✅ GOOD
const gameId = params.get('game');
if (!gameId) {
    alert('Error: No game ID found in URL');
    window.location.href = '/';
    return;
}
```

### 2. Polling Without Stop Condition
```javascript
// ❌ BAD
async function poll() {
    const data = await fetch('/api/status');
    setTimeout(poll, 2000); // Runs forever!
}

// ✅ GOOD
let pollCount = 0;
const MAX_POLLS = 60; // 2 minutes

async function poll() {
    if (pollCount++ > MAX_POLLS) {
        showError('Timeout: Game was not started');
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

### 3. Missing In-Memory Data Validation
```python
# ❌ BAD
def get_game(self, game_id: str) -> Game:
    return self.games[game_id]  # KeyError if doesn't exist!

# ✅ GOOD
def get_game(self, game_id: str) -> Optional[Game]:
    return self.games.get(game_id)
    
# Or with exception
def get_game(self, game_id: str) -> Game:
    if game_id not in self.games:
        raise ValueError(f"Game {game_id} doesn't exist")
    return self.games[game_id]
```

---

## 📁 FILE ORGANIZATION

### When to Create New File?
- **models.py:** All Pydantic models
- **game_service.py:** Business logic (NO API logic!)
- **main.py:** ONLY API endpoints
- **utils.py:** Helper functions (e.g. UUID generator)
- **config.py:** Configuration (e.g. ports, paths)

### What Doesn't Belong in main.py?
```python
# ❌ BAD - Business logic in main.py
@app.post("/api/game/create")
async def create_game(request: CreateGameRequest):
    game_id = str(uuid.uuid4())[:8]
    game = Game(id=game_id, edition=request.edition)
    games[game_id] = game  # Direct access to global dict!
    return {"game_id": game_id}

# ✅ GOOD - Delegate to service
@app.post("/api/game/create")
async def create_game(request: CreateGameRequest):
    try:
        game = game_service.create_game(request.edition, request.storyteller_name)
        return {"game_id": game.id, "storyteller_id": game.players[0].id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## 🔄 CHANGE WORKFLOW

### 1. Understand the Requirement
```
User: "Players should be able to be kicked"

Clarify questions:
- Who can kick? → Only storyteller
- When to kick? → Only before game start
- What happens to role? → N/A (no role assigned yet)
- UI feedback? → Confirmation + list update
```

### 2. Create Task List
```markdown
- [ ] API endpoint: POST /api/game/{game_id}/kick
- [ ] Service method: kick_player(game_id, player_id, requester_id)
- [ ] Validation: Only storyteller, only before start
- [ ] Frontend: Kick button for each player
- [ ] Frontend: Confirmation dialog
- [ ] Frontend: Update list after kick
- [ ] Test: Complete flow end-to-end
```

### 3. Implement Step-by-Step
Implement **one** item, test, then next.

### 4. Document Changes
```markdown
## Changelog Entry

### v1.1 - 2025-01-19
- ✅ Feature: Players can be kicked before game start
  - API: POST /api/game/{game_id}/kick
  - Only storyteller permission
  - Confirmation dialog in frontend
```

---

## 🔧 AVAILABLE TOOLS

### Built-in Tools (IDE)

As Copilot I have access to the following tools:

#### 📁 File Management
- **`read_file`** - Read file contents (with line range)
- **`create_file`** - Create new files
- **`insert_edit_into_file`** - Insert/modify code in existing files
- **`replace_string_in_file`** - Precise string replacements
- **`open_file`** - Open file in editor
- **`list_dir`** - List directory contents
- **`file_search`** - Search files by glob pattern (e.g. `**/*.py`)
- **`grep_search`** - Text search in entire workspace

#### 🔍 Code Analysis
- **`get_errors`** - Get compile/lint errors from a file
  - **IMPORTANT:** Use after every file change!
  - Shows TypeErrors, SyntaxErrors, lint warnings

#### 💻 Terminal
- **`run_in_terminal`** - Execute shell commands
  - PowerShell on Windows
  - Chain commands with `;`
  - `isBackground=true` for server/long-running tasks
- **`get_terminal_output`** - Get output from background processes

#### 🛡️ Security
- **`validate_cves`** - Check dependencies for security vulnerabilities
  - Ecosystem: pip, npm, maven, etc.

#### 🤖 Delegation
- **`run_subagent`** - Specialized agents for complex tasks
  - **Plan Agent:** Researches and creates multi-step plans

---

### 🌐 MCP Server (Model Context Protocol)

Additional capabilities through MCP servers in `mcp.json`:

#### 1. Context7
```json
"context7": {
    "command": "npx",
    "args": [
        "-y",
        "@upstash/context7-mcp",
        "--api-key",
        "ctx7sk-YOUR-API-KEY"
    ]
}
```
**Purpose:** Persistent conversation context between sessions  
**Type:** NPM-based MCP server via npx  
**Use Cases:**
- Store project notes
- Document important decisions
- Maintain context between chat sessions

**Example:**
```
User: "Remember: We use in-memory storage for MVP, later SQLite"
Copilot: [Uses Context7 to store]

--- New Session ---
User: "Why don't we use a real DB?"
Copilot: [Reads from Context7] "We decided to use in-memory for MVP..."
```

#### 2. DuckDuckGo Search
```json
"duckduckgo": {
    "type": "stdio",
    "command": "uvx",
    "args": ["duckduckgo-mcp-server"]
}
```
**Purpose:** Internet search for current information  
**Use Cases:**
- Search for current library versions
- Research best practices
- Google error messages
- Find documentation

**Example:**
```
User: "How to do WebSockets in FastAPI?"
Copilot: [Uses DuckDuckGo Search]
"According to current FastAPI docs (v0.109.0) WebSocket is implemented like this..."
```

---

### 🎯 Tool Usage Best Practices

#### 1. Always Check Errors After Code Changes
```python
# After insert_edit_into_file or replace_string_in_file:
# → ALWAYS call get_errors!

# Example workflow:
1. replace_string_in_file("main.py", ...)
2. get_errors(["main.py"])
3. If errors: Fix and check again
```

#### 2. Use Terminal for Tests
```bash
# Start server (Background)
run_in_terminal("uvicorn main:app --reload", isBackground=True)

# Run tests (Foreground)
run_in_terminal("pytest tests/", isBackground=False)

# Install dependencies
run_in_terminal("pip install fastapi uvicorn", isBackground=False)
```

#### 3. DuckDuckGo Search for Uncertainties
```
When unsure about API/feature:
1. DON'T guess or invent
2. Use DuckDuckGo Search
3. Find official docs
4. Answer with source
```

#### 4. Context7 for Project Memory
```
For important decisions:
- Store architecture decisions
- Store known bugs + workarounds
- Store team preferences
```

#### 5. grep_search Before Changes
```python
# Before changing a function:
# 1. Search where it's used
grep_search("def create_game", includePattern="**/*.py")

# 2. Understand impact
# 3. Change all usage locations
```

---

### 🚫 Tool Limitations

#### What Tools CANNOT Do:
- ❌ **read_file:** Cannot read entire large files at once
  - Solution: Specify line range or use grep_search
- ❌ **run_in_terminal:** No interactive input possible
  - Solution: Use flags (e.g. `pip install -y`)
- ❌ **DuckDuckGo Search:** Rate limits with too many queries
  - Solution: Use sparingly, check local docs first

---

### 📊 Tool Selection Decision Tree

```
Question: "How do I do X in FastAPI?"
├─ Do I have sure answer? → Answer directly
├─ Is it in project docs? → read_file(".github/PROJECT_DOCUMENTATION.md")
├─ Is it in code examples? → grep_search("X")
└─ No idea? → DuckDuckGo Search "FastAPI X documentation"

Task: "Add feature Y"
├─ Complex? → run_subagent("Plan", "Create step-by-step plan for Y")
├─ Simple? → Implement directly
└─ After implementation:
    ├─ get_errors(["changed_file.py"])
    ├─ run_in_terminal("pytest tests/")
    └─ Update documentation

User reports error: "Z doesn't work"
├─ Reproduce error → run_in_terminal("python test_z.py")
├─ Check logs → read_file("logs/error.log")
├─ Search internet → DuckDuckGo Search "FastAPI error message Z"
└─ Implement fix → replace_string_in_file(...)
```

---

### 💡 Tool Combination Examples

#### Example 1: Add New Function
```
1. grep_search("create_game") 
   → Understand existing patterns

2. insert_edit_into_file("game_service.py")
   → Add new function

3. get_errors(["game_service.py"])
   → Check for syntax/type errors

4. grep_search("test_create_game")
   → Find test patterns

5. create_file("tests/test_new_feature.py")
   → Create tests

6. run_in_terminal("pytest tests/test_new_feature.py")
   → Run tests

7. replace_string_in_file(".github/PROJECT_DOCUMENTATION.md")
   → Document feature
```

#### Example 2: Fix Bug with Unknown Error Message
```
1. User: "Error: 'NoneType' has no attribute 'id'"

2. grep_search(".id", includePattern="**/*.py")
   → Find all locations with .id

3. read_file("main.py", lines_with_error)
   → Understand context

4. DuckDuckGo Search "Python NoneType has no attribute best practices"
   → Learn about guard clauses

5. replace_string_in_file("main.py")
   → Add None check

6. get_errors(["main.py"])
   → Validate fix

7. run_in_terminal("uvicorn main:app --reload", isBackground=True)
   → Start server

8. User tests manually → Success!
```

#### Example 3: Research Before Implementation
```
User: "Should we use WebSockets instead of polling?"

1. Context7: Load previous discussions
   → Were there considerations before?

2. DuckDuckGo Search "FastAPI WebSocket vs Polling performance"
   → Research pros/cons

3. DuckDuckGo Search "WebSocket browser support 2025"
   → Check compatibility

4. run_subagent("Plan", "Create migration plan from polling to WebSocket")
   → Plan implementation

5. Present result with sources
   → User decides informed

6. Context7: Store decision
   → For future sessions
```

---

## 🎓 LEARNING RESOURCES

### When you don't know what to do:

1. **Project Documentation:** `.github/PROJECT_DOCUMENTATION.md` (ALWAYS FIRST!)
2. **Copilot Instructions:** `.github/copilot-instructions.md` (This file)
3. **FastAPI Docs:** https://fastapi.tiangolo.com/ (via DuckDuckGo Search)
4. **Pydantic Docs:** https://docs.pydantic.dev/ (via DuckDuckGo Search)
5. **MDN Web Docs:** https://developer.mozilla.org/ (JavaScript, via DuckDuckGo Search)

### Order When Uncertain:
```
1. Read project docs (read_file)
   ↓ No answer?
2. Search code (grep_search)
   ↓ No answer?
3. Internet research (DuckDuckGo Search)
   ↓ No answer?
4. Be HONEST: "I don't know, let's test together"
```

### Example Answer When Uncertain:
```
"I'm not sure if FastAPI has built-in WebSocket support. 

Let me check:
1. [DuckDuckGo Search] Look in FastAPI docs for WebSocket
2. [read_file] Check if it's already used in the project
3. [run_in_terminal] Test with small example

One moment..."

[Uses DuckDuckGo Search]

"✅ Yes, FastAPI has WebSocket support since version 0.45.0. 
Source: https://fastapi.tiangolo.com/advanced/websockets/

Should I implement an example?"
```

---

## ✅ SUCCESS METRICS

A feature is complete when:
- [ ] Code is written and works
- [ ] Manually tested (happy path + edge cases)
- [ ] Error handling implemented
- [ ] Documentation updated (PROJECT_DOCUMENTATION.md)
- [ ] Changelog entry written
- [ ] No errors in browser console
- [ ] No Python exceptions in terminal

---

## 🚀 DEPLOYMENT CHECKLIST

Before production deployment:
- [ ] All TODOs from documentation completed
- [ ] Error messages are user-friendly (no stack traces)
- [ ] Logging implemented (for debugging)
- [ ] Secrets in environment variables (.env)
- [ ] CORS configured (if frontend on separate domain)
- [ ] Consider rate limiting (against spam)

---

## 💡 PHILOSOPHY

### DRY - Don't Repeat Yourself
If code appears 2x → Extract into function

### KISS - Keep It Simple, Stupid
Simple solution > complex solution

### YAGNI - You Ain't Gonna Need It
Don't implement features "for later"

### Testability Over Perfection
Better simple code that can be tested than complex "perfect" code

---

**Summary:**
1. ✅ Be honest when you don't know something
2. ✅ Proceed step-by-step
3. ✅ Everything must be testable
4. ✅ Type hints, error handling, docstrings
5. ✅ Test plan before implementation
6. ✅ Update documentation
7. ✅ Use tools correctly (get_errors, DuckDuckGo Search, Context7)
8. ✅ Always validate after changes

**These principles apply to EVERY code change in the project.**

---

## 🛠️ QUICK REFERENCE: Tool Cheat Sheet

| Situation | Tool | Command |
|-----------|------|---------|
| Read file | `read_file` | read_file("path/to/file", start, end) |
| Change code | `replace_string_in_file` | Precise string replacement |
| New file | `create_file` | create_file("path", content) |
| Check errors | `get_errors` | get_errors(["file.py"]) ⚠️ AFTER EVERY CHANGE |
| Search text | `grep_search` | grep_search("pattern") |
| Find files | `file_search` | file_search("**/*.py") |
| Start server | `run_in_terminal` | isBackground=True |
| Run tests | `run_in_terminal` | isBackground=False |
| Uncertain? | `DuckDuckGo Search` | Internet research |
| Complex? | `run_subagent` | Plan agent for multi-step |
| Remember! | `Context7` | Persistent notes |

---

**Created:** 2025-01-19  
**Last Updated:** 2025-12-19  
**Version:** 1.2.1 (Context7 updated to npx-based configuration)

