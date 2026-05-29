"""
Generates a stylised 2048×2048 Gondwa map image using NumPy (vectorised).
Terrain zones match the resource coordinates used in the app
(origin = NW corner, x grows east, y grows south, full extent = 4096 units).
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

SIZE = 2048
rng  = np.random.default_rng(42)

# ── coordinate grids ───────────────────────────────────────────────────────────
gy, gx = np.mgrid[0:SIZE, 0:SIZE]
nx = gx / SIZE   # 0→1
ny = gy / SIZE   # 0→1

# ── procedural noise (simple, fast) ───────────────────────────────────────────
def value_noise(shape, scale, seed=0):
    rr = np.random.RandomState(seed)
    cells = max(2, int(scale))
    base  = rr.rand(cells + 2, cells + 2).astype(np.float32)
    iy    = np.linspace(0, cells, shape[0])
    ix    = np.linspace(0, cells, shape[1])
    iy0, ix0 = iy.astype(int), ix.astype(int)
    iy1       = np.minimum(iy0 + 1, cells + 1)
    ix1       = np.minimum(ix0 + 1, cells + 1)
    fy, fx    = (iy - iy0)[:, None], (ix - ix0)[None, :]
    # smooth step
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)
    v  = (base[iy0[:,None], ix0[None,:]] * (1-fx) * (1-fy) +
          base[iy0[:,None], ix1[None,:]] *    fx   * (1-fy) +
          base[iy1[:,None], ix0[None,:]] * (1-fx)  *    fy  +
          base[iy1[:,None], ix1[None,:]] *    fx   *    fy)
    return v

def fbm(shape, scale, octaves=5, seed=0):
    result = np.zeros(shape, dtype=np.float32)
    amp = 1.0
    total = 0.0
    for o in range(octaves):
        result += value_noise(shape, scale * (2**o), seed + o) * amp
        total  += amp
        amp    *= 0.5
    return result / total

height = fbm((SIZE, SIZE), scale=6, octaves=6, seed=1)
detail = fbm((SIZE, SIZE), scale=16, octaves=3, seed=99) * 0.25
height = np.clip(height + detail, 0, 1)

# ── zone masks ─────────────────────────────────────────────────────────────────
# lake: crater centred at (0.50, 0.43)
lx, ly  = 0.50, 0.43
lake_d  = np.hypot(nx - lx, ny - ly) / 0.13   # 1.0 = edge of lake

# biome gradients
jungle_w   = np.clip((0.28 - nx) / 0.28, 0, 1)
jungle_sw  = np.clip((ny - 0.55) / 0.45, 0, 1) * np.clip((0.32 - nx) / 0.32, 0, 1)
jungle_str = np.clip(jungle_w + jungle_sw * 1.2, 0, 1)

desert_str  = np.clip((nx - 0.78) / 0.22, 0, 1)
mountain_n  = np.clip((0.22 - ny) / 0.22, 0, 1)
mountain_ne = np.clip((nx - 0.62) / 0.38, 0, 1) * np.clip((0.35 - ny) / 0.35, 0, 1)
mountain_str = np.clip(mountain_n * 0.7 + mountain_ne * 0.9, 0, 1)
swamp_str    = np.clip((0.18 - nx) / 0.18, 0, 1) * np.clip((ny - 0.45) / 0.55, 0, 1)

# ── colour palette (RGB) ───────────────────────────────────────────────────────
DEEP_WATER = np.array([24,  64, 110], np.float32)
SHALLOW    = np.array([38,  96, 148], np.float32)
BEACH      = np.array([178, 160, 110], np.float32)
JUNGLE     = np.array([22,  68,  28], np.float32)
FOREST     = np.array([34,  90,  40], np.float32)
GRASS      = np.array([68, 118,  42], np.float32)
SAVANNA    = np.array([122, 138,  55], np.float32)
ARID       = np.array([155, 130,  68], np.float32)
DESERT     = np.array([188, 158,  88], np.float32)
ROCK       = np.array([90,  85,  80], np.float32)
SNOW       = np.array([210, 220, 225], np.float32)
MOUNTAIN   = np.array([105, 100,  90], np.float32)
MARSH      = np.array([40,  75,  45], np.float32)

def lerp(a, b, t):
    t = t[..., None]
    return a * (1 - t) + b * t

# Start with grass everywhere and blend biomes
t_center = np.clip((ny - 0.35) / 0.65, 0, 1)
canvas = lerp(GRASS, SAVANNA, t_center)

# Swamp (west)
sw_t = np.clip(swamp_str * 1.5, 0, 1)
canvas = lerp(canvas, lerp(MARSH, JUNGLE, np.clip(sw_t * 1.5, 0, 1)), sw_t * (sw_t > 0.3))

# Jungle
canvas = lerp(canvas, lerp(FOREST, JUNGLE, np.clip(jungle_str * 2 - 1, 0, 1)),
              np.clip(jungle_str, 0, 1) * (jungle_str > 0.1))

# Desert
canvas = lerp(canvas, lerp(ARID, DESERT, np.clip((desert_str - 0.5) * 2, 0, 1)),
              np.clip(desert_str, 0, 1) * (desert_str > 0.1))

# Mountains
high_t = np.clip((height - 0.70) / 0.30, 0, 1)
mtn_col = lerp(lerp(GRASS, ROCK, np.clip(mountain_str, 0, 1)), SNOW, high_t)
canvas = lerp(canvas, mtn_col, np.clip(mountain_str * 2, 0, 1) * (mountain_str > 0.25))

# Lake
canvas = lerp(canvas, lerp(DEEP_WATER, SHALLOW, np.clip(lake_d / 0.7, 0, 1)), (lake_d < 0.7).astype(np.float32))
shore_t = np.clip((lake_d - 0.7) / 0.3, 0, 1) ** 0.5
canvas = lerp(canvas, lerp(SHALLOW, BEACH, shore_t), ((lake_d >= 0.7) & (lake_d < 1.0)).astype(np.float32))

# Micro noise
micro = fbm((SIZE, SIZE), scale=32, octaves=2, seed=77) - 0.5
canvas = np.clip(canvas + micro[..., None] * 22, 0, 255).astype(np.uint8)

img = Image.fromarray(canvas, "RGB")
img = img.filter(ImageFilter.GaussianBlur(radius=1.0))

# ── paint rivers ───────────────────────────────────────────────────────────────
draw = ImageDraw.Draw(img)

def gc(mx, my):   # game coords → image pixels
    return int(mx / 4096 * SIZE), int(my / 4096 * SIZE)

draw.line([gc(3200,800),gc(3100,1200),gc(3050,1600),gc(3100,2100),gc(3200,2400)],
          fill=(38,96,148), width=5)
draw.line([gc(500,1600),gc(600,1900),gc(700,2200),gc(800,2600)],
          fill=(38,96,148), width=3)
draw.line([gc(1200,400),gc(1300,600),gc(1400,800)],
          fill=(38,96,148), width=3)
draw.line([gc(2800,1100),gc(2850,1200),gc(2800,1500)],
          fill=(38,96,148), width=4)

# ── vignette ───────────────────────────────────────────────────────────────────
vig = np.ones((SIZE, SIZE), np.float32)
cx2, cy2 = SIZE / 2, SIZE / 2
dist_v = np.hypot((gx - cx2) / cx2, (gy - cy2) / cy2)
vig = np.clip(1 - dist_v * 0.55, 0.25, 1.0)[..., None]
arr = np.array(img, np.float32) * vig
img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

# ── enhance ────────────────────────────────────────────────────────────────────
img = ImageEnhance.Sharpness(img).enhance(1.5)
img = ImageEnhance.Contrast(img).enhance(1.2)
img = ImageEnhance.Color(img).enhance(1.1)

out = "/home/user/Sproutbackup/pot-map/public/maps/gondwa.jpg"
img.save(out, "JPEG", quality=88)
print(f"Saved {SIZE}x{SIZE} → {out}")
