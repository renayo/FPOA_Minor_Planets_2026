# Information sheet 1 — Overview

## The question in one sentence

Do named minor planets attract news coverage in a way that is organised around
the **equinoctial axis** — the line through 0° Aries and 180° Libra that the
First Point of Aries (FPOA) defines as the zero of the tropical zodiac?

## Why FPOA, and why "axial"

The **First Point of Aries** is the vernal equinox: the point where the Sun
crosses the celestial equator going north, and by long convention the origin of
ecliptic longitude in the tropical zodiac. It is not a quantity fitted to these
data — it is fixed by the coordinate system, the same way 0° longitude on Earth
is fixed at Greenwich. The **ayanamsha**, the offset between the tropical and
sidereal zodiacs, is likewise a defined constant. Both conventions therefore
name the **same equinoctial axis in advance**. That matters for the statistics:
a hypothesis about a *pre-specified* direction is tested differently from one
that hunts for the best direction after seeing the data.

"Axial" means the pattern is symmetric under a 180° flip — a concentration near
one end of the Aries–Libra line and a matching thinning near the other. A single
cosine with period 360° is the simplest such shape.

## The data

- **1,122** named minor planets with a complete ephemeris over the window (of
  1,211 compiled).
- **290 days**, 2022-02-15 to 2022-12-01.
- For each body and day: a **Google-News article count** for the body's name, and
  the body's **ecliptic longitude measured from FPOA**.
- A control pool of **1,211 unnamed main-belt asteroids** with comparable orbits
  but no cultural identity.

## What we do with it

1. Give every body equal total weight (normalise each body's daily count series
   to unit length), so a heavily-covered body cannot dominate by volume.
2. Bin all bodies by longitude-from-FPOA into one 360-point **news-presence
   wave** (a per-bin average).
3. Measure how strongly that wave **autocorrelates at the nine classical
   aspect angles** {30, 36, 40, 45, 60, 72, 90, 120, 180}°.
4. Ask whether the measured autocorrelation is larger than chance, using two
   different definitions of "chance."
5. Characterise the shape: is it nine independent bumps, or one axis?
6. Locate the axis and compare it to the pre-registered equinoctial axis, in
   both the tropical (FPOA) and sidereal (ayanamsha-shifted) frames.

## The finding

- The joint aspect autocorrelation is **≈ 4–5× its chance level**
  (p ≈ 0.006 against a compound permutation null, ≈ 0.015 against the
  unnamed-minor-planet control).
- The pattern is **one weak cosine**, not nine aspects: the nine aspect-lag
  autocorrelations follow a single cosine at **r = 0.98**, and the first harmonic
  alone carries **30%** of the wave's variance while every higher harmonic
  carries under 3%.
- The cosine's axis sits **within ~2° of the equinoctial axis**, and among all
  360 possible fixed axes the evidence peaks essentially **on FPOA**.
- Under the correct pre-registered (fixed-axis) treatment, the Bayes factor for
  that axial cosine reaches **≈ 21** against the unnamed-minor-planet control.
- The signal **prefers the tropical axis over the sidereal one**: the data axis
  is ~2° from tropical Aries–Libra but ~26° from the sidereal (Lahiri) Aries
  point, and the fixed-axis Bayes factor is higher at the tropical axis
  (≈ 21) than at the sidereal axis (≈ 14).

## What the finding is not

It is a reproducible statistical regularity in one news index over one 290-day
window. It is **not** a demonstrated physical or causal mechanism, and the
effect is weak when the axis is treated as unknown. Sheet 3 (`INFO_3_findings.md`)
gives the numbers and the caveats in full.
