#!/usr/bin/env julia
# ============================================================================
# beyond_live.jl — BLAQUE BAUX BEYOND live driver (short-horizon growth-momentum).
#
# Runs on the engine (engine/ submodule) — same governed order path + Layer-3 safety gate as the spine.
# SIGNAL (research keeper): the cross-section turns from reversal (<=10d) to MOMENTUM at ~20-60 days.
# Express it the clean way — LONG the top-quintile by multi-horizon (20/40/60-day) growth, SHORT the
# equal-weight basket (beta ~0) — NOT long-winners/short-losers (shorting recent losers fails; they
# bounce). Net Sharpe ~+0.52 (60d), beta ~0. Held at ~1x gross.
#
# MODES: dry-run by default via the wrapper (BB_DRYRUN=1). Paper: unset BB_DRYRUN with paper keys.
# Real money requires BB_LIVE_CONFIRM=I_UNDERSTAND_THIS_IS_REAL_MONEY. Kill switch: ~/.config/blaquebaux/HALT.
# Run: julia --project=engine live/beyond_live.jl.  NOT validated to the spine's bar.
# ============================================================================
using Dates, Printf, Statistics

const REPO   = normpath(joinpath(@__DIR__, ".."))
const ENGINE = joinpath(REPO, "engine")
for m in ("module_7_execution/module_7_execution.jl","module_10_feedback/module_10_feedback.jl",
          "module_13_portfolio/module_13_portfolio.jl","module_1_data/equity_panel.jl",
          "module_1_data/alpaca_panel.jl","module_8_governance/safety_gate.jl")
    include(joinpath(ENGINE, "src", m))
end
using .ExecutionLayer, .FeedbackLayer, .PortfolioOptModule, .EquityPanel, .AlpacaPanel, .SafetyGate
include(joinpath(ENGINE, "scripts/live_execution.jl"))

const BASKET = ["AAPL","MSFT","NVDA","AMZN","GOOGL","META","AVGO","TSLA","JPM","V","MA","UNH","HD","PG","XOM","JNJ",
    "COST","WMT","BAC","KO","PEP","CVX","MRK","CRM","ADBE","NFLX","AMD","INTC","QCOM","TXN","ORCL","DIS","GS","MS","CAT","HON","LLY","ABBV","TMO","NKE"]
const UNIVERSE = BASKET
const LIVE_SENTINEL = "I_UNDERSTAND_THIS_IS_REAL_MONEY"
const GROSS = 1.0

function beyond_target(panel, cap)
    syms = panel.symbols; R = panel.returns; T = size(R, 1); N = length(BASKET)
    col(s) = R[:, findfirst(==(s), syms)]; px(s) = panel.prices[findfirst(==(s), syms)]
    B = hcat([col(s) for s in BASKET]...)
    score = zeros(N)                                                # composite rank over 20/40/60d growth
    for h in (20, 40, 60)
        g = [prod(1 .+ B[T-h+1:T, i]) - 1 for i in 1:N]; score .+= sortperm(sortperm(g))
    end
    k = max(1, round(Int, N * 0.2)); o = sortperm(score)            # ascending; top-q = highest score
    w = fill(-1.0/N, N); for j in o[end-k+1:end]; w[j] += 1.0/k; end   # long top-q, short EW (sum 0)
    s = GROSS / max(sum(abs, w), 1e-9); w .*= s
    net = Dict(BASKET[i] => w[i] for i in 1:N); price = Dict(s => px(s) for s in BASKET)
    (targets = Dict(s => round(Float64, net[s] * cap / price[s]) for s in BASKET), prices = price,
     net = net, gross = sum(abs, values(net)))
end

include(joinpath(@__DIR__, "_sleeve_main.jl"))
if abspath(PROGRAM_FILE) == @__FILE__; sleeve_main(beyond_target; label="beyond", signal_id="beyond",
    regime="growth-momentum", lookback=120, LIVE_SENTINEL=LIVE_SENTINEL, UNIVERSE=UNIVERSE, REPO=REPO); end
