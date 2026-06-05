# Advanced Julia strategy conversion sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "initiatives.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["initiative_id", "initiative_name", "strategy_conversion_score", "confidence_adjusted_score", "implementation_warning"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    score =
        0.14 * num(row, "feasibility") +
        0.15 * num(row, "viability") +
        0.13 * num(row, "desirability") -
        0.11 * num(row, "integration_difficulty") +
        0.15 * num(row, "execution_readiness") +
        0.13 * num(row, "strategic_fit") +
        0.08 * num(row, "evidence_confidence") +
        0.08 * num(row, "ethical_resilience") -
        0.07 * num(row, "resource_intensity") +
        0.10 * num(row, "governance_readiness") +
        0.06 * num(row, "learning_value")

    confidence_adjusted = score * num(row, "evidence_confidence")
    warning =
        0.32 * num(row, "integration_difficulty") +
        0.26 * (1 - num(row, "execution_readiness")) +
        0.16 * (1 - num(row, "governance_readiness")) +
        0.14 * num(row, "resource_intensity") +
        0.12 * (1 - num(row, "evidence_confidence"))

    push!(output, [
        row[col("initiative_id")],
        row[col("initiative_name")],
        round(score, digits = 4),
        round(confidence_adjusted, digits = 4),
        round(warning, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_strategy_conversion_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_strategy_conversion_sensitivity.csv")
