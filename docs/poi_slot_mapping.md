# POI ID ↔ Slot Number Reference

Maps every `poi_id` to its slot number and vice versa.

- **Default** section covers all five shared-grid map types: Default, Crater, Noklateo, Rotted Woods, Mountaintop.
- **Forsaken Hollows** section covers its own 40-slot grid.

Slot positions come from `coordsXY.json`. The slot coordinate approximates the POI's UV × 1000 pixel position; the match is not always exact (up to ~22 px deviation due to manual placement).

---

## Default Map (27 slots, shared by 5 map types)

### Full Slot → POI Table

| Slot | POI ID | UV (approx) | Location | Building Type Group |
|------|--------|-------------|----------|---------------------|
| 01   | 99     | (0.401, 0.168) | Northeast Stormhill | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 02   | 101    | (0.710, 0.204) | Summonwater | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 03   | 35     | (0.536, 0.227) | Northeast of Saintsbridge | churches / sorcerers_rises / spawn / caravan / township |
| 04   | 97     | (0.222, 0.271) | Northwest Stormhill | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 05   | 100    | (0.638, 0.293) | Summonwater Approach | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 06   | 98     | (0.413, 0.297) | Alexander Spot | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 07   | 37     | (0.792, 0.361) | Third Church | churches / sorcerers_rises / caravan / township |
| 08   | 33     | (0.215, 0.350) | West of Warmaster's Shack | churches / sorcerers_rises / spawn / caravan / township |
| 09   | 36     | (0.700, 0.369) | Below Summonwater Hawk | churches / sorcerers_rises / spawn / caravan / township |
| 10   | 34     | (0.363, 0.408) | Above Stormhill Tunnel Entrance | churches / sorcerers_rises / spawn / caravan / township |
| 11   | 102    | (0.578, 0.435) | Artist's Shack | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 12   | 104    | (0.771, 0.422) | Northeast Mistwood | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 13   | 95     | (0.278, 0.441) | Stormhill North of Gate | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 14   | 103    | (0.667, 0.465) | Northwest Mistwood | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 15   | 96     | (0.313, 0.556) | Gatefront | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 16   | 32     | (0.198, 0.573) | Murkwater / West Shore | churches / sorcerers_rises / spawn / caravan / township |
| 17   | 106    | (0.810, 0.586) | Minor Erdtree | churches / sorcerers_rises / spawn / caravan / township |
| 18   | 105    | (0.630, 0.599) | West Mistwood | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 19   | 29     | (0.546, 0.647) | East of Cavalry Bridge | churches / sorcerers_rises / spawn / caravan / township |
| 20   | 215    | (0.754, 0.637) | Southwest of Minor Erdtree | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 21   | 94     | (0.275, 0.662) | Groveside | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 22   | 108    | (0.616, 0.703) | Waypoint Ruins | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 23   | 30     | (0.457, 0.712) | Lake | churches / sorcerers_rises / caravan / township |
| 24   | 31     | (0.192, 0.731) | Far Southwest | churches / sorcerers_rises / spawn / caravan / township |
| 25   | 107    | (0.748, 0.744) | South Mistwood | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 26   | 93     | (0.397, 0.795) | South Lake | ruins / forts / camps / great_churches / marches / blacksmith_towns |
| 27   | 28     | (0.566, 0.830) | Southeast of Lake | churches / sorcerers_rises / spawn / caravan / township |

### Reverse Lookup: POI → Slot

| POI ID | Slot | POI ID | Slot |
|--------|------|--------|------|
| 28     | 27   | 93     | 26   |
| 29     | 19   | 94     | 21   |
| 30     | 23   | 95     | 13   |
| 31     | 24   | 96     | 15   |
| 32     | 16   | 97     | 04   |
| 33     | 08   | 98     | 06   |
| 34     | 10   | 99     | 01   |
| 35     | 03   | 100    | 05   |
| 36     | 09   | 101    | 02   |
| 37     | 07   | 102    | 11   |
| 106    | 17   | 103    | 14   |
|        |      | 104    | 12   |
|        |      | 105    | 18   |
|        |      | 107    | 25   |
|        |      | 108    | 22   |
|        |      | 215    | 20   |

### Field Boss Slots

Slots **01, 02, 04, 06, 11, 15, 25, 26** are designated field boss slots. They are positioned at building POI locations but `seed_data.json` stores a **field boss name** at those slots instead of a building type. This is intentional — these building locations also host nearby roaming field bosses that the seed finder tracks.

| Slot | Building POI at position |
|------|--------------------------|
| 01   | 99 (Northeast Stormhill) |
| 02   | 101 (Summonwater)        |
| 04   | 97 (Northwest Stormhill) |
| 06   | 98 (Alexander Spot)      |
| 11   | 102 (Artist's Shack)     |
| 15   | 96 (Gatefront)           |
| 25   | 107 (South Mistwood)     |
| 26   | 93 (South Lake)          |

### Disabled Slots per Map Variant

All five map types share the Default slot/POI grid. Some slots are disabled in non-Default variants (no building appears at those positions):

| Map Variant | Disabled Slots | Corresponding POIs |
|-------------|----------------|--------------------|
| Crater | 1, 3, 5, 6, 10, 11, 14 | 99, 35, 100, 98, 34, 102, 103 |
| Rotted Woods | 17, 18, 19, 20, 22, 25, 27 | 106, 105, 29, 215, 108, 107, 28 |
| Noklateo | 15, 16, 21, 23, 24, 26 | 96, 32, 94, 30, 31, 93 |
| Mountaintop | 1, 4, 6, 8, 10, 13 | 99, 97, 98, 33, 34, 95 |
| Default | _(none)_ | — |

### Retired / Canonical POI Notes

Several duplicate POIs were collapsed into canonical ones. If you encounter these old IDs in pattern files they have been replaced:

| Retired POI | Replaced by | Slot |
|-------------|-------------|------|
| 157         | 106         | 17   |
| 201         | 29          | 19   |
| 202         | 34          | 10   |
| 203         | 32          | 16   |
| 204         | 36          | 09   |
| 205         | 28          | 27   |
| 206         | 106         | 17   |
| 207         | 31          | 24   |
| 208         | 35          | 03   |
| 209         | 33          | 08   |

Dedicated caravan-only POIs (DLC layouts 1001+) — these share the location of their paired building POI:

| Caravan POI | Paired building POI | Slot | Planned slot ID |
|-------------|---------------------|------|-----------------|
| 201         | 29                  | 19   | `c201`          |
| 202         | 34                  | 10   | `c202`          |
| 206         | 106                 | 17   | `c206`          |

---

## Forsaken Hollows (40 slots)

### Formula

All 40 FH slots map sequentially:

```
poi_id = slot_number + 244
```

Slot `01` → POI `245`, slot `02` → POI `246`, … slot `40` → POI `284`.

### Full Slot → POI Table

| Slot | POI ID | UV | Slot | POI ID | UV |
|------|--------|----|------|--------|----|
| 01   | 245    | (0.446, 0.134) | 21   | 265    | (0.710, 0.557) |
| 02   | 246    | (0.323, 0.209) | 22   | 266    | (0.880, 0.576) |
| 03   | 247    | (0.370, 0.218) | 23   | 267    | (0.225, 0.577) |
| 04   | 248    | (0.853, 0.228) | 24   | 268    | (0.476, 0.579) |
| 05   | 249    | (0.356, 0.243) | 25   | 269    | (0.785, 0.585) |
| 06   | 250    | (0.661, 0.247) | 26   | 270    | (0.238, 0.607) |
| 07   | 251    | (0.186, 0.255) | 27   | 271    | (0.356, 0.610) |
| 08   | 252    | (0.488, 0.289) | 28   | 272    | (0.505, 0.677) |
| 09   | 253    | (0.856, 0.359) | 29   | 273    | (0.747, 0.678) |
| 10   | 254    | (0.238, 0.384) | 30   | 274    | (0.350, 0.695) |
| 11   | 255    | (0.502, 0.393) | 31   | 275    | (0.483, 0.724) |
| 12   | 256    | (0.599, 0.394) | 32   | 276    | (0.236, 0.728) |
| 13   | 257    | (0.422, 0.408) | 33   | 277    | (0.835, 0.728) |
| 14   | 258    | (0.684, 0.464) | 34   | 278    | (0.712, 0.759) |
| 15   | 259    | (0.611, 0.496) | 35   | 279    | (0.903, 0.809) |
| 16   | 260    | (0.709, 0.498) | 36   | 280    | (0.359, 0.826) |
| 17   | 261    | (0.274, 0.501) | 37   | 281    | (0.487, 0.861) |
| 18   | 262    | (0.805, 0.526) | 38   | 282    | (0.354, 0.521) |
| 19   | 263    | (0.206, 0.529) | 39   | 283    | (0.860, 0.596) |
| 20   | 264    | (0.482, 0.536) | 40   | 284    | (0.533, 0.754) |

### Slot count note

Slots 01–37 run top-to-bottom, left-to-right across the map. Slots 38–40 are three additional positions that don't fit the main sequence (out-of-order in the `coordsXY.json` list):

| Slot | POI | Approximate area |
|------|-----|------------------|
| 38   | 282 | (0.354, 0.521) — central-west |
| 39   | 283 | (0.860, 0.596) — far east |
| 40   | 284 | (0.533, 0.754) — south-center |

---

## How slot positions relate to POI UVs

For **Forsaken Hollows**: `coordsXY` pixel coords are exactly `uv × 1000` (e.g. slot 15 pixel `(611, 496)` = POI 259 UV `[0.611, 0.496]`).

For **Default**: slot pixel coords approximate the POI UV × 1000 but may be off by up to ~22 px. The slot was placed near the POI's map landmark visually; the deviation reflects manual placement rather than a computed offset.