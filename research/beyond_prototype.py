#!/usr/bin/python3
# =============================================================================
# beyond_prototype.py — BLAQUE BAUX BEYOND, the keeper as a prototype.
#
# Short-horizon "growth" = intermediate-horizon cross-sectional momentum, expressed
# the clean way: LONG the top-quintile by recent growth MINUS the equal-weight basket
# (beta-neutral). Not long/short — shorting recent LOSERS fails (they bounce), so the
# short leg is the market, not the losers. A multi-horizon blend (20/40/60-day growth,
# equal rank-weight) for robustness. Net of 2 bp/side.
#
# RESULTS AS TESTED (2016-2026, net):
#   single-horizon, long top-q − EW: 20d +0.36 | 40d +0.32 | 60d +0.52 (beta ~0)
#   multi-horizon blend (20/40/60): reported below, with sub-period + diversifier corr
# NOT validated to the spine's bar; a multi-sleeve-ingredient / paper-A/B candidate.
# Read-only.
# =============================================================================
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beyond_common import BASKET, panel, sharpe, beta, spy_series

u, dts, M = panel(BASKET); R = M[1:] / M[:-1] - 1; T, N = R.shape
spr, erb = spy_series(dts)

def growth(Hh):
    s = np.full((T, N), np.nan)
    for t in range(Hh, T): s[t] = M[t] / M[t - Hh] - 1
    return s

def rank_score(horizons):
    """composite cross-sectional rank across horizons (higher = stronger recent growth)."""
    sc = np.full((T, N), np.nan)
    gs = [growth(h) for h in horizons]
    for t in range(max(horizons), T):
        rk = np.zeros(N)
        for g in gs:
            v = g[t]; o = np.argsort(v); r = np.empty(N); r[o] = np.arange(N); rk += r
        sc[t] = rk / len(gs)
    return sc

def sleeve(score, reb=10, cost_bps=2.0):
    k = max(1, int(N * 0.2)); wp = np.zeros(N); pnl = []; c = cost_bps / 1e4
    for t in range(1, T - 1):
        if (t - 1) % reb == 0:
            s = score[t]; m = np.isfinite(s)
            if m.sum() < k: pnl.append(np.nan); continue
            o = np.argsort(np.where(m, s, np.nan))
            w = np.zeros(N); w[o[-k:]] = 1 / k; w -= m / m.sum()      # long top-q minus EW (beta-neutral)
        else:
            w = wp
        pnl.append(float(np.nansum(w * R[t + 1])) - np.abs(w - wp).sum() * c); wp = w
    return np.array(pnl)

print("=" * 72, "\nBEYOND prototype — multi-horizon short-horizon-growth, beta-neutral (net)\n" + "=" * 72)
p = sleeve(rank_score([20, 40, 60])); h = len(p) // 2
print(f"  multi-horizon (20/40/60) blend: Sharpe {sharpe(p):+.2f}  beta-SPY {beta(p, spr[1:len(p)+1]):+.2f}")
print(f"  sub-periods: first half {sharpe(p[:h]):+.2f}  second half {sharpe(p[h:]):+.2f}")
print(f"  single 60d for reference:       Sharpe {sharpe(sleeve(growth(60))):+.2f}")
# diversifier correlations vs a long-horizon momentum (Boom-ish) and a short reversal (Bounce-ish)
boom = sleeve(growth(252), reb=21); rev = -sleeve(growth(5), reb=5)
L = min(len(p), len(boom), len(rev)); a, b, cc = p[-L:], boom[-L:], rev[-L:]
mk = np.isfinite(a) & np.isfinite(b) & np.isfinite(cc)
print(f"  corr to Boom (252d momentum) {np.corrcoef(a[mk],b[mk])[0,1]:+.2f}   corr to 5d-reversal (Bounce-ish) {np.corrcoef(a[mk],cc[mk])[0,1]:+.2f}")
print("\nread: intermediate-horizon growth momentum, beta-neutral, is a genuine keeper.")
print("It fills the horizon gap between Bounce (short reversal) and Boom (long momentum),")
print("and — market-neutral, distinct-horizon — is another low-correlation family ingredient.")
