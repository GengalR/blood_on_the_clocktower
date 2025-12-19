# Implementation Plan: Quick Rules Modal

**Status:** ✅ Geplant  
**Assigned To:** Development Team  
**Estimated Time:** 2.5 Stunden  
**Priority:** P2 (Medium)

---

## 📋 Überblick

Eine "Schnellregeln"-Funktion implementieren, die neuen Spielern während des Spiels einen schnellen Überblick über die 4 wichtigsten Spielregeln bietet. Die Lösung nutzt einen **Pure Frontend-Ansatz** mit Modal-Overlay in `player.html`, folgt dem bestehenden Inline-CSS-Pattern des Projekts und ist vollständig auf Deutsch.

---

## 🎯 Implementierungs-Schritte

### Step 1: Modal-HTML-Struktur in player.html hinzufügen
**Geschätzte Zeit:** 30 Minuten

#### Was zu tun ist:
1. **Quick Rules Button** im Kopfbereich hinzufügen:
   - Position: rechts oben neben "🎭 Blood on the Clocktower"
   - Icon: 📜 oder ❓
   - `position: fixed` oder `absolute` mit hohem z-index

2. **Modal-Container** nach `.container` einfügen:
   - Overlay mit halbtransparentem Hintergrund
   - Zentrierte Modal-Box
   - Close-Button (X) oben rechts
   - 4 Regelblöcke mit Emojis

#### Code-Struktur:
```html
<!-- Quick Rules Button (nach <h1>) -->
<button id="quickRulesBtn" class="quick-rules-btn" 
        aria-label="Schnellregeln anzeigen">
    📜 Regeln
</button>

<!-- Modal Overlay (nach .container) -->
<div id="rulesModal" class="modal-overlay" role="dialog" 
     aria-modal="true" aria-labelledby="rulesModalTitle">
    <div class="modal-content">
        <button class="modal-close" aria-label="Schließen">×</button>
        <h2 id="rulesModalTitle">🎭 Blood on the Clocktower - Schnellregeln</h2>
        
        <div class="rule-section">
            <h3>1️⃣ Siegbedingungen</h3>
            <ul>
                <li><strong>Gut gewinnt</strong>, wenn der Demon stirbt</li>
                <li><strong>Böse gewinnt</strong>, wenn nur noch 2 Spieler leben</li>
            </ul>
        </div>
        
        <!-- Weitere Regelblöcke... -->
    </div>
</div>
```

---

### Step 2: CSS-Styling im `<style>`-Block ergänzen
**Geschätzte Zeit:** 45 Minuten

#### Was zu tun ist:
1. **Button-Styles** (`.quick-rules-btn`):
   - Fixed positioning: `top: 20px, right: 20px`
   - z-index: 1000 (über anderen Elementen)
   - Hover-Effekt für Interaktivität

2. **Modal-Overlay** (`.modal-overlay`):
   - `display: none` initial
   - `position: fixed; top: 0; left: 0; width: 100%; height: 100%`
   - `background: rgba(0, 0, 0, 0.7)`
   - z-index: 2000

3. **Modal-Content** (`.modal-content`):
   - Zentriert: `position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%)`
   - `max-width: 600px; max-height: 80vh`
   - `overflow-y: auto` für Scrollbarkeit
   - Padding und Border-Radius für ansprechendes Design

4. **Responsive Design**:
   - Media Query für `< 600px`: Kleinerer Button, mehr Padding
   - Vollbild-Modal auf mobilen Geräten

#### Code-Template:
```css
.quick-rules-btn {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 10px 15px;
    background: #4a5568;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    z-index: 1000;
    font-size: 16px;
}

.quick-rules-btn:hover {
    background: #2d3748;
}

.modal-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    z-index: 2000;
}

.modal-overlay.active {
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background: white;
    border-radius: 10px;
    padding: 30px;
    max-width: 600px;
    max-height: 80vh;
    overflow-y: auto;
    position: relative;
}

.modal-close {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 30px;
    cursor: pointer;
    color: #888;
}

.rule-section {
    margin: 20px 0;
}

.rule-section h3 {
    color: #2d3748;
    margin-bottom: 10px;
}

.rule-section ul {
    list-style: none;
    padding-left: 0;
}

.rule-section li {
    padding: 5px 0;
}

@media (max-width: 600px) {
    .quick-rules-btn {
        font-size: 14px;
        padding: 8px 12px;
    }
    
    .modal-content {
        padding: 20px;
        max-height: 90vh;
    }
}
```

---

### Step 3: JavaScript-Interaktivität implementieren
**Geschätzte Zeit:** 30 Minuten

#### Was zu tun ist:
1. **Modal öffnen/schließen Funktionen**:
   - `openRulesModal()`: Zeigt Modal, fügt `active` CSS-Klasse hinzu
   - `closeRulesModal()`: Versteckt Modal, entfernt `active` Klasse

2. **Event Listeners**:
   - Button-Click: öffnet Modal
   - Close-Button-Click: schließt Modal
   - ESC-Taste: schließt Modal
   - Click außerhalb Modal: schließt Modal

3. **Keyboard Accessibility**:
   - Focus-Trap im Modal (Tab bleibt innerhalb)
   - ESC-Handler mit `event.key === 'Escape'`

#### Code-Template:
```javascript
// Quick Rules Modal Funktionen
function openRulesModal() {
    const modal = document.getElementById('rulesModal');
    modal.classList.add('active');
    // Focus auf ersten interaktiven Element
    const closeBtn = modal.querySelector('.modal-close');
    closeBtn.focus();
}

function closeRulesModal() {
    const modal = document.getElementById('rulesModal');
    modal.classList.remove('active');
    // Focus zurück auf Button
    document.getElementById('quickRulesBtn').focus();
}

// Event Listeners
document.getElementById('quickRulesBtn').addEventListener('click', openRulesModal);

document.querySelector('.modal-close').addEventListener('click', closeRulesModal);

// Click außerhalb Modal schließt
document.getElementById('rulesModal').addEventListener('click', (e) => {
    if (e.target.id === 'rulesModal') {
        closeRulesModal();
    }
});

// ESC-Taste schließt Modal
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = document.getElementById('rulesModal');
        if (modal.classList.contains('active')) {
            closeRulesModal();
        }
    }
});
```

---

### Step 4: Deutsche Regelinhalte einfügen
**Geschätzte Zeit:** 15 Minuten

#### Was zu tun ist:
Übertrage die 4 Regelblöcke aus dem Feature-Request in HTML-Format:

```html
<div class="rule-section">
    <h3>1️⃣ Siegbedingungen</h3>
    <ul>
        <li><strong>Gut gewinnt</strong>, wenn der Demon stirbt</li>
        <li><strong>Böse gewinnt</strong>, wenn nur noch 2 Spieler leben (Travellers zählen nicht)</li>
    </ul>
</div>

<div class="rule-section">
    <h3>2️⃣ Tag-Phase</h3>
    <ul>
        <li><strong>Diskutieren:</strong> Alle sprechen offen oder privat</li>
        <li><strong>Nominieren:</strong> Spieler nominieren verdächtige Personen</li>
        <li><strong>Hinrichtung:</strong> Bei 50%+ Stimmen wird nominierter Spieler hingerichtet</li>
        <li>Nur <strong>1 Hinrichtung pro Tag</strong> möglich</li>
    </ul>
</div>

<div class="rule-section">
    <h3>3️⃣ Nacht-Phase</h3>
    <ul>
        <li><strong>Augen schließen:</strong> Alle Spieler haben Augen zu</li>
        <li><strong>Fähigkeiten:</strong> Storyteller weckt Charaktere einzeln</li>
        <li><strong>Demon tötet:</strong> Demon wählt ein Opfer</li>
        <li><strong>Morgen:</strong> Storyteller verkündet, wer gestorben ist</li>
    </ul>
</div>

<div class="rule-section">
    <h3>4️⃣ Tod & Abstimmen</h3>
    <ul>
        <li><strong>Sprechen erlaubt:</strong> Tote Spieler dürfen weiter reden</li>
        <li><strong>1 Stimme übrig:</strong> Tote haben nur noch 1 Stimme fürs ganze Spiel</li>
        <li><strong>Team-Sieg:</strong> Tote gewinnen/verlieren mit ihrem Team</li>
    </ul>
</div>
```

---

### Step 5: Cross-Browser-Testing & Mobile-Optimierung
**Geschätzte Zeit:** 30 Minuten

#### Test-Checkliste:

**Desktop-Browser:**
- [ ] Chrome: Modal öffnet/schließt korrekt
- [ ] Firefox: Button sichtbar, Modal zentriert
- [ ] Edge: Keine Layout-Probleme
- [ ] Safari (falls verfügbar): Kompatibilität prüfen

**Mobile:**
- [ ] Button bleibt auf kleinen Bildschirmen erreichbar
- [ ] Modal ist scrollbar auf langen Seiten
- [ ] Text bleibt lesbar (Schriftgröße min. 14px)
- [ ] Touch-Events funktionieren (Tap zum Schließen)

**Keyboard-Navigation:**
- [ ] Tab: Durchläuft Button → Close-Button
- [ ] Enter: Öffnet/Schließt Modal
- [ ] ESC: Schließt Modal
- [ ] Focus-Trap: Tab bleibt im Modal

**Screen-Reader:**
- [ ] Button hat aria-label: "Schnellregeln anzeigen"
- [ ] Modal hat role="dialog" und aria-modal="true"
- [ ] Überschrift hat aria-labelledby
- [ ] Ankündigung beim Öffnen

**Testing-Commands:**
```bash
# Server starten
uvicorn main:app --reload

# Browser öffnen
# http://localhost:8000/player.html?game=test&player=test123

# Manuelle Tests durchführen
```

---

### Step 6: Optional - Zu storyteller.html hinzufügen
**Geschätzte Zeit:** 20 Minuten (optional)

#### Was zu tun ist:
1. Gleichen Code-Block aus `player.html` kopieren
2. In `storyteller.html` einfügen
3. Button könnte kleiner/diskreter sein (optional):
   ```css
   .storyteller-view .quick-rules-btn {
       font-size: 14px;
       padding: 8px 12px;
       top: 80px; /* Unter anderem Content */
   }
   ```

---

## 🔍 Weitere Überlegungen

### 1. Button-Position-Strategie
**Problem:** Fixed vs. Absolute positioning?
- **Fixed:** Button scrollt mit, immer sichtbar
- **Absolute:** Button nur am Seitenanfang sichtbar

**Empfehlung:** 
✅ `position: fixed` für ständige Erreichbarkeit während des Spiels

### 2. Mobile-Button-Größe
**Problem:** Button könnte mit H1-Titel kollidieren auf schmalen Bildschirmen

**Empfehlung:** 
✅ Media Query für `< 600px`:
```css
@media (max-width: 600px) {
    .quick-rules-btn {
        top: 60px; /* Unter Titel verschieben */
        font-size: 14px;
    }
}
```

### 3. Inhaltserweiterung
**Frage:** Später Traveller-Regeln oder Character-Abilities hinzufügen?

**Empfehlung:** 
✅ Vorerst bei 4 Kernregeln bleiben (MVP)
💡 Später optional Tabs/Sections ergänzbar:
```html
<div class="modal-tabs">
    <button class="tab active">Grundregeln</button>
    <button class="tab">Charaktere</button>
    <button class="tab">Travellers</button>
</div>
```

### 4. Performance
**Frage:** Lazy-loading notwendig?

**Empfehlung:** 
✅ Nein - Modal-Content mit `display: none` hat keinen Performance-Impact
- Reiner Text, keine Bilder
- Kein API-Call notwendig

---

## ⚠️ Risiken & Abhängigkeiten

### Risiken:
1. **Z-Index-Konflikte:** Falls andere Elemente hohen z-index haben
   - **Mitigation:** z-index: 2000 für Modal-Overlay

2. **Button-Kollision:** Button könnte auf mobilen Geräten mit Titel überlappen
   - **Mitigation:** Media Query für kleine Bildschirme

3. **Scroll-Lock:** Body könnte weiter scrollen wenn Modal offen
   - **Mitigation:** Optional `body.style.overflow = 'hidden'` beim Öffnen

### Abhängigkeiten:
- ✅ Keine Backend-Änderungen notwendig
- ✅ Keine neuen Libraries/Dependencies
- ✅ Keine API-Endpoints
- ✅ player.html muss existieren (bereits vorhanden)

---

## ✅ Definition of Done

- [ ] Button sichtbar auf player.html (top-right)
- [ ] Modal öffnet beim Button-Click
- [ ] 4 Regelblöcke klar formatiert in Deutsch
- [ ] Close-Button (X) funktioniert
- [ ] ESC-Taste schließt Modal
- [ ] Click außerhalb schließt Modal
- [ ] Mobile responsive (getestet < 600px)
- [ ] Keyboard accessible (Tab, Enter, ESC)
- [ ] Screen-Reader kompatibel (ARIA-Labels)
- [ ] Getestet in Chrome, Firefox, Edge
- [ ] Keine JavaScript-Fehler in Console
- [ ] Code reviewed
- [ ] Optional: Zu storyteller.html hinzugefügt

---

## 📊 Zeitplan

| Phase | Geschätzte Zeit | Kumulative Zeit |
|-------|-----------------|-----------------|
| Step 1: HTML Struktur | 30 min | 30 min |
| Step 2: CSS Styling | 45 min | 1h 15min |
| Step 3: JavaScript | 30 min | 1h 45min |
| Step 4: Content | 15 min | 2h |
| Step 5: Testing | 30 min | 2h 30min |
| Step 6: Storyteller (Optional) | 20 min | 2h 50min |

**Total:** 2.5 - 3 Stunden

---

## 🚀 Nächste Schritte

1. ✅ Plan reviewed und approved
2. 📝 Start mit Step 1: HTML-Struktur hinzufügen
3. 🎨 CSS-Styling implementieren
4. ⚙️ JavaScript-Funktionalität
5. ✍️ Deutsche Inhalte einfügen
6. 🧪 Testing durchführen
7. 🎯 Optional: Storyteller-View ergänzen

---

**Erstellt:** 2025-01-19  
**Geplant von:** Feature Planner Agent  
**Bereit für:** Implementation

