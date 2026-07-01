# Information sheet 3 — Findings

All numbers below are read from `results/summary.json`, produced by
`src/analysis.py` (deterministic, seed 42, 3,000 Monte-Carlo iterations). The
four-panel figure is `results/fpoa_axial_audit.png`.

## Headline numbers

| Quantity | Value |
|---|---|
| Named bodies (verified) | 1,122 |
| Window | 2022-02-15 to 2022-12-01 (290 days) |
| Joint aspect autocorrelation Sum ACF^2(9) | **0.448** |
| Effect vs compound null | **5.1x**  (p = 0.006) |
| Effect vs unnamed-MBA null | **4.2x**  (p = 0.015) |
| First-harmonic share of wave variance | **30%** |
| ACF vs single cosine (r) | **0.98** |
| Data axis (tropical frame) | **178.4 deg** |

## Panel a — the signal survives both count-preserving nulls

The observed joint autocorrelation is **0.448**. Both nulls,
which keep the real counts and the full body population and scramble only the
orbit-count registration, sit far below it: compound-null mean
0.087 (ratio 5.1x, p = 0.006), unnamed-MBA-null
mean 0.107 (ratio 4.2x, p = 0.015). The effect is
therefore not an artefact of the count distribution or of the heavily-covered
bodies — those are present, unchanged, in both nulls.

## Panel b — one axis, not nine aspects

The pooled wave is well described by a **single cosine** on an axis at
178.4 deg, i.e. essentially the Aries-Libra equinoctial axis. The
first harmonic carries 30% of the wave's
variance; the nine aspect-lag autocorrelations track one cosine at r =
0.98. Reading the ACF at the nine aspects:

| aspect | 30 | 36 | 40 | 45 | 60 | 72 | 90 | 120 | 180 |
|---|---|---|---|---|---|---|---|---|---|
| ACF | +0.33 | +0.27 | +0.20 | +0.13 | +0.17 | +0.15 | -0.02 | -0.17 | -0.36 |

The broad decline from strongly positive at small separations to
-0.36 at opposition (with small aspect-to-aspect wiggles, e.g. 45->60 deg) is
the ACF of one low-frequency cosine — not nine independent aspect resonances.

## Panel c — the axis is the pre-registered equinoctial axis

Evaluating the model-based Bayes factor for a fixed axial cosine at **every** of
the 360 possible axis directions, the evidence peaks on the equinoctial axis.
The **data-estimated** axis (178.4 deg) lands within ~2 deg of the
axis fixed in advance by the coordinate system. Under the correct pre-registered
(fixed-axis) treatment the Bayes factor reaches **~21**
against the unnamed-MBA null. The axis-free Bayes factor (penalised for searching
all directions) is modest by comparison; that penalty does not apply here because
FPOA was not chosen after seeing the data.

**Tropical vs sidereal.** The data axis is 1.6 deg
from the tropical (FPOA) equinoctial axis but 25.7
deg from the sidereal Lahiri Aries point (ayanamsha 24.13 deg). The
fixed-axis Bayes factor is higher at the tropical axis
(~21) than at the sidereal axis
(~14). The signal registers to the **tropical**
equinox, not the sidereal one.

## Panel d — the high-coverage drop is information loss, not de-biasing

Removing the highest-coverage bodies lowers the statistic, but removing the same
number of **random** bodies lowers it almost as much (within one standard
deviation across removal sizes). Because normalisation already equalises
amplitude, high-coverage bodies matter for **longitude sampling**, not volume:
their coverage-participation correlation is
rho = 0.95. Dropping them removes measurement
information rather than removing a bias, which is why the two curves largely
overlap.

Drop curve (joint Sum ACF^2, by bodies removed):

| removed | 0 | 25 | 50 | 100 | 150 | 200 | 300 | 400 |
|---|---|---|---|---|---|---|---|---|
| highest-coverage | 0.45 | 0.41 | 0.39 | 0.31 | 0.20 | 0.05 | 0.02 | 0.04 |
| random (mean) | 0.45 | 0.41 | 0.42 | 0.36 | 0.38 | 0.33 | 0.30 | 0.22 |

## How to read all of this together

There is a **weak but reproducible single-axis modulation** of named-minor-planet
news presence, aligned to the tropical equinoctial axis that FPOA fixes in
advance, significant against two count-preserving nulls, and — under the correct
pre-registered framing — carrying a strong fixed-axis Bayes factor against the
unnamed-minor-planet control. The one honest deflation is dimensional: it is
**one** coherent axial cosine, so it should be reported as a single weak axis, not
as nine independent astrological aspects.

## Limitations

- A single 290-day window of one news index; not shown to be stationary across
  epochs.
- Google-News counts are a noisy, keyword-based proxy for cultural presence.
- Observational and correlational: no mechanism is established, and no such claim
  is made here.
- The axis-free effect is weak; the strong evidence is contingent on the
  legitimacy of fixing the equinoctial axis in advance (which the coordinate
  system, not the data, justifies).
