"""
Calibrate titanmap food coordinates onto the zKlau real terrain.

Anchor feature: the Great Lake (large INLAND water body), unambiguous in
both maps. Strategy:
  1. In each map, build a water mask, flood-fill from the borders to drop
     the ocean/background, then take the largest remaining interior blob
     = the Great Lake. Record its centroid and bounding box (normalised).
  2. Derive a similarity transform (uniform scale + translate) mapping the
     titanmap frame onto the zKlau frame so the two lakes coincide.
  3. Apply it to every food coord and write a calibration JSON.
"""
import json, collections
import numpy as np
from PIL import Image

DET = 512  # detection resolution

def load(path):
    im = Image.open(path).convert('RGB').resize((DET, DET))
    return np.asarray(im).astype(int)

def water_mask(a, titan):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    if titan:
        # teal water on near-white land
        return (b > 110) & (g > 110) & (r < 160) & (b >= r) & (g >= r - 10) & ~((r > 200) & (g > 200) & (b > 200))
    # zKlau: bluish ocean/lake
    return (b > r + 6) & (b > 70)

def drop_border(mask):
    """Remove components of mask that touch the image border (the ocean)."""
    H, W = mask.shape
    keep = mask.copy()
    seen = np.zeros_like(mask, bool)
    dq = collections.deque()
    for x in range(W):
        for y in (0, H - 1):
            if mask[y, x] and not seen[y, x]:
                seen[y, x] = True; dq.append((y, x))
    for y in range(H):
        for x in (0, W - 1):
            if mask[y, x] and not seen[y, x]:
                seen[y, x] = True; dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y+dy, x+dx
            if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; dq.append((ny, nx))
    keep[seen] = False  # seen == border-connected (ocean)
    return keep

def largest_blob(mask):
    H, W = mask.shape
    seen = np.zeros_like(mask, bool)
    best = None; best_n = 0
    for sy in range(H):
        for sx in range(W):
            if mask[sy, sx] and not seen[sy, sx]:
                dq = collections.deque([(sy, sx)]); seen[sy, sx] = True
                pts = []
                while dq:
                    y, x = dq.popleft(); pts.append((y, x))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = y+dy, x+dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; dq.append((ny, nx))
                if len(pts) > best_n:
                    best_n = len(pts); best = pts
    ys = np.array([p[0] for p in best]); xs = np.array([p[1] for p in best])
    return dict(cx=xs.mean()/W, cy=ys.mean()/H,
                w=(xs.max()-xs.min())/W, h=(ys.max()-ys.min())/H, n=best_n)

def great_lake(path, titan):
    a = load(path)
    m = water_mask(a, titan)
    m = drop_border(m)
    return largest_blob(m)

tl = great_lake('/tmp/titan_map.png', titan=True)
zl = great_lake('/tmp/gondwa_z4.jpg', titan=False)
print('titan lake:', {k: round(v,4) for k,v in tl.items()})
print('zklau lake:', {k: round(v,4) for k,v in zl.items()})

# uniform scale from lake bbox (average of w,h ratios), normalised frames
sx = zl['w'] / tl['w']
sy = zl['h'] / tl['h']
s = (sx + sy) / 2
print(f'scale x={sx:.3f} y={sy:.3f} -> uniform {s:.3f}')

cal = dict(
    tcx=tl['cx'], tcy=tl['cy'],   # titan lake centroid (normalised 0..1)
    zcx=zl['cx'], zcy=zl['cy'],   # zklau lake centroid (normalised 0..1)
    s=s,
)
json.dump(cal, open('/tmp/cal.json', 'w'))
print('calibration:', {k: round(v,4) for k,v in cal.items()})
