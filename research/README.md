# Blaque Baux Beyond — research

First-pass Path-A research on the short-horizon "growth" sleeve — the CAGR lens applied
over weeks. (Honest note: annualizing a short return is a monotonic transform, so it does
not change the cross-sectional ranking; the real levers are **horizon** and **acceleration**.)
All sketches read Alpaca SIP daily bars, are read-only, print their own results. 2016–2026,
40-name liquid basket, costs at 2 bp/side.

```bash
export $(grep -v '^#' ~/.config/blaquebaux/alpaca.env | xargs)   # or source it
python research/beyond_1_horizon_curve.py   # where reversal becomes momentum
python research/beyond_prototype.py         # the keeper
```

## Scorecard

| # | Question | Result | Verdict |
|---|----------|--------|---------|
| 1 | Where does growth flip from reversal to momentum? | reversal ≤10d, **momentum ≥20d** | ✅ mapped (flagship) |
| 2a | Clean form of the sleeve? | long top-q **minus EW** (not short-losers) — 60d +0.52 net, β~0 | ✅ keeper |
| 2b | Does acceleration (Δ growth) help? | −0.42 — acceleration is a *reversal* signal | ❌ rejected |
| 2c | Regime gate? | momentum improves gated to **trend** (+0.02→+0.16) | ✅ (mirrors Bounce) |

## The synthesis

Beyond fills the horizon gap in the family's momentum picture:

| horizon | behavior | sleeve |
|---|---|---|
| ≤ 10 days | reversal | **Bounce** (gated to chop) |
| ~20–60 days ("weeks") | **momentum** | **Beyond** (this repo) |
| ~12 months | momentum | **Boom** |

- **#1 (flagship):** the cross-section reverses at ≤10 days and turns to momentum at ≥20 —
  the transition is real and marks where "growth over weeks" becomes a continuation signal.

- **#2a (the keeper):** express it as **long top-quintile growth minus the equal-weight
  basket** (beta-neutral), *not* long-winners/short-losers — because shorting recent losers
  fails (they bounce, per Blunt #5 / Bounce). Net Sharpe 20d +0.36, 40d +0.32, **60d +0.52**,
  beta ~0.

- **#2b:** acceleration (the *change* in growth rate) is **not** momentum — it is a reversal
  signal (−0.42). The level carries the continuation; the 2nd derivative over-extends and reverts.

- **#2c:** the regime gate mirrors Bounce exactly — momentum improves when restricted to
  *trend* regimes, as reversal improves in *chop*. Same efficiency-ratio detector, opposite sign.

## The keeper

`beyond_prototype.py`: multi-horizon (20/40/60-day) growth, long top-q minus EW, beta-neutral,
net of 2 bp/side.

| | Sharpe | beta-SPY |
|---|---|---|
| multi-horizon blend | **+0.50** | −0.01 |
| single 60d | +0.65 | — |
| first / second half | +0.76 / +0.29 | (positive but **decaying**) |
| corr to Boom (252d momentum) | +0.34 | (same family, distinct horizon) |
| corr to 5-day reversal | −0.32 | (opposite of Bounce) |

A genuine keeper, with two honest caveats: the edge **decays** across the sample (+0.76 → +0.29
recent), and it is the shorter-horizon **cousin of Boom** (corr +0.34), so its diversification
value overlaps Boom more than the market-neutral sleeves (Bore/Bounce) do. Still beta-neutral
and a distinct horizon — a useful multi-sleeve ingredient. Not validated to the spine's bar.

## Files
- `_beyond_common.py` — shared helpers.
- `beyond_1_horizon_curve.py` — the reversal→momentum flip across horizons.
- `beyond_2_sleeve.py` — clean form (long-minus-EW), acceleration rejected, the regime gate.
- `beyond_prototype.py` — the keeper: multi-horizon short-growth, beta-neutral.
