# Nightreign Overlay — Architecture & Technical Reference

## Table of Contents

1. [Project Goal](#1-project-goal)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Technology Stack](#3-technology-stack)
4. [Directory Structure](#4-directory-structure)
5. [Electron Main Process](#5-electron-main-process)
6. [Seed Finder Window](#6-seed-finder-window)
   - [Data Layer](#61-data-layer)
   - [State Management](#62-state-management)
   - [Filtering Engine](#63-filtering-engine-core)
   - [Selection Controller](#64-selection-controller)
   - [Map View](#65-map-view)
   - [View / UI](#66-view--ui)
7. [Overlay Window](#7-overlay-window)
   - [Canvas Renderer](#71-canvas-renderer)
   - [Seed Display (Label Builder)](#72-seed-display-label-builder)
   - [UI State & Metrics](#73-ui-state--metrics)
8. [Data Files Reference](#8-data-files-reference)
9. [Seed Detection Algorithm (Full Detail)](#9-seed-detection-algorithm-full-detail)
10. [IPC Communication Flow](#10-ipc-communication-flow)
11. [Hotkeys & Gamepad Input](#11-hotkeys--gamepad-input)
12. [Internationalization (i18n)](#12-internationalization-i18n)
13. [Preferences & Persistence](#13-preferences--persistence)
14. [Build & Distribution](#14-build--distribution)
15. [Key Design Decisions](#15-key-design-decisions)

---

## 1. Project Goal

Nightreign Overlay is a **desktop companion app** for *Elden Ring: Nightreign*. It has two core functions:

1. **Seed Finder** — helps players identify which procedural map layout ("seed") they are currently in, by letting them click on visible in-game structures to progressively narrow down candidates until a single seed is identified.

2. **Game Overlay** — once a seed is identified, renders labeled text directly on top of the game screen, showing the locations of bosses, POIs, night circles, temples, townships, and other events on the game's map.

The app is **entirely passive** — it never reads or writes to game memory, injects DLLs, or uses kernel drivers. It is safe to use with Easy Anti-Cheat.

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Electron Main Process                    │
│  app/main/main.js                                               │
│  ┌──────────────┐   IPC    ┌──────────────┐                     │
│  │  Seed Finder │◄────────►│   Overlay    │                     │
│  │  BrowserWin  │          │  BrowserWin  │                     │
│  └──────────────┘          └──────────────┘                     │
│  Global shortcuts, hotkey config, display management            │
└─────────────────────────────────────────────────────────────────┘
         │                            │
         ▼                            ▼
┌─────────────────┐        ┌──────────────────────┐
│  Seed Finder UI │        │  Transparent Overlay │
│  public/finder/ │        │  public/overlay/     │
│                 │        │                      │
│  Map + slot     │        │  <canvas> drawn over │
│  icon buttons   │        │  the game screen     │
│  Candidate list │        │  POI labels rendered │
│  Hotkey config  │        │  at UV positions     │
└─────────────────┘        └──────────────────────┘
```

---

## 3. Technology Stack

| Layer | Technology |
|---|---|
| Desktop shell | **Electron 38** |
| Renderer | Vanilla JS (no framework) |
| Overlay rendering | HTML5 Canvas 2D API |
| Data format | JSON |
| Build output | Portable `.exe` or `.zip` (Windows x64 / ARM64) |
| Packaging | `electron-builder` |

No frontend framework (React, Vue, etc.) is used. All UI is hand-written DOM + CSS. All rendering on the overlay is done via Canvas 2D.

---

## 4. Directory Structure

```
/
├── app/
│   └── main/
│       ├── main.js          # Electron main process entry point
│       └── preload.js       # Context bridge (IPC surface for renderer)
│
├── config/
│   └── hotkeys.json         # User hotkey config (persisted, runtime-writable)
│
├── public/
│   ├── assets/
│   │   ├── data/
│   │   │   ├── seed_data.json                  # All 520 seeds (slot-level data)
│   │   │   ├── coordsXY.json                   # Slot pixel positions per map type
│   │   │   ├── poi_uv_with_ids.json            # POI world positions (UV 0-1)
│   │   │   ├── field_boss_names.json           # Forsaken Hollows boss name list
│   │   │   ├── map_backgrounds.json            # Map type → image file mapping
│   │   │   ├── nightlords.json                 # Nightlord metadata
│   │   │   └── patterns_by_nightlord/
│   │   │       ├── Gladius.json                # Detailed seed data per nightlord
│   │   │       ├── Adel.json
│   │   │       ├── Gnoster.json
│   │   │       ├── Maris.json
│   │   │       ├── Libra.json
│   │   │       ├── Fulghor.json
│   │   │       ├── Caligo.json
│   │   │       ├── Heolstor.json
│   │   │       ├── Harmonia.json
│   │   │       └── Straghess.json
│   │   └── images/          # Icons, map images, nightlord images
│   ├── finder/
│   │   └── index.html       # Seed Finder window HTML
│   ├── overlay/
│   │   └── index.html       # Overlay window HTML
│   └── locales/             # i18n translation files
│
└── src/
    ├── core/
    │   ├── filtering.js     # Constraint-satisfaction seed filtering (shared)
    │   └── i18n/            # i18n helpers
    ├── finder/
    │   ├── modules/
    │   │   ├── data.js      # Data loading, icon pools, normalization
    │   │   └── state.js     # Finder global state
    │   └── runtime/
    │       ├── index.js     # Finder bootstrap / initialization
    │       ├── selection.js # Slot selection controller (core interaction logic)
    │       ├── map-view.js  # Map slot icons rendering and slot picker modal
    │       ├── view.js      # Status bar, candidate list, overlay trigger
    │       ├── dom.js       # DOM element references
    │       ├── events.js    # Event wiring
    │       ├── hotkeys.js   # Hotkey settings UI
    │       └── locale.js    # Language switcher UI
    ├── input/
    │   └── gamepad.js       # DualSense / Xbox controller input
    ├── overlay/
    │   ├── modules/
    │   │   ├── data.js      # POI data loader, seed pattern loader
    │   │   └── state.js     # Overlay prefs, active seed state
    │   └── runtime/
    │       ├── index.js     # Overlay bootstrap / render loop
    │       ├── renderer.js  # Canvas draw functions
    │       ├── seed-display.js  # Label descriptor builder
    │       └── ui-state.js  # UI metric derivation (font, padding, scale)
    └── shared/              # Shared utilities
```

---

## 5. Electron Main Process

**File:** `app/main/main.js`

The main process is the orchestrator. It:

- Enforces **single-instance lock** (second launch focuses the existing window)
- Creates two `BrowserWindow` instances:
  - **`seedWin`** — the Seed Finder (1080×870, normal window)
  - **`overlayWin`** — the overlay (full primary display, transparent, always-on-top, frameless, non-focusable, click-through via `setIgnoreMouseEvents`)
- Registers **global shortcuts** (F7–F10 by default) via `globalShortcut`
- Handles **display change events** (monitors added/removed) by re-creating the overlay on the primary display
- Routes **IPC messages** between the two windows:
  - `seed:selected` → forwards to overlay as `overlay:seed-selected`
  - `overlay:reset` → clears overlay state
  - `hotkeys:save` → writes `config/hotkeys.json` and re-registers shortcuts
  - `locale:changed` → pushes locale to overlay window
- Sanitizes and normalizes hotkey accelerator strings before registering them

### Overlay Window Properties
```
transparent: true
alwaysOnTop: true  ('screen-saver' level)
focusable: false
clickThrough: true  (mouse events forwarded to game beneath)
type: 'toolbar'  (Windows — prevents taskbar entry)
```

---

## 6. Seed Finder Window

The Seed Finder is a normal browser window. Its HTML loads multiple JS modules that wire together into a single interactive UI.

### 6.1 Data Layer

**File:** `src/finder/modules/data.js`

Loaded once at startup via `loadAll()`. Fetches and caches:

| Data | Source | Purpose |
|---|---|---|
| All seeds | `seed_data.json` | The 520 seeds used for filtering |
| Slot coordinates | `coordsXY.json` | Pixel positions of each slot button per map type |
| Map backgrounds | `map_backgrounds.json` | Which image file to use per map type |
| Field boss names | `field_boss_names.json` | Valid field boss options for Forsaken Hollows slots |

Seeds are normalized into a consistent structure by `normalizeSeedData()`:
```js
{
  seed_id: "1026",
  shiftingEarth: "Forsaken Hollows",   // normalized from map_type
  nightlord: "Gnoster",
  slots: { "01": "church", "13": "", "15": "township", ... }
}
```

Icon pools are also defined here:
- `buildingIcons` — maps building type strings (e.g. `"church"`, `"spawn"`, `"township"`) to image paths
- `nightlordIcons` — maps nightlord names to image paths
- `buildingIconIds` — ordered array of all valid building type IDs

### 6.2 State Management

**File:** `src/finder/modules/state.js`

A single `state.current` object holds all mutable state:

```js
{
  seeds: [],              // All normalized seeds
  activeMapType: null,    // e.g. "Forsaken Hollows"
  selectionBySlot: {},    // { "15": "township", "nightlord": "Gnoster", ... }
  candidateSeeds: [],     // Seeds still matching all selections
  resolvedSeed: null,     // Non-null when exactly 1 candidate remains
  slotCoordsByMapType: {},
  fieldBossNames: [],
}
```

State is mutated only through setter functions (`setActiveMapType`, `updateSelection`, `setCandidateSeeds`, etc.), keeping changes trackable.

### 6.3 Filtering Engine (Core)

**File:** `src/core/filtering.js`

The heart of the seed identification system. Pure functions, no side effects, shared between finder and any future consumers.

#### Key Functions

**`matchesSelection(seed, selection)`**
Tests if a seed satisfies all current slot selections. Uses exact string equality — no fuzzy matching.
```js
for each [slotId, value] in selection:
  if slotId === 'nightlord': seed.nightlord must === value
  else: seed.slots[slotId] must === value
→ returns true only if ALL non-empty selections match
```

**`filterBySelection(seeds, selection)`**
Returns only seeds where `matchesSelection` is true.

**`resolveSlotValues({ seeds, selection, slotId })`**
Given current selections, finds every value that *could* appear at `slotId` across all still-valid seeds. Used to populate the slot picker options. It tests each seed against the selection while **ignoring** the slot being resolved, then collects its value for that slot.

**`buildSlotOptions(...)`**
Converts `resolveSlotValues` output into `{ id, src }[]` icon objects for the UI. For Forsaken Hollows, also appends field boss name options to slots that have no building.

**`deriveCandidateState({ seeds, selection, mapType })`**
The main entry point called after every selection change:
1. `filterByMap` → seeds for the active map type
2. `filterBySelection` → seeds matching all current selections
3. If exactly 1 remains → `resolvedSeed` is set

**`deriveGhostOption(options)`**
If a slot has exactly 2 options and one is `"empty"`, returns the non-empty one as a "ghost hint."

### 6.4 Selection Controller

**File:** `src/finder/runtime/selection.js`

Orchestrates user interactions and drives filtering:

**`onSlotClick(slotId)`**
1. Calls `getSlotOptions(slotId)` to compute valid options via `buildSlotOptions`
2. If 2 options (1 non-empty + 1 empty) → auto-selects the non-empty one
3. Otherwise → opens the slot picker modal

**`applySelections()`**
Called after every selection change:
1. Runs `deriveCandidateState` to get filtered candidates
2. Updates state (`candidateSeeds`, `resolvedSeed`)
3. Calls `view.updateStatus()`, `view.updateCandidatesList()`, `view.renderSlotIcons()`
4. If a new unique seed was resolved → calls `view.showSingleSeedOverlay()` automatically

**`selectMap(mapType)`**
Clears all selections, sets active map type, re-renders slot icons.

### 6.5 Map View

**File:** `src/finder/runtime/map-view.js`

Manages the interactive map panel. The DOM structure is:
```
#mapWrapper
  ├── #mapImage          (background map image)
  └── #iconLayer         (absolute-positioned div, overlaid on map)
       └── .slot-icon[data-slot-id] × N   (one per slot)
            └── <img>   (the slot's current icon)
```

**`renderSlotIcons()`**
For each slot coordinate in the active map type:
1. Converts pixel coordinates to display position using `MAP_ORIGINAL_SIZE` constant
2. Sets the `<img>` src to the current selection's icon, or the ghost hint icon, or the empty icon
3. Applies disabled styling for slots that are inactive on the current map type

**Disabled slots per map type** (certain slots are hidden for non-Default maps):
```
Crater:          slots {1,3,5,6,10,11,14}
Rotted Woods:    slots {17,18,19,20,22,25,27}
Noklateo:        slots {15,16,21,23,24,26}
Mountaintop:     slots {1,4,6,8,10,13}
```

**Nightlord Slot**
The nightlord is treated as a special slot at pixel position (112, 900) on all maps. It uses `nightlordIcons` instead of `buildingIcons` and opens a "Nightlords" section in the picker modal.

**Slot Picker Modal**
When a slot is clicked and has >2 options, a modal opens showing all valid icons in a grid. For the nightlord slot, it shows all 10 nightlords. For building slots, it shows building icons. For Forsaken Hollows field boss slots, it shows boss name text options.

### 6.6 View / UI

**File:** `src/finder/runtime/view.js`

Handles all DOM output beyond the map:

- **`updateStatus()`** — Updates the status bar text. When selections are active: `"[Nightlord] | [MapType] | N candidates"`
- **`updateCandidatesList()`** — Lists remaining seed IDs (up to 100)
- **`updateSendButtonState()`** — Enables "Show Overlay" button only when exactly 1 candidate remains
- **`showSingleSeedOverlay()`** — Sends the resolved seed to the overlay window via `window.app.seed.sendSelected(payload)`:
  ```js
  { nightlord, seed_id, seed }
  ```

---

## 7. Overlay Window

The overlay window is a transparent, full-screen, always-on-top window. It renders a `<canvas>` element that covers the entire screen, drawing text labels over the game's map.

### 7.1 Canvas Renderer

**File:** `src/overlay/runtime/renderer.js`

**`renderDescriptors(ctx, descriptors, dependencies)`**

The main render function. For each label descriptor:
1. Looks up the POI record via `getPoiRecord(poiId)` to get UV coordinates `[u, v]`
2. Converts UV → screen pixel via `uvToScreen(panelRect, u, v)`
3. Calls `drawLabel()` to paint the text box on the canvas

The canvas is re-centered around the game's map panel region (`panelRect`) and scaled by `globalScale`.

**`drawLabel(ctx, x, y, text, styleKey, ui, ...)`**

Renders a single text label at `(x, y)`:
1. Splits text on `\n` for multi-line support (used by temple bosses and nightlord + special event combined labels)
2. Draws a semi-transparent black background rectangle
3. Draws text in the category color (from user prefs) centered on the position
4. Applies font size, padding, and offsets from `ui` metrics

### 7.2 Seed Display (Label Builder)

**File:** `src/overlay/runtime/seed-display.js`

**`buildLabelDescriptors(seedData, helpers)`**

Converts a seed's data object into an array of `{ poiId, text, styleKey }` descriptors. Each descriptor maps one POI on the map to one text label.

Label categories and their `styleKey`:

| Category | styleKey | Source field |
|---|---|---|
| Night 1 Boss | `night` | `seedData.night1` |
| Night 2 Boss | `night` | `seedData.night2` |
| Day 2 Circle | `night` | `seedData.day2_location` |
| Nightlord + Special Events | `event` | Always at POI 214; appends `seedData.special_events` if present |
| Evergaols | `evergaol` | `seedData.evergaols[]` |
| Field Bosses | `field-boss` | `seedData.field_bosses[]` |
| Castle Boss | `castle-boss` | `seedData.castle[]` |
| Temple Bosses | `temple` | `seedData.temple[]` (grouped by POI, multi-line) |
| Sorcerer's Rises | `sorcerer-rise` | `seedData.sorcerers_rises[]` |
| Ruins | `ruins` | `seedData.ruins[]` |
| Forts | `fort` | `seedData.forts[]` |
| Camps | `camp` | `seedData.camps[]` |
| Caravans | `caravan` | `seedData.caravans[]` |
| Churches | `church` | `seedData.churches[]` |
| Great Churches | `great-church` | `seedData.great_churches[]` |
| Townships | `township` | `seedData.townships[]` |

**Nightlord + Special Event Label (POI 214)**

The nightlord name is **always** rendered at POI 214 (UV `[0.105, 0.836]`, bottom-left of the Default map). If a special event also exists at POI 214, it is appended on a new line:
```
Nightlord: Gnoster
Day 2 Extra Night Boss - Dragonkin Soldier
```

If the special event is at a different POI (rare), it renders at its own position without the nightlord prefix.

### 7.3 UI State & Metrics

**File:** `src/overlay/runtime/ui-state.js`

**`deriveUiMetrics({ overlayPrefs, labelBaseStyle, scale })`**

Computes display metrics adjusted for DPI scale and user preferences:
```js
{
  fontPx,    // font size in pixels
  labelPad,  // padding around label background
  labelH,    // line height
  bgAlpha,   // background rectangle opacity
  offsetX,   // global X nudge from user prefs
  offsetY,   // global Y nudge from user prefs
}
```

---

## 8. Data Files Reference

### `seed_data.json`

The filtering database. Contains all 520 seeds as flat objects optimized for the constraint-satisfaction algorithm.

```json
{
  "seed_id": "1026",
  "map_type": "Forsaken Hollows",
  "nightlord": "Gnoster",
  "slots": {
    "01": "church",
    "15": "township",
    "17": "Bell Bearing Hunter",
    "32": "spawn",
    ...
  },
  "day2_location": 251
}
```

Slot keys are `"01"` through `"27"` (Default/non-FH maps) or `"01"` through `"40"` (Forsaken Hollows). Values are building type strings or field boss names. Empty slots have value `""`.

**Slot ID ↔ POI ID mapping**: Slot pixel coordinates in `coordsXY.json` correspond 1:1 to POI UV coordinates in `poi_uv_with_ids.json` when multiplied by 1000. For example, slot `"15"` in Forsaken Hollows has pixel `(611, 496)`, which matches POI 259 at UV `[0.611, 0.496]`.

### `coordsXY.json`

Maps each map type to an array of `{ id, x, y }` objects, where `id` is the slot key and `x`, `y` are pixel positions on the `1000×1000` reference map image.

### `poi_uv_with_ids.json`

Maps POI IDs to UV coordinates (normalized 0–1 world positions):
```json
{ "id": 259, "uv": [0.611, 0.496] }
```
Used by the overlay renderer to position labels on the game screen.

### `patterns_by_nightlord/*.json`

Per-nightlord arrays of detailed seed objects. Each seed contains:
- Categorized POI arrays: `churches`, `field_bosses`, `evergaols`, `temple`, `sorcerers_rises`, `forts`, `camps`, `caravans`, `townships`, `ruins`, `castle`, `medium_castle`, `small_castle`, `great_churches`, `spawn_points`
- Night events: `night1`, `night2` (with `poi_id`, `boss`, `circle_location`)
- Special events: `special_events[]` (with `poi_id`, `event`, `night`, `location`)
- `extra_night_boss` — a boss name string appended to the special event label
- `day2_location` — POI for the Day 2 night circle
- `shifting_earth` — map type string

These files are loaded **lazily** by the overlay only when a specific nightlord's seed is needed.

### Map Types

| Map Type | Slots | Notes |
|---|---|---|
| Default | 27 | Standard map |
| Forsaken Hollows | 40 | Includes field boss slots; has Day 2 circle |
| Mountaintop | 27 | Several slots disabled |
| Crater | 27 | Several slots disabled |
| Rotted Woods | 27 | Several slots disabled |
| Noklateo, the Shrouded City | 27 | Several slots disabled |

---

## 9. Seed Detection Algorithm (Full Detail)

The detection system is **interactive constraint-satisfaction**. There is no image recognition, OCR, game memory reading, or fuzzy/scored matching. Everything is exact string equality.

### Algorithm

```
GIVEN:
  seeds[]           - all 520 seeds for the active map type
  selection{}       - user's current slot → value assignments

FILTER:
  candidates = seeds.filter(seed =>
    for every (slotId, value) in selection where value ≠ 'empty':
      seed.slots[slotId] === value
      (or seed.nightlord === value for nightlord slot)
  )

RESOLVE:
  if candidates.length === 1 → seed identified
```

### Slot Option Narrowing

When the user clicks a slot, only options still compatible with all other current selections are shown:

```
valid_options(slotId) =
  { seed.slots[slotId] : seed ∈ seeds, matchesSelection(seed, selection \ {slotId}) }
```

This means as selections accumulate, each new slot's picker automatically hides impossible values.

### Ghost Icon Optimization

When a slot's valid options narrow to exactly `["empty", "SomeValue"]`, the system:
1. Shows a faint "ghost" icon as a visual hint on the map
2. Auto-selects `"SomeValue"` on the next click without opening the modal

### Convergence

Each selection reduces the candidate pool. Typical identification requires 3–6 slot selections. When `candidates.length === 1`, the resolved seed is automatically sent to the overlay window.

---

## 10. IPC Communication Flow

```
Seed Finder Renderer
  │
  │  window.app.seed.sendSelected(payload)
  │  [preload.js context bridge]
  │
  ▼
Electron Main (ipcMain 'seed:selected')
  │
  │  win.webContents.send('overlay:seed-selected', payload)
  │
  ▼
Overlay Renderer
  │
  │  window.app.overlay.onSeedSelected(callback)
  │  [preload.js context bridge]
  │
  ▼
  overlay/runtime/index.js → normalizes payload → loads pattern data → render()
```

The payload sent from finder to overlay:
```js
{
  nightlord: "Gnoster",    // from user selection (may be empty string)
  seed_id: "1026",         // numeric seed ID
  seed: { ... }            // full seed object from seed_data.json
}
```

The overlay normalizes the payload into the detailed pattern object from `patterns_by_nightlord/Gnoster.json` before rendering.

### Other IPC Channels

| Channel | Direction | Purpose |
|---|---|---|
| `overlay:reset` | Main → Overlay | Clear all labels |
| `overlay:locale` | Main → Overlay | Push language code |
| `hotkeys:save` | Finder → Main | Persist hotkey config |
| `hotkeys:request` | Finder → Main | Read current hotkeys |
| `hotkeys:suspend` | Finder → Main | Pause shortcuts while editing |
| `locale:changed` | Finder → Main | Propagate language change |
| `overlay:toggle-overlay` | Finder → Main | Toggle overlay visibility |
| `overlay:hide-overlay` | Finder → Main | Hide overlay |
| `display-info` | Main → Overlay | Send display bounds + scale factor |
| `finder:request-active-seed` | Main → Finder | Trigger "Send to Overlay" (F8) |

---

## 11. Hotkeys & Gamepad Input

### Hotkeys

**File:** `config/hotkeys.json` (runtime-writable)

| Action | Default | Description |
|---|---|---|
| `toggleSeedFinder` | F7 | Show/hide the Seed Finder window |
| `sendToOverlay` | F8 | Manually send current seed to overlay |
| `toggleOverlay` | F9 | Show/hide the overlay |
| `resetOverlay` | F10 | Clear overlay labels |

Hotkeys are registered as Electron global shortcuts (work even when the game is focused). Accelerator strings are sanitized and normalized before registration (handles edge cases like `"Ctrl"` vs `"Control"`, mouse buttons, dead keys, etc.).

### Gamepad Input

**File:** `src/input/gamepad.js`

Polling-based controller support using the browser Gamepad API. Supports DualSense and Xbox controllers:

| Action | DualSense | Xbox |
|---|---|---|
| Toggle Overlay | Touchpad click | View/Back |
| Hide Overlay | Circle / L1 / R1 / Options | B / LB / RB / Start |

---

## 12. Internationalization (i18n)

**Files:** `public/locales/`, `src/core/i18n/`, `src/finder/runtime/locale.js`

Supported languages: Arabic (ar), English (en), Spanish (es), Japanese (ja), Korean (ko), Polish (pl), Portuguese (pt), Russian (ru), Chinese (zh).

- The Seed Finder has its own i18n module (`SeedfinderI18N`) for UI strings and nightlord/building labels
- The Overlay has its own i18n module (`OverlayI18N`) for POI label translation
- Locale is stored in `localStorage` and pushed to the overlay via IPC on change

Translation functions:
- `o18n.bossLabel(category, name)` — translates a boss name
- `o18n.eventLabel(name)` — translates a special event name
- `o18n.poiLabel(name)` — translates a POI value (church, fort, etc.)
- `o18n.tUILabel(key, fallback)` — translates a UI string

---

## 13. Preferences & Persistence

### Overlay Preferences

Stored in `localStorage` under specific keys. Loaded by `loadOverlayPrefsFromStorage()` on every render and on `storage` events (so changes apply immediately across tabs/windows).

| Preference | Type | Default | Description |
|---|---|---|---|
| `fontSize` | number | 14 | Label font size in px |
| `offsetX` | number | 0 | Global X offset for all labels |
| `offsetY` | number | 0 | Global Y offset for all labels |
| `scale` | number | 1 | Global scale multiplier |
| `color_*` | string | varies | Per-category label color |
| `visible_*` | boolean | true | Per-category visibility toggle |

### Category Style Keys

Each label category can have its color and visibility toggled independently:
`night`, `evergaol`, `field-boss`, `event`, `sorcerer-rise`, `castle-boss`, `temple`, `ruins`, `fort`, `camp`, `caravan`, `church`, `great-church`, `township`

### Hotkey Config

Stored in `config/hotkeys.json` (in the app directory, not localStorage). Written by the main process when the user saves hotkeys in the Finder UI.

---

## 14. Build & Distribution

```bash
npm install       # install Electron and electron-builder
npm start         # run in development mode
npm run dist:win  # build Windows portable + zip (x64 and ARM64)
```

**Output:** `dist/` — contains `Nightreign Overlay-<version>-<arch>.exe` (portable) and `.zip`

**ASAR unpacking:** Data files (`config/`, `public/assets/data/`) are unpacked from the ASAR archive so they can be read at runtime without extraction. This also makes it possible to update data files independently of the app binary.

---

## 15. Key Design Decisions

### No Framework
The UI is vanilla JS + DOM. This keeps the bundle small, startup fast, and avoids framework overhead in an always-on-top overlay context where responsiveness matters.

### Two Separate Data Representations
- `seed_data.json` — flat, slot-keyed structure optimized for fast filtering (the constraint-satisfaction algorithm only needs slot values)
- `patterns_by_nightlord/*.json` — rich, categorized structure loaded lazily by the overlay for label rendering

This avoids loading the full rich data for all 520 seeds upfront, while keeping filtering fast.

### Slot ID ↔ POI ID Relationship
Slot IDs in `coordsXY.json` use pixel coordinates that correspond 1:1 to POI UV coordinates when normalized. POI `N` has UV `[x/1000, y/1000]` where `(x, y)` is the pixel coordinate of the matching slot. This was by design — POI IDs and slot positions are kept consistent during data authoring.

### No Scoring / Fuzzy Matching
All filtering is exact string equality. This is intentional — game seed data is deterministic and known in advance, so there is no need for probabilistic approaches.

### EAC Safety
The overlay uses only standard Windows desktop APIs (Electron BrowserWindow with `type: 'toolbar'`). No game process interaction of any kind occurs.

### Single-Instance Enforcement
`app.requestSingleInstanceLock()` ensures only one copy of the app runs at a time, preventing duplicate overlays or hotkey conflicts.
