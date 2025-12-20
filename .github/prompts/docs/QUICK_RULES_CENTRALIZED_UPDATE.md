# ✅ Zentrale Quick Rules - Update Dokumentation

**Datum:** 2025-01-19  
**Update:** Quick Rules werden jetzt aus zentraler JSON-Datei geladen  
**Status:** ✅ Implementiert

---

## 📋 Was wurde geändert?

### Problem
Die Quick Rules waren statisch in beiden HTML-Dateien (`player.html` und `storyteller.html`) hardcodiert. Änderungen mussten an zwei Stellen vorgenommen werden.

### Lösung
Die Regeln werden jetzt aus einer zentralen JSON-Datei geladen:

```
data/quick_rules.json → API: /api/quick-rules → Frontend lädt dynamisch
```

---

## 📁 Neue/Geänderte Dateien

### 1. **`data/quick_rules.json`** (NEU)
**Zweck:** Zentrale Datei für alle Quick Rules

**Struktur:**
```json
{
  "title": "🎭 Blood on the Clocktower - Schnellregeln",
  "sections": [
    {
      "emoji": "1️⃣",
      "title": "Siegbedingungen",
      "rules": [
        "<strong>Gut gewinnt</strong>, wenn der Demon stirbt",
        "..."
      ]
    }
  ]
}
```

**Vorteile:**
- ✅ Regeln nur an **einer Stelle** ändern
- ✅ HTML-Formatierung in JSON möglich (`<strong>`, `<em>`, etc.)
- ✅ Einfach erweiterbar (neue Sections hinzufügen)
- ✅ Übersetzungen möglich (z.B. `quick_rules_en.json`)

---

### 2. **`main.py`** (API-Endpoint hinzugefügt)

**Neuer Endpoint:** `GET /api/quick-rules`

```python
@app.get("/api/quick-rules")
async def get_quick_rules():
    """Gibt die Schnellregeln aus der zentralen JSON-Datei zurück"""
    try:
        with open('data/quick_rules.json', 'r', encoding='utf-8') as f:
            import json
            rules = json.load(f)
        return rules
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Quick Rules Datei nicht gefunden")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden der Regeln: {str(e)}")
```

**Fehlerbehandlung:**
- 404: Wenn Datei nicht existiert
- 500: Wenn JSON-Format ungültig

---

### 3. **`static/player.html`** (Dynamisches Laden)

**Änderungen:**
1. **Modal-Content vereinfacht:**
   ```html
   <h2 id="rulesModalTitle">Lädt...</h2>
   <div id="rulesContent">
       <div class="spinner"></div>
   </div>
   ```

2. **JavaScript-Funktion hinzugefügt:**
   ```javascript
   async function loadQuickRules() {
       if (rulesLoaded) return; // Nur einmal laden
       
       const response = await fetch('/api/quick-rules');
       const data = await response.json();
       
       // Titel setzen
       document.getElementById('rulesModalTitle').textContent = data.title;
       
       // Sections dynamisch erstellen
       data.sections.forEach(section => {
           // ... DOM-Elemente erstellen
       });
   }
   ```

**Ablauf:**
1. User klickt auf "📜 Regeln" Button
2. Modal öffnet (Spinner wird angezeigt)
3. API-Call zu `/api/quick-rules`
4. JSON wird geladen
5. DOM-Elemente werden dynamisch erstellt
6. Spinner verschwindet, Regeln werden angezeigt

**Performance:**
- ✅ Regeln werden **nur beim ersten Öffnen** geladen (Cache mit `rulesLoaded` Flag)
- ✅ Kein erneuter API-Call bei erneutem Öffnen

---

### 4. **`static/storyteller.html`** (Identisch)

Gleiche Änderungen wie in `player.html`:
- Modal-Content vereinfacht
- JavaScript-Funktion `loadQuickRules()` hinzugefügt
- Dynamisches Laden beim ersten Öffnen

---

## 🎯 Wie man Regeln jetzt ändert

### Vorher (kompliziert)
1. Öffne `player.html`
2. Ändere Regeln im Modal-HTML
3. Öffne `storyteller.html`
4. Ändere die **gleichen** Regeln nochmal
5. Beide Dateien speichern

### Jetzt (einfach)
1. Öffne `data/quick_rules.json`
2. Ändere Regeln an **einer Stelle**
3. Speichern → Fertig! ✅

**Beispiel:** Regel hinzufügen
```json
{
  "emoji": "5️⃣",
  "title": "Traveller-Regeln",
  "rules": [
    "<strong>Reisende:</strong> Können jederzeit dem Spiel beitreten",
    "<strong>Exile:</strong> Mit 50%+ Stimmen kann ein Traveller verbannt werden"
  ]
}
```

---

## 🧪 Testing

### Test 1: Quick Rules laden
```bash
# Server starten
uvicorn main:app --reload --host 0.0.0.0

# Browser öffnen
http://localhost:8000/player.html?game=test&player=test123

# Test:
1. Click auf "📜 Regeln" Button
2. Erwartung: Spinner kurz sichtbar, dann Regeln
3. Alle 4 Sections werden angezeigt
4. Schließen und erneut öffnen → kein Spinner (gecacht)
```

### Test 2: API-Endpoint direkt
```bash
# API direkt testen
curl http://localhost:8000/api/quick-rules

# Erwartung: JSON mit title + sections
```

### Test 3: Regeln ändern
```bash
# 1. Bearbeite data/quick_rules.json
# 2. Speichern
# 3. Browser-Reload (Ctrl+F5 um Cache zu leeren)
# 4. Modal öffnen
# Erwartung: Neue Regeln werden angezeigt
```

### Test 4: Fehlerbehandlung
```bash
# Umbenennen: data/quick_rules.json → data/quick_rules_backup.json
# Browser: Modal öffnen
# Erwartung: "Regeln konnten nicht geladen werden." (roter Text)
```

---

## 🚀 Zusätzliche Features (Bonus)

### 1. Server-IP im Join-Link
**Problem:** `localhost` funktioniert nicht auf mobilen Geräten

**Lösung:** 
- Neuer API-Endpoint: `GET /api/server/ip`
- Ermittelt lokale IP-Adresse (z.B. `192.168.1.100`)
- Storyteller-View verwendet diese IP für Join-Link

**Code in `storyteller.html`:**
```javascript
async function loadServerIP() {
    const response = await fetch('/api/server/ip');
    const data = await response.json();
    serverBaseUrl = data.base_url; // z.B. "http://192.168.1.100:8000"
}

// Join URL wird dann:
const joinUrl = `${serverBaseUrl}/join.html?game=${gameData.game_id}`;
```

**Vorteil:**
✅ Mobile Geräte im gleichen WLAN können beitreten  
✅ Kein manuelles Ersetzen von "localhost" mehr nötig

---

## 📊 Vorher/Nachher Vergleich

| Aspekt | Vorher | Nachher |
|--------|--------|---------|
| **Regeln ändern** | 2 Dateien editieren | 1 Datei editieren |
| **HTML-Größe** | ~50 Zeilen Regeln | ~10 Zeilen Container |
| **Laden** | Sofort (inline) | Dynamisch (beim Öffnen) |
| **Wartbarkeit** | Niedrig (Duplikation) | Hoch (DRY) |
| **Erweiterbarkeit** | Aufwändig | Einfach (JSON) |
| **Mehrsprachigkeit** | Unmöglich | Möglich (z.B. `_en.json`) |

---

## 💡 Future Enhancements (Optional)

### 1. Mehrsprachige Regeln
```javascript
// Browser-Sprache erkennen
const lang = navigator.language.startsWith('en') ? 'en' : 'de';
const response = await fetch(`/api/quick-rules?lang=${lang}`);
```

### 2. Markdown-Support
Statt HTML in JSON könnte man Markdown verwenden:
```json
{
  "rules": [
    "**Gut gewinnt**, wenn der Demon stirbt"
  ]
}
```
+ Markdown-Parser im Frontend

### 3. Regelversionen
```json
{
  "version": "1.1",
  "last_updated": "2025-01-19",
  "sections": [...]
}
```

---

## ✅ Definition of Done

- [x] `data/quick_rules.json` erstellt
- [x] API-Endpoint `/api/quick-rules` implementiert
- [x] `player.html` lädt Regeln dynamisch
- [x] `storyteller.html` lädt Regeln dynamisch
- [x] Fehlerbehandlung (404, 500)
- [x] Caching (nur einmal laden)
- [x] Server-IP für Join-Link implementiert
- [x] Keine Fehler in `get_errors`
- [ ] Manuell getestet (siehe Test-Anleitung oben)

---

## 🎯 Zusammenfassung

**Was erreicht wurde:**
1. ✅ **DRY-Prinzip:** Regeln nur an einer Stelle (JSON)
2. ✅ **API-Endpoint:** `/api/quick-rules` für zentrale Verwaltung
3. ✅ **Dynamisches Laden:** Regeln werden beim Öffnen des Modals geladen
4. ✅ **Performance:** Caching verhindert mehrfaches Laden
5. ✅ **Wartbarkeit:** Regeln ändern = nur 1 Datei editieren
6. ✅ **Bonus:** Server-IP für mobilen Zugriff

**Nächste Schritte:**
1. Server neu starten (bereits im Hintergrund)
2. Manuell testen (siehe Test-Anleitung)
3. Optional: Regeln in `quick_rules.json` anpassen

---

**Erstellt:** 2025-01-19  
**Version:** 1.2.0 (Zentrale Quick Rules + Server-IP)  
**Status:** ✅ Ready for Testing

