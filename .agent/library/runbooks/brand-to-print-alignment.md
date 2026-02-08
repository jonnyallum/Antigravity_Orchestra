# Runbook: Brand-to-Print Menu Alignment

> **Source:** Parallel Learning Run #001 (Winner: @Conductor)
> **Use Case:** Updating print materials to match website brand identity
> **Estimated Time:** 15-20 minutes

---

## 📋 Prerequisites

Before starting, ensure you have:
- [ ] Access to the website's `tailwind.config.js` (color definitions)
- [ ] Access to the website's `index.css` (typography and effects)
- [ ] Logo file location identified
- [ ] Current menu content verified (prices, items)

---

## 🔄 Workflow

### Step 1: Extract Brand Colors (2 min)

1. Open `tailwind.config.js`
2. Document the color palette:

```javascript
// Look for these in the theme.extend.colors section
colors: {
    cream: '#F5F1E8',        // Primary text
    gold/olive: {
        300: '#C8D395',       // Primary accent (or similar)
    },
    dark: {
        900: '#0D0D0C',       // Background dark
        800: '#1A1918',       // Background mid
    }
}
```

3. Note any custom gradients in `index.css`

### Step 2: Extract Typography (1 min)

1. Check the Google Fonts import in `index.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Manrope:wght@400;500;600;700&display=swap');
```

2. Map fonts to usage:
   - **Display (headers):** First font family
   - **Body (content):** Second font family

### Step 3: Locate Logo (1 min)

```bash
# Search for logo files
find . -name "logo*" -type f
```

Common locations:
- `/public/images/logo.png`
- `/images/logo.png`
- `/assets/logo.svg`

### Step 4: Update Print Menu HTML (10 min)

#### 4.1 Update Color Variables

Replace all color values with extracted brand colors:

```css
/* BEFORE (generic) */
color: #d4af37;
background: #1a1a1a;

/* AFTER (brand-matched) */
color: #C8D395;          /* Olive accent */
background: #0D0D0C;     /* Brand black */
```

#### 4.2 Update Typography

```css
/* BEFORE */
font-family: 'Inter', sans-serif;

/* AFTER */
font-family: 'Manrope', sans-serif;  /* Body */
font-family: 'Cormorant Garamond', serif;  /* Display */
```

#### 4.3 Add Logo

```html
<div class="logo-container">
    <img src="../source_code/public/images/logo.png" 
         alt="Logo" 
         class="logo"
         onerror="this.style.display='none'">
</div>
```

#### 4.4 Match Visual Effects

Apply website-style effects:

```css
/* Radial glow (from website) */
background: 
    radial-gradient(at 20% 10%, rgba(200, 211, 149, 0.04) 0px, transparent 50%),
    radial-gradient(at 80% 80%, rgba(200, 211, 149, 0.03) 0px, transparent 50%);

/* Card style */
background: linear-gradient(to bottom right, rgba(26, 25, 24, 0.9), rgba(13, 13, 12, 0.9));
border: 1px solid rgba(200, 211, 149, 0.15);
border-radius: 12px;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);

/* Featured item highlight */
background: linear-gradient(135deg, rgba(200, 211, 149, 0.08) 0%, rgba(200, 211, 149, 0.02) 100%);
border: 1.5px solid rgba(200, 211, 149, 0.25);
```

### Step 5: Create Brand Guide (3 min)

Document the system for future reference:

```markdown
# Brand Guide

## Colors
| Name | Hex | Usage |
|:-----|:----|:------|
| Accent | #C8D395 | Headlines, prices |
| Background | #0D0D0C | Page background |
| Text | #F5F1E8 | Body copy |

## Fonts
- Display: Cormorant Garamond
- Body: Manrope

## Effects
- Card shadows: 0 8px 32px rgba(0,0,0,0.4)
- Accent borders: rgba(200, 211, 149, 0.25)
```

### Step 6: Verify & Test (2 min)

1. Open menu HTML files in browser
2. Compare side-by-side with website
3. Check:
   - [ ] Colors match exactly
   - [ ] Fonts rendering correctly
   - [ ] Logo displays (or gracefully fails)
   - [ ] Print preview looks correct (Ctrl+P)

---

## ⚠️ Common Pitfalls

| Issue | Solution |
|:------|:---------|
| Logo 404 error | Add onerror fallback handler |
| Colors look different | Ensure RGB values, not named colors |
| Fonts not loading | Check Google Fonts URL in head |
| Print colors washed out | Enable "Background graphics" in print dialog |
| Card borders invisible | Use rgba with higher alpha value |

---

## 📁 File Locations

| Asset | Typical Path |
|:------|:-------------|
| Tailwind Config | `tailwind.config.js` |
| CSS Styles | `src/index.css` |
| Logo | `/public/images/logo.png` |
| Print Menu | `menu-print/menu-front.html` |

---

## ✅ Checklist

Before marking complete:

- [ ] All colors match website palette
- [ ] Fonts match website typography
- [ ] Logo integrated with fallback
- [ ] Visual effects (shadows, glows) applied
- [ ] Brand guide documented
- [ ] Print preview verified
- [ ] Files saved in correct location

---

## 📊 Success Metrics

| Metric | Target |
|:-------|:-------|
| Color match | 100% hex accuracy |
| Font match | Correct families and weights |
| Time to complete | < 20 minutes |
| Print quality | Professional, readable |

---

*Runbook created from PLR-001 winning approach*
*Author: @Conductor | Date: 2026-02-08*
