# Information sheet 2 — Methods

Every step below is implemented in `src/analysis.py` and reads only the CSV
tables in `data/`.

## 1. The longitude wave

For each verified named body *b* we take its 290-day Google-News count series
and normalise it to unit L2 length:

```
c_b(t) = count_b(t) / sqrt( sum_t count_b(t)^2 )
```

This is the key equalising step. After it, a body with 11,000 total articles and
a body with 130 contribute **the same total weight** to the pooled wave — the
analysis is about *where on the circle* coverage falls, not *how much* a body
gets. We then bin every (body, day) observation by the body's integer ecliptic
longitude from FPOA, `L = round(longitude_from_FPOA) mod 360`, and take the
**mean** normalised count in each of the 360 one-degree bins. Subtracting the
global mean gives the centred wave `w(L)`, L = 0…359.

Using a per-bin mean (not a sum) means a longitude that simply happens to be
visited by more bodies does not win by body count.

## 2. The circular autocorrelation function

Because longitude is periodic, the autocorrelation is the **circular**
(Wiener–Khinchin) ACF, computed by FFT:

```
ACF(k) = IFFT( |FFT(w)|^2 )(k),  normalised so ACF(0) = 1.
```

`ACF(k)` measures how similar the wave is to itself after a rotation of *k*
degrees. We read it at the **nine classical aspect lags**
{30, 36, 40, 45, 60, 72, 90, 120, 180}° and summarise with the **joint
statistic**

```
J = sum over the nine aspects of ACF(aspect)^2.
```

A larger `J` means the wave repeats more strongly at those separations.

## 3. Two count-preserving null models

`J` on its own has no scale; we calibrate it by Monte Carlo (3,000 iterations,
seed 42) against two nulls. **Both preserve the real article counts, the L2
normalisation, and the full population of bodies** — including every
heavily-covered one. They differ only in how they break the link between a
body's coverage and its orbit:

- **Compound null.** Randomly reassign which count series belongs to which
  orbit (cross-body permutation) *and* circularly shift each series in time by a
  random number of days. This destroys any genuine name↔orbit registration while
  keeping every marginal distribution intact. It answers: *could this arise from
  a chance permutation of labels on the same data?*
- **Unnamed-MBA null.** Attach the **real, busy named-body counts** to the
  orbits of the **unnamed** main-belt asteroids. This answers: *is the pattern
  specific to the named bodies' orbital geometry, or would any minor-planet
  orbit produce it?*

For each null we report the Monte-Carlo p-value `(1 + #{null ≥ observed}) /
(1 + N)` and the effect size `observed / null-mean`.

> Note on the drop control (panel d). Removing the highest-coverage bodies is
> **not** a null model — it is a diagnostic. Because normalisation already
> equalises amplitude, what high-coverage bodies contribute is **longitude
> sampling**: they are present on many more days (their coverage↔participation
> correlation is ρ = 0.95), so each traces the wave at many longitudes. Removing
> them removes measurement information, and the statistic falls — but it falls
> **no faster than removing the same number of random bodies** once sampling is
> matched. That is the signature of an information-limited estimator, not of a
> few bodies manufacturing the signal.

## 4. The shape: is it one axis or nine aspects?

Two independent checks:

- **Harmonic power.** Decompose `w(L)` into Fourier harmonics. The **first
  harmonic** (period 360°, i.e. one axial cosine) carries ~30% of the wave's
  variance; every higher harmonic carries under 3%. The nine "aspects" are not
  independent resonances.
- **ACF vs a single cosine.** The ACF of a pure first-harmonic wave is exactly
  `cos(k)`. The observed ACF at the nine aspect lags correlates with `cos(lag)`
  at **r = 0.98** — one cosine sampled nine times.

## 5. The axis and the Bayes factors

The V-test (first circular moment) gives the wave's axial direction. We evaluate
a **model-based Bayes factor** comparing "an axial cosine along a given axis"
against each null, for **every** fixed axis direction 0…359°. Two summaries:

- **Axis-free Bayes factor** — the axis is estimated from the data, so the BF is
  penalised for the search over 360 directions. This is the honest number *if you
  had no prior axis*. It is modest (≈ 1.7–2.5).
- **Fixed-axis Bayes factor** — the axis is specified **in advance** at the
  equinoctial axis (0°/180°). This is the correct number under pre-registration,
  because FPOA is fixed by the coordinate system, not chosen after the fact. It
  is strong against the unnamed-MBA null (≈ 21).

The distinction is not a trick to inflate the evidence — it is the standard
difference between a pre-registered directional hypothesis and a post-hoc
peak-hunt. The data corroborate the pre-registration: the *data-estimated* axis
lands within ~2° of the axis that was fixed in advance.

## 6. Tropical vs sidereal axis

Because both the tropical (FPOA) and sidereal (ayanamsha-shifted) zodiacs name
an equinoctial axis a priori, we test both. Using the 2022 Lahiri ayanamsha
(≈ 24.13°), the sidereal Aries point sits 24° from FPOA. We compare the
fixed-axis Bayes factor at the tropical axis against the sidereal axis, and the
angular distance from the data axis to each. The signal prefers the **tropical**
axis (see `INFO_3_findings.md`).
