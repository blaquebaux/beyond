#!/usr/bin/python3
# =============================================================================
# _beyond_common.py — shared helpers for the Blaque Baux Beyond (short-horizon growth) sketches.
# Alpaca SIP daily bars; reads ALPACA_KEY_ID / ALPACA_SECRET_KEY from env. Read-only.
# NOTE: annualizing a short-horizon return (the "CAGR lens") is a monotonic transform,
# so it does not change the cross-sectional ranking — what matters is the HORIZON.
# =============================================================================
import os, json, urllib.request, math
import numpy as np

H = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
START, END = "2016-01-01", "2026-08-01"
_cache = {}

BASKET = ["AAPL","MSFT","NVDA","AMZN","GOOGL","META","AVGO","TSLA","JPM","V","MA","UNH","HD","PG","XOM","JNJ",
"COST","WMT","BAC","KO","PEP","CVX","MRK","CRM","ADBE","NFLX","AMD","INTC","QCOM","TXN","ORCL","DIS","GS","MS","CAT","HON","LLY","ABBV","TMO","NKE"]

def bars(s):
    if s in _cache: return _cache[s]
    u = (f"https://data.alpaca.markets/v2/stocks/bars?symbols={s}&timeframe=1Day"
         f"&start={START}&end={END}&adjustment=all&feed=sip&limit=10000")
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40))
        _cache[s] = {b["t"][:10]: b for b in d.get("bars", {}).get(s, [])}
    except Exception:
        _cache[s] = {}
    return _cache[s]

def panel(syms):
    D = {s: bars(s) for s in syms}; D = {s: v for s, v in D.items() if len(v) > 500}
    u = list(D); dates = sorted(set.intersection(*[set(D[s]) for s in u]))
    return u, dates, np.array([[D[s][d]["c"] for s in u] for d in dates], float)

def sharpe(r):
    r = np.asarray(r, float); r = r[np.isfinite(r)]
    return r.mean() / r.std() * math.sqrt(252) if len(r) > 30 and r.std() > 0 else float('nan')

def beta(y, x):
    m = np.isfinite(y) & np.isfinite(x); y, x = y[m], x[m]
    return np.cov(y, x)[0, 1] / np.var(x) if len(y) > 30 and np.var(x) > 0 else float('nan')

def eff_ratio(P, n=20):
    er = np.full(len(P), np.nan)
    for t in range(n, len(P)):
        v = np.sum(np.abs(np.diff(P[t - n:t + 1]))); er[t] = abs(P[t] - P[t - n]) / v if v > 0 else np.nan
    return er

def spy_series(dates):
    sp = bars("SPY"); c = {d: sp[d]["c"] for d in sp}
    spc = np.array([c.get(d, np.nan) for d in dates])
    er = eff_ratio(np.array([sp[d]["c"] for d in sorted(sp)]))
    em = {d: e for d, e in zip(sorted(sp), er)}
    return spc[1:] / spc[:-1] - 1, np.array([em.get(d, np.nan) for d in dates])
