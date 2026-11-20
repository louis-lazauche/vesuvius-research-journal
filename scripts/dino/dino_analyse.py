"""Compare scrolls by dinovol embeddings: cosine similarity of centred scroll centroids, with bootstrap stability.

Usage: dino_analyse.py OUTDIR
"""
import glob, json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.expanduser("~/vesuvius-project/dino_scrolls/emb")
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
STUDIO_CORE = ["PHerc0009B", "PHerc0841", "PHerc0814"]  # Studio's core training scrolls

data = {}
for f in sorted(glob.glob(f"{ROOT}/*.npz")):
    d = np.load(f)
    data[os.path.basename(f)[:-4]] = {k: d[k] for k in d.files}
names = list(data)
role = {n: str(data[n]["role"]) for n in names}
session = {n: ("116keV" if abs(float(data[n]["voxel_um"]) - 8.64) < 0.01 else "113keV") for n in names}
eligible = [n for n in names if role[n] == "eligible"]
inked = [n for n in names if role[n] == "ink"]


def unit(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def centroids(variant, centring, rng=None):
    vecs = {}
    for n in names:
        v = data[n][variant].astype(np.float64)
        if rng is not None:
            v = v[rng.integers(0, len(v), len(v))]
        vecs[n] = v
    if centring == "global":
        mu = np.mean([vecs[n].mean(0) for n in names], 0)
        vecs = {n: vecs[n] - mu for n in names}
    elif centring == "session":
        for s in set(session.values()):
            grp = [n for n in names if session[n] == s]
            mu = np.mean([vecs[n].mean(0) for n in grp], 0)
            for n in grp:
                vecs[n] = vecs[n] - mu
    return {n: unit(unit(vecs[n]).mean(0)) for n in names}


def nn_accuracy(variant):
    """Leave-one-out: is each cube nearest to its own scroll's centroid? (does the embedding separate scrolls at all)"""
    X = np.concatenate([unit(data[n][variant]) for n in names]); y = np.concatenate([[i] * len(data[n][variant]) for i, n in enumerate(names)])
    sums = np.stack([X[y == i].sum(0) for i in range(len(names))]); cnt = np.bincount(y)
    ok = 0
    for x, i in zip(X, y):
        c = sums.copy(); c[i] -= x
        c = c / np.maximum(np.c_[cnt - (np.arange(len(names)) == i)], 1)
        ok += int(np.argmax(unit(c) @ x) == i)
    return ok / len(X)


report = {"n_cubes": {n: int(len(data[n]["native_mean"])) for n in names}, "session": session, "variants": {}}
for variant in ("native_mean", "s4_mean"):
    for centring in ("global", "session"):
        key = f"{variant}/{centring}"
        C = centroids(variant, centring)
        S = np.array([[C[a] @ C[b] for b in names] for a in names])
        # bootstrap: how often does each eligible scroll rank in the top 5 by similarity to the Studio core?
        rng = np.random.default_rng(0)
        top5 = {n: 0 for n in eligible}
        boot_scores = {n: [] for n in eligible}
        for _ in range(200):
            Cb = centroids(variant, centring, rng)
            sc = {n: np.mean([Cb[n] @ Cb[r] for r in STUDIO_CORE]) for n in eligible}
            for n, v in sc.items():
                boot_scores[n].append(v)
            for n in sorted(sc, key=sc.get, reverse=True)[:5]:
                top5[n] += 1
        rows = []
        for n in eligible:
            sims = {r: float(S[names.index(n), names.index(r)]) for r in inked}
            rows.append({
                "scroll": n, "session": session[n],
                "studio_core": float(np.mean([sims[r] for r in STUDIO_CORE])),
                "studio_core_ci": [float(np.percentile(boot_scores[n], 5)), float(np.percentile(boot_scores[n], 95))],
                "top5_freq": top5[n] / 200,
                "nearest_ink": sorted(sims, key=sims.get, reverse=True)[:3],
                "sims": sims,
            })
        rows.sort(key=lambda r: -r["studio_core"])
        report["variants"][key] = {"ranking": rows}
        if centring == "global":
            report["variants"][key]["loo_scroll_accuracy"] = nn_accuracy(variant)
        order = sorted(names, key=lambda n: (session[n], role[n] != "ink", n))
        M = np.array([[S[names.index(a), names.index(b)] for b in order] for a in order])
        fig, ax = plt.subplots(figsize=(11, 9.5))
        im = ax.imshow(M, cmap="viridis")
        ax.set_xticks(range(len(order)), [f"{n}{'*' if role[n] == 'ink' else ''}" for n in order], rotation=90, fontsize=8)
        ax.set_yticks(range(len(order)), [f"{n}{'*' if role[n] == 'ink' else ''} ({session[n][:3]})" for n in order], fontsize=8)
        ax.set_title(f"dinovol cosine similarity - {key}  (* = ink found)")
        fig.colorbar(im, ax=ax, shrink=0.8); fig.tight_layout()
        fig.savefig(f"{OUT}/sim_{variant}_{centring}.png", dpi=110); plt.close(fig)

json.dump(report, open(f"{OUT}/dino_report.json", "w"), indent=1)
for key, v in report["variants"].items():
    acc = v.get("loo_scroll_accuracy")
    print(f"\n=== {key}" + (f"  (cube->own scroll accuracy {acc:.2f})" if acc is not None else ""))
    for r in v["ranking"]:
        print(f"{r['scroll']:11s} {r['session']}  core={r['studio_core']:+.3f} [{r['studio_core_ci'][0]:+.3f},{r['studio_core_ci'][1]:+.3f}]"
              f"  top5={r['top5_freq']:.2f}  nearest ink: {', '.join(r['nearest_ink'])}")
