"""Run the Studio ink model (fp32) on a surface-volume zarr.

Builds the [16,H,W] uint8 stack from planes centred on the volume's middle slice, in either order:
  'down' = c+8 ... c-7 (Studio's documented order: planes 23 down to 8 of a 31-plane render)
  'up'   = c-7 ... c+8 (reversed)
usage: python studio_run.py ZARR OUT_PREFIX ORDER [y0 y1 x0 x1] [--batch N] [--shift S]
Writes OUT_PREFIX_<order>[_sS].npy (float32 probabilities) and .tif (uint8).
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import tifffile
import torch

STUDIO_HF = Path.home() / "vesuvius-project/external/vesuvius-studio-multiscroll-cpt/studio-multiscroll-cpt-20261023/hf"
sys.path.insert(0, str(STUDIO_HF))
from inference import load_model, predict  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("zarr"); ap.add_argument("out_prefix"); ap.add_argument("order", choices=["down", "up"])
ap.add_argument("roi", nargs="*", type=int)
ap.add_argument("--batch", type=int, default=2)
ap.add_argument("--shift", type=int, default=0, help="move the 16-plane window by S planes")
ap.add_argument("--ckpt", default=str(Path.home() / "vesuvius-project/checkpoints/studio/studio-softloss-20261023-ema.safetensors"))
a = ap.parse_args()

vol = np.load(a.zarr, mmap_mode="r")
Z = vol.shape[0]
c = Z // 2 + a.shift - 1  # 17 planes: window 0..15
idx = list(range(c + 8, c - 8, -1)) if a.order == "down" else list(range(c - 7, c + 9))
assert min(idx) >= 0 and max(idx) < Z, (idx, Z)
y0, y1, x0, x1 = a.roi if a.roi else (0, vol.shape[1], 0, vol.shape[2])
stack = np.stack([np.asarray(vol[z, y0:y1, x0:x1]) for z in idx]).astype(np.uint8)
print(f"planes {idx[0]}..{idx[-1]} ({a.order}), stack {stack.shape}", flush=True)

tag = f"{a.out_prefix}_{a.order}" + (f"_s{a.shift}" if a.shift else "")
out = Path(tag + ".npy")
if out.exists():
    out.unlink()
model = load_model(a.ckpt, "cuda")
t = time.time()
res = predict(model, stack, out, device="cuda", batch_size=a.batch, amp="fp32", stride=64, blend="hann")
dt = time.time() - t
p = np.asarray(res)
v = p[(stack > 0).any(0)]
print(f"done in {dt:.0f}s | peak VRAM {torch.cuda.max_memory_allocated() / 2**30:.2f} GiB | "
      f"mean {v.mean():.3f} p99 {np.percentile(v, 99):.3f} p99.9 {np.percentile(v, 99.9):.3f} frac>0.5 {(v > 0.5).mean():.4f} nan {np.isnan(p).sum()}")
tifffile.imwrite(tag + ".tif", (np.clip(np.nan_to_num(p), 0, 1) * 255).astype(np.uint8))
