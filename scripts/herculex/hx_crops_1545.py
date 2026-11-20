"""Crop scan sheet / layer0 / ink of chosen PHerc1545 pieces from the HerculeX tile store."""
import json, os, sys
from pathlib import Path
import numpy as np
from PIL import Image

HX = Path.home() / "vesuvius-project/external/HerculeX"
sys.path.insert(0, str(HX))
from website.site_server import tile_bytes, store_at  # noqa: E402

SHEET = HX / "data/outputs/website/sheets/sheet-PHerc1545-113keV-level"
PLACED = HX / "data/outputs/unwrapping/level/PHerc1545/20250821151648/sheet/placed-taught.json"
FACES = HX / "data/outputs/unwrapping/level/PHerc1545/20250821151648/faces/level-0/band-0038-0044"
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 10
T, PX = 512, 0.009362

scores = []
for f in FACES.glob("*-taught-side.json"):
    d = json.loads(f.read_text())
    scores.append((max(d["near"], d["far"]), int(f.name.split("-")[1])))
scores.sort(reverse=True)
top = [p for _, p in scores[:N]]
pieces = {p["piece"]: p for p in json.loads(PLACED.read_text())["pieces"] if p["unit"] == "band-0038-0044"}
stamp, store, _ = store_at(SHEET)


def region(layer, x0, y0, w, h):
    c0, c1, r0, r1 = x0 // T, (x0 + w - 1) // T, y0 // T, (y0 + h - 1) // T
    tiles = [(layer, 0, c, r) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)]
    parts = tile_bytes(SHEET, stamp, tiles, T)
    big = np.zeros(((r1 - r0 + 1) * T, (c1 - c0 + 1) * T), np.uint8)
    for (l, _, c, r), b in zip(tiles, parts):
        big[(r - r0) * T:(r - r0 + 1) * T, (c - c0) * T:(c - c0 + 1) * T] = np.frombuffer(b, np.uint8).reshape(T, T)
    return big[y0 - r0 * T:y0 - r0 * T + h, x0 - c0 * T:x0 - c0 * T + w]


def st(a):
    v = a[a > 0]
    if v.size == 0:
        return a
    lo, hi = np.percentile(v, [1, 99.5])
    return (np.clip((a.astype(np.float32) - lo) / max(hi - lo, 1), 0, 1) * 255).astype(np.uint8)


for rank, pid in enumerate(top, 1):
    p = pieces[pid]
    x0, y0 = int(p["x_mm"] / PX), int(p["y_mm"] / PX)
    w, h = int(p["width_mm"] / PX) + 1, int(p["height_mm"] / PX) + 1
    sheet, layer0, ink = (region(L, x0, y0, w, h) for L in ("sheet", "layer0", "taught"))
    gap = np.full((h, 16), 90, np.uint8)
    Image.fromarray(np.hstack([st(sheet), gap, st(layer0), gap, ink])).save(OUT / f"{rank:02d}_piece-{pid:04d}.png")
    print(rank, pid, "score", round(scores[rank - 1][0], 3), "size mm", round(p["width_mm"], 1), round(p["height_mm"], 1),
          "ink>0", round(float((ink > 0).mean()), 3), "sheet>0", round(float((sheet > 0).mean()), 3))
