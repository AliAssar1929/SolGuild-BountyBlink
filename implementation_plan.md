# Implementation Plan: Dribbble-Inspired High-End Landing Page & Bento Workflow

*Date: October 5, 2026 | Focus: Exact Dribbble Reference Layout (`dit.io`), Clean Component Mockups, Bento Workflow, Custom Sun+Shield SVG Logo*  
*Roles: Frontend Developer & UI Architect*

---

## 1. Executive Summary & Aesthetic Direction

### 1.1 The User's Requirement
- Replace the current landing page (which looked dark, heavy, and "vibecoded") with a clean, high-end design directly inspired by the 2nd attached reference image (the Dribbble SaaS shot for `dit.io`).
- **Exact Layout Mapping from Reference Image**:
  1. **Navbar**: Rounded logo with custom SVG + clean links + ghost button + prominent pill CTA button.
  2. **Hero**: Exact 2-column split:
     - Left: Large editorial typography with colored accent word highlight, clean subtext, dual pill buttons, subtle vector connector doodles.
     - Right: Layered floating white UI card mockup (profile avatar, active bounty card, circular progress meter, floating tags) — **no big external photos or clunky SVGs**, built with lightweight Vue components matching the webapp tokens.
  3. **Social / Hub Proof Strip**: European capital cities and protocol partners (`Berlin`, `London`, `Paris`, `Madrid`, `Rome`, `Amsterdam`, `Solana Devnet`, `Gemini AI`).
  4. **Features Section**: "The Guild Contracts we arbitrate" container with 3 cards (Civil Help, Sensitive Intel, Commercial UGC) matching the 3-tile block in the reference image.
  5. **About / Numbers Section**: "Okay, Let's see SolGuild in numbers" with 4 stats on left and verification preview card on right.
  6. **Workflow Section**: **Replace the reference review section with a Bento Grid of the 4-step workflow** (Post & Lock &rarr; 10-Min Claim &rarr; Multimodal Arbiter &rarr; Zero-Drain Settlement & XP).
  7. **Big MVP Notice**: Prominent explanation that anti-AI image detection is intentionally disabled for hackathon testing.
  8. **CTA Section**: Soft-tinted card with headline, subtext, dual pill buttons, and subtle SVG element.
  9. **Footer**: Clean, balanced minimalist footer with navigation and devnet indicator.
- **Custom Logo**: Generate a custom **Yellow Sun + Shield SVG** logo.
- **Typography & Design Tokens**: Use `"Hanken Grotesk"` (sans) and `"Geist Mono"` (data/numbers/badges) from the webapp; warm paper `#F7F5F0`, dark ink `#1A1A17`, signal yellow `#FFD60A`, hairline borders `#E3DFD6`, and soft pastel accent containers (`#FFFBEA`, `#FDF8F6`, `#F0FDF4`).

---

## 2. Flaw Detection & Current State Audit

| # | Current State | Identified Flaw | Solution in New Design |
|---|---|---|---|
| **L-01** | Heavy black border-boxed simulator in hero | Looked like a retro terminal, high contrast, cluttered ("vibecoded") | Replace with the airy, elevated stacked white card UI mockup from the reference image, featuring an adventurer profile, active bounty card, and 73% geofence meter. |
| **L-02** | Missing the distinct Dribbble layout hierarchy | Did not follow modern SaaS editorial proportions (colored accent words, subtle connector line doodles, soft pastel container blocks) | Implement the exact section flow: Navbar &rarr; 2-col Hero &rarr; City Proof Strip &rarr; 3-Tile Feature Container &rarr; Numbers 2-col Split &rarr; Bento Workflow &rarr; MVP Notice &rarr; Bottom CTA &rarr; Footer. |
| **L-03** | Generic sword emoji in navbar | Lacked distinct brand identity | Create a bespoke **Yellow Sun + Shield SVG logo** with sharp heraldic geometry and radiant sunburst rays. |
| **L-04** | Reviews / testimonials were missing or irrelevant | User specifically instructed: "instead of review section it must only be a bento grid of workflow" | Construct a 4-card asymmetric Bento Grid illustrating the 4 lifecycle stages with miniature interactive status widgets. |
| **L-05** | Reliance on heavy borders | Made components feel rigid and boxy | Use soft elevations (`shadow-[0_8px_30px_rgb(0,0,0,0.04)]`), hairline borders (`#E3DFD6`), and organic pastel background shapes. |

---

## 3. Detailed Component Architecture

### 3.1 Custom SVG Logo: Yellow Sun + Shield
```html
<svg viewBox="0 0 40 40" class="w-9 h-9" fill="none">
  <!-- Sunburst Rays -->
  <circle cx="20" cy="20" r="14" fill="#FFD60A" fill-opacity="0.25" />
  <path d="M20 2v4M20 34v4M2 20h4M34 20h4M7.27 7.27l2.83 2.83M29.9 29.9l2.83 2.83M7.27 32.73l2.83-2.83M29.9 10.1l2.83-2.83" stroke="#FFD60A" stroke-width="2.5" stroke-linecap="round" />
  <!-- Radiant Core -->
  <circle cx="20" cy="20" r="10" fill="#FFD60A" />
  <!-- Heraldic Shield Overlay -->
  <path d="M20 8L27 12V19C27 24.5 24 28 20 30C16 28 13 24.5 13 19V12L20 8Z" fill="#1A1A17" stroke="#1A1A17" stroke-width="1.5" stroke-linejoin="round" />
  <!-- Inner Sun Emblem on Shield -->
  <circle cx="20" cy="18" r="3.5" fill="#FFD60A" />
  <path d="M20 13v2M20 21v2M15 18h2M23 18h2" stroke="#FFD60A" stroke-width="1.2" stroke-linecap="round" />
</svg>
```

### 3.2 Hero Left Column: Editorial Typography & Accents
- **Headline**:
  ```html
  <h1 class="text-4xl sm:text-5xl md:text-[56px] font-bold text-[#1A1A17] leading-[1.12] tracking-tight">
    Improve the way <br class="hidden sm:inline" />
    <span class="text-[#E63946] relative inline-block">
      you quest,
      <svg class="absolute -bottom-1 left-0 w-full h-2 text-[#E63946]/40" viewBox="0 0 100 10" preserveAspectRatio="none"><path d="M0 5 Q 50 12, 100 5" stroke="currentColor" stroke-width="3" fill="none"/></svg>
    </span>
    with one click
  </h1>
  ```
- **Subheadline**: Crisp 2 lines explaining the real-world quest and AI verification premise.
- **Button Group**:
  - `Explore Guild Quests` (Primary Pill: `#1A1A17` or `#FFD60A` with hover lift).
  - `Issue a Quest` (Secondary Pill: White with `#E3DFD6` border).
  - Helper note: `Operating across 8 European capitals · Solana Devnet`.
- **Delicate Line Connector**: Minimalist SVG node doodle (`o----o`) matching the reference image.

### 3.3 Hero Right Column: Layered Floating UI Mockup
- Layered stack built strictly from HTML/CSS components (zero bulky bitmaps):
  - **Base Canvas**: Soft tilted container with subtle organic pastel halo.
  - **Main Card**: Elevated white card (`rounded-[28px]`, `p-6`, `shadow-xl`, `border border-[#E3DFD6]`):
    - Top row: Profile snippet with adventurer avatar, name ("Alex Vance / Scout Operative"), "22 Quests Completed".
    - Floating tag: "Bounty Payout: 0.045 SOL" in pale blue pill.
    - Active Quest Box: "Calico Cat Search at Alexanderplatz", reward "0.045 SOL" (~$7.20), status tag.
    - Circular Progress Meter: SVG circular ring with `73% Geofence Match` and `< 2.8s Verification`.
  - **Floating Accent Chips**:
    - Floating chip 1: `✓ Multimodal Vision Confirmed (98%)`
    - Floating chip 2: `⚡ Solana Escrow Payout Settled`

### 3.4 Social Proof / European Hubs Strip
- "Active across 8 European metropolitan hubs & powered by Solana Devnet"
- Interactive / clean badge tags: `Berlin` · `London` · `Paris` · `Madrid` · `Rome` · `Amsterdam` · `Barcelona` · `Vienna` · `Gemini 3.1 Flash-Lite` · `Solana Devnet`.

### 3.5 Features Container: "The Guild Contracts we arbitrate"
- Enclosed inside a soft rounded container (`rounded-[32px]`, `bg-[#F9F7F2]`, `p-8 sm:p-12`, `border border-[#E3DFD6]`):
  - Centered title: "The <span class="text-[#E63946]">Guild Contracts</span> we arbitrate"
  - 3 clean white card tiles:
    1. **Civil Assistance**: Soft coral rounded icon badge + title + description + tags (Lost pets, designated driver, party escort).
    2. **Sensitive Intelligence**: Soft mint rounded icon badge + title + description + tags (Historical plaques, building facade intel, source dossier).
    3. **Commercial UGC**: Soft lavender rounded icon badge + title + description + tags (Bakery showcase, product reels, billboard verification).

### 3.6 Numbers Section: "Okay, Let's see SolGuild in numbers"
- Exact 2-column layout from image 2:
  - **Left**:
    - Title: "Okay, Let's see <span class="text-[#E63946]">SolGuild in numbers</span>"
    - Explanatory paragraph on smart contract security and real-world throughput.
    - 4 metrics grid:
      - `88+` European Quests
      - `< 2.8s` AI Settlement
      - `100%` Smart Escrow Lock
      - `+50 XP` Per Completed Quest
  - **Right**:
    - Verification card component showing real-time arbitration stages (GPS Match &rarr; Vision Match &rarr; Dossier Review &rarr; Payout).

### 3.7 Bento Grid: 4-Step Workflow (Replacing Review Section)
- User mandate: "instead of review section it must only be a bento grid of workflow".
- 4 asymmetric bento cards in a 12-column grid:
  - **Card 1 (7 cols)**: `01 / Issue & Lock Escrow` — Poster sets GPS coordinates and criteria; SOL locks in Solana smart contract escrow.
  - **Card 2 (5 cols)**: `02 / 10-Minute Lock` — Exclusive countdown reservation for nearby adventurers to prevent race conditions.
  - **Card 3 (5 cols)**: `03 / Multimodal Inspection` — Gemini 3.1 Flash-Lite evaluates GPS proximity (<150m), visual evidence, and source dossier.
  - **Card 4 (7 cols)**: `04 / Instant Settlement or Escrow Lock` — If passed, escrow releases SOL instantly + 50 XP. If rejected, funds remain locked in escrow and quest is marked "Failed 1x" for another hero.

### 3.8 Big MVP AI Notice
- Clean, refined notice box explaining why anti-AI image filters are temporarily bypassed so evaluators worldwide can test quest submissions using mock or AI-generated photos.

### 3.9 Bottom CTA Section
- Soft pastel rounded banner with headline "Ready to take on your <span class="text-[#E63946]">first quest</span>?", dual pill CTA buttons (`Explore Guild Board`, `Issue a Quest`), and subtle SVG emblem.

### 3.10 Minimalist Footer
- Custom Sun + Shield SVG logo, SolGuild wordmark, quick links, Solana Devnet status, and open-source note.

---

## 4. Step-by-Step Implementation Roadmap

1. **Step 1: Write Custom Sun + Shield Logo Component / SVG**:
   - Embed high-resolution SVG inside `LandingPage.vue` header and footer.
2. **Step 2: Rewrite `LandingPage.vue` Template & Styling**:
   - Structure all 8 sections exactly matching the Dribbble reference layout.
   - Use `"Hanken Grotesk"` for headings and body, `"Geist Mono"` for numbers and code/tx snippets.
   - Apply soft elevation shadows, hairline borders, and colored accent words (`text-[#E63946]` with subtle wavy underline).
3. **Step 3: Build Interactive UI Card Stack in Hero Right Column**:
   - Create the adventurer card, active quest card, circular progress meter, and floating chips using lightweight Vue/Tailwind markup.
4. **Step 4: Implement 4-Card Bento Workflow Grid**:
   - Replace old review layout with the 4-step bento workflow.
5. **Step 5: Responsive Audit Across Breakpoints**:
   - Test layout on mobile (375px), tablet (768px), laptop (1024px), and desktop (1440px).
   - Ensure clean stacking, no horizontal overflow, and touch targets &ge; 44px.
6. **Step 6: Build Verification & Atomic Git Commit**:
   - Run `npm run build` in `frontend/` to guarantee zero TypeScript or CSS errors.
   - Stage all files and create an atomic git commit per Rule 1.

---

## 5. Constraints, Risks & Assumptions
- **No Heavy External Images**: All UI mockups and cards are created with native Vue/CSS markup and SVGs (zero slow or unextractable image assets).
- **Font Consistency**: Strict adherence to webapp typography (`Hanken Grotesk` and `Geist Mono`).
- **No Disruptions to Core App**: `App.vue` routing and modal contracts remain unchanged.
