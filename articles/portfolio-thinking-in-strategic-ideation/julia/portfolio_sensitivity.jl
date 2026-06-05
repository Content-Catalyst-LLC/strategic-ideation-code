# Advanced Julia strategic portfolio sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "strategic_ideas.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["idea_id", "idea_name", "portfolio_contribution", "overload_warning", "adaptive_viability"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    contribution =
        0.17 * num(row, "impact") +
        0.16 * num(row, "strategic_fit") +
        0.15 * num(row, "learning_value") +
        0.15 * num(row, "option_value") +
        0.12 * num(row, "ethical_resilience") +
        0.10 * num(row, "evidence_strength") +
        0.08 * num(row, "governance_readiness") -
        0.10 * num(row, "risk") -
        0.08 * num(row, "capacity_demand") -
        0.04 * min(num(row, "dependency_count") / 6, 1)

    overload =
        0.30 * num(row, "capacity_demand") +
        0.24 * num(row, "risk") +
        0.14 * (1 - num(row, "strategic_fit")) +
        0.12 * (1 - num(row, "ethical_resilience")) +
        0.10 * (1 - num(row, "option_value")) +
        0.10 * min(num(row, "dependency_count") / 6, 1)

    adaptive_viability =
        0.20 * num(row, "learning_value") +
        0.20 * num(row, "option_value") +
        0.18 * num(row, "strategic_fit") +
        0.16 * num(row, "ethical_resilience") +
        0.14 * num(row, "governance_readiness") -
        0.07 * num(row, "risk") -
        0.05 * num(row, "capacity_demand")

    push!(output, [
        row[col("idea_id")],
        row[col("idea_name")],
        round(contribution, digits = 4),
        round(overload, digits = 4),
        round(adaptive_viability, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_portfolio_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_portfolio_sensitivity.csv")
