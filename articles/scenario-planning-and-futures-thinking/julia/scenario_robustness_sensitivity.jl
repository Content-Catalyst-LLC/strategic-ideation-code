# Advanced Julia scenario robustness sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "strategy_stress_tests.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenario_cols = [
    "scenario_stable_growth",
    "scenario_tech_disruption",
    "scenario_environmental_stress",
    "scenario_institutional_fragmentation",
    "scenario_supply_disruption"
]

output = [["test_id", "strategy_name", "mean_performance", "worst_case", "volatility", "robustness_profile", "fragility_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]
    values = [num(row, c) for c in scenario_cols]

    mean_performance = mean(values)
    worst_case = minimum(values)
    volatility = std(values)

    robustness =
        0.30 * worst_case +
        0.24 * mean_performance +
        0.16 * num(row, "flexibility") +
        0.12 * num(row, "implementation_readiness") +
        0.10 * num(row, "ethical_resilience") +
        0.10 * num(row, "option_value") -
        0.12 * volatility

    fragility =
        0.30 * (1 - worst_case) +
        0.18 * volatility +
        0.14 * (1 - num(row, "flexibility")) +
        0.12 * (1 - num(row, "option_value")) +
        0.10 * (1 - num(row, "ethical_resilience")) +
        0.08 * (1 - num(row, "implementation_readiness"))

    push!(output, [
        row[col("test_id")],
        row[col("strategy_name")],
        round(mean_performance, digits = 4),
        round(worst_case, digits = 4),
        round(volatility, digits = 4),
        round(robustness, digits = 4),
        round(fragility, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_scenario_robustness_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_scenario_robustness_sensitivity.csv")
