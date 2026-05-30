import type { ResourceCategory, MapId } from '../types';
import { CATEGORY_META, MAP_LABELS } from '../types';

interface Props {
  activeMap: MapId;
  onMapChange: (map: MapId) => void;
  activeCategories: Set<ResourceCategory>;
  onToggleCategory: (cat: ResourceCategory) => void;
  counts: Partial<Record<ResourceCategory, number>>;
  search: string;
  onSearchChange: (v: string) => void;
  totalVisible: number;
  onClose?: () => void;
}

const ALL_CATEGORIES = Object.keys(CATEGORY_META) as ResourceCategory[];
const ALL_MAPS = Object.keys(MAP_LABELS) as MapId[];

export default function FilterPanel({
  activeMap, onMapChange,
  activeCategories, onToggleCategory,
  counts, search, onSearchChange, totalVisible, onClose,
}: Props) {
  return (
    <aside className="w-72 h-full shrink-0 bg-gray-900 border-r border-gray-700 flex flex-col overflow-y-auto overflow-x-hidden">
      {/* Header */}
      <div className="p-4 border-b border-gray-700 bg-gray-800 flex items-start justify-between">
        <div>
          <h1 className="text-lg font-bold text-white tracking-wide">🦕 PoT Map</h1>
          <p className="text-xs text-gray-400 mt-0.5">Path of Titans Resource Finder</p>
        </div>
        {onClose && (
          <button onClick={onClose} className="md:hidden text-gray-400 hover:text-white p-1 ml-2 mt-0.5" aria-label="Close">
            <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="2" y1="2" x2="16" y2="16"/><line x1="16" y1="2" x2="2" y2="16"/>
            </svg>
          </button>
        )}
      </div>

      {/* Map selector */}
      <div className="p-4 border-b border-gray-700">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Map</p>
        <div className="flex gap-2">
          {ALL_MAPS.map(m => (
            <button
              key={m}
              onClick={() => onMapChange(m)}
              className={`flex-1 py-1.5 rounded text-sm font-medium transition-colors ${
                activeMap === m
                  ? 'bg-emerald-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {MAP_LABELS[m]}
            </button>
          ))}
        </div>
      </div>

      {/* Search */}
      <div className="p-4 border-b border-gray-700">
        <input
          type="text"
          placeholder="Search resources…"
          value={search}
          onChange={e => onSearchChange(e.target.value)}
          className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-emerald-500"
        />
      </div>

      {/* Category filters */}
      <div className="p-4 border-b border-gray-700">
        <div className="flex items-center justify-between mb-2">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Categories</p>
          <button
            onClick={() => ALL_CATEGORIES.forEach(c => !activeCategories.has(c) && onToggleCategory(c))}
            className="text-xs text-emerald-400 hover:text-emerald-300"
          >
            All
          </button>
        </div>
        <div className="space-y-1">
          {ALL_CATEGORIES.map(cat => {
            const meta = CATEGORY_META[cat];
            const count = counts[cat] ?? 0;
            const active = activeCategories.has(cat);
            return (
              <button
                key={cat}
                onClick={() => onToggleCategory(cat)}
                className={`w-full flex items-center gap-2 px-2 py-1.5 rounded text-sm transition-all ${
                  active
                    ? 'bg-gray-700 text-white'
                    : 'text-gray-500 hover:text-gray-300'
                }`}
              >
                <span
                  className="w-3 h-3 rounded-full shrink-0"
                  style={{ background: active ? meta.color : '#4b5563' }}
                />
                <span className="flex-1 text-left">{meta.icon} {meta.label}</span>
                <span className={`text-xs tabular-nums ${active ? 'text-gray-400' : 'text-gray-600'}`}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Footer count */}
      <div className="mt-auto p-4">
        <p className="text-xs text-gray-500 text-center">
          Showing <span className="text-emerald-400 font-semibold">{totalVisible}</span> markers
        </p>
      </div>
    </aside>
  );
}
