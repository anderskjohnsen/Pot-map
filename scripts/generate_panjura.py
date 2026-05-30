"""Generate a stylised Panjura map image (2048×2048)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

SIZE = 2048
gy, gx = np.mgrid[0:SIZE, 0:SIZE]
nx = gx / SIZE
ny = gy / SIZE

def value_noise(shape, scale, seed=0):
    rr = np.random.RandomState(seed)
    cells = max(2, int(scale))
    base  = rr.rand(cells + 2, cells + 2).astype(np.float32)
    iy    = np.linspace(0, cells, shape[0])
    ix    = np.linspace(0, cells, shape[1])
    iy0, ix0 = iy.astype(int), ix.astype(int)
    iy1   = np.minimum(iy0 + 1, cells + 1)
    ix1   = np.minimum(ix0 + 1, cells + 1)
    fy, fx = (iy - iy0)[:, None], (ix - ix0)[None, :]
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)
    return (base[iy0[:,None], ix0[None,:]] * (1-fx) * (1-fy) +
            base[iy0[:,None], ix1[None,:]] *    fx   * (1-fy) +
            base[iy1[:,None], ix0[None,:]] * (1-fx)  *    fy  +
            base[iy1[:,None], ix1[None,:]] *    fx   *    fy)

def fbm(shape, scale, octaves=5, seed=0):
    result = np.zeros(shape, np.float32)
    amp = 1.0; total = 0.0
    for o in range(octaves):
        result += value_noise(shape, scale * (2**o), seed + o) * amp
        total  += amp; amp *= 0.5
    return result / total

height = fbm((SIZE, SIZE), 6, 6, seed=5)
detail = fbm((SIZE, SIZE), 18, 3, seed=55) * 0.2
height = np.clip(height + detail, 0, 1)

# Panjura: arid/rocky plateau feel – red-orange rock, sparse grass, central river
DEEP    = np.array([24,  64, 110], np.float32)
SHALLOW = np.array([45,  105, 150], np.float32)
BEACH   = np.array([180, 155, 105], np.float32)
GRASS   = np.array([80, 110,  45], np.float32)
DRY_GRASS=np.array([130, 130, 65], np.float32)
SHRUB   = np.array([95, 105,  50], np.float32)
RED_ROCK= np.array([160,  88,  55], np.float32)
SAND    = np.array([190, 165, 110], np.float32)
ROCK    = np.array([100,  90,  80], np.float32)
DARK_MT = np.array([70,   65,  60], np.float32)
SNOW    = np.array([210, 215, 220], np.float32)
WETLAND = np.array([50,   90,  55], np.float32)

def lerp(a, b, t):
    return a * (1 - t[..., None]) + b * t[..., None]

# Base: dry grass across map
base = lerp(DRY_GRASS, GRASS, np.clip(height * 1.5, 0, 1))

# Red rock region (NE)
rr_str = np.clip((nx - 0.55) / 0.45, 0, 1) * np.clip((0.45 - ny) / 0.45, 0, 1)
base = lerp(base, RED_ROCK, np.clip(rr_str * 1.5, 0, 1))

# Shrubland (W side)
shrub = np.clip((0.35 - nx) / 0.35, 0, 1)
base = lerp(base, SHRUB, shrub * 0.7)

# Wetlands (S centre)
wet = np.clip((ny - 0.65) / 0.35, 0, 1) * np.clip(1 - np.abs(nx - 0.50) / 0.30, 0, 1)
base = lerp(base, WETLAND, wet * 0.8)

# Mountains (NW)
mt = np.clip((0.25 - nx) / 0.25, 0, 1) * np.clip((0.30 - ny) / 0.30, 0, 1)
mt_col = lerp(DARK_MT, SNOW, np.clip((height - 0.65) / 0.35, 0, 1))
base = lerp(base, mt_col, np.clip(mt * 2, 0, 1))

# Central river (vertical, midway)
rx = np.abs(nx - 0.50)
river = np.clip((0.018 - rx) / 0.018, 0, 1)
base = lerp(base, SHALLOW, river)

# Northern lake (nx≈0.44, ny≈0.22)
lx, ly = 0.44, 0.22
lake_d = np.hypot(nx - lx, ny - ly) / 0.10
base = lerp(base, lerp(DEEP, SHALLOW, np.clip(lake_d / 0.7, 0, 1)),
            (lake_d < 0.7).astype(np.float32))
shore_t = np.clip((lake_d - 0.7) / 0.3, 0, 1) ** 0.5
base = lerp(base, lerp(SHALLOW, BEACH, shore_t),
            ((lake_d >= 0.7) & (lake_d < 1.0)).astype(np.float32))

# Southern wetland pool
lx2, ly2 = 0.54, 0.80
lake_d2  = np.hypot(nx - lx2, ny - ly2) / 0.12
base = lerp(base, lerp(DEEP, SHALLOW, np.clip(lake_d2 / 0.7, 0, 1)),
            (lake_d2 < 0.7).astype(np.float32))
shore_t2 = np.clip((lake_d2 - 0.7) / 0.3, 0, 1) ** 0.5
base = lerp(base, lerp(SHALLOW, BEACH, shore_t2),
            ((lake_d2 >= 0.7) & (lake_d2 < 1.0)).astype(np.float32))

micro = fbm((SIZE, SIZE), 32, 2, seed=88) - 0.5
base = np.clip(base + micro[..., None] * 20, 0, 255).astype(np.uint8)

img = Image.fromarray(base, "RGB")
img = img.filter(ImageFilter.GaussianBlur(radius=1.0))

# Vignette
dist_v = np.hypot((gx - SIZE/2) / (SIZE/2), (gy - SIZE/2) / (SIZE/2))
vig    = np.clip(1 - dist_v * 0.50, 0.28, 1.0)[..., None]
arr    = np.array(img, np.float32) * vig
img    = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

img = ImageEnhance.Sharpness(img).enhance(1.5)
img = ImageEnhance.Contrast(img).enhance(1.2)
img = ImageEnhance.Color(img).enhance(1.15)

import os
out = os.path.join(os.path.dirname(__file__), "../public/maps/panjura.jpg")
img.save(out, "JPEG", quality=88)
print(f"Saved {SIZE}x{SIZE} → {out}")
