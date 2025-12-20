# 🧪 Horror Theme - Testing Guide

## 🎯 Quick Start Testing

### 1. Server starten (falls noch nicht aktiv)
```powershell
uvicorn main:app --reload
```

### 2. Browser öffnen
```
http://localhost:8000
```

---

## ✅ Test-Checkliste

### **index.html - Spielerstellung**
- [ ] Seite lädt ohne Fehler
- [ ] Hintergrundbild ist sichtbar
- [ ] Container ist halbtransparent
- [ ] Titel "Blood on the Clocktower" in Rot mit Glow
- [ ] Icon ⚰️ wird angezeigt
- [ ] Labels in Gold (#d4af37)
- [ ] Input-Felder dunkel mit rotem Fokus-Glow
- [ ] Edition-Dropdown funktioniert
- [ ] Edition-Info Box erscheint
- [ ] "Spiel erstellen" Button in Dunkelrot
- [ ] Hover-Effekt auf Button (Glow + translateY)
- [ ] Mobile Ansicht funktioniert

**Expected Look:**
- Dunkler transparenter Container
- Rote Grenzlinien oben/unten
- Goldene Labels
- Gothic-Schriftarten (Cinzel für Titel)
- Animierter Titel-Glow

---

### **join.html - Spiel Beitreten**
- [ ] Ähnlicher Stil wie index.html
- [ ] Icon 🕯️ (Kerze) wird angezeigt
- [ ] Game-Info Box transparent mit lila Hintergrund
- [ ] Spiel-ID wird korrekt angezeigt
- [ ] Input "Dein Name" funktioniert
- [ ] "Beitreten" Button funktioniert
- [ ] Error-Message erscheint bei ungültiger Game-ID
- [ ] Weiterleitung zu player.html nach Join

**Expected Look:**
- Konsistentes Design mit index.html
- Game-Info Box in transparentem Lila
- Goldene Strong-Labels in Info-Box

---

### **player.html - Spieleransicht**
- [ ] Hintergrundbild deutlich sichtbar (weniger Overlay)
- [ ] Waiting-Screen mit rotem Titel
- [ ] Spinner Animation funktioniert
- [ ] Role-Card erscheint nach Spielstart
- [ ] Rollenname in Gold
- [ ] Role-Type Badge (Townsfolk/Outsider/Minion/Demon)
- [ ] Ability-Box mit transparentem Hintergrund
- [ ] "Aktualisieren" Button in Rot
- [ ] Quick Rules Button funktioniert (bereits vorhanden)

**Expected Look:**
- Card halbtransparent (85%)
- Hintergrundbild durch Card erkennbar
- Rollen-Informationen gut lesbar
- Gothic-Styling konsistent

---

### **storyteller.html - Erzähleransicht**
- [ ] Hintergrundbild sichtbar
- [ ] Spiel-Übersicht Card transparent
- [ ] Join-URL Copy-Button funktioniert (grün)
- [ ] Spielerliste erscheint
- [ ] Spieler-Items mit transparentem Hintergrund
- [ ] "Spiel starten" Button funktioniert
- [ ] Night Order wird angezeigt
- [ ] Night-Order Numbers in Rot
- [ ] Character-Namen in Gold
- [ ] Quick Rules Button funktioniert

**Expected Look:**
- Mehrere transparente Cards
- Spielerliste mit dunklen Items
- Night-Order mit roten Nummerierungen
- Grüner Copy-Button als Kontrast

---

## 🔍 Detaillierte Funktions-Tests

### Test 1: Neues Spiel erstellen
```
1. Öffne: http://localhost:8000
2. Eingabe: Name "TestErzähler"
3. Wähle: Edition "Trouble Brewing"
4. Edition-Info sollte erscheinen
5. Klick: "Spiel erstellen"
6. ✅ Redirect zu storyteller.html
```

### Test 2: Spiel beitreten
```
1. Kopiere Join-URL aus storyteller.html
2. Öffne in neuem Inkognito-Tab
3. Eingabe: Name "TestSpieler"
4. Klick: "Beitreten"
5. ✅ Redirect zu player.html
6. ✅ Waiting-Screen erscheint
```

### Test 3: Spiel starten
```
1. Zurück zu storyteller.html
2. Eingabe: Spieleranzahl "5"
3. Klick: "Spiel starten"
4. ✅ Rollen werden verteilt
5. ✅ Night Order erscheint
6. Wechsel zu player.html Tab
7. ✅ Rolle wird angezeigt
```

---

## 🎨 Visuelle Checks

### Farbschema prüfen:
- [ ] **Titel:** #dc143c (Crimson) mit Glow
- [ ] **Labels:** #d4af37 (Gold)
- [ ] **Text:** #f5f5dc (Beige/Bone)
- [ ] **Container:** rgba(26, 26, 26, 0.85-0.9)
- [ ] **Buttons:** linear-gradient(#8b0000, #4a0000)
- [ ] **Borders:** rgba(139, 0, 0, 0.4-0.5)

### Transparenz prüfen:
- [ ] Hintergrundbild durch Container erkennbar
- [ ] backdrop-filter Blur-Effekt sichtbar
- [ ] Keine weißen/hellen Bereiche mehr
- [ ] Text trotz Transparenz lesbar

### Typografie prüfen:
- [ ] Titel in Cinzel (Serif, majestätisch)
- [ ] Labels in Crimson Text (elegant)
- [ ] Body in Lora (klassisch lesbar)
- [ ] Keine alten Sans-Serif Fonts

---

## 📱 Mobile Testing

### iOS Safari
```
1. iPhone/iPad öffnen
2. Navigiere zu http://<your-ip>:8000
3. Prüfe alle 4 Seiten
4. Touch-Gesten funktionieren
5. Schriftgröße angemessen
6. Buttons erreichbar
```

### Android Chrome
```
1. Android Gerät öffnen
2. Navigiere zu http://<your-ip>:8000
3. Prüfe alle 4 Seiten
4. Keine Horizontal-Scrolls
5. Inputs funktionieren
6. Dropdowns öffnen sich
```

---

## 🐛 Häufige Probleme

### Problem: Hintergrundbild nicht sichtbar
**Lösung:**
- Prüfe: `/static/images/blood_on_the_clocktower.webp` existiert
- Browser-Cache leeren (Ctrl+Shift+R)
- DevTools: Network-Tab prüfen (200 OK?)

### Problem: Fonts laden nicht
**Lösung:**
- Internet-Verbindung prüfen
- Google Fonts erreichbar?
- Browser-Konsole: CORS-Fehler?

### Problem: backdrop-filter funktioniert nicht
**Lösung:**
- Browser-Support prüfen (Chrome/Firefox/Safari OK)
- Hardware-Beschleunigung aktiviert?
- Fallback: Container opacity erhöhen

### Problem: Text nicht lesbar
**Lösung:**
- text-shadow zu schwach? → Erhöhen
- Container zu transparent? → Opacity erhöhen
- Kontrast zu gering? → Textfarbe aufhellen

---

## 🎬 Test-Szenarien

### Szenario 1: Quick Game
```
Zeit: ~2 Minuten
1. Spiel erstellen (Trouble Brewing, 5 Spieler)
2. 2 Spieler joinen (Inkognito-Tabs)
3. Spiel starten
4. Rollen prüfen
5. Night Order prüfen
✅ Alles Horror-Styled?
```

### Szenario 2: Edge Cases
```
1. Spiel erstellen ohne Edition → Error in Rot?
2. Join ohne Game-ID → Error in Rot?
3. Join bereits gestartetes Spiel → Error?
4. Browser zurück-Button → Funktioniert?
```

### Szenario 3: Multi-Browser
```
1. Chrome: Spiel erstellen
2. Firefox: Spieler 1 joined
3. Safari: Spieler 2 joined
4. Edge: Spieler 3 joined
✅ Alle sehen Horror-Theme?
```

---

## 📊 Performance-Check

### Lighthouse-Test (Chrome DevTools)
```
1. F12 → Lighthouse Tab
2. Performance-Test starten
3. Ziel: Score > 80
4. Prüfen: backdrop-filter Impact?
```

### FPS-Monitor
```
1. DevTools → Rendering → FPS Meter
2. Animations beobachten
3. Ziel: 60 FPS
4. Bei < 30 FPS: Animationen reduzieren
```

---

## ✅ Sign-Off Checklist

Vor dem Merge:
- [ ] Alle 4 Seiten manuell getestet
- [ ] Chrome, Firefox, Safari getestet
- [ ] Mobile (iOS + Android) getestet
- [ ] Keine Console-Errors
- [ ] Keine Network-Errors
- [ ] Lesbarkeit bestätigt
- [ ] Hintergrundbild auf allen Seiten sichtbar
- [ ] Funktionalität unverändert
- [ ] Screenshots erstellt
- [ ] Team-Feedback positiv

---

## 🎯 Expected Results

### Was du sehen solltest:
1. **Dunkle, mysteriöse Atmosphäre** 🌙
2. **Hintergrundbild durchscheinend** 🖼️
3. **Gothic-Eleganz** 🏰
4. **Blutrot-Gold Kontraste** 🩸✨
5. **Glasmorphism-Effekte** 💎
6. **Smooth Animationen** 🎭

### Was NICHT passieren sollte:
- ❌ Weiße/helle Bereiche
- ❌ Unlesbarer Text
- ❌ Unsichtbares Hintergrundbild
- ❌ Gebrochenes Layout
- ❌ Nicht-funktionierende Buttons
- ❌ JavaScript-Errors

---

## 📸 Screenshot-Punkte

Erstelle Screenshots für:
1. **index.html** - Vollbild
2. **join.html** - Vollbild
3. **player.html** - Waiting Screen
4. **player.html** - Mit Rolle
5. **storyteller.html** - Overview
6. **storyteller.html** - Night Order
7. **Mobile** - index.html
8. **Mobile** - player.html

---

## 🚀 Ready to Test?

```bash
# Server läuft bereits!
# Öffne: http://localhost:8000
# Los geht's! 🎭🩸
```

**Viel Erfolg beim Testing! Möge das Horror-Theme Angst und Schrecken verbreiten! 😈**

