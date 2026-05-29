import L from 'leaflet';
import type { ResourceCategory } from '../types';
import { CATEGORY_META } from '../types';

const iconCache = new Map<string, L.DivIcon>();

export function getCategoryIcon(category: ResourceCategory, highlighted = false): L.DivIcon {
  const key = `${category}-${highlighted}`;
  if (iconCache.has(key)) return iconCache.get(key)!;

  const meta = CATEGORY_META[category];
  const size = highlighted ? 36 : 28;
  const border = highlighted ? `3px solid white` : `2px solid rgba(0,0,0,0.4)`;
  const shadow = highlighted ? '0 0 10px rgba(255,255,255,0.8)' : '0 2px 4px rgba(0,0,0,0.5)';

  const icon = L.divIcon({
    className: '',
    html: `<div style="
      width:${size}px;height:${size}px;
      background:${meta.color};
      border-radius:50% 50% 50% 0;
      transform:rotate(-45deg);
      border:${border};
      box-shadow:${shadow};
      display:flex;align-items:center;justify-content:center;
    "><span style="transform:rotate(45deg);font-size:${size * 0.5}px;line-height:1">${meta.icon}</span></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size],
    popupAnchor: [0, -size],
  });

  iconCache.set(key, icon);
  return icon;
}
