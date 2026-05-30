import { useState, useMemo } from 'react';
import FilterPanel from './components/FilterPanel';
import GameMap from './components/GameMap';
import { resources as allResources } from './data/resources';
import type { ResourceCategory, MapId } from './types';
import { CATEGORY_META } from './types';

const ALL_CATEGORIES = new Set(Object.keys(CATEGORY_META) as ResourceCategory[]);

export default function App() {
  const [activeMap, setActiveMap] = useState<MapId>('gondwa');
  const [activeCategories, setActiveCategories] = useState<Set<ResourceCategory>>(new Set(ALL_CATEGORIES));
  const [search, setSearch] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleCategory = (cat: ResourceCategory) => {
    setActiveCategories(prev => {
      const next = new Set(prev);
      if (next.has(cat)) next.delete(cat);
      else next.add(cat);
      return next;
    });
  };

  const mapResources = useMemo(
    () => allResources.filter(r => r.mapId === activeMap),
    [activeMap],
  );

  const counts = useMemo(() => {
    const c: Partial<Record<ResourceCategory, number>> = {};
    for (const r of mapResources) c[r.category] = (c[r.category] ?? 0) + 1;
    return c;
  }, [mapResources]);

  const visibleResources = useMemo(() => {
    const q = search.toLowerCase();
    return mapResources.filter(r => {
      if (!activeCategories.has(r.category)) return false;
      if (q && !r.name.toLowerCase().includes(q) && !r.tags?.some(t => t.includes(q))) return false;
      return true;
    });
  }, [mapResources, activeCategories, search]);

  return (
    <div className="relative flex h-screen w-screen overflow-hidden bg-gray-950 text-white">

      {/* ── Desktop: static sidebar ── Mobile: overlay sidebar ── */}
      {/* Backdrop (mobile only) */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-30 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed md:static inset-y-0 left-0 z-40
        transform transition-transform duration-200
        md:transform-none
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}>
        <FilterPanel
          activeMap={activeMap}
          onMapChange={m => { setActiveMap(m); setSearch(''); setSidebarOpen(false); }}
          activeCategories={activeCategories}
          onToggleCategory={toggleCategory}
          counts={counts}
          search={search}
          onSearchChange={setSearch}
          totalVisible={visibleResources.length}
          onClose={() => setSidebarOpen(false)}
        />
      </div>

      {/* Map (always full area on mobile) */}
      <div className="flex-1 relative">
        <GameMap resources={visibleResources} activeMap={activeMap} />

        {/* Hamburger toggle (mobile only) */}
        <button
          className="absolute top-3 left-3 z-20 md:hidden bg-gray-900/90 border border-gray-700 rounded-lg p-2.5 text-white shadow-lg"
          onClick={() => setSidebarOpen(true)}
          aria-label="Open filters"
        >
          <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <line x1="2" y1="5"  x2="18" y2="5"/>
            <line x1="2" y1="10" x2="18" y2="10"/>
            <line x1="2" y1="15" x2="18" y2="15"/>
          </svg>
        </button>
      </div>
    </div>
  );
}
