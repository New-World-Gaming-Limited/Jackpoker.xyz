# JackPoker Design Research Notes
## Date: March 28, 2026

---

## LOGO

### SVG Logo (Full Horizontal Version)
- **File**: `jackpoker-logo.svg` (downloaded from WorldPokerDeals CMS)
- **Source URL**: `https://cms.worldpokerdeals.com/assets/3bade674-e683-46ce-841a-f5d41182422c`
- **Dimensions**: 189 × 47px viewBox
- **Format**: SVG (vector, scalable)

### Logo Structure
The logo consists of two parts:
1. **Left Icon** — A stylized abstract icon made of rounded rectangles/pill shapes arranged to form a "J" or card-like symbol. It uses a gradient fill.
2. **Right Text** — "JackPoker" rendered as outlined paths (not live text) in white (#FFFFFF).

### Logo Colors
- **Icon gradient**: Linear gradient from `#8032FF` (purple) → `#FF3D00` (orange-red)
  - Gradient direction: left to right (horizontal)
  - CSS: `linear-gradient(90deg, #8032FF 0%, #FF3D00 100%)`
- **Text color**: Pure white `#FFFFFF`
- **Background**: Transparent (designed for dark backgrounds)

### Official PNG Logo (180×180 favicon/icon)
- **File**: `jackpoker-logo-official.png`  
- **Source**: `https://jack-poker.com/cms-assets/d2a61399-3831-46b0-b46d-7321f5733dbe/`
- This is the square icon version (just the "J" spade icon, no text)

---

## TYPOGRAPHY / FONTS

From the CSS custom properties in jack-poker.com source:
```css
--fontFamily-main: "Main", sans-serif;
--fontFamily-additional: "Additional", sans-serif;
--fontFamily-accent: "Accent", sans-serif;
```

The fonts are custom-named (likely custom licensed fonts loaded via @font-face). Based on the SVG logo, the text uses:
- **Bold/Heavy weight** sans-serif
- The letterforms in the SVG are paths (not live text), indicating a custom/proprietary typeface
- Font weights available: 100 (light), 400 (normal), 600 (semibold), 700 (bold), 900 (superbold)

---

## DESIGN SYSTEM COLORS

From `jack-poker.com` CSS variables:

### Brand Colors
- Background primary: `#000000` (pure black)
- Background secondary: `#171717` (near-black)
- Background tertiary: `#19171F` (dark purple-black)

### Accent Gradients
- **Primary gradient** (left→right): `linear-gradient(270deg, #F4AD23 0%, #FF3D00 50%, #6A2DC0 100%)` — gold to orange-red to purple
- **Primary gradient** (diagonal): `linear-gradient(135deg, #FBBD13 0%, #FF3E1C 50%, #6A2DC0 100%)`
- **Rainbow/prismatic gradient**: `linear-gradient(90deg, #FFC169 0%, #FFFAEA 25%, #FBA2C6 42%, #F057A2 55%, #985BE7 70%, #60ABED 85%, #50E6C1 100%)`

### Surface Colors
- Primary purple: `#893BF7`
- Primary purple dark: `#401A75`
- Primary gradient: `linear-gradient(90deg, #6A2DC0 0%, #FF3D00 100%)`

### Text Colors
- Primary: `#FFFFFF`
- Muted: `rgba(255,255,255,0.7)`
- Secondary: `rgba(255,255,255,0.5)`
- Accent/gold: `#F6BA46`
- Accent hovered: `#F9D48C`
- Selection: `#C49BFC` (light purple)
- Hover effect: `#A66BFA`

### Status Colors
- Destructive/error: `#DD4952`
- Success: `#66C95B`

### VIP Gradient
- `linear-gradient(270deg, #AE6E1D 0%, #FFDA8A 62.74%, #C8842E 100%)` — gold/bronze

---

## NAVIGATION BAR

From the jack-poker.com source code analysis:
- **Background**: Dark (background-secondary: `#171717`), with `backdrop-filter: blur(24px)` for glassmorphism effect
- **Supported languages**: en, es, fi, hu, it, pl, pt, ru (8 languages)
- **Logo position**: Left side
- **CTA button**: Gradient button (purple to orange-red)
- Navigation items use `transition-colors` with cubic-bezier(0.4, 0, 0.2, 1) timing

---

## FOOTER DESIGN

From the HTML source, the site uses a React/Remix framework with:
- Dark background (`#000000` or `#171717`)
- Multiple sections (Terms, Privacy Policy, responsible gambling)
- Licensed under Anjou Gaming regulations (Comoros license)
- GTM ID: KWXWXJCN

---

## MICRO-INTERACTIONS & DESIGN ELEMENTS

From CSS analysis:
1. **Hover effects**: Text color transitions from white to `#A66BFA` (purple) on hover
2. **Button gradients**: Primary CTA buttons use animated gradient (purple to red-orange, reverses on hover)
3. **Glassmorphism**: Navigation uses `backdrop-filter: blur(24px)` + semi-transparent backgrounds
4. **Transitions**: `transition-colors` with 150ms duration, cubic-bezier(0.4, 0, 0.2, 1) easing
5. **Drop shadows**: Glow effects using `drop-shadow(0px 0px 6px var(--colors-text-accent-default))` — golden glow
6. **Card skew**: `.skew-x-[-16deg]` and `.skew-x-[16deg]` used for italicized card/banner elements
7. **Focus ring**: Purple focus ring `#c8a0f0` (light purple)
8. **Gradient text**: Using `bg-clip-text` + `text-transparent` technique for gradient text

---

## TECHNOLOGY STACK
- Frontend: React/Remix (SSR)
- CSS: Tailwind CSS (utility-first)
- CMS: Directus
- Analytics: Google Tag Manager (GTM-KWXWXJCN)
- Metrics: Custom collector at `collector-proxy.jack-flush.com`
- License: Anjou Gaming (Comoros)

---

## ASSETS SAVED
1. `/home/user/workspace/jackpoker-fan-site/assets/images/jackpoker-logo.svg` — Full horizontal SVG logo (189×47px viewbox)
2. `/home/user/workspace/jackpoker-fan-site/assets/images/jackpoker-logo.png` — Same SVG saved as PNG extension
3. `/home/user/workspace/jackpoker-fan-site/assets/images/jackpoker-logo-official.png` — Official 180×180 PNG icon from jack-poker.com CMS
4. `/home/user/workspace/jackpoker-fan-site/assets/images/jackpoker-worldpokerdeals-screenshot.jpg` — Screenshot showing logo in context
