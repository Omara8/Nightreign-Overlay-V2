(function () {
  const Seedfinder = (window.Seedfinder = window.Seedfinder || {});

  const MAP_ORIGINAL_SIZE = 1000;
  const MAP_MIN_SIZE = 400;
  const MAP_MAX_SIZE = 1500;
  const ICON_SCALE_RATIO = 1 / 14;

  function deriveSlotIdRange(slotCoordsByMapType) {
    const ids = new Set();
    for (const coords of Object.values(slotCoordsByMapType || {})) {
      if (!Array.isArray(coords)) continue;
      for (const coord of coords) {
        if (coord && coord.id && coord.id !== 'nightlord') {
          ids.add(String(coord.id));
        }
      }
    }
    return Array.from(ids).sort();
  }

  const buildingIconIds = [
    'empty',
    // original types
    'church',
    'church_spawn',
    'spawn',
    'greatchurch',
    'greatchurch_fire',
    'greatchurch_holy',
    'fort',
    'fort_magic',
    'mainencampment',
    'mainencampment_electric',
    'mainencampment_fire',
    'mainencampment_madness',
    'ruins',
    'ruins_bleed',
    'ruins_blight',
    'ruins_electric',
    'ruins_fire',
    'ruins_frostbite',
    'ruins_holy',
    'ruins_magic',
    'ruins_poison',
    'ruins_sleep',
    'sorcerers',
    'township',
    // new types
    'temple',
    'blacksmith_town',
    'blacksmith_town_bleed',
    'blacksmith_town_blight',
    'blacksmith_town_fire',
    'blacksmith_town_frostbite',
    'blacksmith_town_holy',
    'blacksmith_town_lightning',
    'blacksmith_town_madness',
    'blacksmith_town_magic',
    'blacksmith_town_poison',
    'blacksmith_town_rot',
    'blacksmith_town_sleep',
    'small_castle',
    'small_castle_fire',
    'small_castle_magic',
    'medium_castle',
    'medium_castle_holy',
    'medium_castle_rot',
    'march',
    'march_bleed',
    'march_blight',
    'march_fire',
    'march_frostbite',
    'march_holy',
    'march_lightning',
    'march_madness',
    'march_magic',
    'march_poison',
    'march_rot',
    'march_sleep',
  ];

  function buildIconPath(dir, file) {
    return `../assets/${dir}/${file}.webp`;
  }

  const buildingIcons = {};
  for (const id of buildingIconIds) {
    buildingIcons[id] = buildIconPath('buildingIcons', id);
  }

  const nightlordIcons = {
    Gladius: buildIconPath('nightlordIcons', 'Gladius'),
    Adel: buildIconPath('nightlordIcons', 'Adel'),
    Gnoster: buildIconPath('nightlordIcons', 'Gnoster'),
    Maris: buildIconPath('nightlordIcons', 'Maris'),
    Libra: buildIconPath('nightlordIcons', 'Libra'),
    Fulghor: buildIconPath('nightlordIcons', 'Fulghor'),
    Caligo: buildIconPath('nightlordIcons', 'Caligo'),
    Heolstor: buildIconPath('nightlordIcons', 'Heolstor'),
    Harmonia: buildIconPath('nightlordIcons', 'Harmonia'),
    Straghess: buildIconPath('nightlordIcons', 'Straghess'),
  };

  const DEFAULT_MAP_THUMB_ORDER = [
    'Default',
    'Mountaintop',
    'Crater',
    'Rotted Woods',
    'Noklateo, the Shrouded City',
    'Forsaken Hollows',
  ];

  const disabledSlotsByMap = {
    Crater: new Set([1, 3, 5, 6, 10, 11, 14]),
    'Rotted Woods': new Set([17, 18, 19, 20, 22, 25, 27]),
    'Noklateo, the Shrouded City': new Set([15, 16, 21, 23, 24, 26]),
    Mountaintop: new Set([1, 4, 6, 8, 10, 13]),
  };

  async function fetchJson(url, fallback) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      return data ?? fallback;
    } catch (error) {
      console.error(`[seedfinder] Failed to load ${url}`, error);
      return fallback;
    }
  }

  function resolveMapThumbOrder(mapBackgroundByType) {
    const preferred = DEFAULT_MAP_THUMB_ORDER.filter(type => mapBackgroundByType[type]);
    const fallback = Object.keys(mapBackgroundByType).sort();
    return preferred.length > 0 ? preferred : fallback;
  }

  function resolveMapTypes(seeds, mapBackgroundByType) {
    const seen = new Set();
    const ordered = [];
    for (const seed of seeds) {
      const type = seed?.shiftingEarth || 'Default';
      if (!seen.has(type)) {
        seen.add(type);
        ordered.push(type);
      }
    }
    return ordered.filter(type => mapBackgroundByType[type]);
  }

  function normalizeSlots(slots, slotIdRange) {
    const normalized = {};
    const source = slots && typeof slots === 'object' ? slots : {};
    for (const slotId of slotIdRange) {
      const fallbackKey = String(Number(slotId));
      const value = source[slotId] ?? source[fallbackKey] ?? '';
      normalized[slotId] = typeof value === 'string' ? value : String(value || '');
    }
    return normalized;
  }

  function normalizeSeedData(record, slotIdRange) {
    if (!record || typeof record !== 'object') {
      return null;
    }

    const shiftingEarth = record.map_type || 'Default';
    const normalized = {
      ...record,
      slots: normalizeSlots(record.slots, slotIdRange),
      shiftingEarth,
    };

    normalized.camelCase = {
      seedId: record.seed_id,
      mapType: shiftingEarth,
    };

    return normalized;
  }

  async function loadAll() {
    const rawCoords = (await fetchJson('../assets/data/coordsXY.json', [])) || [];
    const rawSeeds = (await fetchJson('../assets/data/seed_data.json', [])) || [];
    const rawBackgrounds = (await fetchJson('../assets/data/map_backgrounds.json', {})) || {};

    const mapBackgroundByType = {};
    for (const [type, relPath] of Object.entries(rawBackgrounds)) {
      if (typeof relPath === 'string' && relPath.trim().length > 0) {
        mapBackgroundByType[type] = `../assets/${relPath}`;
      }
    }

    // coordsXY.json is either the new per-map-type dict or the legacy flat array.
    // Shifting Earth variants (Mountaintop, Crater, Rotted Woods, Noklateo) share
    // the Default grid, so they fall back to Default when not explicitly listed.
    const slotCoordsByMapType = Array.isArray(rawCoords)
      ? { Default: rawCoords }
      : rawCoords;

    const slotIdRange = deriveSlotIdRange(slotCoordsByMapType);
    const seeds = rawSeeds.map(record => normalizeSeedData(record, slotIdRange)).filter(Boolean);

    const mapThumbOrder = resolveMapThumbOrder(mapBackgroundByType);
    const mapTypeList = resolveMapTypes(seeds, mapBackgroundByType);

    return {
      slotCoordsByMapType,
      seeds,
      mapBackgroundByType,
      mapThumbOrder,
      mapTypeList,
    };
  }

  Seedfinder.data = {
    config: {
      MAP_ORIGINAL_SIZE,
      MAP_MIN_SIZE,
      MAP_MAX_SIZE,
      ICON_SCALE_RATIO,
    },
    supportedLocales: {
      ar: 'العربية',
      en: 'English',
      es: 'Español',
      ja: '日本語',
      ko: '한국어',
      pl: 'Polski',
      pt: 'Português',
      ru: 'Русский',
      zh: '中文',
    },
    buildingIconIds,
    buildingIcons,
    nightlordIcons,
    disabledSlotsByMap,
    defaultThumbOrder: DEFAULT_MAP_THUMB_ORDER,
    loadAll,
  };
})();
