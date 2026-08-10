# Blaque Baux Beyond

**Growth, measured in weeks — the CAGR lens applied over the short term, not years.**

Beyond is a member of the Blaque Baux family. The [core repo](https://github.com/Carter-Warrens/blaquebaux)
is the **engine and blueprint** — a governed, systematic platform (Julia) with a venue-agnostic
execution controller and a Layer-3 live-money safety gate. Beyond points that engine in its own
direction and inherits the governance wholesale.

> **Not investment advice.** Educational/research software. Nothing here is validated. See [LICENSE](LICENSE).

```bash
git clone --recursive https://github.com/Carter-Warrens/blaquebaux-beyond.git
julia --project=engine -e 'using Pkg; Pkg.instantiate()'   # one-time engine setup
```

## The thesis

Compound annual growth rate is a long-horizon idea; Beyond flips it short — annualizing near-term growth and trading its *acceleration*. Boom's 12-1 momentum shows leader-selection works at long horizons; Beyond asks whether short-horizon growth-rate acceleration is a prospective signal or just the mean-reverting chop the base's short-horizon tests keep flagging.

## Research plan (Path A — not yet built)

- Short-horizon growth momentum — annualized N-week growth, ranked, tilted; tested beta-neutral.
- Acceleration — is the *change* in short-term growth rate predictive beyond its level?
- Regime gate — separate genuine short-term compounding from mean-reverting chop (see Bounce).

Nothing above is implemented or validated. This is the map, not the territory.

## Status
**Scaffold.** Engine wired as a submodule; strategy research not yet conducted.

## The Blaque Baux family
This repo is one sleeve of the **Blaque Baux** family — a single governed engine steered in
many directions. The [core repo](https://github.com/Carter-Warrens/blaquebaux) is the
base/blueprint and holds the [full family roster](https://github.com/Carter-Warrens/blaquebaux#the-blaque-baux-family).

## Layout
```
engine/     the Blaque Baux platform (git submodule -> Carter-Warrens/blaquebaux)
research/   Path-A strategy sketches (to come)
live/       governed live drivers (once a sleeve graduates to paper A/B)
```

## License
[MIT](LICENSE). (c) 2026 Carter Warrens.
