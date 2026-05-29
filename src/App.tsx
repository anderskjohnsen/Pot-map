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
    <div className="flex h-screen w-screen overflow-hidden bg-gray-950 text-white">
      <FilterPanel
        activeMap={activeMap}
        onMapChange={m => { setActiveMap(m); setSearch(''); }}
        activeCategories={activeCategories}
        onToggleCategory={toggleCategory}
        counts={counts}
        search={search}
        onSearchChange={setSearch}
        totalVisible={visibleResources.length}
      />
      <GameMap resources={visibleResources} activeMap={activeMap} />
    </div>
  );
}
