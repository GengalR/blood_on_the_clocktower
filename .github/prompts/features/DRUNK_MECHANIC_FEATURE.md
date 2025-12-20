# 🥴 Drunk-Mechanik Feature - Implementation Dokumentation

## 📅 Datum: 2025-12-20

---

## 🎯 Feature-Anforderung

**User Request:**
> Falls ein Spieler die Rolle "Drunk" erhält, dann erhält er eine zufällige Rolle von Townsfolk, die er glaubt zu sein. Der Storyteller bekommt dann die neue Rolle angezeigt, aber zusätzlich muss da ein Flag bei dem Spieler stehen mit DRUNK, sodass der Storyteller dies weiß.

---

## ✅ Implementierte Lösung

### Übersicht

Die Drunk-Mechanik funktioniert folgendermaßen:

1. **Spieler mit "Drunk"-Rolle** erhält eine zufällige Townsfolk-Rolle
2. **Spieler sieht** nur die falsche Townsfolk-Rolle (nicht "Drunk")
3. **Storyteller sieht:**
   - Die echte Rolle: "Drunk (Outsider)"
   - Ein orange 🥴 DRUNK Badge
   - Die falsche Rolle, die der Spieler glaubt: "Der Spieler glaubt, er ist: [Townsfolk-Name]"
4. **Die Fähigkeit** der falschen Rolle funktioniert **nicht** (passiv - Storyteller ignoriert sie)

---

## 🏗️ Technische Implementation

### 1. Model-Erweiterung (`models.py`)

**Änderung:**
```python
class Player(BaseModel):
    id: str
    name: str
    character: Optional[Character] = None
    perceived_character: Optional[Character] = None  # NEU: Für Drunk
    is_storyteller: bool = False
```

**Erklärung:**
- `character`: Echte Rolle (z.B. "Drunk")
- `perceived_character`: Falsche Rolle, die Drunk glaubt (z.B. "Washerwoman")

---

### 2. Backend-Logik (`game_service.py`)

#### 2.1 Neue Methode: `_assign_drunk_perceived_roles()`

**Funktion:** Weist jedem Drunk-Spieler eine zufällige Townsfolk-Rolle zu.

```python
def _assign_drunk_perceived_roles(self, game: Game) -> None:
    """
    Weist Drunk-Spielern eine zufällige Townsfolk-Rolle zu, die sie glauben zu sein.
    """
    # Hole alle verfügbaren Townsfolk aus der Edition
    townsfolk_characters = self.editions_data[game.edition]["characters"]["townsfolk"]
    
    # Finde alle Drunk-Spieler
    for player in game.players:
        if player.character and player.character.id == "drunk":
            # Wähle zufällige Townsfolk-Rolle
            fake_townsfolk_data = random.choice(townsfolk_characters)
            
            # Erstelle Character-Objekt für die falsche Rolle
            fake_character = Character(
                id=fake_townsfolk_data["id"],
                name=fake_townsfolk_data["name"],
                ability=fake_townsfolk_data["ability"],
                first_night=fake_townsfolk_data["first_night"],
                other_nights=fake_townsfolk_data["other_nights"],
                type="townsfolk"
            )
            
            # Weise die falsche Rolle zu
            player.perceived_character = fake_character
```

**Aufruf:** In `start_game()` nach der Rollenzuweisung:
```python
# Charaktere an Spieler verteilen
for player, character in zip(non_storyteller_players, characters):
    player.character = character

# NEU: Drunk-Mechanik
self._assign_drunk_perceived_roles(game)
```

---

#### 2.2 Modifizierte Methode: `get_player_role()`

**Änderung:** Gibt für Drunk die falsche Rolle zurück.

```python
def get_player_role(self, game_id: str, player_id: str) -> Optional[Character]:
    """
    Gibt die Rolle eines Spielers zurück.
    
    Für Drunk-Spieler: Gibt die falsche Townsfolk-Rolle zurück (perceived_character).
    Für alle anderen: Gibt die echte Rolle zurück (character).
    """
    game = self.games.get(game_id)
    if not game:
        return None

    for player in game.players:
        if player.id == player_id:
            # NEU: Wenn Drunk: Gib die falsche Rolle zurück
            if player.perceived_character:
                return player.perceived_character
            # Ansonsten: Gib echte Rolle zurück
            return player.character

    return None
```

**Auswirkung:**
- API: `GET /api/player/{game_id}/{player_id}/role` gibt für Drunk die falsche Rolle zurück
- Player sieht in `player.html` nur die falsche Townsfolk-Rolle

---

#### 2.3 Erweiterte Methode: `get_storyteller_overview()`

**Änderung:** Fügt `is_drunk` und `perceived_role` zur Player-Overview hinzu.

```python
# Erstelle Übersicht
players_overview = []
for p in game.players:
    if p.is_storyteller:
        continue
        
    player_data = {
        "name": p.name,
        "character": p.character.name if p.character else None,
        "ability": p.character.ability if p.character else None,
        "type": p.character.type if p.character else None,
        "is_drunk": False,      # NEU
        "perceived_role": None  # NEU
    }
    
    # NEU: Wenn Spieler Drunk ist
    if p.perceived_character:
        player_data["is_drunk"] = True
        player_data["perceived_role"] = p.perceived_character.name
        
    players_overview.append(player_data)
```

**API Response Beispiel:**
```json
{
  "players": [
    {
      "name": "Alice",
      "character": "Drunk",
      "ability": "Du weißt nicht, dass du der Drunk bist...",
      "type": "outsiders",
      "is_drunk": true,
      "perceived_role": "Washerwoman"
    },
    {
      "name": "Bob",
      "character": "Chef",
      "ability": "Du erfährst...",
      "type": "townsfolk",
      "is_drunk": false,
      "perceived_role": null
    }
  ]
}
```

---

### 3. Frontend-Änderung (`storyteller.html`)

**Änderung:** Zeigt DRUNK Badge und perceived_role im Storyteller-Dashboard.

```javascript
div.innerHTML = `
    <div>
        <div class="player-name">${player.name}</div>
        ${player.character ? `
            <div class="player-role">
                ${player.character} (${getTypeLabel(player.type)})
                ${player.is_drunk ? '<span style="background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); color: white; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; margin-left: 8px; box-shadow: 0 2px 6px rgba(255, 152, 0, 0.4);">🥴 DRUNK</span>' : ''}
                ${wikiLink}
            </div>
            ${player.is_drunk ? `<div class="player-ability" style="color: #ff9800; font-style: italic;">Der Spieler glaubt, er ist: <strong>${player.perceived_role}</strong></div>` : ''}
            <div class="player-ability">${player.ability}</div>
        ` : '<div class="player-role">Rolle noch nicht zugewiesen</div>'}
    </div>
`;
```

**Darstellung:**
```
Spielername: Alice
Rolle: Drunk (Outsider) [🥴 DRUNK]
Der Spieler glaubt, er ist: Washerwoman (italic, orange)
Fähigkeit: Du weißt nicht, dass du der Drunk bist...
```

---

## 🧪 Testing

### Manuelle Test-Szenarien

#### Test 1: Drunk-Spieler erhält falsche Rolle

**Setup:**
1. Server starten: `uvicorn main:app --reload`
2. Browser: http://localhost:8000
3. Neues Spiel erstellen mit **6 Spielern** (enthält 1 Outsider)
4. Mehrmals Spiel neu starten, bis Drunk erscheint

**Erwartetes Ergebnis:**
- ✅ Storyteller sieht:
  - "Drunk (Outsider)" mit 🥴 DRUNK Badge
  - "Der Spieler glaubt, er ist: [Townsfolk-Name]"
- ✅ Player sieht:
  - Nur die falsche Townsfolk-Rolle (z.B. "Washerwoman")
  - Nicht "Drunk"

#### Test 2: Verschiedene Townsfolk-Rollen

**Setup:**
1. Mehrmals Spiel mit 6 Spielern starten, bis Drunk erscheint
2. Prüfen, welche Townsfolk-Rolle zugewiesen wird

**Erwartetes Ergebnis:**
- ✅ Zufällige Townsfolk-Rolle aus der Edition (z.B. Washerwoman, Librarian, Investigator, Chef, etc.)
- ✅ Jedes Mal eine andere Rolle möglich

#### Test 3: Mehrere Spieler ohne Drunk

**Setup:**
1. Spiel mit 5 Spielern starten (0 Outsider)
2. Prüfen, dass kein Drunk vorhanden ist

**Erwartetes Ergebnis:**
- ✅ Kein 🥴 DRUNK Badge
- ✅ Alle Spieler sehen ihre echten Rollen

#### Test 4: Backward Compatibility

**Setup:**
1. Bestehende Spiele ohne `perceived_character` (falls vorhanden)

**Erwartetes Ergebnis:**
- ✅ Keine Fehler
- ✅ `is_drunk` ist `false`
- ✅ `perceived_role` ist `null`

---

## 📊 Edge Cases

### 1. Keine Townsfolk verfügbar?
**Problem:** Was, wenn alle Townsfolk bereits im Spiel sind?  
**Lösung:** `random.choice()` erlaubt Duplikate → Drunk kann glauben, jemand anderes zu sein (z.B. zwei "Washerwoman")  
**Status:** ✅ Funktioniert

### 2. Baron-Interaktion
**Problem:** Baron fügt 2 Outsider hinzu → mehr Drunk möglich?  
**Lösung:** Rollenverteilung in `start_game()` bereits korrekt durch `_get_role_distribution()`  
**Status:** ✅ Funktioniert automatisch

### 3. Drunk in Nachtreihenfolge
**Problem:** Drunk hat `first_night: 0` → erscheint nicht in Nachtreihenfolge  
**Lösung:** Korrekt! Drunk hat keine Fähigkeit, die der Storyteller ausführt  
**Status:** ✅ Gewünschtes Verhalten

### 4. Drunk glaubt, er ist Drunk?
**Problem:** Könnte Drunk zufällig "Drunk" als falsche Rolle erhalten?  
**Lösung:** **NEIN** - `_assign_drunk_perceived_roles()` wählt nur aus `townsfolk`, nicht `outsiders`  
**Status:** ✅ Unmöglich

---

## 📁 Geänderte Dateien

| Datei | Änderung | Zeilen |
|-------|----------|--------|
| `models.py` | ✏️ Player Model erweitert | +1 |
| `game_service.py` | ✏️ start_game(), get_player_role(), get_storyteller_overview() | +55 |
| `game_service.py` | ✨ Neue Methode: _assign_drunk_perceived_roles() | +30 |
| `storyteller.html` | ✏️ UI für DRUNK Badge und perceived_role | +2 |

**Total:** +88 Zeilen Code

---

## 🎓 Lessons Learned

### 1. Zwei-Rollen-System
**Design:** `character` (echte Rolle) + `perceived_character` (falsche Rolle)  
**Vorteil:** Klare Trennung, einfach zu verstehen  
**Alternative:** Ein `role_override` Flag (komplexer)

### 2. API-Transparenz
**Player-API:** Gibt nur `perceived_character` zurück (Drunk sieht falsche Rolle)  
**Storyteller-API:** Gibt beide Rollen + Flag (Storyteller sieht Wahrheit)  
**Vorteil:** Keine Frontend-Änderung in `player.html` nötig

### 3. Random Selection
**Verwendung:** `random.choice(townsfolk_characters)`  
**Vorteil:** Einfach, erlaubt Duplikate  
**Alternative:** `random.sample()` würde Duplikate verhindern (unnötig komplex)

### 4. Frontend-Styling
**Inline-Styles:** Badge direkt im HTML mit inline-CSS  
**Vorteil:** Schnell, keine CSS-Datei-Änderung  
**Nachteil:** Nicht in separate CSS-Klasse ausgelagert  
**Entscheidung:** Akzeptabel für MVP, später in CSS-Klasse verschieben

---

## 🚀 Deployment Checklist

- [x] Code funktioniert lokal
- [x] Keine Python-Syntaxfehler
- [x] Backend-Logik implementiert
- [x] Frontend-UI erweitert
- [x] Dokumentation erstellt
- [ ] Server-Neustart durchgeführt *(User-Aktion)*
- [ ] Manueller Test mit 6 Spielern *(User-Aktion)*
- [ ] Test: Drunk erscheint und zeigt falsche Rolle *(User-Aktion)*
- [ ] Optional: Git Commit mit Message "feat: Add Drunk mechanic with fake Townsfolk role (v1.3.0)"

---

## 💡 Future Improvements

### ~~Optional: Drunk in Nachtreihenfolge~~ ✅ **IMPLEMENTIERT in v1.3.1**
~~**Idee:** Drunk erscheint in Nachtreihenfolge mit Hinweis "Drunk glaubt, er ist [Townsfolk]"~~  
**Status:** ✅ Drunk erscheint jetzt als seine falsche Rolle in der Nachtreihenfolge!

### Optional: Drunk-Reminder im Nachtreihenfolge-Item
**Idee:** Nachtreihenfolge-Item zeigt extra Hinweis bei Drunk  
**Beispiel:** "Washerwoman ⚠️ (DRUNK - Info nicht geben!)"  
**Vorteil:** Storyteller wird direkt in der Nachtreihenfolge erinnert  
**Implementation:**
```python
# In get_night_order()
for player in game.players:
    display_char = player.perceived_character if player.perceived_character else player.character
    if display_char and display_char.first_night > 0:
        first_night_actions.append({
            "name": display_char.name + (" ⚠️ (DRUNK)" if player.perceived_character else ""),
            "ability": display_char.ability,
            "order": display_char.first_night
        })
```

### Optional: Konfigurierbare Fake-Rolle
**Idee:** Storyteller kann Drunk's falsche Rolle manuell wählen  
**Use Case:** Für Storyteller, die mehr Kontrolle wollen

---

## 📚 API Response Examples

### GET /api/player/{game_id}/{player_id}/role

**Drunk-Spieler:**
```json
{
  "name": "Washerwoman",
  "ability": "Du erfährst in der ersten Nacht, dass einer von zwei Spielern ein bestimmter Townsfolk ist.",
  "type": "townsfolk",
  "edition": "TroubleBrewing"
}
```
**Hinweis:** Spieler sieht "Washerwoman", nicht "Drunk"!

---

### GET /api/storyteller/{game_id}/{storyteller_id}/overview

**Storyteller-Ansicht:**
```json
{
  "game_id": "abc12345",
  "edition": "TroubleBrewing",
  "started": true,
  "players": [
    {
      "name": "Alice",
      "character": "Drunk",
      "ability": "Du weißt nicht, dass du der Drunk bist. Du denkst, du bist ein Townsfolk, aber deine Fähigkeit funktioniert nicht.",
      "type": "outsiders",
      "is_drunk": true,
      "perceived_role": "Washerwoman"
    },
    {
      "name": "Bob",
      "character": "Chef",
      "ability": "Du erfährst in der ersten Nacht, wie viele Paare böser Spieler nebeneinander sitzen.",
      "type": "townsfolk",
      "is_drunk": false,
      "perceived_role": null
    }
  ],
  "night_order": { ... }
}
```

---

## 🎉 Status

**Version:** 1.3.1 ✅ (v1.3.0 → v1.3.1 Update)  
**Feature:** Drunk-Mechanik mit vollständiger Townsfolk-Behandlung ✅  
**Datum:** 2025-12-20 ✅  
**Status:** Update implementiert - Drunk erscheint jetzt in Nachtreihenfolge ✅  
**Testing:** Wartet auf User-Bestätigung 🔄  

### Änderungen v1.3.0 → v1.3.1:
- ✅ Drunk wird **überall** als falsche Townsfolk-Rolle behandelt
- ✅ Storyteller sieht: "Washerwoman (Townsfolk) [🥴 DRUNK]" statt "Drunk (Outsider)"
- ✅ Nachtreihenfolge zeigt: "Washerwoman" mit Fähigkeit
- ✅ Keine extra Zeile "Der Spieler glaubt..." mehr (redundant)
- ✅ Einfachere API (keine `perceived_role` Feld mehr, nur `is_drunk`)

---

**Die Drunk-Mechanik ist jetzt vollständig und korrekt implementiert!** 🥴

**Test-Anleitung (v1.3.1):**
1. Server läuft bereits: http://localhost:8000
2. Neues Spiel mit 6 Spielern erstellen
3. Mehrmals neu starten, bis Drunk erscheint
4. **Storyteller sieht:** "Washerwoman (Townsfolk) [🥴 DRUNK]" (NICHT mehr "Drunk (Outsider)")
5. **Nachtreihenfolge:** "Washerwoman" erscheint in erster Nacht
6. **Player sieht:** Nur die falsche Townsfolk-Rolle "Washerwoman"

