# Data dictionary

All files in `data/` are UTF-8 CSV with a header row. Matrices are stored wide:
the first column is the ISO date (`YYYY-MM-DD`) and every remaining column is one
body or reference point. The **290 rows** are the analysed days,
2022-02-15 to 2022-12-01.

## Reference frame (important)

The angle tables are in the **Sun-relative frame**: each value is an angular
separation **from the Sun** (degrees, 0…360), not an absolute ecliptic
longitude. Consequences:

- the **Sun** column of the reference table is a constant **0**;
- the **FPOA** column is `(0 − Sun_longitude) mod 360`, so it sweeps the whole
  circle (~−1°/day) as the Sun advances — expected, not an error;
- a body's separation from any reference R is `(body − R) mod 360`, which cancels
  the Sun term. The circular ACF and V-test are rotation-invariant, so this
  storage is lossless for the analysis.

The analysis uses `fpoa_angles_named.csv` directly, which already expresses each
body's separation **from FPOA**, so most users never need the Sun-relative
subtlety.

## Files

| File | Shape | Meaning |
|------|-------|---------|
| `dates.csv` | 290 × 2 | day index and ISO date |
| `body_names.csv` | 1211 × 3 | named astronyms in column order; `verified` = 1 if the body has a complete ephemeris over the window (1,122 of 1,211) |
| `unnamed_mba_names.csv` | 1211 × 2 | unnamed main-belt designations (the control pool) |
| `article_counts.csv` | 290 × 1212 | integer Google-News article count per named body per day (col 1 = date) |
| `named_sun_relative_angles.csv` | 290 × 1212 | each named body's angular separation from the Sun (deg) |
| `unnamed_mba_sun_relative_angles.csv` | 290 × 1212 | each control body's separation from the Sun (deg) |
| `reference_sun_relative_angles.csv` | 290 × 13 | each reference point's separation from the Sun; **column 1 = FPOA, column 2 = Sun (= 0)** |
| `fpoa_angles_named.csv` | 290 × 1212 | integer separation of each named body from FPOA = `round((body − FPOA) mod 360)`; the direct input to the analysis |

## Column conventions

- In every 1212-column table, column 1 is `date`; columns 2…1212 are bodies in
  the order given by `body_names.csv` (named tables) or `unnamed_mba_names.csv`
  (control table).
- A blank/`0` in `body_names.verified` marks a body with an incomplete ephemeris
  over the window; those columns are dropped by the analysis.
- FPOA is the First Point of Aries — 0° tropical Aries, the vernal equinox.

## Derived results (`results/`)

| File | Meaning |
|------|---------|
| `summary.json` | Single source of truth: dataset facts, signal statistics, null comparisons, robustness curve, sidereal test. Consumed by the report and the web page. |
| `null_comparison.csv` | Observed statistic vs each null, effect ratios, p-values, axis-free and fixed-axis Bayes factors. |
| `robustness_curve.csv` | Joint Σ ACF² as highest-coverage vs random bodies are removed. |
| `reconstructed_acf.csv` | Independently recomputed ACF at the nine aspect lags, with the single-cosine reference `cos(lag)`. |
| `fpoa_v_bf_*.npy`, `fpoa_v_p_*.npy` | Directional Bayes-factor and p-value curves (360 axis directions) for each null. |
| `fpoa_axial_audit.png` | The four-panel audit figure. |
