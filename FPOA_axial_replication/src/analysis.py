"""analysis.py -- self-contained replication of the axial-modulation audit.

Reads only the open CSV tables in ../data/ and writes every headline number to
../results/summary.json plus the result CSVs and the audit figure. Nothing is
hand-typed downstream: the report (paper/) and the web page (site/) both read
results/summary.json, so the documents cannot drift from the analysis.

The question. Each named minor planet's daily Google-News article count is
normalised (L2, per body) and binned by its integer ecliptic longitude measured
from the First Point of Aries (FPOA, the vernal equinox). Pooling gives one
360-point longitude wave. We ask whether that wave is autocorrelated at the nine
classical aspect separations {30,36,40,45,60,72,90,120,180} deg, quantify the
joint aspect autocorrelation Sum ACF^2(9), calibrate it against two
count-preserving nulls, and then characterise the signal.

Run:  python analysis.py            (uses ../data and ../results by default)
"""
from __future__ import annotations
import os, json
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
RES  = os.path.abspath(os.path.join(HERE, "..", "results"))
ASPECTS = [30, 36, 40, 45, 60, 72, 90, 120, 180]
SEED, N_MC = 42, 3000
AYANAMSHA_2022 = 24.13   # Lahiri ayanamsha, mid-window 2022 (tropical->sidereal offset)


# ---------------------------------------------------------------- data loading
def load():
    body = pd.read_csv(f"{DATA}/body_names.csv")
    verified = body.loc[body["verified"] == 1, "name"].tolist()
    counts = pd.read_csv(f"{DATA}/article_counts.csv").set_index("date")[verified].astype(float)
    angles = pd.read_csv(f"{DATA}/fpoa_angles_named.csv").set_index("date")[verified].astype(float)
    ref = pd.read_csv(f"{DATA}/reference_sun_relative_angles.csv")
    fpoa_col = ref.iloc[:, 1].values                      # col 1 = FPOA (Sun-relative)
    unnamed = pd.read_csv(f"{DATA}/unnamed_mba_sun_relative_angles.csv").set_index("date")
    unnamed = unnamed.iloc[:, :len(verified)].values
    ang_unnamed = (np.round(unnamed - fpoa_col[:, None]) % 360).astype(int) % 360
    return verified, counts, angles, ang_unnamed


# --------------------------------------------------------- core wave statistics
def longitude_wave(counts_arr, ang_arr):
    """L2-normalise each body, bin by integer FPOA longitude, mean per bin -> centred wave."""
    nrm = np.sqrt((counts_arr ** 2).sum(0)); nrm[nrm == 0] = 1.0
    cn = counts_arr / nrm
    lon = np.round(ang_arr).astype(int) % 360
    wsum = np.zeros(360); wcnt = np.zeros(360)
    np.add.at(wsum, lon.ravel(), cn.ravel())
    np.add.at(wcnt, lon.ravel(), 1.0)
    w = wsum / np.maximum(wcnt, 1.0)
    return w - w.mean()


def circular_acf(w):
    """Biased circular (Wiener-Khinchin) ACF, normalised so acf[0]=1."""
    f = np.fft.rfft(w)
    ac = np.fft.irfft(f * np.conj(f), n=360)
    return ac / ac[0]


def joint_acf_sq(w):
    ac = circular_acf(w)
    return float(sum(ac[a] ** 2 for a in ASPECTS))


def h1_fraction(w):
    p = np.abs(np.fft.rfft(w)) ** 2
    return float(p[1] / p[1:].sum())


# ------------------------------------------------------------------------- main
def main():
    os.makedirs(RES, exist_ok=True)
    verified, counts, angles, ang_unnamed = load()
    C = counts.values; ANG = angles.values
    tot = C.sum(0); order = np.argsort(-tot)
    rng = np.random.default_rng(SEED)

    # observed
    w = longitude_wave(C, ANG)
    obs = joint_acf_sq(w)
    acf = circular_acf(w)
    r_asp, _ = pearsonr(acf[ASPECTS], np.cos(np.deg2rad(ASPECTS)))
    axis_deg = float(np.degrees(np.angle(np.fft.rfft(w)[1])) % 360)

    # nulls: both preserve counts, normalisation, and the full body population;
    # they scramble only the orbit<->count registration.
    lon = np.round(ANG).astype(int) % 360
    comp = np.empty(N_MC); unn = np.empty(N_MC); nb = C.shape[1]
    for i in range(N_MC):
        perm = rng.permutation(nb); shift = rng.integers(0, 290, size=nb)
        cs = np.empty_like(C); craw = C[:, perm]
        for j in range(nb):
            cs[:, j] = np.roll(craw[:, j], shift[j])
        comp[i] = joint_acf_sq(longitude_wave(cs, ANG))
        unn[i]  = joint_acf_sq(longitude_wave(C[:, rng.permutation(nb)], ang_unnamed))
    p_comp = float((1 + (comp >= obs).sum()) / (1 + N_MC))
    p_unn  = float((1 + (unn  >= obs).sum()) / (1 + N_MC))

    # drop control: highest-coverage vs random removal
    Ns = [0, 25, 50, 100, 150, 200, 300, 400]
    rng2 = np.random.default_rng(1)
    top = [joint_acf_sq(longitude_wave(C[:, order[n:]], ANG[:, order[n:]])) for n in Ns]
    rmean, rsd = [], []
    for n in Ns:
        vals = []
        for _ in range(30):
            keep = np.sort(rng2.permutation(nb)[n:])
            vals.append(joint_acf_sq(longitude_wave(C[:, keep], ANG[:, keep])))
        rmean.append(float(np.mean(vals))); rsd.append(float(np.std(vals)))

    # burstiness: high-coverage bodies sample more longitudes (participation ratio)
    cn = C / np.where(np.sqrt((C ** 2).sum(0)) == 0, 1, np.sqrt((C ** 2).sum(0)))
    with np.errstate(divide="ignore"):
        pr = 1.0 / np.sum(cn ** 4, axis=0)
    m = tot > 0
    rho, _ = spearmanr(np.log10(tot[m] + 1), pr[m])

    # directional Bayes-factor curves (precomputed in results/), plus sidereal test
    def axial_dist(a, b):
        d = abs((a - b) % 180); return min(d, 180 - d)
    bf_mba = np.load(f"{RES}/fpoa_v_bf_mba.npy") if os.path.exists(f"{RES}/fpoa_v_bf_mba.npy") else None
    sidereal = {
        "ayanamsha": AYANAMSHA_2022,
        "axis_trop": round(axis_deg, 1),
        "dist_to_tropical_axis": round(axial_dist(axis_deg, 0), 1),
        "dist_to_sidereal_axis": round(axial_dist(axis_deg, AYANAMSHA_2022), 1),
    }
    if bf_mba is not None:
        sidereal["BF_fixed_tropical"] = round(float(bf_mba[0]), 1)
        sidereal["BF_fixed_sidereal"] = round(float(bf_mba[int(round(AYANAMSHA_2022)) % 360]), 1)

    summary = {
        "dataset": {"named_bodies_verified": int(nb), "days": int(C.shape[0]),
                    "date_start": counts.index[0], "date_end": counts.index[-1]},
        "aspects": ASPECTS,
        "signal": {"joint_acf_sq": round(obs, 4),
                   "h1_variance_fraction": round(h1_fraction(w), 3),
                   "acf_vs_single_cosine_r": round(float(r_asp), 3),
                   "axis_deg": round(axis_deg, 1),
                   "acf_at_lag": {str(a): round(float(acf[a]), 4) for a in ASPECTS}},
        "nulls": {"compound": {"mean": round(float(comp.mean()), 4),
                               "ratio": round(obs / float(comp.mean()), 2), "p": p_comp},
                  "unnamed_mba": {"mean": round(float(unn.mean()), 4),
                                  "ratio": round(obs / float(unn.mean()), 2), "p": p_unn},
                  "n_mc": N_MC, "seed": SEED},
        "robustness": {"bodies_removed": Ns,
                       "top_coverage_drop": [round(x, 4) for x in top],
                       "random_drop_mean": [round(x, 4) for x in rmean],
                       "random_drop_sd": [round(x, 4) for x in rsd],
                       "coverage_burstiness_spearman": round(float(rho), 3)},
        "sidereal": sidereal,
    }
    with open(f"{RES}/summary.json", "w") as fh:
        json.dump(summary, fh, indent=2)
    print("wrote", f"{RES}/summary.json")
    print(f"joint ACF2(9)={obs:.3f}  ratio c/u={summary['nulls']['compound']['ratio']}/"
          f"{summary['nulls']['unnamed_mba']['ratio']}  p={p_comp:.3f}/{p_unn:.3f}")
    print(f"axis={axis_deg:.1f} deg  H1 frac={summary['signal']['h1_variance_fraction']}  "
          f"ACF~cosine r={r_asp:.3f}")
    return summary


if __name__ == "__main__":
    main()
