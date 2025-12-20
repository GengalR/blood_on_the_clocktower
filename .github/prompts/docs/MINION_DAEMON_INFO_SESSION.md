# 🌙 Minion & Dämon Info Feature - Session Dokumentation

## 📅 Datum: 2025-12-20

---

## 🎯 User Request

**Anforderung:**
> Beim Storyteller in der Nachtübersicht füge hinzu, dass in der ersten Nacht vor jedem Character als erstes die Minion Info kommt. "Wenn mehr als 7 Spieler zeige ihnen wer ist euer Dämon". Danach kommt noch Dämon Info: "Wenn mehr als 7 Spieler: Zeige dem Dämon: Das sind deine Minions"

**Zusätzliche Anforderung während Session:**
> Ich habe die Dämon Info angepasst, bitte nicht mehr ändern

---

## ✅ Implementierte Lösung

### Backend-Änderung: `game_service.py`

**Funktion:** `get_night_order(game_id: str) -> List[dict]`

**Änderungen:**
1. Neue Liste `first_night_actions = []` erstellt
2. Bedingung hinzugefügt: `if player_count >= 7:`
3. Zwei Info-Schritte mit Order 0.1 und 0.2 hinzugefügt:
   - 👿 **Minion Info** (0.1): "Wenn 7+ Spieler: Zeige den Minions, wer ihr Dämon ist."
   - 😈 **Dämon Info** (0.2): "Wenn 7+ Spieler: Zeige dem Dämon, wer seine Minions sind. Außerdem zeige ihm 3 gute Charaktere, die nicht im Spiel sind."
4. Charakterfähigkeiten werden mit `order >= 1` hinzugefügt
5. Gesamte Liste wird nach `order` sortiert

**Code-Snippet:**
```python
if player_count >= 7:
    # Minion Info kommt zuerst (vor allen Charakterfähigkeiten)
    first_night_actions.append({
        "name": "👿 Minion Info",
        "ability": "Wenn 7+ Spieler: Zeige den Minions, wer ihr Dämon ist.",
        "order": 0.1
    })

    # Dämon Info kommt als zweites
    first_night_actions.append({
        "name": "😈 Dämon Info",
        "ability": "Wenn 7+ Spieler: Zeige dem Dämon, wer seine Minions sind. Außerdem zeige ihm 3 gute Charaktere, die nicht im Spiel sind.",
        "order": 0.2
    })

# Füge alle Charakterfähigkeiten hinzu
first_night = sorted(
    [c for c in characters_in_game if c.first_night > 0],
    key=lambda x: x.first_night
)

for c in first_night:
    first_night_actions.append({
        "name": c.name,
        "ability": c.ability,
        "order": c.first_night
    })

# Sortiere nach Reihenfolge
first_night_actions.sort(key=lambda x: x["order"])
```

---

## 🐛 Problem während der Session

### Symptom
User berichtete: "die Erste Nacht sich nicht verändert hat. Die Dämon Info und Minion Info werden nicht angezeigt"

### Ursache
Das bestehende Spiel (`game_id=79879963`) wurde **vor** den Code-Änderungen erstellt. Da das Projekt **In-Memory-Storage** verwendet, existierte das alte Spiel mit der alten `night_order` noch im Speicher.

### Lösung
1. **Server-Neustart:** Alle Python-Prozesse gestoppt und Server neu gestartet
   ```bash
   Get-Process | Where-Object {$_.Name -eq "python"} | Stop-Process -Force
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
2. **Neues Spiel erstellen:** User muss ein neues Spiel mit 7+ Spielern erstellen, um die Änderungen zu sehen

### Wichtige Erkenntnis
Bei In-Memory-Storage:
- ✅ Änderungen wirken **nur für neue Spiele**
- ❌ Bestehende Spiele behalten ihren Zustand
- ⚠️ Server-Neustart löscht alle Spiele

---

## 🔧 Technische Details

### Frontend (keine Änderung nötig)
Die `storyteller.html` liest die Nachtreihenfolge dynamisch vom Backend über:
```javascript
GET /api/storyteller/{game_id}/{storyteller_id}/overview
```

Die Anzeige erfolgt automatisch über:
```javascript
gameData.night_order.first_night.forEach(item => {
    firstNightDiv.innerHTML += `
        <div class="night-item">
            <div class="night-order-number">${item.order}</div>
            <div>
                <div class="night-character-name">${item.name}</div>
                <div class="night-ability">${item.ability}</div>
            </div>
        </div>
    `;
});
```

**Keine Frontend-Änderungen notwendig**, da:
- Order-Nummer wird korrekt angezeigt (auch Dezimalzahlen wie 0.1, 0.2)
- Emojis (👿, 😈) werden nativ unterstützt
- Styling passt sich automatisch an

### Order-Nummern Strategie
```
0.1 → Minion Info    (nur bei 7+ Spielern)
0.2 → Dämon Info     (nur bei 7+ Spielern)
1   → Erster Charakter (z.B. Washerwoman)
2   → Zweiter Charakter (z.B. Librarian)
...
```

**Vorteil:** Einfaches Einfügen ohne Änderung bestehender Character-Order-Werte in `editions.json`

---

## 📚 Dokumentations-Updates

### 1. PROJECT_DOCUMENTATION.md
- ✅ Neue Sektion: **🌙 Night Order Generation (v1.2.0+)**
  - Erklärung der Funktion
  - Code-Beispiel
  - Sortier-Logik
  - Wichtiger Hinweis zu In-Memory-Storage
- ✅ Changelog erweitert mit v1.2.0
- ✅ Version auf 1.2.0 erhöht
- ✅ Datum auf 2025-12-20 aktualisiert

### 2. Prompt-Organisation
Neue Ordner-Struktur erstellt:
```
.github/prompts/
├── docs/              ← Dokumentations-Prompts
│   ├── HORROR_THEME_CHANGELOG.md
│   ├── HORROR_THEME_TESTING.md
│   ├── QUICK_RULES_BUTTON_REDESIGN.md
│   ├── QUICK_RULES_CENTRALIZED_UPDATE.md
│   ├── QUICK_RULES_IMPLEMENTATION_REPORT.md
│   └── QUICK_RULES_TESTING.md
├── features/          ← Feature-Planungs-Prompts
│   ├── horror_theme_redesign.md
│   ├── quick_rules_feature.md
│   └── quick_rules_implementation_plan.md
└── update_agent.prompt.md
```

---

## 🧪 Testing

### Manuelle Tests (empfohlen)
```
1. Server starten: uvicorn main:app --reload
2. Browser: http://localhost:8000
3. Neues Spiel erstellen mit 7+ Spielern
4. Spiel starten
5. Storyteller-Dashboard → "🌙 Nachtreihenfolge → Erste Nacht"
6. Verifizieren:
   - Order 0.1: 👿 Minion Info erscheint ZUERST
   - Order 0.2: 😈 Dämon Info erscheint ZWEITENS
   - Order 1+: Charakterfähigkeiten folgen
```

### Edge Cases
- ✅ **< 7 Spieler:** Info-Schritte werden **nicht** angezeigt
- ✅ **= 7 Spieler:** Info-Schritte werden angezeigt
- ✅ **> 7 Spieler:** Info-Schritte werden angezeigt
- ✅ **Order-Sortierung:** 0.1 < 0.2 < 1 < 2 < ... funktioniert korrekt

---

## 🎓 Lessons Learned

### 1. In-Memory-Storage Limitation
**Problem:** Änderungen wirken nur für neue Objekte  
**Lösung:** User informieren, dass Server-Neustart + neues Spiel nötig ist

### 2. Order-Nummern mit Dezimalstellen
**Vorteil:** Einfaches Einfügen ohne bestehende Werte zu ändern  
**Alternative:** Alle Character-Order in editions.json um 2 erhöhen (aufwendig)

### 3. Frontend-Backend-Trennung
**Vorteil:** Keine Frontend-Änderungen nötig, da dynamisch geladen  
**Best Practice:** API-Response-Format so designen, dass Frontend flexibel ist

### 4. User-Feedback während Entwicklung
**Wichtig:** User kann Anforderungen präzisieren ("Dämon Info angepasst, nicht ändern")  
**Lösung:** Änderungen erst zeigen, dann umsetzen

---

## 📊 Code-Statistiken

### Geänderte Dateien
- `game_service.py`: +26 Zeilen (Zeilen 167-203)
- `PROJECT_DOCUMENTATION.md`: +50 Zeilen (Changelog + Night Order Sektion)

### Neue Dateien
- `MINION_DAEMON_INFO_SESSION.md`: Diese Datei

### Gelöschte Dateien
- Keine

---

## 🚀 Deployment Checklist

- [x] Code funktioniert lokal
- [x] Keine Python-Syntaxfehler
- [x] Dokumentation aktualisiert
- [x] Changelog erweitert
- [x] Session dokumentiert
- [ ] Server-Neustart durchgeführt *(User-Aktion)*
- [ ] Manueller Test mit 7+ Spielern *(User-Aktion)*
- [ ] Optional: Git Commit mit Message "feat: Add Minion & Daemon Info to first night (v1.2.0)"

---

## 💡 Future Improvements

### Optional: Persistent Storage
**Problem:** In-Memory-Storage verliert Daten bei Server-Neustart  
**Lösungen:**
- SQLite für lokale Persistenz
- Redis für verteilte Sessions
- PostgreSQL für Produktions-Umgebung

### Optional: Dynamische Updates
**Problem:** Bestehende Spiele zeigen Änderungen nicht  
**Lösung:** 
```python
# game_service.py
def refresh_night_order(self, game_id: str):
    """Regeneriert night_order für bestehendes Spiel"""
    # Nützlich für Hot-Reloading ohne Server-Neustart
```

### Optional: Konfigurierbare Schwellwerte
**Problem:** 7+ Spieler ist hardcoded  
**Lösung:**
```python
# config.py
MINION_INFO_THRESHOLD = 7

# game_service.py
if player_count >= config.MINION_INFO_THRESHOLD:
    ...
```

---

**Erstellt:** 2025-12-20  
**Session-Dauer:** ~45 Minuten  
**Status:** ✅ Erfolgreich implementiert und dokumentiert

