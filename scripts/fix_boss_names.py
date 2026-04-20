import json, glob

CANONICAL = {
    # Existing in field_boss_names, wrong cap in pattern files
    "Dragonkin soldier": "Dragonkin Soldier",
    "Golden hippopotamus": "Golden Hippopotamus",
    "bell bearing hunter": "Bell Bearing Hunter",
    "cleanrot knights": "Cleanrot Knights",
    "death rite bird": "Death Rite Bird",
    "divine beast warrior": "Divine Beast Warrior",
    "dragonkin soldier": "Dragonkin Soldier",
    "fallingstar beast": "Fallingstar Beast",
    "falingstar beast": "Fallingstar Beast",
    "golden hippopotamus": "Golden Hippopotamus",
    "royal revenant": "Royal Revenant",
    "ulcerated tree spirit": "Ulcerated Tree Spirit",
    "valiant gargoyle": "Valiant Gargoyle",

    # New canonicals
    "Ancient Dragon": "Ancient Dragon",
    "Banished Knights": "Banished Knights",
    "banished Knights": "Banished Knights",
    "banished knight": "Banished Knights",
    "banished knights": "Banished Knights",
    "Battlefield Commander": "Battlefield Commander",
    "battlefield commander": "Battlefield Commander",
    "Beastly Brigade": "Beastly Brigade",
    "Beastmen of Farum Azula": "Beastmen of Farum Azula",
    "beastmen of arum azula": "Beastmen of Farum Azula",
    "Bloodhound Knight": "Bloodhound Knight",
    "Centipede Demon": "Centipede Demon",
    "centipede demon": "Centipede Demon",
    "Crucible Knight and Golden Hippopotamus": "Crucible Knight and Golden Hippopotamus",
    "Crucible Knight and golden hippopotamus": "Crucible Knight and Golden Hippopotamus",
    "crucible knight and golden hippopotamus": "Crucible Knight and Golden Hippopotamus",
    "Crucible Knight with Spear": "Crucible Knight with Spear",
    "Crucible Knight with Sword": "Crucible Knight with Sword",
    "crucible with sword": "Crucible Knight with Sword",
    "Crucible Knights": "Crucible Knights",
    "crucible knights": "Crucible Knights",
    "Crystalians": "Crystalians",
    "crystalians": "Crystalians",
    "Curseblade and Divine Beast Warrior": "Curseblade and Divine Beast Warrior",
    "Dancer of The Boreal Valley": "Dancer of the Boreal Valley",
    "Dancer of the Boreal Valley": "Dancer of the Boreal Valley",
    "dancer of the boreal valley": "Dancer of the Boreal Valley",
    "Death Knights": "Death Knights",
    "Demi-Human Queen and Swordmaster": "Demi-Human Queen and Swordmaster",
    "demi-human queen and swordmaster": "Demi-Human Queen and Swordmaster",
    "demi-queen human and swordmaster": "Demi-Human Queen and Swordmaster",
    "Demon Prince": "Demon Prince",
    "Demon Princes": "Demon Princes",
    "Divine Beast Dancing Lion": "Divine Beast Dancing Lion",
    "Draconic Tree Sentinel and Royal Cavalrymen": "Draconic Tree Sentinel and Royal Cavalrymen",
    "draconic tree sentinel and royal cavalrymen": "Draconic Tree Sentinel and Royal Cavalrymen",
    "Gaping Dragon": "Gaping Dragon",
    "gaping dragon": "Gaping Dragon",
    "Godskin Apostle": "Godskin Apostle",
    "Godskin Duo": "Godskin Duo",
    "Godskin duo": "Godskin Duo",
    "godskin duo": "Godskin Duo",
    "Godskin Noble": "Godskin Noble",
    "Grafted Monarch": "Grafted Monarch",
    "grafted monarch": "Grafted Monarch",
    "Grave Warden Duelist": "Grave Warden Duelist",
    "Great Red Bear": "Great Red Bear",
    "Great Wyrm": "Great Wyrm",
    "great wyrm": "Great Wyrm",
    "Knight Artorias": "Knight Artorias",
    "Mohg": "Mohg",
    "Morgott": "Morgott",
    "morgott": "Morgott",
    "Nameless King": "Nameless King",
    "Night's Cavalry Duo": "Night's Cavalry Duo",
    "Nights Cavalry Duo": "Night's Cavalry Duo",
    "night's cavalry duo": "Night's Cavalry Duo",
    "Nox Warriors": "Nox Warriors",
    "Omen": "Omen",
    "Outland Commander": "Outland Commander",
    "outland commander": "Outland Commander",
    "Smelter Demon": "Smelter Demon",
    "smelter demon": "Smelter Demon",
    "Stoneskin Lords": "Stoneskin Lords",
    "The Duke's Dear Freja": "The Duke's Dear Freja",
    "the duke's dear freja": "The Duke's Dear Freja",
    "Tibia Mariner": "Tibia Mariner",
    "Tree Sentinel and Royal Cavalry Men": "Tree Sentinel and Royal Cavalrymen",
    "Tree Sentinel and Royal Cavalrymen": "Tree Sentinel and Royal Cavalrymen",
    "tree sentinel and royal cavalrymen": "Tree Sentinel and Royal Cavalrymen",
    "Trolls": "Trolls",
    "trolls": "Trolls",
    "Wormface": "Wormface",
}

BOSS_FIELDS_LIST = ["field_bosses", "evergaols", "castle", "small_castle", "medium_castle", "temple"]
BOSS_FIELDS_SINGLE = ["night1", "night2"]

def fix_name(name):
    if not name or name.strip().lower() == "empty":
        return name
    return CANONICAL.get(name, name)

total_fixes = 0
files_changed = 0

for fpath in sorted(glob.glob("public/assets/data/patterns_by_nightlord/*.json")):
    with open(fpath) as f:
        seeds = json.load(f)

    changed = False
    for seed in seeds:
        for cat in BOSS_FIELDS_LIST:
            entries = seed.get(cat, [])
            if isinstance(entries, dict):
                entries = [entries]
            for entry in entries:
                old = entry.get("boss")
                if old:
                    new = fix_name(old)
                    if new != old:
                        entry["boss"] = new
                        print(f'[{seed["layout_number"]}:{cat}] "{old}" -> "{new}"')
                        total_fixes += 1
                        changed = True

        for cat in BOSS_FIELDS_SINGLE:
            entry = seed.get(cat, {})
            if entry and entry.get("boss"):
                old = entry["boss"]
                new = fix_name(old)
                if new != old:
                    entry["boss"] = new
                    print(f'[{seed["layout_number"]}:{cat}] "{old}" -> "{new}"')
                    total_fixes += 1
                    changed = True

        old = seed.get("extra_night_boss", "")
        if old:
            new = fix_name(old)
            if new != old:
                seed["extra_night_boss"] = new
                print(f'[{seed["layout_number"]}:extra_night_boss] "{old}" -> "{new}"')
                total_fixes += 1
                changed = True

    if changed:
        with open(fpath, "w") as f:
            json.dump(seeds, f, indent=2, ensure_ascii=False)
        files_changed += 1

print(f"\nTotal fixes in pattern files: {total_fixes} across {files_changed} files")

# Update field_boss_names.json
with open("public/assets/data/field_boss_names.json") as f:
    fbn = json.load(f)

existing = set(fbn)
new_entries = sorted(set(CANONICAL.values()) - existing)
fbn.extend(new_entries)
fbn_sorted = sorted(fbn, key=lambda x: x.lower())

with open("public/assets/data/field_boss_names.json", "w") as f:
    json.dump(fbn_sorted, f, indent=2, ensure_ascii=False)

print(f"Added {len(new_entries)} new entries to field_boss_names.json")
print(f"field_boss_names.json now has {len(fbn_sorted)} entries")
print(f"New entries: {new_entries}")