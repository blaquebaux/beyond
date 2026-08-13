# Blaque Baux Beyond

**Growth, measured in weeks — the CAGR lens applied over the short term, not years.**

Beyond is a member of the Blaque Baux family. The [core repo](https://github.com/blaquebaux/base)
is the **engine and blueprint** — a governed, systematic platform (Julia) with a venue-agnostic
execution controller and a Layer-3 live-money safety gate. Beyond points that engine in its own
direction and inherits the governance wholesale.

> **Not investment advice.** Educational/research software. Nothing here is validated. See [LICENSE](LICENSE).

```bash
git clone --recursive https://github.com/blaquebaux/beyond.git
julia --project=engine -e 'using Pkg; Pkg.instantiate()'   # one-time engine setup
```

## The thesis

Compound annual growth rate is a long-horizon idea; Beyond flips it short — annualizing near-term growth and trading its *acceleration*. Boom's 12-1 momentum shows leader-selection works at long horizons; Beyond asks whether short-horizon growth-rate acceleration is a prospective signal or just the mean-reverting chop the base's short-horizon tests keep flagging.

## Research plan (Path A — not yet built)

- Short-horizon growth momentum — annualized N-week growth, ranked, tilted; tested beta-neutral.
- Acceleration — is the *change* in short-term growth rate predictive beyond its level?
- Regime gate — separate genuine short-term compounding from mean-reverting chop (see Bounce).

## Research — first pass done

Full detail in [`research/README.md`](research/README.md). The scorecard:

| # | Question | Verdict |
|---|----------|---------|
| 1 | Where does growth flip from reversal to momentum? | ✅ **mapped** — reversal ≤10d, momentum ≥20d |
| 2a | Clean form of the sleeve? | ✅ **keeper** — long top-q minus EW, 60d +0.52 net, β~0 |
| 2b | Does acceleration help? | ❌ rejected — Δ growth is a *reversal* signal (−0.42) |
| 2c | Regime gate? | ✅ momentum improves gated to *trend* (mirror of Bounce) |

**The synthesis:** Beyond fills the horizon gap between Bounce (≤10d reversal) and Boom
(12-month momentum). The cross-section flips from reversal to momentum at ~20 days, so
"growth over weeks" *is* a real continuation signal — expressed the clean way (long winners
**minus the market**, not short the losers, which bounce). Keeper: multi-horizon (20/40/60)
growth, beta-neutral, **net +0.50** (single 60d +0.65), beta ~0. Two honest caveats — the
edge **decays** (+0.76 → +0.29 across halves) and it's the shorter-horizon cousin of Boom
(corr +0.34), so it overlaps the momentum family more than the market-neutral sleeves do.
Acceleration (Δ growth) is rejected — it's reversal, not momentum.

## Status
**Research: first pass complete; multi-horizon keeper — standalone driver built** (`research/` +
`live/`). `live/beyond_live.jl` runs it standalone through the engine's governed order path + Layer-3
safety gate: long the top-quintile by 20/40/60-day growth minus the equal-weight basket (beta ~0),
~1× gross. **Dry-run by default**; graduates to paper with its own isolated keys. Not validated to the
spine's bar.
```bash
BB_DRYRUN=1 julia --project=engine live/beyond_live.jl
```

## About Blaque Baux

**Blaque Baux** is a quantitative research initiative and a subsidiary of **[Carter Warrens](https://carterwarrens.com)**.
[**BlaqueBaux.com**](https://blaquebaux.com) is the home for the work; the code lives here on GitHub — open to
study, test, and build bespoke strategies on top of.

Anyone can point an AI at a market. The edge is **understanding what the data actually says — and turning it
into something you can act on.** We test relentlessly and put most of it *on the record as rejected, with the
reason*; what survives is built, governed, and validated before it is ever called real. That combination —
honest research, reproducible evidence, and execution you can trust — is why Carter Warrens leads on
**strategy and implementation**, not merely uses the tools everyone now has.

## The Blaque Baux family
This repo is one sleeve of the **Blaque Baux** family — a single governed engine steered in
many directions. The [core repo](https://github.com/blaquebaux/base) is the
base/blueprint and holds the [full family roster](https://github.com/blaquebaux/base#the-blaquebaux-family).

## Layout
```
engine/     the Blaque Baux platform (git submodule -> blaquebaux/base)
research/   three Path-A sketches (horizon curve, sleeve/acceleration/gate) + prototype + scorecard
live/       governed live drivers (once a sleeve graduates to paper A/B)
```

## License
[MIT](LICENSE). (c) 2026 Carter Warrens.
