#!/usr/bin/env julia
# beyond_validation.jl — validate-before-live gate for the BEYOND sleeve (walk-forward / OOS / net-of-cost).
# Reuses beyond_target from beyond_live.jl. Run:  julia --project=engine live/beyond_validation.jl
include(joinpath(@__DIR__, "beyond_live.jl"))
include(joinpath(@__DIR__, "_sleeve_validation.jl"))
validate_sleeve(beyond_target; label = "BEYOND", universe = UNIVERSE, warmup = 120, kind = :neutral)
