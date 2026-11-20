# 1. Literature review: how were the first letters found?

The full review (in French, about 20 pages, with every claim tagged by source reliability) is in [fr/literature-review-fr.md](fr/literature-review-fr.md). This page summarises what shaped my plan.

## Method

I read the published write-ups of every First Letters prize and progress prize, the model cards of the community ink models, and the prize rules. I tagged each claim by reliability:

- **[ORG]**: published by the organisers;
- **[AUTHOR]**: claimed by a model's or tool's author and not independently checked;
- **[THIRD PARTY]**: re-measured by someone else;
- **[OURS]**: my own experiments.

This separation turned out to matter, because many of the most attractive numbers are author claims.

## Three winning recipes, one common base

| Scroll | Ink model | Where the first signal came from |
|---|---|---|
| PHerc. 343 (8.64 µm, 116 keV) | Averaged ensemble of existing 9 µm models | Off-the-shelf models, no training on the target |
| PHerc. 306B (same scan session as my first target) | Product of two models, one fine-tuned on human labels from a 116 keV sibling scroll | Labels taken in the right scan conditions, plus pseudo-labels |
| PHerc. 211 | Studio, a 223M-parameter 3D U-Net | Ink distilled from 2 µm scans of scrolls chosen **by DINO similarity** |

What every winner shares is a **large, well-segmented surface**: a spiral fit over the full height of the scroll, then refinement. None of them found letters by staring at about 9 cm².

## What this told me to do

1. **Surface area comes first.** The 9.2 cm² of public segments on my first target was far too little. → Step 4: whole-scroll unwrapping.
2. **The model has to match the scan.** Models trained on a different energy or resolution may see nothing. → Step 3: pick the scroll that looks most like the training data of the best model.
3. **False positives are the main danger.** Organisers warn that models produce "things that look a lot like letters" in deformed areas. Documented controls:
   - reversing the depth order of the input;
   - checking agreement between different architectures;
   - tolerance to small depth shifts;
   - pre-registered blank regions;
   - a 3D exclusion zone between training labels and the claimed area.
   → Step 5: controls on every result.
4. **Iterative pseudo-labelling works, but it amplifies mistakes.** It can only start from reliable seeds, and it needs held-out zones. I kept it for after a first credible ink signal.
