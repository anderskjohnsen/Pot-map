export type ResourceCategory =
  | 'acorn'
  | 'lychee'
  | 'amanita'
  | 'milkcap'
  | 'tigernut'
  | 'root';

export type MapId = 'gondwa';

export interface Resource {
  id: string;
  name: string;
  category: ResourceCategory;
  mapId: MapId;
  x: number; // 0–4096 grid, origin NW, x east
  y: number; // 0–4096 grid, origin NW, y south
  description?: string;
  tags?: string[];
}

export interface CategoryMeta {
  label: string;
  color: string;
  icon: string;
}

export const CATEGORY_META: Record<ResourceCategory, CategoryMeta> = {
  acorn:    { label: 'Acorn',    color: '#c2843f', icon: '🌰' },
  lychee:   { label: 'Lychee',   color: '#e0457b', icon: '🍒' },
  amanita:  { label: 'Amanita',  color: '#ef4444', icon: '🍄' },
  milkcap:  { label: 'Milkcap',  color: '#f59e0b', icon: '🍄' },
  tigernut: { label: 'Tigernut', color: '#a3a31f', icon: '🥜' },
  root:     { label: 'Root',     color: '#b06b3a', icon: '🥕' },
};

export const MAP_LABELS: Record<MapId, string> = {
  gondwa: 'Gondwa',
};
