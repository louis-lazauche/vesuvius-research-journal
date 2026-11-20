# 2. First baselines on PHerc. 0800

## Why PHerc. 0800 first

The volume identifiers showed that PHerc. 0800 was reconstructed on the same day, at the same ESRF beamline settings (8.64 µm, 116 keV), as two scrolls where letters had already been read (PHerc. 0009B and 306B). Models trained on PHerc. 0009B had therefore already "seen" these scan conditions. It was a reasonable first bet.

## Setup

- **Hardware:** Windows 11 + WSL2 Ubuntu, NVIDIA GTX 1650 with 4 GB VRAM, about 10 GB RAM.
- **First obstacle:** in half precision (fp16), the models returned NaNs on this GPU. I wrote a small fp32 wrapper ([`scripts/readers/infer_fp32.py`](../scripts/readers/infer_fp32.py)). Every result in this repository is fp32.
- **Data:** the 6 published segments of PHerc. 0800, 9.2 cm² in total, rendered as layer stacks around the surface.

## Models tested

| Model | Trained on these scan conditions? | Runtime per segment (fp32, GTX 1650) |
|---|---|---|
| Official ink_9um (2 seeds × 2 checkpoints, 6-model ensemble, several depth windows) | No | ~30–40 s |
| Reader v3 | Yes (PHerc. 0009B) | ~20–45 s |
| Argus v3 (window average L5/L7/L9) | Yes | ~20–45 s |
| Studio | Yes, trained from scratch on 0009B, 0814 and 0841 | 3–17 min |

Each model was run in **both depth orders**, because the convention differs between tools and a wrong order silently gives noise.

## Results

- **No readable letters** with any model, in any order.
- The models agreed with each other a lot (Argus vs Studio, r = 0.60–0.85), but on the wrong things. The strong areas followed a horizontal crack, a seam between two surface patches, a damaged zone, and the segment edges. This is the textbook false positive described in the literature.
- **Positive control:** on segment w035 of PHerc. 0139, a scroll that has already been read, the same chain shows clear Greek letters in the correct order and noise in the reversed order (figure in the README). So the pipeline works, and the negative on PHerc. 0800 is informative.

## A second recipe, on a free cloud GPU

I also reproduced the PHerc. 306B winning recipe (TRACE v3B × A-hn) in a Kaggle notebook on a free T4 GPU. On the control, the product first failed. Diagnosis: the two models expect **opposite depth orders** (A-hn reverses layers by default). Each model therefore picked a different orientation, and multiplying the two maps mixed them up. The fix is to combine each model's map in its own correct orientation. Re-running the control with that fix is still pending.

## Conclusion of this step

9.2 cm² was too little surface, and nothing in it looked like text. The two levers from the literature review were more surface and a better-matched scroll.
