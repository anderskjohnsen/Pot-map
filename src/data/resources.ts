import type { Resource } from '../types';

// Coordinates are normalized to a 4096x4096 grid matching the map image.
// Gondwa: NW corner = (0,0), SE corner = (4096,4096).
export const resources: Resource[] = [
  // ─── GONDWA – WATER ─────────────────────────────────────────────────────────
  { id: 'g-w-01', mapId: 'gondwa', category: 'water', name: 'Great Lake North Shore', x: 2048, y: 1600, description: 'Large freshwater lake, safe drinking spot' },
  { id: 'g-w-02', mapId: 'gondwa', category: 'water', name: 'Great Lake South Shore', x: 2100, y: 2000, description: 'Shallow southern bank' },
  { id: 'g-w-03', mapId: 'gondwa', category: 'water', name: 'Eastern River Delta', x: 3200, y: 2400, description: 'Fast-flowing freshwater river' },
  { id: 'g-w-04', mapId: 'gondwa', category: 'water', name: 'West Marsh', x: 700,  y: 2200, description: 'Muddy marshland, fresh water available' },
  { id: 'g-w-05', mapId: 'gondwa', category: 'water', name: 'Northern Stream', x: 1400, y: 800, description: 'Small but reliable stream' },
  { id: 'g-w-06', mapId: 'gondwa', category: 'water', name: 'Jungle Pool', x: 1200, y: 3000, description: 'Hidden freshwater pool in dense jungle' },
  { id: 'g-w-07', mapId: 'gondwa', category: 'water', name: 'Waterfall Basin', x: 2800, y: 1200, description: 'Crystal clear waterfall pool' },
  { id: 'g-w-08', mapId: 'gondwa', category: 'water', name: 'Southeast Swamp', x: 3400, y: 3200, description: 'Brackish swamp water' },
  { id: 'g-w-09', mapId: 'gondwa', category: 'water', name: 'Central Oasis', x: 2050, y: 1800, description: 'Central freshwater oasis' },
  { id: 'g-w-10', mapId: 'gondwa', category: 'water', name: 'Highland Creek', x: 3000, y: 700, description: 'Mountain creek, cold and fast' },

  // ─── GONDWA – HERB FOOD ──────────────────────────────────────────────────────
  { id: 'g-hf-01', mapId: 'gondwa', category: 'herb_food', name: 'Berry Bush Patch', x: 900, y: 1400, tags: ['berry'], description: 'Dense berry bushes, great for small herbivores' },
  { id: 'g-hf-02', mapId: 'gondwa', category: 'herb_food', name: 'Cycad Grove', x: 1600, y: 2600, tags: ['cycad'], description: 'Large cycads suitable for big herbivores' },
  { id: 'g-hf-03', mapId: 'gondwa', category: 'herb_food', name: 'Fern Valley', x: 1300, y: 2200, tags: ['fern'], description: 'Ground ferns carpet the valley floor' },
  { id: 'g-hf-04', mapId: 'gondwa', category: 'herb_food', name: 'Palm Grove', x: 3100, y: 3000, tags: ['palm'], description: 'Tropical palms line the coast' },
  { id: 'g-hf-05', mapId: 'gondwa', category: 'herb_food', name: 'Mushroom Hollow', x: 800, y: 2800, tags: ['mushroom'], description: 'Dense mushroom clusters in shaded area' },
  { id: 'g-hf-06', mapId: 'gondwa', category: 'herb_food', name: 'Grasslands', x: 2600, y: 2800, tags: ['grass'], description: 'Open plains with abundant grass' },
  { id: 'g-hf-07', mapId: 'gondwa', category: 'herb_food', name: 'Jungle Canopy Ferns', x: 1100, y: 3200, tags: ['fern'], description: 'High-growth ferns under jungle canopy' },
  { id: 'g-hf-08', mapId: 'gondwa', category: 'herb_food', name: 'Riverside Reeds', x: 2900, y: 2500, tags: ['water plant', 'reed'], description: 'Water plants along river banks' },
  { id: 'g-hf-09', mapId: 'gondwa', category: 'herb_food', name: 'Northern Meadow', x: 1800, y: 600, tags: ['grass'], description: 'Vast northern meadow' },
  { id: 'g-hf-10', mapId: 'gondwa', category: 'herb_food', name: 'Berry Hillside', x: 600, y: 1800, tags: ['berry'], description: 'Hillside covered in berry bushes' },
  { id: 'g-hf-11', mapId: 'gondwa', category: 'herb_food', name: 'Savanna Bush', x: 3300, y: 2000, tags: ['bush', 'grass'], description: 'Scattered bushes in savanna region' },
  { id: 'g-hf-12', mapId: 'gondwa', category: 'herb_food', name: 'Lakeside Reeds', x: 1900, y: 1750, tags: ['reed', 'water plant'], description: 'Reeds growing at lake edge' },
  { id: 'g-hf-13', mapId: 'gondwa', category: 'herb_food', name: 'Cycad Plateau', x: 2400, y: 1000, tags: ['cycad'], description: 'Cycads on elevated plateau' },
  { id: 'g-hf-14', mapId: 'gondwa', category: 'herb_food', name: 'Desert Fern Oasis', x: 3600, y: 1400, tags: ['fern'], description: 'Ferns surviving near desert edge' },
  { id: 'g-hf-15', mapId: 'gondwa', category: 'herb_food', name: 'Swamp Vegetation', x: 3500, y: 3300, tags: ['water plant', 'fern'], description: 'Rich vegetation in swamp area' },

  // ─── GONDWA – CARN FOOD ──────────────────────────────────────────────────────
  { id: 'g-cf-01', mapId: 'gondwa', category: 'carn_food', name: 'Fish Shoal – Great Lake', x: 2000, y: 1700, tags: ['fish'], description: 'Plentiful fish in the lake shallows' },
  { id: 'g-cf-02', mapId: 'gondwa', category: 'carn_food', name: 'River Fish Run', x: 3100, y: 2300, tags: ['fish'], description: 'Upstream fish migration corridor' },
  { id: 'g-cf-03', mapId: 'gondwa', category: 'carn_food', name: 'AI Dino Spawn – Savanna', x: 2700, y: 2600, tags: ['ai prey'], description: 'Small AI dinosaurs spawn here regularly' },
  { id: 'g-cf-04', mapId: 'gondwa', category: 'carn_food', name: 'AI Dino Spawn – Plains', x: 2200, y: 3000, tags: ['ai prey'], description: 'Open plains with regular prey spawns' },
  { id: 'g-cf-05', mapId: 'gondwa', category: 'carn_food', name: 'Coastal Fish – East', x: 3800, y: 2800, tags: ['fish'], description: 'Shallow coastal waters with fish' },
  { id: 'g-cf-06', mapId: 'gondwa', category: 'carn_food', name: 'Swamp Creatures', x: 3400, y: 3100, tags: ['ai prey'], description: 'Small creatures inhabit the swamp' },
  { id: 'g-cf-07', mapId: 'gondwa', category: 'carn_food', name: 'AI Dino Spawn – Jungle', x: 1000, y: 3100, tags: ['ai prey'], description: 'Dense jungle prey spawns' },
  { id: 'g-cf-08', mapId: 'gondwa', category: 'carn_food', name: 'Highland Prey Zone', x: 2900, y: 900, tags: ['ai prey'], description: 'Mountain prey in highland terrain' },

  // ─── GONDWA – MINERALS ──────────────────────────────────────────────────────
  { id: 'g-m-01', mapId: 'gondwa', category: 'mineral', name: 'Salt Lick – Central', x: 2150, y: 2100, description: 'High-traffic salt lick near lake' },
  { id: 'g-m-02', mapId: 'gondwa', category: 'mineral', name: 'Salt Lick – North', x: 1500, y: 700, description: 'Salt deposit in northern plains' },
  { id: 'g-m-03', mapId: 'gondwa', category: 'mineral', name: 'Salt Lick – Southwest', x: 900, y: 3400, description: 'Coastal salt flat' },
  { id: 'g-m-04', mapId: 'gondwa', category: 'mineral', name: 'Phosphorus Deposit', x: 3200, y: 1600, description: 'Rich phosphorus mineral vein' },
  { id: 'g-m-05', mapId: 'gondwa', category: 'mineral', name: 'Salt Flat – East Coast', x: 3700, y: 2200, description: 'Exposed salt flat along eastern coast' },
  { id: 'g-m-06', mapId: 'gondwa', category: 'mineral', name: 'Mineral Spring', x: 1700, y: 3200, description: 'Natural mineral spring' },

  // ─── GONDWA – NESTING ───────────────────────────────────────────────────────
  { id: 'g-n-01', mapId: 'gondwa', category: 'nesting', name: 'Safe Nesting Cove', x: 700, y: 1200, description: 'Hidden cove, excellent for nesting' },
  { id: 'g-n-02', mapId: 'gondwa', category: 'nesting', name: 'Hilltop Nest Site', x: 2500, y: 800, description: 'Elevated vantage point for safe nesting' },
  { id: 'g-n-03', mapId: 'gondwa', category: 'nesting', name: 'Dense Forest Nest', x: 1200, y: 2700, description: 'Well-concealed deep forest nesting area' },
  { id: 'g-n-04', mapId: 'gondwa', category: 'nesting', name: 'Rocky Outcrop Nest', x: 3000, y: 1500, description: 'Protected rocky ledge for nesting' },
  { id: 'g-n-05', mapId: 'gondwa', category: 'nesting', name: 'Riverside Nest', x: 2800, y: 2700, description: 'Flat river bank, good nesting spot' },
  { id: 'g-n-06', mapId: 'gondwa', category: 'nesting', name: 'Canyon Nest', x: 3500, y: 1000, description: 'Protected canyon walls' },

  // ─── GONDWA – LANDMARKS ─────────────────────────────────────────────────────
  { id: 'g-l-01', mapId: 'gondwa', category: 'landmark', name: 'The Great Crater', x: 2048, y: 1800, description: 'Massive impact crater forming the central lake' },
  { id: 'g-l-02', mapId: 'gondwa', category: 'landmark', name: 'Twin Peaks', x: 2900, y: 650, description: 'Distinctive twin mountain peaks' },
  { id: 'g-l-03', mapId: 'gondwa', category: 'landmark', name: 'Ancient Ruins', x: 1500, y: 3500, description: 'Crumbling stone structures' },
  { id: 'g-l-04', mapId: 'gondwa', category: 'landmark', name: 'Bone Fields', x: 3400, y: 2600, description: 'Dangerous zone, many fossils here' },
  { id: 'g-l-05', mapId: 'gondwa', category: 'landmark', name: 'The Canyon', x: 3500, y: 1200, description: 'Deep canyon running N–S' },
  { id: 'g-l-06', mapId: 'gondwa', category: 'landmark', name: 'Jungle Canopy', x: 1000, y: 3000, description: 'Impenetrable dense jungle zone' },
  { id: 'g-l-07', mapId: 'gondwa', category: 'landmark', name: 'Northern Cliffs', x: 1800, y: 400, description: 'Sheer northern cliff face' },
  { id: 'g-l-08', mapId: 'gondwa', category: 'landmark', name: 'Volcano Rock Field', x: 500, y: 600, description: 'Ancient volcanic rock formations' },

  // ─── PANJURA ─────────────────────────────────────────────────────────────────
  { id: 'p-w-01', mapId: 'panjura', category: 'water', name: 'Central River', x: 2048, y: 2048, description: 'Main river bisecting the map' },
  { id: 'p-w-02', mapId: 'panjura', category: 'water', name: 'Northern Lake', x: 1800, y: 900, description: 'Calm northern lake' },
  { id: 'p-w-03', mapId: 'panjura', category: 'water', name: 'South Wetlands', x: 2200, y: 3300, description: 'Flooded wetland region' },
  { id: 'p-hf-01', mapId: 'panjura', category: 'herb_food', name: 'Eastern Berry Patch', x: 3000, y: 1500, tags: ['berry'] },
  { id: 'p-hf-02', mapId: 'panjura', category: 'herb_food', name: 'Western Ferns', x: 900, y: 2200, tags: ['fern'] },
  { id: 'p-hf-03', mapId: 'panjura', category: 'herb_food', name: 'Cycad Forest', x: 1600, y: 2800, tags: ['cycad'] },
  { id: 'p-cf-01', mapId: 'panjura', category: 'carn_food', name: 'River Fish Spot', x: 2100, y: 2000, tags: ['fish'] },
  { id: 'p-cf-02', mapId: 'panjura', category: 'carn_food', name: 'Prey Spawn Plains', x: 2800, y: 2600, tags: ['ai prey'] },
  { id: 'p-m-01', mapId: 'panjura', category: 'mineral', name: 'Salt Lick Central', x: 2000, y: 2200 },
  { id: 'p-n-01', mapId: 'panjura', category: 'nesting', name: 'Forest Nest Site', x: 1300, y: 1600 },
  { id: 'p-n-02', mapId: 'panjura', category: 'nesting', name: 'Hilltop Nest', x: 2700, y: 900 },
  { id: 'p-l-01', mapId: 'panjura', category: 'landmark', name: 'The Spire', x: 2100, y: 1400, description: 'Tall rock spire, major landmark' },
  { id: 'p-l-02', mapId: 'panjura', category: 'landmark', name: 'Old Volcano', x: 3200, y: 800, description: 'Dormant volcano in the northeast' },
];
