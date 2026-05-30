"""
High-quality stylised top-down map for Path of Titans (Panjura).
Same hillshade-relief engine as generate_map.py, tuned for Panjura:
a large central river valley, a northern lake, southern wetlands,
mountains in the NW and red-rock highlands in the NE.

Output: 2048x2048 JPEG on the 4096-unit coordinate grid.
"""
import os
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

SIZE = 2048

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

shape = (SIZE, SIZE)
gy, gx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
nx, ny = gx / SIZE, gy / SIZE

base = fbm(shape, 4, 8, seed=71)
warped = fbm(shape, 5, 7, seed=88)
elev = 0.6 * base + 0.4 * warped

# island falloff (Panjura is a touch taller than wide)
d = np.sqrt(((nx - 0.5) * 1.0) ** 2 + ((ny - 0.5) * 0.95) ** 2) / 0.64
d = d + (fbm(shape, 6, 5, seed=142) - 0.5) * 0.35
falloff = np.clip(1.0 - d, 0.0, 1.0) ** 1.1
elev = elev * 0.55 + falloff * 0.55
elev = (elev - elev.min()) / (elev.max() - elev.min())

SEA = 0.32

# mountains NW + red-rock highlands NE
mtn_nw = np.clip((0.28 - nx) / 0.28, 0, 1) * np.clip((0.32 - ny) / 0.32, 0, 1)
rock_ne = np.clip((nx - 0.58) / 0.42, 0, 1) * np.clip((0.42 - ny) / 0.42, 0, 1)
elev = elev + (mtn_nw * 0.24 + rock_ne * 0.16) * (elev > SEA)
elev = np.clip(elev, 0, 1)

# northern lake at (0.44, 0.22)
ld = np.sqrt((nx - 0.44) ** 2 + ((ny - 0.22) * 1.1) ** 2) / 0.10
ld += (fbm(shape, 9, 4, seed=33) - 0.5) * 0.20
elev = np.where(ld < 1.1, np.minimum(elev, 0.15 + np.clip(ld,0,1.2) * 0.15), elev)

# southern wetland basin at (0.54, 0.80)
wd = np.sqrt((nx - 0.54) ** 2 + ((ny - 0.80) * 1.1) ** 2) / 0.13
wd += (fbm(shape, 8, 4, seed=44) - 0.5) * 0.22
elev = np.where(wd < 1.1, np.minimum(elev, 0.24 + np.clip(wd,0,1.2) * 0.10), elev)

# central river valley: lower a vertical corridor near nx=0.5
rx = np.abs(nx - (0.50 + (fbm(shape, 3, 4, seed=66)[:, :] - 0.5) * 0.12))
valley = np.clip((0.05 - rx) / 0.05, 0, 1)
elev = elev - valley * 0.12 * (elev > SEA)
elev = np.clip(elev, 0, 1)

# ── hillshade ─────────────────────────────────────────────────────────────────
eh = np.array(Image.fromarray((elev * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(1.5)), np.float32) / 255.0
dy, dx = np.gradient(eh)
zscale = 4.0
nx3 = -dx * zscale; ny3 = -dy * zscale; nz3 = np.ones_like(eh)
norm = np.sqrt(nx3**2 + ny3**2 + nz3**2)
nx3 /= norm; ny3 /= norm; nz3 /= norm
az, alt = np.radians(315), np.radians(55)
lx = np.cos(alt)*np.cos(az); ly = np.cos(alt)*np.sin(az); lz = np.sin(alt)
shade = np.clip(nx3*lx + ny3*ly + nz3*lz, 0, 1)
shade = 0.72 + 0.34 * shade

moisture = fbm(shape, 4, 6, seed=123)

def col(c): return np.array(c, np.float32)
DEEP   = col([18,  48,  86]);  SHALLOW = col([40,  98, 138])
SAND   = col([186, 168, 116]); WET     = col([60,  92,  64])
DGRASS = col([132, 132,  68]); GRASS   = col([96, 124,  58])
SHRUB  = col([108, 120,  62]); FOREST  = col([54,  88,  50])
REDROCK= col([150,  92,  60]); HILL    = col([110, 102,  64])
ROCK   = col([116, 104,  92]); SCREE   = col([140, 130, 118]); SNOW = col([228,234,238])

rgb = np.zeros((SIZE, SIZE, 3), np.float32)

def band(lo, hi, ca, cb):
    m = (elev >= lo) & (elev < hi)
    t = ((elev - lo) / (hi - lo))[..., None]
    rgb[m] = (ca * (1 - t) + cb * t)[m]

# water
deep_t = np.clip((SEA - elev) / SEA, 0, 1)[..., None]
wm = elev < SEA
rgb[wm] = (DEEP * deep_t + SHALLOW * (1 - deep_t))[wm]

band(SEA, SEA + 0.022, SAND, DGRASS)

# lowlands: dry-grass / shrub, wetter -> forest; south basin -> wetland
low = (elev >= SEA + 0.022) & (elev < 0.62)
mt = moisture[..., None]
veg = DGRASS * (1 - mt) + FOREST * mt
veg = veg * 0.6 + GRASS * 0.4
swet = (np.clip((ny - 0.65), 0, 1) * np.clip(1 - np.abs(nx - 0.54) / 0.28, 0, 1))[..., None]
veg = veg * (1 - swet).clip(0,1) + WET * swet.clip(0,1)
# red-rock tint in NE
rr = (np.clip((nx - 0.58)/0.42,0,1) * np.clip((0.42-ny)/0.42,0,1))[..., None]
veg = veg * (1 - rr*0.8).clip(0,1) + REDROCK * (rr*0.8).clip(0,1)
rgb[low] = veg[low]

band(0.62, 0.72, GRASS, HILL)
band(0.72, 0.82, HILL, ROCK)
band(0.82, 0.91, ROCK, SCREE)
band(0.91, 1.01, SCREE, SNOW)

micro = (fbm(shape, 16, 3, seed=200) - 0.5)[..., None]
rgb = rgb + micro * 16

shade3 = shade[..., None]
land = (elev >= SEA)[..., None]
rgb = np.where(land, rgb * shade3, rgb * (0.94 + 0.06 * shade3))
rgb = np.clip(rgb, 0, 255)

img = Image.fromarray(rgb.astype(np.uint8), "RGB")

# rivers
draw = ImageDraw.Draw(img, "RGBA")
def descend(sx, sy, steps=1400):
    pts = []; x, y = float(sx), float(sy)
    for _ in range(steps):
        ix, iy = int(x), int(y)
        if ix < 2 or iy < 2 or ix >= SIZE-2 or iy >= SIZE-2: break
        if eh[iy, ix] < SEA - 0.01: pts.append((x, y)); break
        gxv = eh[iy, ix+1] - eh[iy, ix-1]; gyv = eh[iy+1, ix] - eh[iy-1, ix]
        mag = np.hypot(gxv, gyv) + 1e-6
        x -= gxv/mag*1.6; y -= gyv/mag*1.6; pts.append((x, y))
    return pts

rng = np.random.RandomState(909)
hi_idx = np.argwhere(eh > 0.58)
if len(hi_idx):
    for _ in range(40):
        sy, sx = hi_idx[rng.randint(len(hi_idx))]
        pts = descend(sx, sy)
        if len(pts) > 60:
            for i in range(1, len(pts)):
                w = 2 + int(5 * i / len(pts))
                draw.line([pts[i-1], pts[i]], fill=(46, 104, 144, 200), width=w)

img = img.filter(ImageFilter.GaussianBlur(0.6))

vy, vx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
vd = np.sqrt(((vx-SIZE/2)/(SIZE/2))**2 + ((vy-SIZE/2)/(SIZE/2))**2)
vig = np.clip(1 - (vd - 0.85) * 1.4, 0.35, 1.0)[..., None]
arr = np.clip(np.array(img, np.float32) * vig, 0, 255).astype(np.uint8)
img = Image.fromarray(arr)

out = os.path.join(os.path.dirname(__file__), "../public/maps/panjura.jpg")
img.save(out, "JPEG", quality=90)
print(f"Saved {SIZE}x{SIZE} -> {out}")
