"""Make HerculeX-style 17-layer windows from the w035 control crop (both stack orientations)."""
import sys
from pathlib import Path
import numpy as np

HX = Path.home() / "vesuvius-project/external/HerculeX"
sys.path.insert(0, str(HX))
from ink.model.input_stack import DEPTH, PAST_FACE, face_layer_of, profile_of  # noqa: E402

Z = Path.home() / "vesuvius-project/control/pherc0139-w035/w035_9um.zarr/0"
OUT = Path.home() / "vesuvius-project/hx1545_stacks/control"
OUT.mkdir(parents=True, exist_ok=True)
y0, y1, x0, x1 = 1000, 2024, 1600, 2624
nz, ny, nx = 28, 5820, 5240
cy, cx = 128, 128
vol = np.zeros((nz, y1 - y0, x1 - x0), np.uint8)
for by in range(y0 // cy, (y1 - 1) // cy + 1):
    for bx in range(x0 // cx, (x1 - 1) // cx + 1):
        f = Z / "0" / str(by) / str(bx)
        if not f.exists():
            continue
        blk = np.frombuffer(f.read_bytes(), np.uint8).reshape(nz, cy, cx)
        ys, xs = by * cy, bx * cx
        a0, a1 = max(ys, y0), min(ys + cy, y1)
        b0, b1 = max(xs, x0), min(xs + cx, x1)
        vol[:, a0 - y0:a1 - y0, b0 - x0:b1 - x0] = blk[:, a0 - ys:a1 - ys, b0 - xs:b1 - xs]
print("profile", np.round(profile_of(vol), 1).tolist())
for name, s, idx in (("fwd", vol, np.arange(nz)), ("rev", vol[::-1], np.arange(nz)[::-1])):
    first = min(face_layer_of(s) + PAST_FACE, s.shape[0] - DEPTH)
    win = np.ascontiguousarray(s[first:first + DEPTH])
    print(name, "window planes (original numbering):", idx[first:first + DEPTH].tolist())
    np.save(OUT / f"w035_hx_{name}.npy", win)
