# Advanced Julia strategic tradeoff sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "strategic_options.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["option_id", "option_name", "tradeoff_score", "fragility_warning", "projected_viability_after_40_steps"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    tradeoff_score =
        0.18 * num(row, "short_term_return") +
        0.20 * num(row, "resilience") +
        0.16 * num(row, "flexibility") +
        0.14 * num(row, "stakeholder_legitimacy") +
        0.14 * num(row, "opportunity_value") -
        0.18 * num(row, "exposure") +
        0.08 * num(row, "reversibility") +
        0.06 * num(row, "implementation_readiness") +
        0.08 * num(row, "ethical_resilience") +
        0.08 * num(row, "learning_value")

    fragility_warning =
        0.26 * num(row, "exposure") +
        0.18 * (1 - num(row, "resilience")) +
        0.14 * (1 - num(row, "flexibility")) +
        0.12 * (1 - num(row, "stakeholder_legitimacy")) +
        0.12 * (1 - num(row, "opportunity_value")) +
        0.10 * (1 - num(row, "reversibility")) +
        0.08 * (1 - num(row, "ethical_resilience"))

    state = 1.0
    option_value_path = num(row, "opportunity_value")

    for t in 2:40
        if t < 20
            shock = 0.03
            gain = 0.18 * num(row, "short_term_return") + 0.06 * num(row, "flexibility")
        else
            shock = 0.14
            gain =
                0.10 * num(row, "short_term_return") +
                0.16 * num(row, "resilience") +
                0.12 * num(row, "flexibility") +
                0.08 * option_value_path -
                0.14 * num(row, "exposure")
        end

        option_value_path = min(1.2, max(0.0, option_value_path + 0.04 * num(row, "flexibility") - 0.05 * num(row, "exposure")))
        state = min(1.8, max(0.0, state + gain / 4 - shock / 5))
    end

    push!(output, [
        row[col("option_id")],
        row[col("option_name")],
        round(tradeoff_score, digits = 4),
        round(fragility_warning, digits = 4),
        round(state, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_strategic_tradeoff_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_strategic_tradeoff_sensitivity.csv")
