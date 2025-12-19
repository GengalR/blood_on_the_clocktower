# Feature Request: Quick Rules Guide for Players

## 📋 User Story

**As a player**, I want to access a quick rules summary with a button in my browser,  
**so that** I can quickly review the basic game rules without reading the full rulebook.

## 🎯 Objective

Implement a "Quick Rules" button that shows a simplified 4-rule summary of Blood on the Clocktower gameplay. The summary should be accessible from the player view and provide essential information for beginners.

## 📖 Content Source

Based on: https://wiki.bloodontheclocktower.com/Rules_Explanation

The rules should be condensed into 4 core rules that cover:
1. **Win Conditions** - How each team wins
2. **Day Phase** - What happens during the day (discussion, nomination, execution)
3. **Night Phase** - What happens at night (eyes closed, abilities, Demon kills)
4. **Death & Voting** - What dead players can do (still talk, one vote left)

## 🎨 Suggested UI/UX

### Button Placement
- **Player View** (`player.html`): Top-right corner with icon (❓ or 📜)
- **Storyteller View** (`storyteller.html`): Optional, but can be included
- **Join View** (`join.html`): Optional, for new players

### Modal/Overlay Design
```
┌─────────────────────────────────────────┐
│  ❌ Blood on the Clocktower - Quick Rules │
├─────────────────────────────────────────┤
│                                         │
│  1️⃣ **Win Conditions**                  │
│  • Good wins if Demon dies              │
│  • Evil wins if only 2 players alive    │
│                                         │
│  2️⃣ **Day Phase**                        │
│  • Discuss and share information        │
│  • Nominate and vote to execute         │
│  • Only 1 execution per day             │
│                                         │
│  3️⃣ **Night Phase**                      │
│  • All close eyes                       │
│  • Characters wake to use abilities     │
│  • Demon kills a player                 │
│                                         │
│  4️⃣ **Death & Voting**                   │
│  • Dead players can still talk          │
│  • Dead have only 1 vote left           │
│  • Dead players can still win           │
│                                         │
│            [ Close ]                     │
└─────────────────────────────────────────┘
```

### Alternative: Dedicated Page
Could also be a separate `/rules.html` page that opens in a new tab.

## ✅ Acceptance Criteria

### Functional Requirements
- [ ] "Quick Rules" button is visible on player view
- [ ] Button opens modal/overlay with 4-rule summary
- [ ] Rules are clearly formatted and easy to read
- [ ] Modal can be closed (X button, ESC key, click outside)
- [ ] Mobile-responsive design
- [ ] Rules are in German (project language)

### Non-Functional Requirements
- [ ] Modal loads instantly (no API call needed)
- [ ] Clean, readable typography
- [ ] Accessible (keyboard navigation, screen reader friendly)
- [ ] No JavaScript errors
- [ ] Cross-browser compatible

## 🔧 Technical Considerations

### Implementation Options

#### Option A: Pure Frontend (Recommended)
- **Files:** `static/player.html`, `static/css/rules-modal.css`
- **Pros:** 
  - ✅ No backend needed
  - ✅ Instant loading
  - ✅ Easy to implement
- **Cons:**
  - ⚠️ Rules hardcoded in HTML (changes require file edit)

#### Option B: Backend API
- **Files:** `main.py`, `static/player.html`, `data/rules.json`
- **Pros:**
  - ✅ Rules easily updatable via JSON
  - ✅ Could support multiple languages
- **Cons:**
  - ⚠️ Additional API endpoint needed
  - ⚠️ Slower (HTTP request)

#### Option C: Markdown File
- **Files:** `data/quick_rules.md`, parser in JavaScript
- **Pros:**
  - ✅ Easy to edit
  - ✅ Version control friendly
- **Cons:**
  - ⚠️ Requires markdown parser
  - ⚠️ Slightly more complex

**Recommendation:** Start with **Option A** (Pure Frontend) for MVP.

### German Rules Text (Draft)

```markdown
# Blood on the Clocktower - Schnellregeln

## 1️⃣ Siegbedingungen
• **Gut gewinnt**, wenn der Demon stirbt
• **Böse gewinnt**, wenn nur noch 2 Spieler leben (Travellers zählen nicht)

## 2️⃣ Tag-Phase
• **Diskutieren:** Alle sprechen offen oder privat
• **Nominieren:** Spieler nominieren verdächtige Personen
• **Hinrichtung:** Bei 50%+ Stimmen wird nominierter Spieler hingerichtet
• Nur **1 Hinrichtung pro Tag** möglich

## 3️⃣ Nacht-Phase
• **Augen schließen:** Alle Spieler haben Augen zu
• **Fähigkeiten:** Storyteller weckt Charaktere einzeln
• **Demon tötet:** Demon wählt ein Opfer
• **Morgen:** Storyteller verkündet, wer gestorben ist

## 4️⃣ Tod & Abstimmen
• **Sprechen erlaubt:** Tote Spieler dürfen weiter reden
• **1 Stimme übrig:** Tote haben nur noch 1 Stimme fürs ganze Spiel
• **Team-Sieg:** Tote gewinnen/verlieren mit ihrem Team
```

## 📐 Suggested Implementation Plan

### Phase 1: HTML Structure (30min)
- Add button to `player.html`
- Create modal HTML structure
- Semantic HTML with proper ARIA labels

### Phase 2: Styling (45min)
- CSS for button (position, colors, hover effects)
- CSS for modal (overlay, animation, responsive)
- Typography for readability

### Phase 3: JavaScript Interaction (30min)
- Open/close modal functionality
- ESC key handler
- Click-outside-to-close handler

### Phase 4: Content (15min)
- Write final German rules text
- Format with icons/emojis
- Proofread for clarity

### Phase 5: Testing (30min)
- Test on different browsers
- Test on mobile devices
- Test keyboard accessibility
- Test with screen reader

### Phase 6: Optional Enhancements (if time permits)
- Add to `storyteller.html` and `join.html`
- Add "Print" button for rules
- Add link to full rulebook

**Total Estimated Time:** 2.5 hours

## 🚀 Priority

**Priority:** P2 (Medium)
- **Impact:** Medium (helpful for new players, reduces Storyteller interruptions)
- **Effort:** Low (2.5h)
- **Dependencies:** None

## 📊 Success Metrics

- [ ] Players use Quick Rules button (track with GA if available)
- [ ] Fewer rule questions during game
- [ ] Positive player feedback
- [ ] No reported bugs within first week

## 🔗 Related Features

### Depends On:
- ✅ Player View exists (`player.html`)

### Blocks:
- None (standalone feature)

### Future Enhancements:
- 💡 Extended Rules page with character abilities
- 💡 Interactive tutorial/walkthrough
- 💡 Video tutorial integration
- 💡 Multi-language support (EN, DE)

## 📝 Additional Notes

### Design Inspiration:
- Keep it simple and scannable
- Use emoji/icons for visual hierarchy
- Mobile-first approach
- Dark mode support (if project theme supports it)

### Accessibility:
- Button must have clear label/aria-label
- Modal must trap focus when open
- ESC key must close modal
- Announce modal opening to screen readers

### Content Guidelines:
- Use simple, clear language
- Avoid jargon
- One sentence per rule point
- Bold key terms

## 🎯 Definition of Done

- [ ] Quick Rules button implemented on player view
- [ ] Modal opens/closes correctly
- [ ] 4 rules clearly displayed in German
- [ ] Mobile responsive
- [ ] No console errors
- [ ] Keyboard accessible (TAB, ESC, ENTER)
- [ ] Cross-browser tested (Chrome, Firefox, Safari, Edge)
- [ ] Code reviewed
- [ ] Merged to main branch

---

**Created:** 2025-01-19  
**Requested By:** User  
**Assigned To:** Feature Planner → Copilot Implementation  
**Status:** 📋 Ready for Planning

