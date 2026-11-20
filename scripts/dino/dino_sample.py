"""Fetch random 128^3 level-0 chunks of papyrus from each scroll's ~9 um volume over public HTTPS.

Saves ~/vesuvius-project/dino_scrolls/cubes/<scroll>.npz with cubes (N,128,128,128) uint8 and their chunk indices.
Run with the HerculeX runtime python (has numcodecs).
"""
import json, os, sys, time, urllib.request, zlib
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import numcodecs

B = "https://vesuvius-challenge-open-data.s3.amazonaws.com"
VOLS = {  # scroll: (volume, voxel um, role)
    "PHerc0125": ("20250821151825-9.362um-1.2m-113keV-masked.zarr", 9.362, "eligible"),
    "PHerc0175A": ("20250521115057-8.640um-1.2m-116keV-masked.zarr", 8.64, "eligible"),
    "PHerc0175B": ("20250521125822-8.640um-1.2m-116keV-masked.zarr", 8.64, "eligible"),
    "PHerc0191": ("20250821151635-9.362um-1.2m-113keV-masked.zarr", 9.362, "eligible"),
    "PHerc0257": ("20250821151750-9.362um-1.2m-113keV-masked.zarr", 9.362, "eligible"),
    "PHerc0268": ("20251110183117-8.640um-1.2m-116keV-masked.zarr", 8.64, "eligible"),
    "PHerc0358": ("20250821151737-9.362um-1.2m-113keV-masked.zarr", 9.362, "eligible"),
    "PHerc0483A": ("20250521140913-8.640um-1.2m-116keV-masked.zarr", 8.64, "eligible"),
    "PHerc0483B": ("20251124083638-8.640um-1.2m-116keV-masked.zarr", 8.64, "eligible"),
    "PHerc0490A": ("20250521151210-8.640um-1.2m-116keV-masked.zarr", 8.64, "eligible"),
    "PHerc0490B": ("20250521151215-8.640um-1.2m-116keV-masked.zarr", 8.64, "eligible"),
    "PHerc0800": ("20250521135224-8.640um-1.2m-116keV-masked.zarr", 8.64, "eligible"),
    "PHerc0813": ("20250821151723-9.362um-1.2m-113keV-masked.zarr", 9.362, "eligible"),
    "PHerc0826": ("20250821151701-9.362um-1.2m-113keV-masked.zarr", 9.362, "eligible"),
    "PHerc0846A": ("20250728152254-9.362um-1.2m-113keV-masked.zarr", 9.362, "eligible"),
    "PHerc0846B": ("20250804142305-9.362um-1.2m-113keV-masked.zarr", 9.362, "eligible"),
    "PHerc1203": ("20250820131727-9.362um-1.2m-113keV-masked.zarr", 9.362, "eligible"),
    "PHerc1218": ("20250521120456-8.640um-1.2m-116keV-masked.zarr", 8.64, "eligible"),
    "PHerc1545": ("20250821151648-9.362um-1.2m-113keV-masked.zarr", 9.362, "eligible"),
    "PHerc0009B": ("20250521125136-8.640um-1.2m-116keV-masked.zarr", 8.64, "ink"),
    "PHerc0306B": ("20250521133212-8.640um-1.2m-116keV-masked.zarr", 8.64, "ink"),
    "PHerc1447": ("20250521151220-8.640um-1.2m-116keV-masked.zarr", 8.64, "ink"),
    "PHerc0343P": ("20250521134555-8.640um-1.2m-116keV-masked.zarr", 8.64, "ink"),
    "PHerc0841": ("20250821151531-9.366um-1.2m-113keV-masked.zarr", 9.366, "ink"),
    "PHerc0814": ("20250804134230-9.362um-1.2m-113keV-masked.zarr", 9.362, "ink"),
    "PHerc0211": ("20250821151803-9.362um-1.2m-113keV-masked.zarr", 9.362, "ink"),
    "PHerc0139": ("20250728140407-9.362um-1.2m-113keV-masked.zarr", 9.362, "ink"),
}
N_WANT, MAX_TRY, C = 24, 200, 128
OUT = os.path.expanduser("~/vesuvius-project/dino_scrolls/cubes")
os.makedirs(OUT, exist_ok=True)


def get(url, tries=4):
    for k in range(tries):
        try:
            return urllib.request.urlopen(url, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return None
            time.sleep(2 * (k + 1))
        except Exception:
            time.sleep(2 * (k + 1))
    return None


def sample(scroll):
    dst = f"{OUT}/{scroll}.npz"
    if os.path.exists(dst):
        return f"{scroll} cached"
    vol, vox, role = VOLS[scroll]
    base = f"{B}/{scroll}/volumes/{vol}/0"
    za = json.loads(get(base + "/.zarray"))
    codec = numcodecs.get_codec(za["compressor"]) if za.get("compressor") else None
    sep = za.get("dimension_separator", ".")
    cs = za["chunks"]
    nz, ny, nx = (s // c for s, c in zip(za["shape"], cs))
    rng = np.random.default_rng(zlib.crc32(scroll.encode()))
    cubes, idx, tried = [], [], 0
    while len(cubes) < N_WANT and tried < MAX_TRY:
        tried += 1
        cz = int(rng.integers(int(nz * 0.15), int(nz * 0.85)))
        r, a = 0.42 * np.sqrt(rng.random()), rng.random() * 2 * np.pi  # inside the central disc
        cy, cx = int(ny / 2 + r * ny * np.sin(a)), int(nx / 2 + r * nx * np.cos(a))
        raw = get(f"{base}/{cz}{sep}{cy}{sep}{cx}")
        if raw is None:
            continue
        buf = codec.decode(raw) if codec else raw
        flat = np.frombuffer(buf, dtype=np.uint8)
        if flat.size != int(np.prod(cs)):
            print(f"{scroll}: chunk {cz},{cy},{cx} has {flat.size} bytes, expected {int(np.prod(cs))}; zarray={za}", flush=True)
            return f"{scroll}: SKIPPED (unexpected chunk size)"
        a3 = flat.reshape(cs)
        o = [(c - C) // 2 for c in cs]  # centre 128^3 of larger chunks
        a3 = a3[o[0]:o[0] + C, o[1]:o[1] + C, o[2]:o[2] + C]
        if (a3 > 0).mean() < 0.7:  # mostly outside the scroll mask
            continue
        cubes.append(a3.copy()); idx.append((cz, cy, cx))
    np.savez(dst, cubes=np.stack(cubes) if cubes else np.zeros((0, C, C, C), np.uint8),
             idx=np.array(idx), voxel_um=vox, role=role, volume=vol)
    return f"{scroll}: {len(cubes)} cubes from {tried} tries"


if __name__ == "__main__":
    names = sys.argv[1:] or list(VOLS)
    with ThreadPoolExecutor(6) as ex:
        for msg in ex.map(sample, names):
            print(msg, flush=True)
    print("DONE")
