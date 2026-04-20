# POI 201 / 202 / 206 — Caravan Dedication & Value Cleanup Plan

## Background

POIs 201, 202, and 206 were introduced in the DLC seed range (layouts 1001+) as **dedicated caravan spawn entities** at three existing building locations:

| Caravan POI | UV position | Pixel | Paired building POI | Slot |
|---|---|---|---|---|
| 201 | (0.555, 0.636) | (555, 636) | POI 29  — East of Cavalry Bridge  | 19 |
| 202 | (0.360, 0.405) | (360, 405) | POI 34  — Above Stormhill Tunnel  | 10 |
| 206 | (0.812, 0.564) | (812, 564) | POI 106 — Minor Erdtree           | 17 |

The intent is: POIs 29/34/106 own the **building type** at each location (church / sorcerers / township / empty), while POIs 201/202/206 own a **separate caravan entity** that can appear at the same spot independently.

---

## Problem 1 — POIs 201/202/206 appear in non-caravan categories

The DLC pattern data incorrectly assigns building types to these POI IDs in many layouts. They are found in `churches`, `sorcerers_rises`, and `townships` instead of exclusively in `caravans`.

**Scale of incorrect assignments (DLC seeds only):**

| POI | churches | sorcerers_rises | townships | correct (caravans) |
|-----|----------|-----------------|-----------|---------------------|
| 201 | 0        | 2               | 4         | 2                   |
| 202 | 0        | 2               | 1         | 9                   |
| 206 | 37       | 19              | 5         | 12                  |

**Affected layouts (sample):**

- `POI 206 in churches`: layouts 1013, 1014, 1023, 1031, 1033, 1034, 1041, 1051 (via `church_spawn`), 1075, 1082, 1083, 1091–1094, 1096, 1099–1102, 1104–1105, 1107, 1110, 1136–1137, 1140, 1142, 1150–1151, 1154, 1157, 1159, 1163, 1168–1169, 1197 and more
- `POI 206 in sorcerers_rises`: layouts 1021, 1022, 1032, 1043–1044, 1071, 1073, 1087, 1093, 1104, 1108, 1136, 1139, 1144, 1146, 1153, 1155, 1160, 1196, 1198 and more
- `POI 206 in townships`: layouts 1042, 1096, 1107, 1161 and more
- `POI 202 in townships`: layout 1053
- `POI 202 in sorcerers_rises`: layouts 1004, 1041
- `POI 201 in sorcerers_rises`: layouts 1001, 1075
- `POI 201 in townships`: layouts 1097, 1071, 1137 and more

---

## Problem 2 — Lowercase caravan values in pattern files

Two pattern files contain a lowercase `'small camp - caravans'` instead of `'Small Camp - Caravans'`:

| File | Count |
|------|-------|
| `Harmonia.json` | 1 |
| `Straghess.json` | 1 |

No other files have malformed caravan values. The locale translation files (`overlay_poi_values.json`) use correct casing throughout.

---

## Fix Plan

### Step 1 — Remap incorrect building assignments off POIs 201/202/206

For every DLC seed (layouts 1001+), scan all building categories (`churches`, `sorcerers_rises`, `townships`). Wherever `poi_id` is 201, 202, or 206, replace it with the correct base building POI:

| Incorrect POI | Replace with |
|---------------|--------------|
| 201           | 29           |
| 202           | 34           |
| 206           | 106          |

This leaves POIs 201/202/206 exclusively in the `caravans` category across all pattern files, which is their correct role.

**Script target:** `public/assets/data/patterns_by_nightlord/*.json` — DLC layouts (1001+) only.

After this step, verify:
- `grep poi_id 201/202/206` in non-caravan categories returns zero results.

---

### Step 2 — Add coordsXY slots for POIs 201/202/206

Add three new slot entries to `coordsXY.json` under `"Default"` (shared by all non-FH maps):

```json
{ "id": "c201", "x": 555, "y": 636 },
{ "id": "c202", "x": 360, "y": 405 },
{ "id": "c206", "x": 812, "y": 564 }
```

These positions come directly from the POI UV coordinates × 1000.

The slot IDs `"c201"`, `"c202"`, `"c206"` use a `c` prefix to distinguish them from numeric building slots and avoid collisions with FH numeric slot IDs.

---

### Step 3 — Populate seed_data.json for new slots

For every non-FH seed (440 seeds: Default + Mountaintop + Crater + Rotted Woods + Noklateo):

- Cross-reference the layout's pattern file.
- If `caravans` contains `poi_id == 201` → slot `"c201"` = `"caravan"`.
- If absent → slot `"c201"` = `""`.
- Same logic for `"c202"` (POI 202) and `"c206"` (POI 206).

Most original seeds (1–240 range) will be `""` since POIs 201/202/206 only appear in DLC layouts. DLC seeds (1001+) will have a mix of `"caravan"` and `""`.

**Prerequisite:** Step 1 must be complete first so caravan entries are clean before reading them.

---

### Step 4 — Rename malformed caravan values in pattern files

Scan all `patterns_by_nightlord/*.json` files. For every `caravans[].value` field, apply:

| From | To |
|------|----|
| `'small camp - caravans'` | `'Small Camp - Caravans'` |
| `'Small camp - Caravans'` | `'Small Camp - Caravans'` |
| `'small camp - caravans and nobles'` | `'Small Camp - Caravans and Nobles'` |
| any blank `''` caravan value | investigate — may be a data gap |

**Scope:** pattern files only. `seed_data.json` is explicitly excluded — its `"caravan"` values are the correct short icon key for the finder and must remain unchanged.

---

## What This Enables After Completion

| Capability | Before | After |
|---|---|---|
| Filter seeds by building type at slot 10/17/19/23 | ✗ non-clickable | ✓ already fixed |
| Filter seeds by caravan at POI 29/34/106 location | ✗ no slot | ✓ via slots c201/c202/c206 |
| Correct overlay display of buildings at POI 201/202/206 | ✗ wrong poi_id in data | ✓ remapped to 29/34/106 |
| Correct overlay display of caravans at POI 201/202/206 | ✓ already correct | ✓ unchanged |
| Clean caravan value casing across all pattern files | ✗ 2 lowercase entries | ✓ normalized |

**Note:** Displaying the `"caravan"` filter option in the slot picker UI still requires adding `"caravan"` to `buildingIconIds` in `src/finder/modules/data.js` and a corresponding `public/assets/buildingIcons/caravan.webp` icon file. Until then, the value is stored correctly in seed_data but will not surface as a selectable option in the picker.