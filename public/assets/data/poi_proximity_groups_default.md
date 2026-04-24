# POI Proximity Groups — Default Map

POI IDs that share the same map location. The plan is to collapse each group to a single canonical ID (lowest number in the group), then update all boss JSON files in `patterns_by_nightlord/` to replace every occurrence of the retired IDs with the canonical one.

Two IDs (30, 37) are intentionally ungrouped — solo by design, no changes needed.

---

## Migration Plan

| Group | Old IDs (all) | Canonical ID (keep) | Retire (replace with canonical) |
|-------|--------------|--------------------|---------------------------------|
| 1 | 31, 207 | **31** | 207 → 31 |
| 2 | 32, 203 | **32** | 203 → 32 |
| 3 | 33, 209 | **33** | 209 → 33 |
| 4 | 34, 202 | **34** | 202 → 34 |
| 5 | 35, 208 | **35** | 208 → 35 |
| 6 | 36, 204 | **36** | 204 → 36 |
| 7 | 106, 157, 206 | **106** | 157 → 106, 206 → 106 |
| 8 | 28, 205 | **28** | 205 → 28 |
| 9 | 29, 201 | **29** | 201 → 29 |

---

## Ungrouped (solo by design — no change)

- **30**
- **37**

---

## Summary of All ID Replacements

| Retire | Replace With |
|--------|-------------|
| 157 | 106 |
| 201 | 29 |
| 202 | 34 |
| 203 | 32 |
| 204 | 36 |
| 205 | 28 |
| 206 | 106 |
| 207 | 31 |
| 208 | 35 |
| 209 | 33 |

---

## Affected Types & JSON Examples

These `poi_id` values can appear under the following keys in any layout file inside `patterns_by_nightlord/`. Each key has a specific object shape shown below.

> **Matching rules for any script:**
> - **Primary match: `poi_id` only.** Scan every object in every key of every layout for a `poi_id` that appears in the retirement table above. Ignore `location` entirely.
> - **Secondary verification: type value field.** Once a matching `poi_id` is found, read the type string from whichever field is present: `value`, `boss`, or `event` (some entries use alternate field names). Check that string against the known types below. If it matches → apply the ID replacement. If it does **not** match → **do not change it**, add to mismatch report with: `layout_number`, `poi_id`, `value`.
> - All type comparisons are **case-insensitive**.
> - For `sorcerers_rises` and `special_events` Sorcerer variants, use a **substring match** on `"sorcerer's rise"` — covers both standard prefix `"Sorcerer's Rise -"` and rare variants like `"Difficult Sorcerer's Rise"`.
> - For all other types, use a **case-insensitive exact match** against the known strings listed below.

### `churches` — Church Normal
```json
{ "poi_id": 31, "value": "Church - Normal", "location": "Far Southwest" }
```

### `churches` — Church Rats
```json
{ "poi_id": 31, "value": "Church - Rats", "location": "Far Southwest" }
```

### `townships`
```json
{ "poi_id": 157, "value": "Township - Township", "location": "Minor Erdtree" }
```

### `spawn_points`
```json
{ "poi_id": 205, "value": "Spawn Point", "location": "Southeast of Lake" }
```

### `caravans`
```json
{ "poi_id": 34, "value": "Small Camp - Caravans", "location": "Above Stormhill Tunnel Entrance" }
{ "poi_id": 34, "value": "Small Camp - Caravans and Nobles", "location": "..." }
```
> Also appears with `"boss"` key instead of `"value"` in some layouts (e.g. Harmonia, Straghess), and with lowercase — matching is case-insensitive.

### `sorcerers_rises`
```json
{ "poi_id": 30, "value": "Sorcerer's Rise - Imp Statue", "location": "Lake" }
```

---

## Script Run Report

**Status: COMPLETED ✓**  
**Total replaced:** 634  
**Total mismatches (skipped):** 0  
**Files modified:** 10 / 10

| File | Replacements |
|------|-------------|
| Adel.json | 57 |
| Caligo.json | 53 |
| Fulghor.json | 53 |
| Gladius.json | 54 |
| Gnoster.json | 55 |
| Harmonia.json | 100 |
| Heolstor.json | 65 |
| Libra.json | 60 |
| Maris.json | 58 |
| Straghess.json | 79 |

All retired POI IDs have been replaced with their canonical equivalents. Matching was performed using exact integer comparison on `poi_id` — no risk of partial ID collision (e.g. 34 vs 234). No mismatches or skipped entries.