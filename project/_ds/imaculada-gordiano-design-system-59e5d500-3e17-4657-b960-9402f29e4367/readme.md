# Imaculada Gordiano — Sociedade de Advogados · Design System

A design system for **Imaculada Gordiano Sociedade de Advogados**, a Brazilian law
firm. The brand is built around a heraldic wine-and-gold crest and reads as
**formal, traditional, and serious** — appropriate to the legal world — while the
working software (a legal practice-management dashboard) stays **light, calm, and
easy to read** on a warm off-white canvas.

> Language: the product and brand copy are in **Brazilian Portuguese (pt-BR)**.

## Sources provided
- `uploads/IGSA.jfif` — the firm's primary logo (200×200 raster). Copied to
  `assets/logo-crest.jpg`; the crest was cropped to `assets/crest.png` for use as an
  app mark / avatar.
- A written brand-palette brief (wine/burgundy gradient banner, near off-white beige
  page, white cards, soft gold accents, vivid-green status dots, rose-red card icons).

No codebase, Figma file, or font binaries were provided. The component and UI-kit
recreations below are built from the brand brief and the dashboard described in it
(panels for *Publicações*, *Prazos Preclusivos*, *Pauta de Audiências*, plus a gold
*CONTROLADORIA* action). Treat them as a faithful first interpretation to refine
against the real product.

---

## CONTENT FUNDAMENTALS

**Language & voice.** Brazilian Portuguese, formal register (3rd person / impersonal,
not the casual *você* tone you'd find in consumer apps). The voice is institutional and
reassuring: precise, restrained, never playful. Think of how a tradicional banca de
advocacia addresses its clients — *"Prezado cliente"*, not *"E aí!"*.

**Casing.**
- Brand marks and section titles use **ALL CAPS with generous letter-spacing**
  (Cinzel): `IMACULADA GORDIANO`, `SOCIEDADE DE ADVOGADOS`, `CONTROLADORIA`.
- Category / kicker labels are **UPPERCASE, small, gold**, joined by a middle dot:
  `AUTOMAÇÃO · DIÁRIO`, `PRAZOS · CONTROLE`, `AUDIÊNCIAS · AGENDA`.
- UI labels, body, table content use **sentence case**: *"Painel de Publicações"*,
  *"Prazo preclusivo"*, *"Próxima audiência"*.

**Terminology (use the firm's words).** Publicações, Intimações, Prazos preclusivos,
Pauta de audiências, Processo (nº), Vara, Comarca, Controladoria, Diário oficial,
Andamentos, Petição, Prazo fatal.

**Numbers.** Brazilian formatting — dates `dd/mm/aaaa`, currency `R$ 1.250,00`,
decimal comma. Process numbers use the CNJ mask in **mono**:
`0001234-56.2025.8.26.0100`.

**Tone examples**
- Empty state: *"Nenhuma publicação nova hoje. Você está em dia."*
- Deadline warning: *"Prazo preclusivo vence em 2 dias."*
- Action confirmation: *"Andamento registrado com sucesso."*

**Emoji:** never. Status and emphasis are carried by the green status dot, gold
category labels, and wine iconography — not by emoji.

---

## VISUAL FOUNDATIONS

**Overall impression.** Wine/burgundy + gold = formality, tradition, gravitas. Warm
neutrals (beige + white) keep the layout light and legible; small green accents signal
status/activity discreetly. Nothing is loud; the gold is *soft*, the green is *small*.

**Color.**
- **Primary** is wine/burgundy `--wine-600 #7E1F2C`. The signature banner is a
  left-to-right **gradient** from a deeper wine to a lighter red (`--gradient-wine`,
  `--wine-700 → --wine-600 → --wine-500`).
- **Accent** is a muted, soft **gold** `--gold-400 #CDA736` — used for the primary
  *CONTROLADORIA*-style action and for category kickers (as the darker `--gold-600`
  on light surfaces for contrast). Gold is an accent, never a flood.
- **Status green** `--green-500 #2E9E5B` appears only as small dots / pills indicating
  activity, never as large fills.
- **Rose-red** (`--rose-300/400`) is the wine family diluted — used for card icon
  glyphs and the occasional hairline inside cards.
- **Neutrals** are warm: page is off-white beige `--sand-100 #F7F2E9`; cards are pure
  white; text is a warm near-black `--ink-900 #2A2420`. Avoid cool grays.

**Type.** Cinzel (Trajan-like caps) for the brandmark and section marks; Cormorant
Garamond for editorial/large headings and pull-quotes; Libre Franklin for all UI and
body; IBM Plex Mono for process numbers and codes. Display caps carry wide tracking
(`--ls-caps 0.18em`); body stays at normal tracking with relaxed line-height for
documents.

**Backgrounds.** Flat warm off-white; **no** photographic hero washes inside the app.
The one expressive surface is the **wine gradient banner** at the top of the app and on
slide title/section frames. No repeating textures, no noise, no glassmorphism in the
product. Marketing/slides may use a subtle gold hairline frame or a faint crest
watermark at very low opacity.

**Cards.** White fill, `--radius-lg (12px)` corners, **1px warm border**
(`--border-soft`), soft warm-tinted `--shadow-sm`. They sit on the beige page so the
border + shadow does the separating. A card often carries: a gold category kicker, a
title, a small **green status dot in the top-right**, and a rose-red leading icon.
Restrained corners — this is a formal brand, not a rounded consumer app.

**Borders & lines.** Hairlines are warm sand (`--border-soft #E5DAC7`), never pure
gray. Inside wine surfaces, dividers are gold at low opacity.

**Shadows.** Soft, low-spread, and **warm-tinted** (shadows use a wine-brown rgba, not
neutral black) so elevation feels of-a-piece with the palette. Wine buttons get a
colored `--shadow-wine` lift.

**Radii.** Small and conservative: inputs/buttons `--radius-sm/md (5–8px)`, cards
`--radius-lg (12px)`, pills only for tags/status. Never fully-rounded large surfaces.

**Motion.** Subtle and professional. 120–320ms, `--ease-standard` for most,
`--ease-out` for entrances. Fades and small (4–8px) rises — **no** bounces, no springy
overshoot. Respect `prefers-reduced-motion`.

**Hover / press.**
- Buttons: hover **darkens** the fill (wine→wine-700; gold→gold-500); press darkens
  further and removes the lift. No scale-up on hover.
- Cards/list rows: hover raises shadow one step and warms the background a touch
  (`--sand-50`). Press: settle back down.
- Links: wine text, underline on hover.
- Focus: a soft **gold** focus ring (`--ring`) — accessible and on-brand.

**Transparency / blur.** Used sparingly — only for modal scrims (wine-tinted, ~45%
opacity) and the optional crest watermark. No frosted-glass panels in the product UI.

**Imagery vibe.** When photography is used (marketing, partner portraits), keep it
**warm-toned and restrained** — natural light, muted saturation, no heavy filters.
The product itself is illustration-free apart from the crest.

---

## ICONOGRAPHY

The brand had no bundled icon set, so the system standardizes on **Lucide** (loaded
from CDN) — clean, consistent 1.5px-stroke line icons that read as professional and
neutral, complementing (not competing with) the ornate crest.

- **Style:** stroke (outline) icons, `stroke-width: 1.5`, `24px` default box, rounded
  joins. Use `--wine-600` for primary/leading icons, `--ink-500` for neutral UI icons,
  `--gold-600` sparingly for accent.
- **In cards:** the leading glyph is rendered in **rose-red** inside a soft `--rose-soft`
  rounded square (the "ícones em vermelho claro" described in the brief).
- **CDN:** `https://unpkg.com/lucide@latest` (or `lucide-static` SVGs). **Substitution
  flagged** — swap to the firm's real icon set if one exists.
- **The crest** (`assets/crest.png` / `assets/logo-crest.jpg`) is the one ornamental
  mark: app favicon, sidebar header, slide corners, avatars. Do not redraw it.
- **No emoji. No unicode-glyph icons.** A few middle dots (`·`) join category labels;
  that is the only "glyph as decoration" allowed.

---

## INDEX / MANIFEST

**Root**
- `styles.css` — global entry (import this). `@import` lines only.
- `readme.md` — this guide.
- `SKILL.md` — Agent-Skill front-matter wrapper.

**Tokens** (`tokens/`)
- `fonts.css` — Google Fonts @import (Cinzel, Cormorant Garamond, Libre Franklin, IBM Plex Mono).
- `colors.css` — wine, rose, gold, green ramps + warm neutrals + semantic aliases.
- `typography.css` — families, weights, scale, tracking.
- `spacing.css` — spacing grid, radii, shadows, motion, layout.

**Assets** (`assets/`)
- `logo-crest.jpg` — full logo (crest + wordmark).
- `crest.png` — cropped crest mark.

**Foundations** — specimen cards in `guidelines/` (Design System tab: Type, Colors, Spacing, Brand).

**Components** (`components/`)
- `core/` — Button, IconButton, Card, Avatar (+ `core.card.html`).
- `forms/` — Input, Select (+ `forms.card.html`).
- `display/` — Badge, StatusDot, Tag, Tabs (+ `display.card.html`).
- `feedback/` — Toast (+ `feedback.card.html`).

Each component ships `<Name>.jsx` + `<Name>.d.ts` (props) + `<Name>.prompt.md` (usage).

**UI kit** (`ui_kits/dashboard/`) — the legal practice-management dashboard
recreation: `index.html` (interactive), `Header.jsx`, `Panels.jsx`, `README.md`.

**Slides** — not created: no deck template was provided. Attach a sample deck to add branded slide masters.

---

### Caveats
- Logo supplied at 200×200 raster only; the cropped crest carries a faint off-white
  background. A vector / transparent-PNG logo would sharpen every surface.
- Fonts are **substitutions** (Cinzel for the Trajan-style wordmark). Provide real
  brand fonts to finalize.
- Icons use **Lucide** as a stand-in for any real icon set.
