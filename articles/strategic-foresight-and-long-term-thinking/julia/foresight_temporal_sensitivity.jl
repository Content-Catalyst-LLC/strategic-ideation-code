# Advanced Julia strategic foresight temporal sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "foresight_profiles.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["profile_id", "strategy_name", "future_viability_score", "short_term_bias", "projected_viability_after_40_steps"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    future_viability =
        0.18 * num(row, "foresight_depth") +
        0.18 * num(row, "resilience") +
        0.16 * num(row, "flexibility") +
        0.14 * num(row, "option_value") +
        0.12 * num(row, "scenario_capacity") +
        0.10 * num(row, "signal_capacity") +
        0.08 * num(row, "governance_capacity") +
        0.08 * num(row, "ethics_review") -
        0.14 * num(row, "path_dependence_risk")

    short_term_bias =
        num(row, "short_term_return") -
        mean([
            num(row, "foresight_depth"),
            num(row, "resilience"),
            num(row, "flexibility"),
            num(row, "option_value")
        ])

    state = 1.0
    option_value = num(row, "option_value")
    for t in 2:40
        if t < 20
            shock = 0.03
            gain = 0.14 * num(row, "short_term_return") + 0.08 * num(row, "flexibility") + 0.06 * num(row, "foresight_depth")
        else
            shock = 0.15
            gain =
                0.08 * num(row, "short_term_return") +
                0.18 * num(row, "resilience") +
                0.14 * num(row, "flexibility") +
                0.12 * num(row, "foresight_depth") +
                0.08 * num(row, "signal_capacity") -
                0.16 * num(row, "path_dependence_risk")
        end

        option_value = min(1.2, max(0.0, option_value + 0.04 * num(row, "flexibility") + 0.04 * num(row, "foresight_depth") - 0.06 * num(row, "path_dependence_risk")))
        state = min(1.8, max(0.0, state + gain / 4 - shock / 5 + option_value / 45))
    end

    push!(output, [
        row[col("profile_id")],
        row[col("strategy_name")],
        round(future_viability, digits = 4),
        round(short_term_bias, digits = 4),
        round(state, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_foresight_temporal_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_foresight_temporal_sensitivity.csv")
