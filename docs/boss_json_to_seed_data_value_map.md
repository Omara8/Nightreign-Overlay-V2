# Boss JSON Value → seed_data.json Slot Value Map

Used by the population script to translate every `value`/`boss` string from `patterns_by_nightlord/*.json`
into the corresponding slot value written to `seed_data.json`.

Entries marked **VERIFY** have conflicting evidence in existing seed data and need manual confirmation before the script runs.

---

## Church-type POI categories
*(POIs 28–37, 106 → slots 03/07/08/09/10/16/17/19/23/24/27)*

### `churches`
| Pattern `value` | seed_data value |
|-----------------|-----------------|
| Church - Normal | `church` |
| Church - Rats | `church_spawn` |

### `spawn_points`
| Pattern `value` | seed_data value |
|-----------------|-----------------|
| Spawn Point | `spawn` |

### `townships`
| Pattern `value` | seed_data value |
|-----------------|-----------------|
| Township - Township | `township` |

### `sorcerers_rises`
All variants map to the same seed_data value regardless of sub-type (the sub-type is display-only).

| Pattern `value` | seed_data value |
|-----------------|-----------------|
| Sorcerer's Rise - * (any variant) | `sorcerers` |
| Difficult Sorcerer's Rise - * (any variant) | `sorcerers` |

### `caravans`
| Pattern `value` | seed_data value |
|-----------------|-----------------|
| Small Camp - Caravans | `caravan` |
| Small Camp - Caravans and Nobles | `caravan` |
| small camp - caravans *(lowercase variant)* | `caravan` |

---

## Ruins-type POI categories
*(POIs 93–108, 215 → slots 01/02/04/05/06/11/12/13/14/15/18/20/21/22/25/26)*

### `ruins`
| Pattern `value` | seed_data value |
|-----------------|-----------------|
| Ruins - Albinauric Archers | `ruins_frostbite` |
| Ruins - Albinaurics | `ruins_holy` |
| Ruins - Ancient Heroes of Zamor | `ruins_frostbite` |
| Ruins - Battlemages | `ruins_magic` |
| Ruins - Beastmen of Farum Azula | `ruins_electric` |
| Ruins - Depraved Perfumer | `ruins_poison` |
| Ruins - Erdtree Burial Watchdogs | `ruins` |
| Ruins - Perfumer | `ruins_poison` |
| Ruins - Runebear | `ruins_sleep` |
| Ruins - Sanguine Noble | `ruins_bleed` |
| Ruins - Wormface | `ruins_blight` |

### `forts`
| Pattern `value` | seed_data value |
|-----------------|---------------|
| Fort - Abductor Virgin | `fort` |
| Fort - Crystalians | `fort_magic` |
| Fort - Guardian Golem | `fort` |
| Fort - Lordsworn Captain | `fort` |

### `camps`
| Pattern `value` | seed_data value |
|-----------------|-----------------|
| Camp - Banished Knights | `mainencampment` |
| Camp - Elder Lion | `mainencampment` |
| Camp - Flame Chariots | `mainencampment_fire` |
| Camp - Frenzied Flame Troll | `mainencampment_madness` |
| Camp - Leonine Misbegotten | `mainencampment` |
| Camp - Redmane Knights | `mainencampment_fire` |
| Camp - Royal Army Knights | `mainencampment_electric` |

### `great_churches`
| Pattern `value` | seed_data value |
|-----------------|-----------------|
| Great Church - Fire Monk | `greatchurch_fire` |
| Great Church - Guardian Golem | `greatchurch` |
| Great Church - Mausoleum Knight | `greatchurch` |
| Great Church - Oracle Envoys | `greatchurch_holy` |

### `march`
| Pattern `value` | seed_data value   |
|-----------------|-------------------|
| March - Cleanrot Knight | `march_rot`       |
| March - Cuckoo Knights | `march_sleep`     |
| March - Frost Crayfish | `march_frostbite` |
| March - Kindred of Rot | `march_poison`    |
| March - Nomads | `march_madness`   |
| March - Sanguine Nobles | `march_bleed`     |
| March - Spider Scorpion | `march_poison`    |

### `blacksmith_town`
| Pattern `value` | seed_data value |
|-----------------|-----------------|
| Blacksmith Town - Ancestral Follower Warriors | `blacksmith_town_lightning` |
| Blacksmith Town - Blackflame Monks | `blacksmith_town_fire` |
| Blacksmith Town - Chief Bloodfiend | `blacksmith_town_bleed` |
| Blacksmith Town - Death Knight | `blacksmith_town_lightning` |
| Blacksmith Town - Divine Bird Warrior | `blacksmith_town_holy` |
| Blacksmith Town - Grave Warden Duelists | `blacksmith_town` |
| Blacksmith Town - Omen | `blacksmith_town` |
| Blacksmith Town - Omenkillers | `blacksmith_town_poison` |

---

## Not mapped to seed_data slots (overlay-only)

These categories carry display data for the overlay but their POI IDs fall outside both
slot grids (Default 27-slot and FH 40-slot), so they do not contribute slot values to `seed_data.json`:

- `evergaols` (Default map POIs 76–82)
- `field_bosses` (Default map — boss names used for overlay labels only)
- `castle`, `small_castle`, `medium_castle`, `temple` (FH overlay structures)
- `night1`, `night2`, `special_events`, `extra_night_boss` (overlay-only)

---

## Notes

- `field_bosses` in **FH layouts** DO go into seed_data slots — the boss name string is stored as-is (e.g. `"Flying Dragon"`). No translation needed; the raw `boss` field value is used directly.
- For `sorcerers_rises`, only the slot value `sorcerers` is stored; the full puzzle sub-type is display-only.
- For `caravans`, the caravan sub-type detail is display-only; all variants → `caravan`.