# A weak axial modulation of named-minor-planet news presence, on the equinoctial axis

This repository is a self-contained replication and audit of a single, well-posed
question: when the daily news presence of named minor planets is pooled by
ecliptic longitude, is the resulting wave organised around the **equinoctial
(Aries–Libra) axis** defined by the **First Point of Aries (FPOA)** — the zero of
the tropical zodiac, the vernal equinox?

The short answer is **yes, weakly, and specifically as one axis rather than as
nine independent astrological aspects.** The joint autocorrelation of the news
wave at the nine classical aspect separations runs about **4–5× its chance
expectation** against two count-preserving null models (Monte-Carlo
p ≈ 0.006 and 0.015), the entire pattern collapses to a **single low-order
cosine** (the nine aspect-lag autocorrelations track one cosine at r = 0.98),
and that cosine's axis lands **within ~2° of the pre-registered equinoctial
axis**. Because FPOA is fixed a priori by the coordinate system, the appropriate
evidence measure is the **fixed-axis** Bayes factor, which reaches ≈ 21 against
the unnamed-minor-planet control.

## What is in this folder

| Path | Contents |
|------|----------|
| `data/` | The open, self-describing CSV tables (article counts, longitudes, body names). See `data_dictionary.md` (also `INFO_*.md` sheets). |
| `src/analysis.py` | The whole analysis, reading only `data/` and writing `results/summary.json` and the result CSVs. |
| `src/make_figure.py` | Builds `results/fpoa_axial_audit.png` (the four-panel audit). |
| `results/` | `summary.json` (single source of truth), result CSVs, and figures. |
| `site/index.html` | A self-contained, dynamic web page that reads `../results/summary.json` at load time. Deployable to Netlify as-is. |
| `paper/` | `report.docx`, a formal write-up whose every headline number is read from `results/summary.json` at build time. |
| `docs/` | The four markdown information sheets. |

## Information sheets (`docs/`)

1. **`INFO_1_overview.md`** — plain-language description of the question, the data, and the finding.
2. **`INFO_2_methods.md`** — how the wave, the autocorrelation, the nulls, and the Bayes factors are computed.
3. **`INFO_3_findings.md`** — the numbers, panel by panel, with interpretation.
4. **`data_dictionary.md`** — every column of every data file.

## Reproduce

```bash
pip install numpy pandas scipy matplotlib python-docx
cd src
python analysis.py       # writes results/summary.json + result CSVs
python make_figure.py     # writes results/fpoa_axial_audit.png
python build_report.py    # writes paper/report.docx from results/summary.json
```

The analysis is deterministic (seed 42, 3,000 Monte-Carlo iterations). The
documents never hand-type a number: both `report.docx` and `site/index.html`
draw from `results/summary.json`, so they cannot drift from the analysis.

## The one-paragraph method

Each verified named body's daily Google-News article count is normalised to unit
L2 length (so a heavily-covered body and a lightly-covered one contribute equal
total weight), then binned by its integer ecliptic longitude measured from FPOA
into a single 360-point wave (a per-bin mean). The primary instrument is the
biased circular autocorrelation function read at the nine aspect lags
{30, 36, 40, 45, 60, 72, 90, 120, 180}°, summarised by the joint Σ ACF². A
supporting directional V-test and a single-cosine fit characterise the signal as
one coherent low-order axial pattern. Significance is Monte-Carlo against a
compound permutation null and a stricter unnamed-minor-planet null; for the axial
cosine we report a model-based Bayes factor, both with the axis estimated from
the data and with it fixed at the equinoctial axis in advance.

## Scope and honesty

This is an **observational, exploratory** result on a **single 290-day window**
of one news index. It establishes an internally consistent, reproducible
statistical pattern and locates it on the tropical equinoctial axis. It does
**not** establish a mechanism, and the axis-free effect is weak. The `docs/` and
`paper/` materials state these limits explicitly.
