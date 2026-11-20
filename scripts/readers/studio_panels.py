"""Panel: central scan layer | Studio down | Studio up, for each exported piece."""
import sys
from pathlib import Path
import numpy as np
import tifffile
from PIL import Image

S = Path.home() / "vesuvius-project/hx1545_stacks"
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)


def st(a):
    v = a[a > 0]
    lo, hi = np.percentile(v, [1, 99.5]) if v.size else (0, 255)
    return (np.clip((a.astype(np.float32) - lo) / max(hi - lo, 1), 0, 1) * 255).astype(np.uint8)


for p in sys.argv[2:]:
    stack = np.load(S / f"piece-{p}.npy", mmap_mode="r")
    mid = st(np.asarray(stack[8]))
    mask = (np.asarray(stack) > 0).any(0)
    tiles = [mid]
    for o in ("down", "up"):
        f = S / f"studio_{p}_{o}.tif"
        if not f.exists():
            continue
        pr = tifffile.imread(f).astype(np.float32) * mask
        v = pr[mask]
        print(p, o, "mean", round(v.mean() / 255, 3), "p99", round(np.percentile(v, 99) / 255, 3), "frac>0.5", round((v > 127).mean(), 4))
        tiles.append(pr.clip(0, 255).astype(np.uint8))
    gap = np.full((mid.shape[0], 16), 90, np.uint8)
    row = [tiles[0]]
    for t in tiles[1:]:
        row += [gap, t]
    Image.fromarray(np.hstack(row)).save(OUT / f"studio_piece-{p}.png")
