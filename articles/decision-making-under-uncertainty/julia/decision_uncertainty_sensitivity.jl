# Advanced Julia decision-making under uncertainty sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "decision_options.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["option_id", "option_name", "decision_profile_score", "fragility_risk", "projected_viability_after_40_steps"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    profile =
        0.14 * num(row, "expected_return") +
        0.18 * num(row, "robustness") +
        0.16 * num(row, "flexibility") +
        0.12 * num(row, "information_quality") -
        0.16 * num(row, "exposure") +
        0.14 * num(row, "option_value") +
        0.10 * num(row, "reversibility") +
        0.08 * num(row, "implementation_readiness") +
        0.10 * num(row, "ethical_resilience") +
        0.10 * num(row, "learning_value")

    fragility =
        0.24 * num(row, "exposure") +
        0.18 * (1 - num(row, "robustness")) +
        0.14 * (1 - num(row, "flexibility")) +
        0.13 * (1 - num(row, "option_value")) +
        0.12 * (1 - num(row, "reversibility")) +
        0.10 * (1 - num(row, "ethical_resilience")) +
        0.09 * (1 - num(row, "information_quality"))

    state = 1.0
    option_path = num(row, "option_value")

    for t in 2:40
        if t < 20
            shock = 0.03
            gain = 0.18 * num(row, "expected_return") + 0.08 * num(row, "flexibility")
        else
            shock = 0.15
            gain =
                0.08 * num(row, "expected_return") +
                0.18 * num(row, "robustness") +
                0.14 * num(row, "flexibility") +
                0.08 * option_path -
                0.14 * num(row, "exposure")
        end

        option_path = min(1.2, max(0.0, option_path + 0.04 * num(row, "flexibility") - 0.05 * num(row, "exposure")))
        state = min(1.8, max(0.0, state + gain / 4 - shock / 5))
    end

    push!(output, [
        row[col("option_id")],
        row[col("option_name")],
        round(profile, digits = 4),
        round(fragility, digits = 4),
        round(state, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_decision_uncertainty_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_decision_uncertainty_sensitivity.csv")
