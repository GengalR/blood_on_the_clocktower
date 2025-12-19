# 📝 Update Agent - Dokumentations-Synchronisation

## 🎯 Zweck

Dieser Agent aktualisiert die `PROJEKT_DOKUMENTATION.md` mit allen Änderungen, die seit dem letzten Update gemacht wurden.

---

## 🚀 Aufruf

```
/update_agent
```

Oder:

```
Führe update_agent aus
```

---

## 📋 Was dieser Agent tut

### 1. **Analyse der Änderungen**
- Durchsucht alle relevanten Dateien nach Änderungen
- Identifiziert neue Features, Bugfixes, Refactorings
- Erkennt neue API-Endpoints
- Findet neue Dependencies

### 2. **Kategorisierung**
- ✅ **Neue Features:** Funktionen die hinzugefügt wurden
- 🐛 **Bugfixes:** Behobene Fehler
- 🔧 **Refactoring:** Code-Verbesserungen ohne Feature-Änderung
- 📚 **Dokumentation:** Docs-Updates
- ⚠️ **Breaking Changes:** Änderungen die Kompatibilität brechen

### 3. **Dokumentation aktualisieren**
- Updates in `PROJEKT_DOKUMENTATION.md` einfügen
- Changelog erweitern
- TODO-Liste aktualisieren
- Neue Sections hinzufügen falls nötig

---

## 🔍 Check-Liste für den Agent

### Backend-Änderungen (Python)
- [ ] Neue API-Endpoints in `main.py`
- [ ] Neue Funktionen in `game_service.py`
- [ ] Neue Models in `models.py`
- [ ] Neue Dependencies in `requirements.txt`
- [ ] Geänderte Datenstrukturen

### Frontend-Änderungen (HTML/JS)
- [ ] Neue HTML-Seiten in `static/`
- [ ] Neue JavaScript-Funktionen
- [ ] Geänderte UI-Elemente
- [ ] Neue CSS-Styles

### Daten-Änderungen
- [ ] Neue Editionen in `data/editions.json`
- [ ] Geänderte Character-Definitionen
- [ ] Setup-Änderungen

### Konfiguration
- [ ] Neue MCP-Server in `mcp.json`
- [ ] Neue Environment-Variables
- [ ] Geänderte Ports/Konfiguration

---

## 📝 Workflow

### Schritt 1: Code-Analyse
```bash
1. read_file("main.py", 0, 200)
2. read_file("game_service.py", 0, 300)
3. read_file("models.py", 0, 100)
4. list_dir("static/")
5. read_file("requirements.txt", 0, 50)
```

### Schritt 2: Vergleich mit Dokumentation
```bash
1. read_file(".github/PROJEKT_DOKUMENTATION.md", 0, 100)
2. Identifiziere: Was steht in Docs, was nicht im Code?
3. Identifiziere: Was steht im Code, was nicht in Docs?
```

### Schritt 3: Changelog erstellen
```markdown
### Version X.X.X - YYYY-MM-DD

#### ✅ Neue Features
- Feature 1: Beschreibung
- Feature 2: Beschreibung

#### 🐛 Bugfixes
- Fix 1: Beschreibung des behobenen Fehlers
- Fix 2: Beschreibung

#### 🔧 Verbesserungen
- Refactoring 1: Was wurde verbessert
- Performance: Was wurde optimiert

#### 📚 Dokumentation
- Docs 1: Was wurde dokumentiert
```

### Schritt 4: Dokumentation updaten
```bash
1. replace_string_in_file(".github/PROJEKT_DOKUMENTATION.md")
   → Füge neuen Changelog-Eintrag hinzu

2. replace_string_in_file(".github/PROJEKT_DOKUMENTATION.md")
   → Aktualisiere API-Endpoint-Liste

3. replace_string_in_file(".github/PROJEKT_DOKUMENTATION.md")
   → Aktualisiere TODO-Liste

4. replace_string_in_file(".github/PROJEKT_DOKUMENTATION.md")
   → Aktualisiere Version und Datum
```

---

## 🎯 Template für Updates

### API-Endpoint hinzufügen
```markdown
| `/api/new/endpoint` | POST | Beschreibung | `{request}` → `{response}` |
```

### Feature dokumentieren
```markdown
### Neue Funktion: [Name]
**Zweck:** [Beschreibung]

**Verwendung:**
\`\`\`python
# Code-Beispiel
\`\`\`

**Tests:**
- [ ] Test 1
- [ ] Test 2
```

### Bugfix dokumentieren
```markdown
#### 🐛 BEHOBEN: [Kurzbeschreibung]
**Problem:** [Was war kaputt]  
**Ursache:** [Warum war es kaputt]  
**Lösung:** [Wie wurde es gefixt]  
**Commit:** [Optional: Commit-Hash]
```

### TODO aktualisieren
```markdown
# Von:
- [ ] Feature X implementieren

# Zu:
- [x] Feature X implementieren ✅ (v1.2.0)
```

---

## 🔧 Erweiterte Analyse-Tools

### 1. API-Endpoint-Erkennung
```python
# Suche nach @app.post, @app.get, etc.
grep_search("@app\\.(get|post|put|delete)", includePattern="**/*.py", isRegexp=True)
```

### 2. TODO-Tracking
```python
# Finde alle TODOs im Code
grep_search("TODO:", includePattern="**/*.py")
grep_search("TODO:", includePattern="**/*.js")
```

### 3. Neue Dependencies
```python
# Vergleiche requirements.txt mit dokumentierter Version
read_file("requirements.txt", 0, 100)
# → Prüfe ob neue Packages hinzugefügt wurden
```

### 4. Git-History (falls verfügbar)
```bash
# Optional: Nutze Git-Commits für Changelog
run_in_terminal("git log --oneline --since='2 weeks ago'")
```

---

## 📊 Output-Format

Nach der Analyse präsentiert der Agent:

```markdown
# 🔍 Analyse-Ergebnis

## Gefundene Änderungen

### ✅ Neue Features (3)
1. **Spieler-Kick-Funktion**
   - Endpoint: POST /api/game/{game_id}/kick
   - Service: kick_player() in game_service.py
   - Frontend: Kick-Button in storyteller.html

2. **Edition: Sects & Violets**
   - Datei: data/editions.json erweitert
   - Neue Charaktere: 20 hinzugefügt

3. **Dark Mode Toggle**
   - Frontend: style-toggle.js neu
   - CSS: dark-theme.css neu

### 🐛 Bugfixes (2)
1. **Polling stoppt nach Spielstart**
   - Datei: player.html
   - Zeilen: 180-185

2. **Edition-Select war leer**
   - Datei: index.html
   - Zeilen: 95-100

### 🔧 Refactoring (1)
1. **Error Handling vereinheitlicht**
   - Alle fetch() Calls haben jetzt try-catch

### ❌ Offene TODOs (2)
1. Storyteller-UI nach Start ausblenden
2. Player-Refresh-Button entfernen

---

## 📝 Changelog-Entwurf

\`\`\`markdown
### v1.2.0 - 2025-01-19

#### ✅ Neue Features
- Spieler-Kick-Funktion für Erzähler
- Edition "Sects & Violets" hinzugefügt
- Dark Mode Toggle im Frontend

#### 🐛 Bugfixes
- Polling stoppt korrekt nach Spielstart
- Edition-Select wird beim Laden befüllt

#### 🔧 Verbesserungen
- Error Handling vereinheitlicht über alle API-Calls
- Code-Kommentare für komplexe Logik hinzugefügt
\`\`\`

---

## 📥 Soll ich die Dokumentation jetzt updaten?
- [ ] Ja, aktualisiere PROJEKT_DOKUMENTATION.md
- [ ] Nein, zeige mir erst die Änderungen
```

---

## 🤖 Agent-Instruktionen

### Wenn du als Agent diesen Command ausführst:

1. **Sei gründlich:** Prüfe ALLE relevanten Dateien
2. **Sei präzise:** Nutze grep_search für Pattern-Matching
3. **Sei strukturiert:** Folge dem Workflow Schritt für Schritt
4. **Sei transparent:** Zeige was du findest bevor du updatest
5. **Sei vorsichtig:** Backup wichtiger Sections vor Änderung

### Tools die du nutzen sollst:
- ✅ `read_file` - Für Code-Analyse
- ✅ `grep_search` - Für Pattern-Suche
- ✅ `list_dir` - Für neue Dateien
- ✅ `replace_string_in_file` - Für Updates
- ✅ `get_errors` - Nach Änderungen validieren

### Was du NICHT tun sollst:
- ❌ Keine Vermutungen über Code den du nicht gesehen hast
- ❌ Keine Breaking Changes ohne Rückfrage
- ❌ Keine Löschung von Sections ohne Bestätigung
- ❌ Kein Update ohne Changelog-Entwurf zu zeigen

---

## 📋 Beispiel-Ausführung

**User:**
```
/update_agent
```

**Agent:**
```
🔍 Starte Dokumentations-Analyse...

Schritt 1: Analysiere Backend...
- Lese main.py... ✅
- Lese game_service.py... ✅
- Lese models.py... ✅

Schritt 2: Analysiere Frontend...
- Liste static/ Dateien... ✅
- Lese index.html... ✅
- Lese storyteller.html... ✅

Schritt 3: Vergleiche mit Docs...
- Lese PROJEKT_DOKUMENTATION.md... ✅
- Identifiziere Unterschiede... ✅

📊 Analyse-Ergebnis:
[... zeigt Änderungen ...]

📝 Changelog-Entwurf:
[... zeigt vorgeschlagenen Changelog ...]

Soll ich die Dokumentation jetzt aktualisieren? (ja/nein)
```

**User:**
```
ja
```

**Agent:**
```
✅ Aktualisiere PROJEKT_DOKUMENTATION.md...
- Changelog hinzugefügt ✅
- API-Endpoints aktualisiert ✅
- TODO-Liste aktualisiert ✅
- Version auf 1.2.0 erhöht ✅

Dokumentation erfolgreich aktualisiert! 🎉
```

---

## 🎓 Lern-Modus

Wenn User mehr Details will:

```
/update_agent --verbose
```

Zeigt zusätzlich:
- Welche Dateien wurden gescannt
- Welche Patterns wurden gesucht
- Welche Zeilen wurden geändert
- Diff-Preview vor dem Update

---

## 🚀 Quick Commands

```bash
# Standard-Update
/update_agent

# Nur Analyse, kein Update
/update_agent --dry-run

# Mit detaillierter Ausgabe
/update_agent --verbose

# Nur Backend analysieren
/update_agent --backend-only

# Nur Frontend analysieren
/update_agent --frontend-only

# Nur Changelog erstellen
/update_agent --changelog-only
```

---

## ⚠️ Wichtige Hinweise

### Vor jedem Update:
1. Stelle sicher dass der Code funktioniert
2. Alle Tests sind grün
3. Keine offenen Merge-Konflikte
4. Version-Nummer ist eindeutig

### Nach jedem Update:
1. Prüfe ob Dokumentation konsistent ist
2. Validiere alle Links
3. Teste ob Code-Beispiele noch funktionieren
4. Commit mit aussagekräftiger Message

---

**Erstellt:** 2025-01-19  
**Version:** 1.0.0  
**Kompatibel mit:** PROJEKT_DOKUMENTATION.md v1.0.0+

