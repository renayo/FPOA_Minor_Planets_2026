"""make_figure.py -- build results/fpoa_axial_audit.png from the open data.

Four panels: (a) observed joint aspect autocorrelation vs both count-preserving
nulls; (b) the pooled longitude wave and its single-cosine fit; (c) the
model-based Bayes factor by fixed axis direction, marking the pre-registered
tropical (FPOA) axis and the sidereal Lahiri axis; (d) the drop control showing
that removing the highest-coverage bodies degrades the statistic no faster than
removing random bodies once sampling is matched.

Depends only on numpy/pandas/matplotlib and the CSVs in ../data plus the
precomputed directional BF arrays in ../results.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import analysis as an

RES = an.RES
FOCAL, BLUE, GREY, AMBER = "#d23553", "#2c63d6", "#8a8f9c", "#c5860f"


def main():
    verified, counts, angles, ang_unnamed = an.load()
    C, ANG = counts.values, angles.values
    tot = C.sum(0); order = np.argsort(-tot); nb = C.shape[1]

    w = an.longitude_wave(C, ANG)
    obs = an.joint_acf_sq(w)
    Fw = np.fft.rfft(w); amp = 2 * np.abs(Fw[1]) / 360; phi = np.angle(Fw[1])
    cos_fit = amp * np.cos(np.deg2rad(np.arange(360)) - phi)

    rng = np.random.default_rng(an.SEED)
    comp = np.empty(an.N_MC); unn = np.empty(an.N_MC)
    lon = np.round(ANG).astype(int) % 360
    for i in range(an.N_MC):
        perm = rng.permutation(nb); shift = rng.integers(0, 290, size=nb)
        cs = np.empty_like(C); craw = C[:, perm]
        for j in range(nb):
            cs[:, j] = np.roll(craw[:, j], shift[j])
        comp[i] = an.joint_acf_sq(an.longitude_wave(cs, ANG))
        unn[i]  = an.joint_acf_sq(an.longitude_wave(C[:, rng.permutation(nb)], ang_unnamed))
    p_comp = (1 + (comp >= obs).sum()) / (1 + an.N_MC)
    p_unn  = (1 + (unn  >= obs).sum()) / (1 + an.N_MC)

    Ns = [0, 25, 50, 100, 150, 200, 300, 400]
    rng2 = np.random.default_rng(1)
    top = [an.joint_acf_sq(an.longitude_wave(C[:, order[n:]], ANG[:, order[n:]])) for n in Ns]
    rmean, rsd = [], []
    for n in Ns:
        vals = []
        for _ in range(30):
            keep = np.sort(rng2.permutation(nb)[n:])      # ONE index set for counts and angles
            vals.append(an.joint_acf_sq(an.longitude_wave(C[:, keep], ANG[:, keep])))
        rmean.append(np.mean(vals)); rsd.append(np.std(vals))

    bf_mba = np.load(f"{RES}/fpoa_v_bf_mba.npy"); bf_cmp = np.load(f"{RES}/fpoa_v_bf_cmp.npy")

    plt.rcParams.update({"font.size": 8, "axes.titlelocation": "left",
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axs = plt.subplots(2, 2, figsize=(11, 8.4))

    axA = axs[0, 0]
    axA.hist(comp, bins=40, color=BLUE, alpha=0.55, density=True, label="compound null")
    axA.hist(unn, bins=40, color=GREY, alpha=0.55, density=True, label="unnamed-MBA null")
    axA.axvline(obs, color=FOCAL, lw=2.4)
    axA.annotate(f"observed {obs:.2f}\np ~ {p_comp:.3f}/{p_unn:.3f}", xy=(obs, axA.get_ylim()[1]*0.6),
                 xytext=(0.30, axA.get_ylim()[1]*0.55), fontsize=6.3, color=FOCAL, ha="right",
                 arrowprops=dict(arrowstyle="->", color=FOCAL, lw=0.8))
    axA.set_xlabel("joint aspect autocorrelation  Sum ACF^2(9)"); axA.set_ylabel("null density")
    axA.set_title("Signal survives both count-preserving nulls", fontsize=8)
    axA.legend(frameon=False, fontsize=6)

    axB = axs[0, 1]
    axB.plot(np.arange(360), w, color=GREY, lw=0.7, label="observed wave")
    axB.plot(np.arange(360), cos_fit, color=FOCAL, lw=2.2, label="single cosine")
    axB.axhline(0, color="k", lw=0.5, ls=":"); axB.axvline(180, color=BLUE, lw=1, ls="--")
    axB.set_xlim(0, 359); axB.set_xticks([0, 90, 180, 270, 360])
    axB.set_xticklabels(["0 Aries", "90", "180 Libra", "270", "360"])
    axB.set_xlabel("ecliptic longitude from FPOA"); axB.set_ylabel("mean normalised news presence")
    axB.set_title("One weak axial modulation, not nine aspects", fontsize=8)
    axB.legend(frameon=False, fontsize=6)

    axC = axs[1, 0]
    axC.plot(np.arange(360), bf_mba, color=FOCAL, lw=1.6, label="unnamed-MBA null")
    axC.plot(np.arange(360), bf_cmp, color=BLUE, lw=1.6, label="compound null")
    axC.axhline(10, color="#888", ls=":", lw=0.8); axC.axhline(3, color="#bbb", ls=":", lw=0.8)
    for xa in (0, 180):
        axC.axvline(xa, color="k", lw=1.1)
    axC.axvline(an.AYANAMSHA_2022, color=AMBER, lw=1.1, ls=":")
    axC.set_yscale("log"); axC.set_xlim(0, 359); axC.set_xticks([0, 90, 180, 270, 360])
    axC.set_yticks([1, 3, 10]); axC.set_yticklabels(["1", "3", "10"]); axC.minorticks_off()
    axC.set_xlabel("reference axis direction from FPOA (deg)")
    axC.set_ylabel("model-based Bayes factor (log)")
    axC.set_title("Data axis on the pre-registered tropical axis", fontsize=8)
    axC.legend(frameon=False, fontsize=6, loc="lower center")

    axD = axs[1, 1]
    axD.plot(Ns, top, "-o", color=FOCAL, ms=4, label="drop HIGHEST-coverage")
    axD.plot(Ns, rmean, "-s", color=BLUE, ms=4, label="drop RANDOM (mean+/-sd)")
    axD.fill_between(Ns, np.array(rmean)-np.array(rsd), np.array(rmean)+np.array(rsd),
                     color=BLUE, alpha=0.18)
    axD.axhline(0.10, color=GREY, ls="--", lw=1)
    axD.set_xlabel("bodies removed (of 1122)"); axD.set_ylabel("joint aspect autocorrelation")
    axD.set_title("High-coverage drop is information loss", fontsize=8)
    axD.legend(frameon=False, fontsize=6); axD.set_ylim(0, 0.5)

    for ax, l in zip(axs.ravel(), "abcd"):
        ax.text(-0.15, 1.02, l, transform=ax.transAxes, fontweight="bold", fontsize=9)
    fig.suptitle("Named-minor-planet news presence: a weak single-axis modulation "
                 "on the pre-registered equinoctial axis", fontsize=9.3, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(f"{RES}/fpoa_axial_audit.png", dpi=200)
    print("wrote", f"{RES}/fpoa_axial_audit.png")


if __name__ == "__main__":
    main()
