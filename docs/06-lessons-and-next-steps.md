# 6. Lessons and next steps

## Where things stand

| Scroll | Surface examined | Models | Result |
|---|---|---|---|
| PHerc. 0800 | 9.2 cm² (6 public segments) | ink_9um ensemble, Reader v3, Argus v3, Studio | No letters; responses follow cracks and seams |
| PHerc. 1545 | 471 cm² (one HerculeX band); top-10 pieces inspected | Reader v3 (all pieces), Studio (2 pieces) | No letters; negative confirmed by a format control |
| PHerc. 0846A | One HerculeX band (attempted) | — | First run stopped before any ink reading (see below) |

## What happened on the first PHerc. 0846A run

HerculeX picks a CT volume automatically. For PHerc. 0846A it chose a **2.4 µm** scan instead of the 9.4 µm one. At that resolution, one band meant about 66 GB of CT bricks, which filled the laptop disk and stopped the run silently, before any piece was flattened. Lesson: pin the scan volume explicitly and check disk headroom before an overnight run. The rerun will force the 9.4 µm volume, the same resolution as the controls.

## Why PHerc. 0846A next

- It ranks **first or third** in two of the four DINO variants.
- Another participant has reported a cluster of letters on PHerc. 0846 using HerculeX. This is unverified (community chat), but it is a concrete sign that the same tool chain can reveal ink there.

## Plan

1. Screen the PHerc. 0846A band with the method that is now validated:
   1. rank pieces by ink score;
   2. inspect them by eye;
   3. run Studio in the correct order;
   4. look for **rows with interline gaps**, not isolated blobs.
2. If a credible seed appears:
   1. build a clean ≥ 4 cm² surface around it;
   2. run the full control set: depth reversal, agreement across architectures, depth-shift tolerance, a pre-registered blank region;
   3. only then start **iterative pseudo-labelling**. This means a few very confident ink and non-ink labels taken from the scroll itself, a fine-tuned reader, and leave-one-zone-out so that no prediction is ever judged on a zone used for training (this is also a prize rule).
3. If nothing appears: unwrap further bands, which costs about one night of laptop GPU per band, and move down the DINO ranking.

## What I would do differently

- Run the target-selection step (DINO) **before** investing in the first scroll, not after.
- Write the positive control into the pipeline from day one, as an automatic test, rather than adding it after each surprise.
- Keep a dated log of decisions from the start, which this repository now is.
