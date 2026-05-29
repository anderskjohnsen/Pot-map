export type ResourceCategory =
  | 'herb_food'
  | 'carn_food'
  | 'water'
  | 'mineral'
  | 'nesting'
  | 'landmark';

export type MapId = 'gondwa' | 'panjura';

export interface Resource {
  id: string;
  name: string;
  category: ResourceCategory;
  mapId: MapId;
  x: number; // normalized 0–4096
  y: number; // normalized 0–4096
  description?: string;
  tags?: string[];
}

export interface CategoryMeta {
  label: string;
  color: string;
  icon: string;
}

export const CATEGORY_META: Record<ResourceCategory, CategoryMeta> = {
  herb_food: { label: 'Herb Food', color: '#4ade80', icon: '🌿' },
  carn_food: { label: 'Carn Food', color: '#f87171', icon: '🦴' },
  water:     { label: 'Water',     color: '#60a5fa', icon: '💧' },
  mineral:   { label: 'Minerals',  color: '#facc15', icon: '🪨' },
  nesting:   { label: 'Nesting',   color: '#f0abfc', icon: '🥚' },
  landmark:  { label: 'Landmark',  color: '#94a3b8', icon: '📍' },
};

export const MAP_LABELS: Record<MapId, string> = {
  gondwa: 'Gondwa',
  panjura: 'Panjura',
};
