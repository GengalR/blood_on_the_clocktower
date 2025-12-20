# Baron-Feature Dokumentation

## Übersicht

Das Baron-Feature implementiert die spezielle Fähigkeit des Baron-Charakters aus der "Trouble Brewing" Edition von Blood on the Clocktower.

**Baron-Fähigkeit:** "Es gibt 2 zusätzliche Outsider im Spiel."

## Implementierung

### Automatische Mechanik

Wenn der Baron-Charakter während der Spielinitialisierung zufällig ausgewählt wird, tritt automatisch folgender Prozess ein:

1. **Erkennung:** Das System prüft, ob Baron in der Charakterliste ist
2. **Ersetzung:** 2 zufällig ausgewählte Townsfolk-Charaktere werden entfernt
3. **Hinzufügen:** 2 zufällig ausgewählte Outsider-Charaktere werden hinzugefügt
4. **Tracking:** Das `baron_active` Flag im Game-Objekt wird auf `true` gesetzt

### Technische Details

#### Dateien
- **`models.py`:** `Game.baron_active` Flag hinzugefügt
- **`game_service.py`:** `_apply_baron_ability()` Methode implementiert
- **Integration:** Baron-Logik wird in `start_game()` nach Charakterauswahl, aber vor Zuweisung an Spieler angewendet

#### Code-Flow
```
start_game()
  ↓
_get_role_distribution() - Hole Setup für Spielerzahl
  ↓
_select_random_characters() - Wähle Charaktere nach Setup
  ↓
_apply_baron_ability() - ⭐ BARON-LOGIK HIER
  ↓
random.shuffle() - Mische Charaktere
  ↓
Weise Charaktere den Spielern zu
```

### Validierungen

Die `_apply_baron_ability()` Methode führt folgende Validierungen durch:

1. **Baron-Check:** Ist Baron überhaupt im Spiel?
   - Nein → Keine Änderung, gebe Charaktere unverändert zurück
   
2. **Townsfolk-Check:** Sind mindestens 2 Townsfolk vorhanden?
   - Nein → Warnung ausgeben, keine Änderung
   
3. **Outsider-Check:** Sind mindestens 2 Outsider in der Edition verfügbar?
   - Nein → Warnung ausgeben, keine Änderung
   
4. **Erfolg:** Führe Ersetzung durch und setze `game.baron_active = true`

## Beispiele

### Beispiel 1: 5 Spieler mit Baron

**Setup ohne Baron:**
- 3 Townsfolk
- 0 Outsider
- 1 Minion
- 1 Dämon

**Setup mit Baron:**
- 1 Townsfolk (3 - 2)
- 2 Outsider (0 + 2)
- 1 Minion (Baron)
- 1 Dämon

**Konsolausgabe:**
```
🎭 Baron im Spiel erkannt! Wende Baron-Fähigkeit an...
   ❌ Entferne Townsfolk: Washerwoman
   ❌ Entferne Townsfolk: Chef
   ✅ Füge Outsider hinzu: Drunk
   ✅ Füge Outsider hinzu: Saint
✨ Baron-Fähigkeit erfolgreich angewendet!
```

### Beispiel 2: 10 Spieler mit Baron

**Setup ohne Baron:**
- 7 Townsfolk
- 0 Outsider
- 2 Minions
- 1 Dämon

**Setup mit Baron:**
- 5 Townsfolk (7 - 2)
- 2 Outsider (0 + 2)
- 2 Minions (inkl. Baron)
- 1 Dämon

### Beispiel 3: 6 Spieler OHNE Baron

**Setup bleibt unverändert:**
- 3 Townsfolk
- 1 Outsider (aus normalem Setup)
- 1 Minion (z.B. Poisoner, Spy)
- 1 Dämon

Keine Baron-Logik wird angewendet, da Baron nicht im Spiel ist.

## API-Erweiterungen

### GET `/api/game/{game_id}/storyteller`

Die Storyteller-Overview gibt nun das `baron_active` Feld zurück:

```json
{
  "game_id": "abc123",
  "edition": "TroubleBrewing",
  "started": true,
  "baron_active": true,
  "players": [...],
  "night_order": {...}
}
```

**Verwendung im Frontend:**
```javascript
if (overview.baron_active) {
  showBanner("⚠️ Baron ist aktiv! 2 Outsider wurden hinzugefügt.");
}
```

## Tests

### Automatische Tests

Das Feature wurde mit `test_baron.py` getestet:

```bash
python test_baron.py
```

**Test-Szenarien:**
1. ✅ 5 Spieler mit Baron → 2 Outsider korrekt hinzugefügt
2. ✅ 10 Spieler mit Baron → 2 Outsider korrekt hinzugefügt
3. ✅ 6 Spieler ohne Baron → Normale Verteilung unverändert

### Manuelle Tests

**Server starten:**
```bash
uvicorn main:app --reload
```

**Test-Ablauf:**
1. Öffne http://localhost:8000
2. Erstelle Spiel mit "Trouble Brewing" Edition
3. Füge 5-10 Spieler hinzu
4. Starte Spiel
5. Prüfe in Storyteller-Overview:
   - Wenn Baron vorhanden: `baron_active: true` und 2 Outsider mehr als im Setup
   - Sonst: Normale Setup-Verteilung

## Edge Cases

### Fall 1: Zu wenig Townsfolk
Wenn durch Modifikationen oder andere Charakterfähigkeiten weniger als 2 Townsfolk vorhanden sind:
- ⚠️ Warnung wird ausgegeben
- Keine Änderung wird vorgenommen
- Spiel läuft normal weiter

### Fall 2: Zu wenig Outsider in Edition
Falls eine zukünftige Edition weniger als 2 Outsider hat:
- ⚠️ Warnung wird ausgegeben
- Keine Änderung wird vorgenommen
- Spiel läuft normal weiter

### Fall 3: Mehrere Baron-Charaktere
Falls durch zukünftige Erweiterungen mehrere Barons im Spiel sein könnten:
- Die Logik wird nur **einmal** angewendet (beim ersten Baron in der Liste)
- Kein doppeltes Ersetzen

## Zukünftige Erweiterungen

### Storyteller-UI Erweiterung
Zeige in der Storyteller-Overview deutlich an:
```
⚠️ BARON AKTIV
Folgende Charaktere wurden ersetzt:
  - Washerwoman → Drunk
  - Chef → Saint
```

### Log-Persistenz
Speichere die Baron-Anwendung im Spiel-Log:
```json
{
  "event": "baron_ability_applied",
  "timestamp": "2025-01-19T14:30:00Z",
  "removed": ["washerwoman", "chef"],
  "added": ["drunk", "saint"]
}
```

### Andere Editionen
Baron existiert aktuell nur in "Trouble Brewing". Falls andere Editionen ähnliche Charaktere bekommen:
- Die Logik ist generisch implementiert (prüft auf `char.id == "baron"`)
- Kann leicht auf andere Charaktere erweitert werden

## Spielregeln-Hinweise

### Für den Storyteller
- Baron-Fähigkeit ist **passiv** und wird automatisch angewendet
- Informiere die Spieler **vor** Spielbeginn über die Baron-Mechanik
- Die ersetzten Charaktere werden **zufällig** ausgewählt
- Drunk kann als Outsider erscheinen (und denkt, er ist Townsfolk)

### Für die Spieler
- Wenn Baron im Spiel ist, gibt es **immer genau 2 mehr Outsider** als im Setup
- Dies ist eine wichtige Information für Investigatoren
- Baron ist ein **Minion** (böses Team)

## Changelog

### Version 1.0 - 2025-01-20
- ✅ Initiale Implementierung der Baron-Fähigkeit
- ✅ Automatische Outsider-Umwandlung bei Spielstart
- ✅ `baron_active` Flag im Game-Modell
- ✅ Validierungen für Edge Cases
- ✅ Konsolausgaben für Debugging
- ✅ Integration in Storyteller-Overview
- ✅ Umfassende Tests (automatisch + manuell)
- ✅ Dokumentation

---

**Erstellt:** 2025-01-20  
**Autor:** GitHub Copilot  
**Status:** ✅ Produktionsbereit

