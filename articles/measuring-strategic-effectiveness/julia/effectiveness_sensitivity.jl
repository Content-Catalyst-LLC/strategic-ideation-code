# Advanced Julia strategic effectiveness sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "strategies.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["strategy_id", "strategy_name", "strategic_effectiveness_score", "confidence_adjusted_effectiveness"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    effectiveness =
        0.18 * num(row, "performance") +
        0.14 * num(row, "alignment") +
        0.15 * num(row, "resilience") +
        0.15 * num(row, "adaptability") +
        0.13 * num(row, "impact") +
        0.10 * num(row, "learning_value") +
        0.06 * num(row, "evidence_confidence") +
        0.06 * num(row, "ethical_resilience") -
        0.05 * num(row, "measurement_burden") +
        0.08 * num(row, "strategic_fit")

    push!(output, [
        row[col("strategy_id")],
        row[col("strategy_name")],
        round(effectiveness, digits = 4),
        round(effectiveness * num(row, "evidence_confidence"), digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_effectiveness_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_effectiveness_sensitivity.csv")
