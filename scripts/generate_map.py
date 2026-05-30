"""
High-quality stylised top-down map generator for Path of Titans (Gondwa).

Technique: domain-warped fractal noise heightmap -> island landmass ->
hillshade relief -> elevation/moisture biome colouring -> carved rivers.
Hillshading (directional lighting on the heightmap) is what gives the
terrain a real, 3D cartographic look instead of a flat gradient.

Output: 2048x2048 JPEG aligned to the app's 4096-unit coordinate grid
(origin = NW corner, x east, y south).
"""
import os
import numpy as np
from PIL import Image, ImageFilter

SIZE = 2048

# ── value noise + fbm + domain warp ─────────────────────────────────────────────
def _value_noise(shape, cells, seed):
    rs = np.random.RandomState(seed)
    g = rs.rand(cells + 2, cells + 2).astype(np.float32)
    ys = np.linspace(0, cells, shape[0], endpoint=False)
    xs = np.linspace(0, cells, shape[1], endpoint=False)
    y0, x0 = ys.astype(int), xs.astype(int)
    y1, x1 = y0 + 1, x0 + 1
    fy = (ys - y0)[:, None]; fx = (xs - x0)[None, :]
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    return (g[y0[:,None], x0[None,:]] * (1-fx)*(1-fy) +
            g[y0[:,None], x1[None,:]] *    fx *(1-fy) +
            g[y1[:,None], x0[None,:]] * (1-fx)*   fy  +
            g[y1[:,None], x1[None,:]] *    fx *   fy)

def fbm(shape, base_cells=4, octaves=7, seed=0, persistence=0.5):
    out = np.zeros(shape, np.float32); amp = 1.0; tot = 0.0
    for o in range(octaves):
        out += _value_noise(shape, base_cells * (2 ** o), seed + o * 17) * amp
        tot += amp; amp *= persistence
    return out / tot

def warp(shape, seed):
    """Return warped coordinate fields for organic shapes."""
    wx = (fbm(shape, 3, 5, seed + 100) - 0.5) * 2
    wy = (fbm(shape, 3, 5, seed + 200) - 0.5) * 2
    return wx, wy

# ── build heightmap ─────────────────────────────────────────────────────────────
shape = (SIZE, SIZE)
gy, gx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
nx, ny = gx / SIZE, gy / SIZE

# domain-warped base terrain
wx, wy = warp(shape, seed=1)
base = fbm(shape, base_cells=4, octaves=8, seed=3)
warped = fbm(shape, base_cells=5, octaves=7, seed=3)  # second sample for variety
elev = 0.6 * base + 0.4 * warped
elev += (wx + wy) * 0.06  # nudge with warp fields

# island falloff: keep land in centre, water at edges (with noisy coastline)
cx, cy = 0.5, 0.5
d = np.sqrt(((nx - cx) * 1.05) ** 2 + ((ny - cy) * 1.0) ** 2) / 0.62
coast_noise = (fbm(shape, 6, 5, seed=42) - 0.5) * 0.35
d = d + coast_noise
falloff = np.clip(1.0 - d, 0.0, 1.0) ** 1.1
elev = elev * 0.55 + falloff * 0.55

# normalise 0..1
elev = (elev - elev.min()) / (elev.max() - elev.min())

SEA = 0.32  # sea level

# raise some mountains in the north/NE BEFORE carving the lake
mtn_mask = np.clip((0.30 - ny) / 0.30, 0, 1) * (0.5 + 0.5 * fbm(shape, 5, 6, seed=9))
mtn_ne   = np.clip((nx - 0.62) / 0.38, 0, 1) * np.clip((0.40 - ny) / 0.40, 0, 1)
elev = elev + (mtn_mask * 0.16 + mtn_ne * 0.20) * (elev > SEA)
elev = np.clip(elev, 0, 1)

# carve an IRREGULAR central lake (the Great Lake) at ~(0.50, 0.43).
# heavy domain warp on the radius makes the shoreline organic, not a circle.
lwx = (fbm(shape, 4, 5, seed=311) - 0.5) * 0.30
lwy = (fbm(shape, 4, 5, seed=312) - 0.5) * 0.30
lake_d = np.sqrt((nx - 0.50 + lwx) ** 2 + ((ny - 0.43 + lwy) * 1.15) ** 2) / 0.150
lake_d += (fbm(shape, 9, 4, seed=7) - 0.5) * 0.22
# smoothly pull elevation down toward a lake floor; gentle so no hard rim
lake_floor = 0.14 + np.clip(lake_d, 0, 1.3) * 0.16
elev = np.where(lake_d < 1.15, np.minimum(elev, lake_floor), elev)
elev = np.clip(elev, 0, 1)

# ── hillshade (relief lighting) ──────────────────────────────────────────────────
# smooth slightly before computing normals
eh = np.array(Image.fromarray((elev * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(1.5)), np.float32) / 255.0
dy, dx = np.gradient(eh)
zscale = 4.0
nx3 = -dx * zscale; ny3 = -dy * zscale; nz3 = np.ones_like(eh)
norm = np.sqrt(nx3**2 + ny3**2 + nz3**2)
nx3 /= norm; ny3 /= norm; nz3 /= norm
# light from NW, altitude ~55deg
az, alt = np.radians(315), np.radians(55)
lx = np.cos(alt) * np.cos(az); ly = np.cos(alt) * np.sin(az); lz = np.sin(alt)
shade = np.clip(nx3 * lx + ny3 * ly + nz3 * lz, 0, 1)
# gentle relief: keep within a tight band so no blown-out white highlights
shade = 0.72 + 0.34 * shade

# ── moisture (for biome variety) ─────────────────────────────────────────────────
moisture = fbm(shape, 4, 6, seed=23)

# ── biome colouring by elevation + moisture ──────────────────────────────────────
def col(c): return np.array(c, np.float32)
DEEP   = col([18,  48,  86]);  SHALLOW = col([40,  98, 138])
SAND   = col([182, 168, 120]); MARSH   = col([74,  96,  58])
GRASS  = col([88, 124,  56]);  GRASS2  = col([108, 138, 66])
FOREST = col([48,  86,  46]);  JUNGLE  = col([34,  72,  38])
HILL   = col([96, 110,  58]);  ROCK    = col([110, 104,  92])
SCREE  = col([138, 130, 120]); SNOW    = col([228, 234, 238])

rgb = np.zeros((SIZE, SIZE, 3), np.float32)

def band(lo, hi, ca, cb, extra=None):
    m = (elev >= lo) & (elev < hi)
    t = ((elev - lo) / (hi - lo))[..., None]
    c = ca * (1 - t) + cb * t
    if extra is not None:
        c = c + extra
    rgb[m] = c[m]

# water
deep_t = np.clip((SEA - elev) / SEA, 0, 1)[..., None]
water_c = DEEP * deep_t + SHALLOW * (1 - deep_t)
wm = elev < SEA
rgb[wm] = water_c[wm]

# beach (thin, only true coastline)
band(SEA, SEA + 0.022, SAND, GRASS2)

# lowlands: grass<->forest by moisture
low = (elev >= SEA + 0.022) & (elev < 0.62)
mt = moisture[..., None]
veg = GRASS2 * (1 - mt) + FOREST * mt
# wetter + lower -> jungle/marsh in the south-west
sw = (np.clip((ny - 0.5), 0, 1) * np.clip((0.4 - nx), 0, 1))[..., None]
veg = veg * (1 - sw * 1.5).clip(0,1) + JUNGLE * (sw * 1.5).clip(0,1)
rgb[low] = veg[low]

# highlands (start higher so normal land stays green)
band(0.62, 0.72, GRASS, HILL)
band(0.72, 0.82, HILL, ROCK)
band(0.82, 0.91, ROCK, SCREE)
band(0.91, 1.01, SCREE, SNOW)

# micro colour noise for texture
micro = (fbm(shape, 16, 3, seed=55) - 0.5)[..., None]
rgb = rgb + micro * 16

# apply hillshade (multiply) — but keep water flat & calm
shade3 = shade[..., None]
land = (elev >= SEA)[..., None]
rgb = np.where(land, rgb * shade3, rgb * (0.94 + 0.06 * shade3))
rgb = np.clip(rgb, 0, 255)

img = Image.fromarray(rgb.astype(np.uint8), "RGB")

# ── rivers: trace downhill from a few sources ────────────────────────────────────
from PIL import ImageDraw
draw = ImageDraw.Draw(img, "RGBA")

def descend(sx, sy, steps=1400):
    pts = []
    x, y = float(sx), float(sy)
    for _ in range(steps):
        ix, iy = int(x), int(y)
        if ix < 2 or iy < 2 or ix >= SIZE - 2 or iy >= SIZE - 2:
            break
        if eh[iy, ix] < SEA - 0.01:  # reached water
            pts.append((x, y)); break
        gxv = eh[iy, ix + 1] - eh[iy, ix - 1]
        gyv = eh[iy + 1, ix] - eh[iy - 1, ix]
        mag = np.hypot(gxv, gyv) + 1e-6
        x -= gxv / mag * 1.6
        y -= gyv / mag * 1.6
        pts.append((x, y))
    return pts

rng = np.random.RandomState(2024)
# pick elevated points as river sources
hi_idx = np.argwhere(eh > 0.58)
if len(hi_idx) > 0:
    for _ in range(40):
        sy, sx = hi_idx[rng.randint(len(hi_idx))]
        pts = descend(sx, sy)
        if len(pts) > 60:  # only keep long rivers
            for i in range(1, len(pts)):
                w = 2 + int(5 * i / len(pts))
                draw.line([pts[i-1], pts[i]], fill=(46, 104, 144, 200), width=w)

img = img.filter(ImageFilter.GaussianBlur(0.6))

# subtle dark vignette so it blends into the app's dark theme
vy, vx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
vd = np.sqrt(((vx - SIZE/2)/(SIZE/2))**2 + ((vy - SIZE/2)/(SIZE/2))**2)
vig = np.clip(1 - (vd - 0.85) * 1.4, 0.35, 1.0)[..., None]
arr = np.clip(np.array(img, np.float32) * vig, 0, 255).astype(np.uint8)
img = Image.fromarray(arr)

out = os.path.join(os.path.dirname(__file__), "../public/maps/gondwa.jpg")
img.save(out, "JPEG", quality=90)
print(f"Saved {SIZE}x{SIZE} -> {out}")
