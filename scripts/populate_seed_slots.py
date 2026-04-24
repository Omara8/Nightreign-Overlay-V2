"""
populate_seed_slots.py

Reads every layout from all 10 patterns_by_nightlord/*.json files and writes the
correct slot values into public/assets/data/seed_data.json.

Value translation follows docs/boss_json_to_seed_data_value_map.md.

Usage (from repo root):
    python scripts/populate_seed_slots.py
"""

import json
import os

# ---------------------------------------------------------------------------
# POI → slot mapping
# ---------------------------------------------------------------------------

# Default / Shifting Earth variants (27-slot grid)
DEFAULT_POI_TO_SLOT = {
    # Church-type POIs
    28: "27", 29: "19", 30: "23", 31: "24", 32: "16",
    33: "08", 34: "10", 35: "03", 36: "09", 37: "07",
    106: "17",
    # Ruins-type POIs
    99: "01", 101: "02", 97: "04", 100: "05", 98: "06",
    102: "11", 104: "12", 95: "13", 103: "14", 96: "15",
    105: "18", 215: "20", 94: "21", 108: "22", 107: "25", 93: "26",
}

FH_POI_MIN = 245
FH_POI_MAX = 284


def fh_poi_to_slot(poi_id):
    """Returns zero-padded slot string for an FH POI, or None if out of range."""
    if FH_POI_MIN <= poi_id <= FH_POI_MAX:
        return f"{poi_id - 244:02d}"
    return None


# ---------------------------------------------------------------------------
# Value translation tables  (from docs/boss_json_to_seed_data_value_map.md)
# ---------------------------------------------------------------------------

EXACT_VALUE_MAP = {
    # churches
    "Church - Normal":               "church",
    "Church - Rats":                 "church_spawn",
    # spawn_points
    "Spawn Point":                   "spawn",
    # townships
    "Township - Township":           "township",
    # caravans (all variants → caravan)
    "Small Camp - Caravans":         "caravan",
    "Small Camp - Caravans and Nobles": "caravan",
    "small camp - caravans":         "caravan",
    # ruins
    "Ruins - Albinauric Archers":    "ruins_frostbite",
    "Ruins - Albinaurics":           "ruins_holy",
    "Ruins - Ancient Heroes of Zamor": "ruins_frostbite",
    "Ruins - Battlemages":           "ruins_magic",
    "Ruins - Beastmen of Farum Azula": "ruins_electric",
    "Ruins - Depraved Perfumer":     "ruins_poison",
    "Ruins - Erdtree Burial Watchdogs": "ruins",
    "Ruins - Perfumer":              "ruins_poison",
    "Ruins - Runebear":              "ruins_sleep",
    "Ruins - Sanguine Noble":        "ruins_bleed",
    "Ruins - Wormface":              "ruins_blight",
    # forts
    "Fort - Abductor Virgin":        "fort",
    "Fort - Crystalians":            "fort_magic",
    "Fort - Guardian Golem":         "fort",
    "Fort - Lordsworn Captain":      "fort",
    # camps
    "Camp - Banished Knights":       "mainencampment",
    "Camp - Elder Lion":             "mainencampment",
    "Camp - Flame Chariots":         "mainencampment_fire",
    "Camp - Frenzied Flame Troll":   "mainencampment_madness",
    "Camp - Leonine Misbegotten":    "mainencampment",
    "Camp - Redmane Knights":        "mainencampment_fire",
    "Camp - Royal Army Knights":     "mainencampment_electric",
    # great_churches
    "Great Church - Fire Monk":      "greatchurch_fire",
    "Great Church - Guardian Golem": "greatchurch",
    "Great Church - Mausoleum Knight": "greatchurch",
    "Great Church - Oracle Envoys":  "greatchurch_holy",
    # march
    "March - Cleanrot Knight":       "march_rot",
    "March - Cuckoo Knights":        "march_sleep",
    "March - Frost Crayfish":        "march_frostbite",
    "March - Kindred of Rot":        "march_poison",
    "March - Nomads":                "march_madness",
    "March - Sanguine Nobles":       "march_bleed",
    "March - Spider Scorpion":       "march_poison",
    # blacksmith_town
    "Blacksmith Town - Ancestral Follower Warriors": "blacksmith_town_lightning",
    "Blacksmith Town - Blackflame Monks":  "blacksmith_town_fire",
    "Blacksmith Town - Chief Bloodfiend":  "blacksmith_town_bleed",
    "Blacksmith Town - Death Knight":      "blacksmith_town_lightning",
    "Blacksmith Town - Divine Bird Warrior": "blacksmith_town_holy",
    "Blacksmith Town - Grave Warden Duelists": "blacksmith_town",
    "Blacksmith Town - Omen":              "blacksmith_town",
    "Blacksmith Town - Omenkillers":       "blacksmith_town_poison",
}

# Categories whose value field is translated via EXACT_VALUE_MAP
TRANSLATED_CATS = {
    "churches", "spawn_points", "townships", "sorcerers_rises", "caravans",
    "ruins", "forts", "camps", "great_churches", "march", "blacksmith_town",
}

# Categories whose boss field is stored as-is (FH field bosses and evergaols)
RAW_BOSS_CATS = {"field_bosses", "evergaols"}

# Skipped entirely (overlay-only, no slot value)
SKIP_CATS = {"castle", "small_castle", "medium_castle", "temple",
             "night1", "night2", "special_events", "extra_night_boss"}


def translate_value(category, raw_value):
    """
    Return the seed_data slot value for a given pattern category + raw value string.
    Returns None if the value should not be written (unmapped or skip).
    """
    if not raw_value:
        return None

    if category == "sorcerers_rises":
        lower = raw_value.lower()
        if "sorcerer's rise" in lower:
            return "sorcerers"
        return None

    if category in TRANSLATED_CATS:
        return EXACT_VALUE_MAP.get(raw_value)

    if category in RAW_BOSS_CATS:
        return raw_value if raw_value.lower() != "empty" else None

    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    patterns_dir = os.path.join(base, "public", "assets", "data", "patterns_by_nightlord")
    seed_data_path = os.path.join(base, "public", "assets", "data", "seed_data.json")

    with open(seed_data_path, encoding="utf-8") as f:
        seed_data = json.load(f)

    seeds_by_id = {str(s["seed_id"]): s for s in seed_data}

    updated = 0
    overwritten = 0
    unmapped_values = {}  # raw_value -> count, for any untranslated entries
    missing_layouts = []

    pattern_files = sorted(f for f in os.listdir(patterns_dir) if f.endswith(".json"))

    for fname in pattern_files:
        nightlord = fname[:-5]
        with open(os.path.join(patterns_dir, fname), encoding="utf-8") as f:
            layouts = json.load(f)

        is_fh_file = any(
            lay.get("shifting_earth") == "Forsaken Hollows" for lay in layouts
        )

        for layout in layouts:
            ln = str(layout.get("layout_number", ""))
            seed = seeds_by_id.get(ln)
            if not seed:
                missing_layouts.append((nightlord, ln))
                continue

            is_fh = layout.get("shifting_earth") == "Forsaken Hollows"

            for cat, entries in layout.items():
                if cat in SKIP_CATS:
                    continue
                if not isinstance(entries, list):
                    continue

                for entry in entries:
                    poi_id = entry.get("poi_id")
                    if poi_id is None:
                        continue

                    # Resolve slot
                    if is_fh:
                        slot = fh_poi_to_slot(poi_id)
                    else:
                        slot = DEFAULT_POI_TO_SLOT.get(poi_id)

                    if slot is None:
                        continue  # POI not in any slot grid (overlay-only POI)

                    # Get raw value
                    raw = entry.get("value") or entry.get("boss") or entry.get("event") or ""
                    if not raw:
                        continue

                    # Translate
                    new_val = translate_value(cat, raw)
                    if new_val is None:
                        key = f"{cat}: {raw!r}"
                        unmapped_values[key] = unmapped_values.get(key, 0) + 1
                        continue

                    current = seed["slots"].get(slot, "")
                    if current == new_val:
                        continue

                    if current and current != new_val:
                        overwritten += 1

                    seed["slots"][slot] = new_val
                    updated += 1

    with open(seed_data_path, "w", encoding="utf-8") as f:
        json.dump(seed_data, f, separators=(",", ":"))
        f.write("\n")

    print(f"Done.")
    print(f"  Slots updated (was empty):    {updated - overwritten}")
    print(f"  Slots overwritten (had value): {overwritten}")
    print(f"  Total writes:                  {updated}")

    if missing_layouts:
        print(f"\n  Layouts in pattern files but not in seed_data ({len(missing_layouts)}):")
        for nl, ln in missing_layouts[:20]:
            print(f"    {nl} layout {ln}")
        if len(missing_layouts) > 20:
            print(f"    ... and {len(missing_layouts) - 20} more")

    if unmapped_values:
        print(f"\n  Unmapped values (add to boss_json_to_seed_data_value_map.md if needed):")
        for key, cnt in sorted(unmapped_values.items(), key=lambda x: -x[1]):
            print(f"    {key}: {cnt} occurrence(s)")


if __name__ == "__main__":
    main()