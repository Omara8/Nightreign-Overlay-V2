# POI Building Slot Fix — Non-Clickable Building Locations

## Problem

On the Default map (and all Shifting Earth variants sharing the Default grid: Mountaintop, Crater, Rotted Woods, Noklateo), four specific building locations were non-functional in the seed finder slot picker:

| Slot | coordsXY position | Building POI | Was tracking instead |
|------|-------------------|--------------|----------------------|
| 10   | (357, 395)        | POI 34       | Nearby field boss names |
| 17   | (804, 576)        | POI 106      | Nearby field boss names |
| 19   | (550, 630)        | POI 29       | Nearby field boss names |
| 23   | (452, 695)        | POI 30       | Nearby field boss names |

Clicking these slots in the finder opened the slot picker but showed **no selectable options** (or only `empty`). This is because:

1. `buildSlotOptions()` in `filtering.js` only maps values against `buildingIconIds` for non-FH maps.
2. Field boss names (e.g. `"Elder Lion"`, `"Red Wolf"`) are not in `buildingIconIds`.
3. Therefore the picker rendered nothing useful and the click appeared to do nothing.

## Root Cause

`seed_data.json` for these four slots was populated with **field boss names** from nearby field boss POIs rather than the **building type** of the building POI that shares or is closest to the slot position.

For example, for Default seed 001:
- Slot 23 stored `"Bell Bearing Hunter"` — the boss at field boss POI 84 (Lake Field Boss)
- The actual building at POI 30 (same location, "Lake") was `sorcerers_rise`
- Slot 23 should have stored `"sorcerers"`

Geometric note: POI 30 (UV 0.457, 0.712 → pixel 457, 712) is only ~18px from slot 23 (452, 695), while POI 84 (pixel 450, 724) is ~29px away. The building POI is actually **closer** to the slot than the field boss POI. Despite this, the original data extraction explicitly assigned field boss data to these slots.

## Affected POI pairs

These are "hot spot" locations where a **building POI** and a **nearby field boss POI** both map close to the same slot:

| Slot | Building POI | Field Boss POI (was wrongly assigned) |
|------|-------------|--------------------------------------|
| 10   | POI 34 (church / sorcerers_rise / caravan)  | POI 86 (field boss, ~43px from slot) |
| 17   | POI 106 (sorcerers_rise / church)            | Varies (~11px field boss)            |
| 19   | POI 29 (church / sorcerers_rise / caravan)  | Varies (~121px field boss)           |
| 23   | POI 30 (church / sorcerers_rise / township / caravan) | POI 84 (~29px field boss) |

Additionally, the user reported overlapping/nearby POI pairs:
- POIs **29 and 201** — same spot (POI 201 is a dedicated caravan entity, ~14.6px from POI 29)
- POIs **34 and 202** — same spot (POI 202 is a dedicated caravan entity, ~4.5px from POI 34)
- POIs **106 and 206** — short radius (POI 206 is a dedicated caravan entity, ~21.5px from POI 106)

POIs 201, 202, 206 appear in DLC seeds (1001+) as additional caravan entities at the same building locations. These are **not yet handled** (see Remaining Work below).

## Fix Applied

### seed_data.json — 1,750 slot value changes

For all 440 non-FH seeds (Default × 240, Mountaintop × 50, Crater × 50, Rotted Woods × 50, Noklateo × 50), slots 10 / 17 / 19 / 23 were repopulated by cross-referencing each seed's pattern file layout:

| Pattern category | New seed_data value |
|------------------|---------------------|
| `churches`       | `"church"`          |
| `sorcerers_rises`| `"sorcerers"`       |
| `townships`      | `"township"`        |
| `caravans`       | `"caravan"` *(see note)* |
| Not present      | `""` (empty)        |

**Script used:** inline Python — loads all `patterns_by_nightlord/*.json`, resolves `layout_number == int(seed_id)`, reads the building category for the target POI, writes the value.

**Result for Default map (240 seeds):**
- Slot 10 (POI 34): church×67, sorcerers×31, township×9, caravan×30, empty×103
- Slot 17 (POI 106): church×27, sorcerers×36, empty×177
- Slot 19 (POI 29): church×83, sorcerers×42, township×7, caravan×28, empty×80
- Slot 23 (POI 30): church×80, sorcerers×59, township×12, caravan×29, empty×60

Zero boss names remain in any of these slots for non-FH maps.

### Side effect: field bosses at these locations are no longer filterable

The field bosses that were previously tracked by slots 10, 17, 19, 23 (e.g. the "Lake Field Boss" at POI 84) are no longer independently filterable via those slots. This is architecturally correct — these slots are building slots. Other field boss slots (01, 02, 04, 06, 11, 15, 25, 26) remain unchanged.

## Remaining Work

### 1. `"caravan"` value needs an icon

The value `"caravan"` is now stored in seed_data for seeds where POI 29/30/34 host a caravan. However `"caravan"` is **not yet in `buildingIconIds`** (in `src/finder/modules/data.js`) and has no corresponding icon file (`public/assets/buildingIcons/caravan.webp`).

**Effect:** Clicking a slot where the value is `"caravan"` will show only the `empty` option in the picker — the caravan variant is stored but not yet displayed. This is no worse than the previous state (boss name = nothing shown).

**To complete:** Add `caravan.webp` icon file and add `"caravan"` to `buildingIconIds` in `data.js`.

### 2. Dedicated caravan POIs 201, 202, 206 have no slots

POIs 201 (near slot 19), 202 (near slot 10), and 206 (near slot 17) are dedicated caravan entities that appear in DLC seeds. They currently have no coordsXY slot entries and no seed_data tracking.

**To complete:** Add new slot entries to `coordsXY.json` (Default section) for POIs 201, 202, 206 at their UV positions, and populate `seed_data.json` for those slots using a new DLC-aware extraction pass.

### 3. Caravan capitalization in pattern files

The `caravans[].value` field in some pattern file entries uses lowercase (`"small camp - caravans"` instead of `"Small Camp - Caravans"`). A fix pass was prepared but returned 0 matches, meaning this may already be consistent — verify with a grep.

## Files Changed

- `public/assets/data/seed_data.json` — 1,750 slot value updates across 440 seeds
