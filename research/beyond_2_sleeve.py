#!/usr/bin/python3
# =============================================================================
# beyond_2_sleeve.py — BLAQUE BAUX BEYOND #2: the sleeve, acceleration, and the gate.
#
# Three findings that shape the Beyond keeper:
#   (a) THE CLEAN FORM is long top-quintile growth MINUS the equal-weight basket
#       (beta-neutral), NOT long-winners/short-losers — because shorting recent LOSERS
#       fails (they bounce). Best at ~60 days.
#   (b) ACCELERATION is NOT momentum: the CHANGE in growth rate is a reversal signal
#       (long-accelerating/short-decelerating loses). The level (horizon return) carries
#       the continuation, not the 2nd derivative.
#   (c) THE REGIME GATE mirrors Bounce: momentum improves when gated to TREND regimes
#       (as Bounce's reversal improves when gated to chop).
#
# RESULTS AS TESTED (2016-2026, net 2 bp/side):
#   (a) long top-q − EW: 20d +0.36 | 40d +0.32 | 60d +0.52  (beta ~0)
#   (b) 40d level L/S +0.02  vs  40d acceleration L/S -0.42
#   (c) 40d momentum L/S: ungated +0.02  ->  gated to trend (ER>0.31) +0.16
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
def run(score, reb, mode, gate=None, cost_bps=2.0):
    k = max(1, int(N * 0.2)); wp = np.zeros(N); pnl = []; c = cost_bps / 1e4
    for t in range(1, T - 1):
        if (t - 1) % reb == 0:
            s = score[t]; m = np.isfinite(s)
            if m.sum() < 2 * k: pnl.append(np.nan); continue
            o = np.argsort(np.where(m, s, np.nan)); w = np.zeros(N)
            if mode == "neutral": w[o[-k:]] = 1 / k; w -= m / m.sum()
            else: w[o[-k:]] = 1 / k; w[o[:k]] = -1 / k
            if gate is not None and not (erb[t] > gate): w = np.zeros(N)
        else:
            w = wp
        pnl.append(float(np.nansum(w * R[t + 1])) - np.abs(w - wp).sum() * c); wp = w
    return np.array(pnl)

print("=" * 72, "\nBEYOND #2 — the sleeve, acceleration, and the regime gate\n" + "=" * 72)
print("(a) clean form — long top-q growth MINUS EW (beta-neutral), net:")
for Hh in [20, 40, 60]:
    p = run(growth(Hh), max(5, Hh // 4), "neutral")
    print(f"     {Hh}d growth: Sharpe {sharpe(p):+.2f}  beta-SPY {beta(p, spr[1:len(p)+1]):+.2f}")
acc = np.full((T, N), np.nan)
for t in range(80, T): acc[t] = (M[t] / M[t-40] - 1) - (M[t-40] / M[t-80] - 1)
print("\n(b) level vs acceleration (40d, long/short, net):")
print(f"     level  Sharpe {sharpe(run(growth(40),10,'ls')):+.2f}   acceleration Sharpe {sharpe(run(acc,10,'ls')):+.2f}  (accel = reversal, not momentum)")
q = np.nanpercentile(erb, 66)
print("\n(c) regime gate (40d momentum L/S, net):")
print(f"     ungated {sharpe(run(growth(40),10,'ls')):+.2f}   gated to trend (ER>{q:.2f}) {sharpe(run(growth(40),10,'ls',gate=q)):+.2f}")
print("\nVERDICT: express growth as long-winners-minus-market (not short-losers); the level")
print("not the acceleration; and gate to trend regimes. The keeper is in beyond_prototype.py.")
