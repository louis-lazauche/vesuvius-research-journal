"""Embed sampled scroll cubes with the dinovol v2 ps8 teacher backbone (fp32), two variants per cube.

native: cube resampled to a common 9.362 um grid, centre 112^3 (dinovol saw 2.4 um data, so this is off-scale).
scale4: the densest 32^3-at-9.362um subcrop, upsampled x4 to 128^3, i.e. roughly dinovol's 2.4 um training scale.
Writes ~/vesuvius-project/dino_scrolls/emb/<scroll>.npz (per-cube mean patch token and cls token for each variant).
"""
import glob, os, sys, time
import numpy as np
import torch
import torch.nn.functional as F

sys.path[:0] = [os.path.expanduser("~/vesuvius-project/villa/dinovol")]
from dinovol_2.model.model import DinoVitStudentTeacher
from dinovol_2.dataset.normalization import get_normalization

ROOT = os.path.expanduser("~/vesuvius-project/dino_scrolls")
os.makedirs(f"{ROOT}/emb", exist_ok=True)
REF_UM = 9.362
dev = "cuda"

ck = torch.load(os.path.expanduser("~/vesuvius-project/checkpoints/dinovol/backbone.pt"), map_location="cpu", weights_only=True)
model_cfg = ck["config"]["model"]
state = {k[len("backbone."):]: v for k, v in ck["teacher"].items() if k.startswith("backbone.")}
backbone = DinoVitStudentTeacher._build_backbone(model_cfg)
backbone.load_state_dict(state, strict=True)
backbone = backbone.to(dev).eval()
norm = get_normalization(str(ck["config"]["dataset"].get("normalization_scheme", "robust")), intensityproperties=None)
print("backbone ready", sum(p.numel() for p in backbone.parameters()) / 1e6, "M params", flush=True)


def embed(x):
    """x: (D,H,W) float32 normalised -> (mean patch token, cls token) as float32 numpy."""
    t = torch.from_numpy(np.ascontiguousarray(x))[None, None].to(dev)
    with torch.no_grad():
        out = backbone.forward_features(t, masks=None, view_kind="global")
    return out["x_norm_patchtokens"][0].mean(0).float().cpu().numpy(), out["x_norm_clstoken"][0].float().cpu().numpy()


def resample(cube, factor, size):
    t = torch.from_numpy(cube.astype(np.float32))[None, None]
    shape = [max(size, round(s * factor)) for s in cube.shape]
    t = F.interpolate(t, size=shape, mode="trilinear", align_corners=False)[0, 0]
    o = [(s - size) // 2 for s in t.shape]
    return t[o[0]:o[0] + size, o[1]:o[1] + size, o[2]:o[2] + size].numpy()


def densest_subcrop(cube, n):
    best, arg = -1, (0, 0, 0)
    for z in range(0, cube.shape[0] - n + 1, n // 2):
        for y in range(0, cube.shape[1] - n + 1, n // 2):
            for x in range(0, cube.shape[2] - n + 1, n // 2):
                m = cube[z:z + n, y:y + n, x:x + n].mean()
                if m > best:
                    best, arg = m, (z, y, x)
    z, y, x = arg
    return cube[z:z + n, y:y + n, x:x + n]


files = sorted(glob.glob(f"{ROOT}/cubes/*.npz"))
if len(sys.argv) > 1:
    files = [f for f in files if os.path.basename(f)[:-4] in sys.argv[1:]]
for f in files:
    name = os.path.basename(f)[:-4]
    dst = f"{ROOT}/emb/{name}.npz"
    if os.path.exists(dst):
        continue
    d = np.load(f)
    cubes, vox = d["cubes"], float(d["voxel_um"])
    t0 = time.time()
    res = {k: [] for k in ("native_mean", "native_cls", "s4_mean", "s4_cls")}
    for cube in cubes:
        nat = resample(cube, vox / REF_UM, 112)
        m, c = embed(norm.run(nat).astype(np.float32))
        res["native_mean"].append(m); res["native_cls"].append(c)
        n = int(round(32 * REF_UM / vox))  # voxels covering 32 * 9.362 um
        sub = densest_subcrop(cube, n)
        up = resample(sub, 128 / n, 128)
        m, c = embed(norm.run(up).astype(np.float32))
        res["s4_mean"].append(m); res["s4_cls"].append(c)
    np.savez(dst, role=d["role"], voxel_um=vox, **{k: np.stack(v) for k, v in res.items()})
    print(f"{name}: {len(cubes)} cubes, {time.time() - t0:.0f}s, gpu peak {torch.cuda.max_memory_allocated() / 2**30:.2f} GiB", flush=True)
print("DONE")
