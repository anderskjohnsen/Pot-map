import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import 'leaflet.markercluster';
import type { Resource, MapId } from '../types';
import { CATEGORY_META } from '../types';
import { getCategoryIcon } from './markerIcons';

// Logical coordinate space (matches resource data)
const MAP_SIZE = 4096;

const MAP_IMAGES: Record<MapId, string> = {
  gondwa:  '/maps/gondwa.jpg',
  panjura: '/maps/panjura.jpg',
};

interface Props {
  resources: Resource[];
  activeMap: MapId;
}

type MCG = L.MarkerClusterGroup;

export default function GameMap({ resources, activeMap }: Props) {
  const containerRef   = useRef<HTMLDivElement>(null);
  const mapRef         = useRef<L.Map | null>(null);
  const clusterRef     = useRef<MCG | null>(null);
  const overlayRef     = useRef<L.ImageOverlay | null>(null);
  const [loading, setLoading] = useState(true);

  // Init Leaflet map once
  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const bounds: L.LatLngBoundsLiteral = [[0, 0], [MAP_SIZE, MAP_SIZE]];

    const map = L.map(containerRef.current, {
      crs: L.CRS.Simple,
      minZoom: -3,
      maxZoom: 3,
      maxBounds: [[-MAP_SIZE * 0.2, -MAP_SIZE * 0.2], [MAP_SIZE * 1.2, MAP_SIZE * 1.2]],
      zoomSnap: 0.5,
      attributionControl: false,
    });

    map.fitBounds(bounds);

    const overlay = L.imageOverlay(MAP_IMAGES[activeMap], bounds).addTo(map);
    overlay.on('load',  () => setLoading(false));
    overlay.on('error', () => setLoading(false));

    const cluster = (L as unknown as { markerClusterGroup: (o?: object) => MCG })
      .markerClusterGroup({
        maxClusterRadius: 50,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false,
        iconCreateFunction: (c: L.MarkerCluster) =>
          L.divIcon({
            html: `<div style="
              background:rgba(20,24,36,0.92);
              border:2px solid #4ade80;
              color:#f3f4f6;
              border-radius:50%;
              width:36px;height:36px;
              display:flex;align-items:center;justify-content:center;
              font-size:13px;font-weight:700;
              box-shadow:0 2px 8px rgba(0,0,0,0.6);
            ">${c.getChildCount()}</div>`,
            className: '',
            iconSize: [36, 36],
          }),
      });

    map.addLayer(cluster);
    mapRef.current    = map;
    clusterRef.current = cluster;
    overlayRef.current = overlay;

    return () => {
      map.remove();
      mapRef.current = clusterRef.current = overlayRef.current = null;
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Swap map image on map change
  useEffect(() => {
    if (!overlayRef.current) return;
    setLoading(true);
    overlayRef.current.setUrl(MAP_IMAGES[activeMap]);
    overlayRef.current.on('load',  () => setLoading(false));
    overlayRef.current.on('error', () => setLoading(false));
  }, [activeMap]);

  // Sync markers
  useEffect(() => {
    const cluster = clusterRef.current;
    if (!cluster) return;

    cluster.clearLayers();

    resources.forEach(r => {
      const meta   = CATEGORY_META[r.category];
      const marker = L.marker([MAP_SIZE - r.y, r.x], {
        icon:  getCategoryIcon(r.category),
        title: r.name,
      });

      const tagsHtml = r.tags?.length
        ? `<div class="pot-tags">${r.tags.map(t => `<span class="pot-tag">${t}</span>`).join('')}</div>`
        : '';

      marker.bindPopup(
        `<div class="pot-popup">
          <div class="pot-popup-header" style="background:${meta.color}20;border-left:4px solid ${meta.color}">
            <span class="pot-popup-icon">${meta.icon}</span>
            <div>
              <div class="pot-popup-name">${r.name}</div>
              <div class="pot-popup-cat">${meta.label}</div>
            </div>
          </div>
          ${r.description ? `<p class="pot-popup-desc">${r.description}</p>` : ''}
          ${tagsHtml}
        </div>`,
        { maxWidth: 240 },
      );

      cluster.addLayer(marker);
    });
  }, [resources]);

  return (
    <div className="relative flex-1 h-full">
      <div ref={containerRef} className="w-full h-full" />
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-950 bg-opacity-70 z-[1000] pointer-events-none">
          <div className="flex flex-col items-center gap-3">
            <div className="w-8 h-8 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin" />
            <span className="text-sm text-gray-300">Loading map…</span>
          </div>
        </div>
      )}
    </div>
  );
}
