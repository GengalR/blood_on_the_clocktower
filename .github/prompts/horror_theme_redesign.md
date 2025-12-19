# 🎭 Blood on the Clocktower - Horror Theme Redesign
## Umfassende UI/UX Überarbeitung im Gothic Horror Stil

**Erstellt:** 2025-01-19  
**Version:** 1.0  
**Ziel:** Alle HTML-Seiten im Horror-Stil überarbeiten mit transparenten Elementen über Hintergrundbild

---

## 📋 Übersicht

Dieses Dokument beschreibt die vollständige Überarbeitung aller HTML-Seiten im `static/` Ordner, um ein immersives Horror-Erlebnis zu schaffen, das dem Thema "Blood on the Clocktower" gerecht wird.

### Zu überarbeitende Dateien:
1. ✅ `static/index.html` - Hauptmenü/Spielerstellung
2. ✅ `static/join.html` - Spiel beitreten
3. ✅ `static/player.html` - Spieleransicht
4. ✅ `static/storyteller.html` - Erzähler/Storyteller-Ansicht

---

## 🎨 Design-Philosophie

### 1. **Gothic Victorian Horror Ästhetik**
- Dunkle, mysteriöse Atmosphäre
- Elegante, aber bedrohliche Gestaltung
- Anspielung auf viktorianische Zeiten und okkulte Symbolik
- Subtile Animationen für mehr Lebendigkeit

### 2. **Farbpalette**
```css
/* Primärfarben */
--blood-red: #8b0000;           /* Dunkelrot - Blut */
--crimson: #dc143c;             /* Crimson - Akzente */
--midnight-black: #0f0f0f;      /* Tiefes Schwarz */
--charcoal: #1a1a1a;            /* Dunkelgrau */
--gothic-purple: #2d1b3d;       /* Dunkles Lila */

/* Akzentfarben */
--gold: #d4af37;                /* Antikes Gold */
--silver: #c0c0c0;              /* Silber */
--bone-white: #f5f5dc;          /* Knochenfarbe für Text */

/* Transparenz-Overlays */
--dark-overlay: rgba(15, 15, 15, 0.85);
--red-glow: rgba(139, 0, 0, 0.3);
--purple-mist: rgba(45, 27, 61, 0.6);
```

### 3. **Schriftarten**
```css
/* Hauptschriften */
--font-gothic: 'Crimson Text', 'Georgia', serif;
--font-title: 'Cinzel', 'Times New Roman', serif;
--font-body: 'Lora', 'Georgia', serif;

/* Google Fonts Import */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:wght@400;600;700&family=Lora:wght@400;500;600&display=swap');
```

---

## 🖼️ Hintergrundbild Integration

### Kernanforderung:
Das Bild `static/images/blood_on_the_clocktower.webp` soll **immer sichtbar** bleiben!

### Implementierung:
```css
body {
    /* Hintergrundbild fest verankert */
    background: url('/static/images/blood_on_the_clocktower.webp') center/cover no-repeat fixed;
    
    /* Dunkles Overlay für bessere Lesbarkeit */
    background-color: #0f0f0f;
    
    /* Falls mehrere Overlays gewünscht */
    background-image: 
        linear-gradient(to bottom, rgba(15, 15, 15, 0.7), rgba(139, 0, 0, 0.5)),
        url('/static/images/blood_on_the_clocktower.webp');
    
    min-height: 100vh;
    background-attachment: fixed; /* Parallax-Effekt */
}
```

### Transparente Container:
```css
.container, .card {
    /* Halbtransparenter Hintergrund */
    background: rgba(26, 26, 26, 0.85);
    
    /* Glasmorphism-Effekt */
    backdrop-filter: blur(10px) saturate(150%);
    -webkit-backdrop-filter: blur(10px) saturate(150%);
    
    /* Dunkelroter Rand mit Glow */
    border: 2px solid rgba(139, 0, 0, 0.6);
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.8),
        inset 0 0 40px rgba(139, 0, 0, 0.1),
        0 0 20px rgba(139, 0, 0, 0.3);
    
    border-radius: 15px;
    padding: 30px;
}
```

---

## 📄 Datei-spezifische Änderungen

### 1. **index.html - Spielerstellung**

#### Aktuelle Probleme:
- ❌ Helles weißes Design (nicht Horror-gerecht)
- ❌ Fröhliche Lila-Gradienten
- ❌ Generisches Icon (🎭)
- ❌ Kein Hintergrundbild

#### Redesign-Ziele:
- ✅ Dunkles, geheimnisvolles Willkommensportal
- ✅ Transparente Container über Hintergrundbild
- ✅ Gothic-Schriftarten
- ✅ Düstere Farbpalette

#### Code-Änderungen:

**CSS Änderungen (im `<style>` Tag):**
```css
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:wght@400;600;700&family=Lora:wght@400;500;600&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Lora', 'Georgia', serif;
    background: 
        linear-gradient(to bottom, rgba(15, 15, 15, 0.75), rgba(45, 27, 61, 0.65)),
        url('/static/images/blood_on_the_clocktower.webp') center/cover no-repeat fixed;
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    color: #f5f5dc;
}

.container {
    background: rgba(26, 26, 26, 0.9);
    backdrop-filter: blur(15px) saturate(150%);
    -webkit-backdrop-filter: blur(15px) saturate(150%);
    border-radius: 20px;
    padding: 50px 40px;
    max-width: 600px;
    width: 100%;
    box-shadow: 
        0 20px 60px rgba(0, 0, 0, 0.9),
        inset 0 0 60px rgba(139, 0, 0, 0.1),
        0 0 40px rgba(139, 0, 0, 0.3);
    border: 2px solid rgba(139, 0, 0, 0.5);
    position: relative;
    overflow: hidden;
}

/* Gothic Border Decoration */
.container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, 
        transparent, 
        #8b0000, 
        #dc143c, 
        #8b0000, 
        transparent);
    box-shadow: 0 0 10px #8b0000;
}

.container::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, 
        transparent, 
        #8b0000, 
        #dc143c, 
        #8b0000, 
        transparent);
    box-shadow: 0 0 10px #8b0000;
}

h1 {
    font-family: 'Cinzel', 'Times New Roman', serif;
    color: #dc143c;
    margin-bottom: 10px;
    text-align: center;
    font-size: 3em;
    font-weight: 700;
    text-shadow: 
        0 0 20px rgba(220, 20, 60, 0.8),
        0 0 40px rgba(139, 0, 0, 0.5),
        2px 2px 4px rgba(0, 0, 0, 0.9);
    letter-spacing: 2px;
    animation: titleGlow 3s ease-in-out infinite alternate;
}

@keyframes titleGlow {
    from {
        text-shadow: 
            0 0 20px rgba(220, 20, 60, 0.6),
            0 0 40px rgba(139, 0, 0, 0.3),
            2px 2px 4px rgba(0, 0, 0, 0.9);
    }
    to {
        text-shadow: 
            0 0 30px rgba(220, 20, 60, 1),
            0 0 60px rgba(139, 0, 0, 0.7),
            2px 2px 4px rgba(0, 0, 0, 0.9);
    }
}

.subtitle {
    text-align: center;
    color: #c0c0c0;
    margin-bottom: 40px;
    font-size: 1.2em;
    font-family: 'Crimson Text', serif;
    font-style: italic;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

.icon {
    font-size: 4em;
    text-align: center;
    margin-bottom: 20px;
    filter: drop-shadow(0 0 10px rgba(220, 20, 60, 0.6));
    animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
    0%, 100% { 
        transform: scale(1);
        filter: drop-shadow(0 0 10px rgba(220, 20, 60, 0.6));
    }
    50% { 
        transform: scale(1.05);
        filter: drop-shadow(0 0 20px rgba(220, 20, 60, 0.9));
    }
}

.form-group {
    margin-bottom: 25px;
}

label {
    display: block;
    margin-bottom: 10px;
    color: #d4af37;
    font-weight: 600;
    font-family: 'Crimson Text', serif;
    font-size: 1.1em;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

input[type="text"],
select {
    width: 100%;
    padding: 14px 16px;
    border: 2px solid rgba(139, 0, 0, 0.4);
    border-radius: 10px;
    font-size: 16px;
    font-family: 'Lora', serif;
    background: rgba(15, 15, 15, 0.6);
    color: #f5f5dc;
    transition: all 0.3s ease;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5);
}

input[type="text"]:focus,
select:focus {
    outline: none;
    border-color: #dc143c;
    background: rgba(15, 15, 15, 0.8);
    box-shadow: 
        inset 0 2px 8px rgba(0, 0, 0, 0.7),
        0 0 15px rgba(220, 20, 60, 0.4);
}

input[type="text"]::placeholder {
    color: #888;
}

select option {
    background: #1a1a1a;
    color: #f5f5dc;
}

button {
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, #8b0000 0%, #4a0000 100%);
    color: #f5f5dc;
    border: 2px solid rgba(220, 20, 60, 0.4);
    border-radius: 10px;
    font-size: 18px;
    font-weight: 700;
    font-family: 'Cinzel', serif;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 
        0 6px 20px rgba(139, 0, 0, 0.6),
        0 0 30px rgba(139, 0, 0, 0.3);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
    position: relative;
    overflow: hidden;
}

button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(220, 20, 60, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

button:hover::before {
    width: 300px;
    height: 300px;
}

button:hover {
    transform: translateY(-3px);
    box-shadow: 
        0 10px 30px rgba(139, 0, 0, 0.8),
        0 0 40px rgba(255, 0, 0, 0.5);
    border-color: rgba(220, 20, 60, 0.7);
    background: linear-gradient(135deg, #a00000 0%, #5a0000 100%);
}

button:active {
    transform: translateY(-1px);
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

.loading {
    display: none;
    text-align: center;
    margin-top: 20px;
    color: #dc143c;
    font-style: italic;
    text-shadow: 0 0 10px rgba(220, 20, 60, 0.5);
}

.error {
    background-color: rgba(139, 0, 0, 0.3);
    border: 2px solid rgba(220, 20, 60, 0.6);
    color: #ff6b6b;
    padding: 14px;
    border-radius: 10px;
    margin-bottom: 20px;
    display: none;
    text-align: center;
    font-weight: 600;
    box-shadow: 
        0 4px 15px rgba(139, 0, 0, 0.4),
        inset 0 0 20px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(5px);
}

.edition-info {
    background: rgba(45, 27, 61, 0.4);
    border: 1px solid rgba(139, 0, 0, 0.3);
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
    font-size: 14px;
    color: #c0c0c0;
    backdrop-filter: blur(5px);
    box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.3);
}

.edition-info strong {
    color: #d4af37;
}

/* Responsive Design */
@media (max-width: 600px) {
    .container {
        padding: 30px 25px;
    }
    
    h1 {
        font-size: 2.2em;
    }
    
    .subtitle {
        font-size: 1em;
    }
}
```

**HTML Änderungen:**
```html
<!-- Icon ändern von 🎭 zu etwas Gruseligeren -->
<div class="icon">⚰️</div>
<!-- Oder: 🕯️, 🩸, ☠️, 🌙 -->
```

---

### 2. **join.html - Spiel Beitreten**

#### Redesign-Ziele:
- ✅ Ähnlicher Stil wie index.html für Konsistenz
- ✅ Transparente Game-Info Box
- ✅ Horror-Atmosphäre beibehalten

#### Code-Änderungen:

**CSS Änderungen:**
```css
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:wght@400;600;700&family=Lora:wght@400;500;600&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Lora', 'Georgia', serif;
    background: 
        linear-gradient(to bottom, rgba(15, 15, 15, 0.75), rgba(45, 27, 61, 0.65)),
        url('/static/images/blood_on_the_clocktower.webp') center/cover no-repeat fixed;
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    color: #f5f5dc;
}

.container {
    background: rgba(26, 26, 26, 0.9);
    backdrop-filter: blur(15px) saturate(150%);
    -webkit-backdrop-filter: blur(15px) saturate(150%);
    border-radius: 20px;
    padding: 40px;
    max-width: 500px;
    width: 100%;
    box-shadow: 
        0 20px 60px rgba(0, 0, 0, 0.9),
        inset 0 0 60px rgba(139, 0, 0, 0.1),
        0 0 40px rgba(139, 0, 0, 0.3);
    border: 2px solid rgba(139, 0, 0, 0.5);
    position: relative;
}

.container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, 
        transparent, #8b0000, #dc143c, #8b0000, transparent);
    box-shadow: 0 0 10px #8b0000;
}

h1 {
    font-family: 'Cinzel', 'Times New Roman', serif;
    color: #dc143c;
    margin-bottom: 10px;
    text-align: center;
    font-size: 2em;
    font-weight: 700;
    text-shadow: 
        0 0 20px rgba(220, 20, 60, 0.8),
        0 0 40px rgba(139, 0, 0, 0.5),
        2px 2px 4px rgba(0, 0, 0, 0.9);
}

.subtitle {
    text-align: center;
    color: #c0c0c0;
    margin-bottom: 30px;
    font-family: 'Crimson Text', serif;
    font-style: italic;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

.game-info {
    background: rgba(45, 27, 61, 0.4);
    border: 1px solid rgba(139, 0, 0, 0.3);
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 25px;
    backdrop-filter: blur(8px);
    box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.4);
}

.game-info p {
    margin: 8px 0;
    color: #c0c0c0;
    font-family: 'Crimson Text', serif;
    font-size: 16px;
}

.game-info strong {
    color: #d4af37;
    font-weight: 600;
}

.game-info span {
    color: #f5f5dc;
}

.form-group {
    margin-bottom: 25px;
}

label {
    display: block;
    margin-bottom: 10px;
    color: #d4af37;
    font-weight: 600;
    font-family: 'Crimson Text', serif;
    font-size: 1.1em;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

input {
    width: 100%;
    padding: 14px;
    border: 2px solid rgba(139, 0, 0, 0.4);
    border-radius: 10px;
    font-size: 16px;
    font-family: 'Lora', serif;
    background: rgba(15, 15, 15, 0.6);
    color: #f5f5dc;
    transition: all 0.3s ease;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5);
}

input:focus {
    outline: none;
    border-color: #dc143c;
    background: rgba(15, 15, 15, 0.8);
    box-shadow: 
        inset 0 2px 8px rgba(0, 0, 0, 0.7),
        0 0 15px rgba(220, 20, 60, 0.4);
}

input::placeholder {
    color: #888;
}

button {
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, #8b0000 0%, #4a0000 100%);
    color: #f5f5dc;
    border: 2px solid rgba(220, 20, 60, 0.4);
    border-radius: 10px;
    font-size: 18px;
    font-weight: 700;
    font-family: 'Cinzel', serif;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 
        0 6px 20px rgba(139, 0, 0, 0.6),
        0 0 30px rgba(139, 0, 0, 0.3);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

button:hover {
    transform: translateY(-3px);
    box-shadow: 
        0 10px 30px rgba(139, 0, 0, 0.8),
        0 0 40px rgba(255, 0, 0, 0.5);
    border-color: rgba(220, 20, 60, 0.7);
    background: linear-gradient(135deg, #a00000 0%, #5a0000 100%);
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

.loading {
    text-align: center;
    color: #dc143c;
    margin-top: 15px;
    font-style: italic;
    text-shadow: 0 0 10px rgba(220, 20, 60, 0.5);
}

.error {
    background: rgba(139, 0, 0, 0.3);
    border: 2px solid rgba(220, 20, 60, 0.6);
    color: #ff6b6b;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
    font-weight: 600;
    box-shadow: 
        0 4px 15px rgba(139, 0, 0, 0.4),
        inset 0 0 20px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(5px);
}

/* Responsive */
@media (max-width: 600px) {
    .container {
        padding: 30px 25px;
    }
}
```

---

### 3. **player.html - Spieleransicht**

#### Hinweis:
Diese Seite verwendet bereits das Hintergrundbild! Aber es ist noch nicht optimal umgesetzt.

#### Aktuelle Probleme:
- ⚠️ Overlay zu stark (Bild kaum sichtbar)
- ⚠️ Weiße Cards stechen zu stark hervor

#### Verbesserungen:

**CSS Änderungen:**
```css
/* In der body Definition ändern: */
body {
    font-family: 'Lora', 'Georgia', serif;
    /* ALTES Overlay entfernen oder reduzieren */
    background: 
        linear-gradient(to bottom, rgba(15, 15, 15, 0.5), rgba(45, 27, 61, 0.4)),
        url('/static/images/blood_on_the_clocktower.webp') center/cover no-repeat fixed;
    background-attachment: fixed;
    min-height: 100vh;
    padding: 20px;
    color: #f5f5dc;
}

/* Card Transparenz erhöhen */
.card {
    background: rgba(26, 26, 26, 0.85);  /* Statt white */
    backdrop-filter: blur(12px) saturate(150%);
    -webkit-backdrop-filter: blur(12px) saturate(150%);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 
        0 20px 60px rgba(0, 0, 0, 0.9),
        inset 0 0 40px rgba(139, 0, 0, 0.1),
        0 0 30px rgba(139, 0, 0, 0.3);
    margin-bottom: 20px;
    border: 2px solid rgba(139, 0, 0, 0.4);
}

h1 {
    font-family: 'Cinzel', serif;
    color: #dc143c;
    margin-bottom: 20px;
    text-align: center;
    text-shadow: 
        0 0 20px rgba(220, 20, 60, 0.8),
        2px 2px 4px rgba(0, 0, 0, 0.9);
}

.waiting h2 {
    color: #dc143c;
    font-family: 'Cinzel', serif;
    text-shadow: 0 0 15px rgba(220, 20, 60, 0.6);
}

.waiting p {
    color: #c0c0c0;
}

.role-name {
    color: #d4af37;  /* Gold für Rollennamen */
    text-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
}

.role-type {
    /* Angepasste Farben für Horror-Theme */
}

.role-type.townsfolk {
    background: rgba(25, 118, 210, 0.3);
    color: #64b5f6;
    border: 1px solid rgba(25, 118, 210, 0.5);
}

.role-type.outsiders {
    background: rgba(245, 124, 0, 0.3);
    color: #ffb74d;
    border: 1px solid rgba(245, 124, 0, 0.5);
}

.role-type.minions {
    background: rgba(194, 24, 91, 0.3);
    color: #f06292;
    border: 1px solid rgba(194, 24, 91, 0.5);
}

.role-type.demons {
    background: rgba(211, 47, 47, 0.3);
    color: #e57373;
    border: 1px solid rgba(211, 47, 47, 0.5);
}

.role-ability {
    background: rgba(45, 27, 61, 0.3);
    border: 1px solid rgba(139, 0, 0, 0.3);
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    backdrop-filter: blur(5px);
    box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.3);
}

.role-ability h3 {
    color: #d4af37;
    font-family: 'Crimson Text', serif;
}

.role-ability p {
    color: #c0c0c0;
}

.refresh-btn {
    background: linear-gradient(135deg, #8b0000 0%, #4a0000 100%);
    border: 2px solid rgba(220, 20, 60, 0.4);
    color: #f5f5dc;
    font-family: 'Cinzel', serif;
    box-shadow: 
        0 4px 15px rgba(139, 0, 0, 0.5),
        0 0 20px rgba(139, 0, 0, 0.3);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

.refresh-btn:hover {
    background: linear-gradient(135deg, #a00000 0%, #5a0000 100%);
    transform: translateY(-2px);
    box-shadow: 
        0 6px 20px rgba(139, 0, 0, 0.7),
        0 0 30px rgba(255, 0, 0, 0.4);
}
```

**Hinweis:** Die Quick Rules Buttons sind bereits im Horror-Stil gestaltet - gut!

---

### 4. **storyteller.html - Erzähleransicht**

#### Ähnliche Änderungen wie player.html:

**CSS Änderungen:**
```css
body {
    font-family: 'Lora', 'Georgia', serif;
    background: 
        linear-gradient(to bottom, rgba(15, 15, 15, 0.5), rgba(45, 27, 61, 0.4)),
        url('/static/images/blood_on_the_clocktower.webp') center/cover no-repeat fixed;
    background-attachment: fixed;
    min-height: 100vh;
    padding: 20px;
    color: #f5f5dc;
}

.card {
    background: rgba(26, 26, 26, 0.85);
    backdrop-filter: blur(12px) saturate(150%);
    -webkit-backdrop-filter: blur(12px) saturate(150%);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 
        0 20px 60px rgba(0, 0, 0, 0.9),
        inset 0 0 40px rgba(139, 0, 0, 0.1),
        0 0 30px rgba(139, 0, 0, 0.3);
    margin-bottom: 20px;
    border: 2px solid rgba(139, 0, 0, 0.4);
}

h1 {
    font-family: 'Cinzel', serif;
    color: #dc143c;
    text-shadow: 
        0 0 20px rgba(220, 20, 60, 0.8),
        2px 2px 4px rgba(0, 0, 0, 0.9);
}

.subtitle {
    color: #c0c0c0;
    font-family: 'Crimson Text', serif;
    font-style: italic;
}

.game-info {
    background: rgba(45, 27, 61, 0.3);
    border: 1px solid rgba(139, 0, 0, 0.3);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    backdrop-filter: blur(5px);
    box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.3);
}

.game-info p {
    color: #c0c0c0;
}

.game-info strong {
    color: #d4af37;
}

label {
    color: #d4af37;
    font-family: 'Crimson Text', serif;
    font-weight: 600;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

input, select {
    background: rgba(15, 15, 15, 0.6);
    border: 2px solid rgba(139, 0, 0, 0.4);
    color: #f5f5dc;
    font-family: 'Lora', serif;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5);
}

input:focus, select:focus {
    border-color: #dc143c;
    background: rgba(15, 15, 15, 0.8);
    box-shadow: 
        inset 0 2px 8px rgba(0, 0, 0, 0.7),
        0 0 15px rgba(220, 20, 60, 0.4);
}

button {
    background: linear-gradient(135deg, #8b0000 0%, #4a0000 100%);
    color: #f5f5dc;
    border: 2px solid rgba(220, 20, 60, 0.4);
    font-family: 'Cinzel', serif;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 
        0 4px 15px rgba(139, 0, 0, 0.5),
        0 0 20px rgba(139, 0, 0, 0.3);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

button:hover {
    background: linear-gradient(135deg, #a00000 0%, #5a0000 100%);
    transform: translateY(-2px);
    box-shadow: 
        0 6px 20px rgba(139, 0, 0, 0.7),
        0 0 30px rgba(255, 0, 0, 0.4);
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

.player-item {
    background: rgba(45, 27, 61, 0.3);
    border: 1px solid rgba(139, 0, 0, 0.2);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    backdrop-filter: blur(5px);
    box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.3);
}

.player-name {
    color: #f5f5dc;
    font-weight: 600;
}

.player-role {
    color: #dc143c;
}

.player-ability {
    color: #c0c0c0;
}

.night-item {
    background: rgba(45, 27, 61, 0.3);
    border: 1px solid rgba(139, 0, 0, 0.2);
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    backdrop-filter: blur(3px);
}

.night-order-number {
    background: linear-gradient(135deg, #8b0000 0%, #4a0000 100%);
    color: #f5f5dc;
    border: 1px solid rgba(220, 20, 60, 0.4);
    box-shadow: 0 2px 8px rgba(139, 0, 0, 0.5);
}

.night-character-name {
    color: #d4af37;
}

.night-ability {
    color: #c0c0c0;
}

.alert {
    background: rgba(25, 118, 210, 0.2);
    border: 1px solid rgba(25, 118, 210, 0.4);
    color: #64b5f6;
    backdrop-filter: blur(5px);
}

.copy-btn {
    background: linear-gradient(135deg, #1b5e20 0%, #0d2f10 100%);
    border: 2px solid rgba(76, 175, 80, 0.4);
}

.copy-btn:hover {
    background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
}

.characters-preview {
    background: rgba(45, 27, 61, 0.3);
    border: 1px solid rgba(139, 0, 0, 0.3);
    backdrop-filter: blur(5px);
}

.character-item {
    background: rgba(15, 15, 15, 0.6);
    border: 1px solid rgba(139, 0, 0, 0.2);
    color: #c0c0c0;
}

.loading {
    color: #dc143c;
    text-shadow: 0 0 10px rgba(220, 20, 60, 0.5);
}
```

---

## 🎬 Zusätzliche Verbesserungen

### 1. **Animationen für mehr Atmosphäre**

```css
/* Flackernde Kerze Animation für Überschriften */
@keyframes candleFlicker {
    0%, 100% { 
        opacity: 1;
        text-shadow: 
            0 0 20px rgba(220, 20, 60, 0.8),
            0 0 40px rgba(139, 0, 0, 0.5);
    }
    50% { 
        opacity: 0.95;
        text-shadow: 
            0 0 15px rgba(220, 20, 60, 0.6),
            0 0 30px rgba(139, 0, 0, 0.3);
    }
}

h1, h2 {
    animation: candleFlicker 3s ease-in-out infinite;
}

/* Subtile Blut-Tropfen Animation */
@keyframes bloodDrip {
    0% {
        transform: translateY(0);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    100% {
        transform: translateY(20px);
        opacity: 0;
    }
}

/* Geister-Nebel Effekt */
@keyframes ghostlyMist {
    0%, 100% {
        opacity: 0.3;
        transform: translateX(-10px);
    }
    50% {
        opacity: 0.5;
        transform: translateX(10px);
    }
}
```

### 2. **Cursor Änderung für Horror-Feeling**

```css
body {
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"><text y="24" font-size="24">🕯️</text></svg>'), auto;
}

button, a, input, select {
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"><text y="24" font-size="24">☠️</text></svg>'), pointer;
}
```

### 3. **Partikel-Effekt (Optional - JavaScript)**

```javascript
// Blut-Tropfen oder Schnee-/Asche-Partikel
function createParticles() {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
    document.body.appendChild(particle);
    
    setTimeout(() => particle.remove(), 5000);
}

setInterval(createParticles, 300);
```

```css
.particle {
    position: fixed;
    top: -10px;
    width: 3px;
    height: 10px;
    background: #8b0000;
    border-radius: 50%;
    animation: bloodDrip 3s linear forwards;
    pointer-events: none;
    z-index: 9999;
    box-shadow: 0 0 5px rgba(139, 0, 0, 0.8);
}
```

---

## 📱 Responsive Design

Alle Änderungen müssen Mobile-freundlich bleiben:

```css
@media (max-width: 768px) {
    body {
        /* Einfacheres Overlay auf Mobile */
        background: 
            linear-gradient(to bottom, rgba(15, 15, 15, 0.8), rgba(45, 27, 61, 0.7)),
            url('/static/images/blood_on_the_clocktower.webp') center/cover no-repeat fixed;
    }
    
    .container, .card {
        padding: 25px 20px;
        backdrop-filter: blur(8px);
    }
    
    h1 {
        font-size: 1.8em;
    }
    
    /* Reduzierte Animationen für Performance */
    * {
        animation: none !important;
    }
}
```

---

## ✅ Implementierungs-Checkliste

### Phase 1: Basis-Styling
- [ ] Google Fonts importieren (Cinzel, Crimson Text, Lora)
- [ ] CSS-Variablen für Farbpalette definieren
- [ ] Body Hintergrundbild für alle Seiten setzen
- [ ] Container Transparenz implementieren

### Phase 2: Typografie
- [ ] Überschriften mit Gothic-Fonts stylen
- [ ] Text-Schatten für bessere Lesbarkeit
- [ ] Labels und Buttons anpassen

### Phase 3: Formular-Elemente
- [ ] Inputs transparent mit dunklem Hintergrund
- [ ] Buttons im Horror-Stil mit Glowing-Effekt
- [ ] Select-Dropdowns anpassen
- [ ] Placeholder-Farben ändern

### Phase 4: Komponenten
- [ ] Game-Info Boxen transparent
- [ ] Player-Lists dunkel gestalten
- [ ] Role-Cards anpassen
- [ ] Night-Order Listen stylen

### Phase 5: Feinschliff
- [ ] Animationen hinzufügen (optional)
- [ ] Hover-Effekte optimieren
- [ ] Mobile Responsive testen
- [ ] Browser-Kompatibilität prüfen

### Phase 6: Testing
- [ ] index.html in Browser testen
- [ ] join.html in Browser testen
- [ ] player.html in Browser testen
- [ ] storyteller.html in Browser testen
- [ ] Mobile Ansicht testen
- [ ] Lesbarkeit auf allen Seiten prüfen
- [ ] Hintergrundbild Sichtbarkeit verifizieren

---

## 🎯 Erwartetes Ergebnis

Nach der Implementierung sollte:
1. ✅ Das Hintergrundbild auf **allen** Seiten sichtbar sein
2. ✅ Alle Container halbtransparent sein mit Glasmorphism-Effekt
3. ✅ Horror-Atmosphäre durch dunkle Farben und Gothic-Fonts
4. ✅ Text trotz Transparenz gut lesbar (durch Schatten/Kontrast)
5. ✅ Konsistentes Design über alle 4 Seiten
6. ✅ Responsive und benutzerfreundlich
7. ✅ Passend zum Spiel-Thema "Blood on the Clocktower"

---

## 🚀 Nächste Schritte

1. **Backup erstellen:**
   ```bash
   # Kopiere static/ Ordner als Backup
   cp -r static/ static_backup/
   ```

2. **Implementierung starten:**
   - Beginne mit `index.html`
   - Teste nach jeder Datei
   - Nutze Browser DevTools für Live-Anpassungen

3. **Iteratives Vorgehen:**
   - Erst Basis-Styling
   - Dann Feinschliff
   - Zuletzt Animationen

4. **Dokumentation:**
   - Screenshots vor/nach erstellen
   - Changelog aktualisieren
   - Benutzer-Feedback einholen

---

## 📚 Referenzen

### Inspiration:
- Victorian Gothic Design
- Bloodborne UI
- Darkest Dungeon Aesthetic
- Penny Dreadful TV Series

### Technisch:
- [Glassmorphism CSS](https://css.glass/)
- [Google Fonts - Cinzel](https://fonts.google.com/specimen/Cinzel)
- [MDN - backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter)

---

**Viel Erfolg bei der Implementierung! 🩸**

*Remember: Das Hintergrundbild muss IMMER sichtbar bleiben - das ist die Hauptanforderung!*

