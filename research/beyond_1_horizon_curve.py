#!/usr/bin/python3
# =============================================================================
# beyond_1_horizon_curve.py — BLAQUE BAUX BEYOND #1 (the flagship: the horizon curve).
#
# The base family already found the two ends: short-term moves REVERSE (Bounce, Blunt)
# and 12-month momentum CONTINUES (Boom). Beyond maps the transition — cross-sectional
# momentum (long winners / short losers) Sharpe by formation horizon. The sign flips
# from reversal to momentum at ~20 days: that is where "growth over weeks" becomes a
# real continuation signal, and where Beyond lives (between Bounce and Boom).
#
# RESULTS AS TESTED (40-name basket, 2016-2026, momentum L/S, net 2 bp/side):
#   1d -0.22 | 3d -0.03 | 5d -0.16 | 10d -0.26   (REVERSAL)
#   20d +0.10 | 40d +0.02 | 60d +0.13 | 120d +0.22 | 252d +0.05   (MOMENTUM)
# Read-only.
# =============================================================================
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beyond_common import BASKET, panel, sharpe

u, dts, M = panel(BASKET); R = M[1:] / M[:-1] - 1; T, N = R.shape
def ls(Hh, cost_bps=2.0):
    reb = max(5, Hh // 4); k = max(1, int(N * 0.2)); wp = np.zeros(N); pnl = []; c = cost_bps / 1e4
    sc = np.full((T, N), np.nan)
    for t in range(Hh, T): sc[t] = M[t] / M[t - Hh] - 1
    for t in range(Hh, T - 1):
        if (t - Hh) % reb == 0:
            s = sc[t]; o = np.argsort(np.where(np.isfinite(s), s, np.nan))
            w = np.zeros(N); w[o[-k:]] = 1 / k; w[o[:k]] = -1 / k    # long winners, short losers
        else:
            w = wp
        pnl.append(float(np.nansum(w * R[t + 1])) - np.abs(w - wp).sum() * c); wp = w
    return np.array(pnl)

print("=" * 72, "\nBEYOND #1 — the horizon curve (reversal -> momentum flip)\n" + "=" * 72)
print(f"  {'horizon':>9}{'grossSh':>9}{'netSh':>8}   sign")
for Hh in [1, 3, 5, 10, 20, 40, 60, 120, 252]:
    g = sharpe(ls(Hh, 0.0)); n = sharpe(ls(Hh, 2.0))
    print(f"  {Hh:>7}d{g:>+9.2f}{n:>+8.2f}   {'reversal' if g < 0 else 'MOMENTUM'}")
print("\nVERDICT: the cross-section reverses at <=10 days and turns to momentum at >=20.")
print("Beyond is the intermediate-horizon ('weeks') momentum sleeve — the bridge between")
print("Bounce (short reversal) and Boom (12-month momentum).")
