# 🎯 Player Flags Feature - Implementierungs-Dokumentation

## ✅ Fertiggestellt: Player Flags System für Storyteller

### 📋 Übersicht

Das Player Flags System ermöglicht es dem Storyteller, spielmechanische Status-Flags auf Spieler zu setzen, wie z.B.:
- 🧪 **Vergiftet** (Poisoner-Fähigkeit)
- 👹 **Dämon** (Dämon-Markierung)
- 🎯 **Red Herring** (Fortune Teller)
- 💀 **Tot**
- ✅ **Fähigkeit genutzt**
- 🛡️ **Geschützt** (Monk)

---

## 🏗️ Implementierung

### 1. **Backend - Models** (`models.py`)

#### Neue Enums und Models:
```python
class FlagType(str, Enum):
    """Spielmechanische Flags für Spieler-Status"""
    POISONED = "poisoned"
    DEMON = "demon"
    RED_HERRING = "red_herring"
    DEAD = "dead"
    USED_ABILITY = "used_ability"
    PROTECTED = "protected"
```

#### Erweiterte Player Model:
```python
class Player(BaseModel):
    # ...existing fields...
    flags: Dict[str, bool] = {}  # Aktive Flags
    flag_metadata: Dict[str, Any] = {}  # Zusätzliche Flag-Infos
```

#### Request Models:
- `SetPlayerFlagRequest`: Zum Setzen von Flags mit optionalen Metadaten
- `RemovePlayerFlagRequest`: Zum Entfernen einzelner Flags

---

### 2. **Backend - Service** (`game_service.py`)

#### Neue Methoden:

**`set_player_flag(game_id, player_id, flag_type, storyteller_id, metadata)`**
- Setzt ein Flag für einen Spieler
- Validiert Storyteller-Berechtigung
- Speichert optionale Metadaten (z.B. Zeitstempel, Nacht-Nummer)

**`remove_player_flag(game_id, player_id, flag_type, storyteller_id)`**
- Entfernt ein spezifisches Flag von einem Spieler
- Validiert Storyteller-Berechtigung

**`get_player_flags(game_id, player_id)`**
- Gibt alle aktiven Flags eines Spielers zurück

**`clear_temporary_flags(game_id, storyteller_id)`**
- Löscht alle temporären Flags (poisoned, protected, used_ability)
- Wird normalerweise am Ende einer Nacht verwendet

**Erweitert: `get_storyteller_overview()`**
- Gibt jetzt auch `flags` und `flag_metadata` für jeden Spieler zurück

---

### 3. **Backend - API Endpoints** (`main.py`)

#### Neue Endpoints:

**POST** `/api/game/{game_id}/player/{player_id}/flag/set?storyteller_id={id}`
```json
Body: {
    "flag_type": "poisoned",
    "metadata": {"night": 1, "set_at": "..."}
}

Response: {
    "success": true,
    "player_id": "...",
    "player_name": "...",
    "flags": {"poisoned": true},
    "flag_metadata": {...}
}
```

**DELETE** `/api/game/{game_id}/player/{player_id}/flag/{flag_type}?storyteller_id={id}`
```json
Response: {
    "success": true,
    "player_id": "...",
    "flags": {...}
}
```

**POST** `/api/game/{game_id}/flags/clear-temporary?storyteller_id={id}`
```json
Response: {
    "success": true,
    "message": "Temporäre Flags wurden entfernt"
}
```

---

### 4. **Frontend - UI** (`storyteller.html`)

#### Neue Features:

**Flag-Badges auf Player Items:**
- Farbcodierte Badges für aktive Flags
- Icons für visuelle Unterscheidung
- Tooltips mit Beschreibungen

**Flag-Controls für jeden Spieler:**
- Dropdown zur Auswahl des Flag-Typs
- "Setzen"-Button zum Hinzufügen eines Flags
- "Flags löschen"-Button zum Entfernen aller Flags eines Spielers

**Bulk-Operation:**
- Button "Alle temporären Flags löschen" in der Night Order Card
- Entfernt poisoned, protected, used_ability von allen Spielern

#### CSS-Styles:
```css
.flag-badge {
    /* Styled badges mit Gradient-Backgrounds */
}

.flag-controls {
    /* Flex-Layout für Controls */
}
```

#### JavaScript-Funktionen:
- `getFlagInfo(flagType)`: Gibt Icon, Label, Farbe und Beschreibung zurück
- `setPlayerFlag(playerId)`: Setzt Flag via API
- `clearPlayerFlags(playerId)`: Löscht alle Flags eines Spielers
- `clearAllTemporaryFlags()`: Bulk-Delete temporärer Flags

---

## 🧪 Tests

### Test-Skript: `test_flags.py`

Testet vollständigen Workflow:
1. ✅ Spiel erstellen
2. ✅ Spieler hinzufügen
3. ✅ Spiel starten
4. ✅ Flag setzen (poisoned)
5. ✅ Weiteres Flag setzen (demon)
6. ✅ Flags in Overview anzeigen
7. ✅ Einzelnes Flag entfernen
8. ✅ Temporäre Flags bei mehreren Spielern setzen
9. ✅ Alle temporären Flags löschen
10. ✅ Finale Übersicht

**Ergebnis:** ✅ Alle Tests erfolgreich!

---

## 🎮 Verwendung im Spiel

### Beispiel-Workflow: Poisoner vergiftet einen Spieler

1. **Nachts:** Poisoner wählt ein Opfer
2. **Storyteller:** Öffnet Storyteller-Ansicht
3. **Aktion:** Wählt im Dropdown "🧪 Vergiftet"
4. **Aktion:** Klickt "Setzen" beim entsprechenden Spieler
5. **Ergebnis:** Badge "🧪 Vergiftet" erscheint unter dem Spielernamen
6. **Am Morgen:** Storyteller klickt "Alle temporären Flags löschen"
7. **Ergebnis:** Badge verschwindet automatisch

### Beispiel-Workflow: Red Herring markieren

1. **Spielstart:** Fortune Teller im Spiel
2. **Storyteller:** Wählt zufälligen Spieler als Red Herring
3. **Aktion:** Setzt Flag "🎯 Red Herring"
4. **Ergebnis:** Badge bleibt während des gesamten Spiels
5. **Verwendung:** Storyteller weiß, wer der Red Herring ist

---

## 📊 Flag-Typen und Verwendung

| Flag | Icon | Farbe | Temporär? | Verwendung |
|------|------|-------|-----------|------------|
| Vergiftet | 🧪 | Violett | ✅ Ja | Poisoner-Fähigkeit (jede Nacht) |
| Dämon | 👹 | Rot | ❌ Nein | Aktuelle Dämon-Markierung |
| Red Herring | 🎯 | Orange | ❌ Nein | Fortune Teller (Spielstart) |
| Tot | 💀 | Grau | ❌ Nein | Toter Spieler |
| Fähigkeit genutzt | ✅ | Grün | ✅ Ja | Einmalige Fähigkeiten |
| Geschützt | 🛡️ | Blau | ✅ Ja | Monk-Schutz (jede Nacht) |

---

## 🔮 Erweiterbarkeit

### Neue Flags hinzufügen:

**1. Backend:**
```python
# models.py
class FlagType(str, Enum):
    # ...existing flags...
    NEW_FLAG = "new_flag"  # 🆕 Neue Fähigkeit
```

**2. Frontend:**
```javascript
// storyteller.html - In getFlagInfo()
'new_flag': { 
    icon: '🆕', 
    label: 'Neue Fähigkeit', 
    color: 'linear-gradient(...)', 
    description: '...' 
}
```

```html
<!-- In Flag-Dropdown -->
<option value="new_flag">🆕 Neue Fähigkeit</option>
```

**3. Service (optional):**
```python
# game_service.py - Für temporäre Flags:
TEMPORARY_FLAGS = {"poisoned", "protected", "used_ability", "new_flag"}
```

---

## ✅ Vorteile des Systems

1. **Flexibel:** Beliebige Flags können einfach hinzugefügt werden
2. **Typsicher:** Pydantic-Validierung + Enum für Flag-Typen
3. **Metadaten:** Zusätzliche Infos können zu jedem Flag gespeichert werden
4. **Berechtigungen:** Nur Storyteller kann Flags verwalten
5. **Automatisierung:** Bulk-Operationen für temporäre Flags
6. **Visuell:** Farbcodierte Badges mit Icons

---

## 🚀 Nächste Schritte (Optional)

### Mögliche Erweiterungen:

1. **Flag-Historie:**
   ```python
   flag_history: List[Dict] = []  # Wer, wann, welches Flag
   ```

2. **Auto-Clear bei Phasenwechsel:**
   ```python
   def advance_phase(game_id, storyteller_id):
       # Automatisch temporäre Flags löschen
       clear_temporary_flags(game_id, storyteller_id)
   ```

3. **Flag-Kombinationen validieren:**
   ```python
   # Nur ein Dämon erlaubt
   if flag_type == "demon":
       # Entferne "demon" von allen anderen Spielern
   ```

4. **Benachrichtigungen:**
   ```javascript
   // Toast-Notification bei Flag-Änderung
   showToast('🧪 Spieler wurde vergiftet', 'success')
   ```

---

## 📝 Changelog

### v1.0.0 - 2025-12-20

**✨ Features:**
- ✅ Player Flags System implementiert
- ✅ 6 vordefinierte Flag-Typen
- ✅ API-Endpoints für Set/Remove/Clear
- ✅ Storyteller UI mit Badges und Controls
- ✅ Temporäre Flags Bulk-Delete
- ✅ Vollständige Tests

**🏗️ Architektur:**
- ✅ Type-safe mit Pydantic Models
- ✅ Berechtigungsprüfung (nur Storyteller)
- ✅ Metadata-Unterstützung
- ✅ Erweiterbar für neue Flags

---

## 🎓 Lessons Learned

1. **DRY-Prinzip:** Flag-Infos (Icon, Farbe, etc.) zentral in `getFlagInfo()`
2. **Type Safety:** Enum für Flag-Typen verhindert Tippfehler
3. **Testbarkeit:** Klare Trennung Backend/Frontend ermöglicht automatisierte Tests
4. **UX:** Farbcodierung + Icons machen Flags sofort erkennbar
5. **Bulk-Operations:** Temporäre Flags gemeinsam löschen spart Zeit

---

## 📚 Dokumentation

- **Copilot Instructions:** `.github/copilot-instructions.md`
- **API-Docs:** FastAPI Auto-Docs unter `/docs`
- **Test-Skript:** `test_flags.py`
- **Dieses Dokument:** `FLAG_FEATURE_DOCUMENTATION.md`

---

**Erstellt:** 2025-12-20  
**Version:** 1.0.0  
**Status:** ✅ Vollständig implementiert und getestet

