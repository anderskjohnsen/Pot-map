"""
Download a zKlau/PathOfTitansMapsTiles zoom level and stitch it into a
single image. Tiles are 256x256 in a standard XYZ quadtree
(z4 = 16x16 = 4096x4096). Saves both an XYZ stitch and a TMS (y-flipped)
stitch so we can pick whichever is right-side-up.
"""
import sys, io, urllib.request, concurrent.futures as cf
from PIL import Image

MAP = sys.argv[1] if len(sys.argv) > 1 else 'Gondwa'
Z   = int(sys.argv[2]) if len(sys.argv) > 2 else 4
N   = 2 ** Z
TS  = 256
BASE = f'https://raw.githubusercontent.com/zKlau/PathOfTitansMapsTiles/main/{MAP}Tiles/{Z}'

def fetch(xy):
    x, y = xy
    url = f'{BASE}/{x}/{y}.webp'
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return (x, y, r.read())
    except Exception:
        return (x, y, None)

coords = [(x, y) for x in range(N) for y in range(N)]
canvas = Image.new('RGB', (N * TS, N * TS), (13, 15, 22))
got = 0
with cf.ThreadPoolExecutor(max_workers=16) as ex:
    for x, y, data in ex.map(fetch, coords):
        if not data:
            continue
        try:
            tile = Image.open(io.BytesIO(data)).convert('RGB')
        except Exception:
            continue
        canvas.paste(tile, (x * TS, y * TS))  # XYZ: y grows downward
        got += 1

out = f'/tmp/{MAP.lower()}_z{Z}.jpg'
canvas.save(out, 'JPEG', quality=90)
print(f'{MAP} z{Z}: stitched {got}/{len(coords)} tiles -> {out} ({canvas.size})')
