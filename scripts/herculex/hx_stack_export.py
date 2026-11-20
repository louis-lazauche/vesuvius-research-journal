"""Export HerculeX layer stacks (.zst) of given PHerc1545 pieces to .npy [layers, H, W] uint8."""
import struct, sys
from pathlib import Path
import numpy as np
import zstandard

ST = Path.home() / "vesuvius-project/external/HerculeX/data/outputs/stacks/level/PHerc1545/20250821151648/mesh-bridged-8-smoothed-1.5/band-0038-0044"
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
for pid in sys.argv[2:]:
    raw = (ST / f"piece-{int(pid):04d}.zst").read_bytes()
    shape = struct.unpack_from("III", raw)
    a = np.frombuffer(zstandard.ZstdDecompressor().decompress(memoryview(raw)[12:], max_output_size=int(np.prod(shape))), np.uint8).reshape(shape)
    np.save(OUT / f"piece-{int(pid):04d}.npy", a)
    nz = a[a > 0]
    print(pid, "shape", shape, "layer means", [round(float(a[i][a[i] > 0].mean()), 1) if (a[i] > 0).any() else 0 for i in range(0, shape[0], 5)])
