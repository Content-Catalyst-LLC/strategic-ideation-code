# Advanced Julia coherence sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "coherence_contexts.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["context_id", "context_name", "strategic_coherence_score", "alignment_drift_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    coherence =
        0.13 * num(row, "purpose_clarity") +
        0.12 * num(row, "priority_discipline") +
        0.11 * num(row, "tradeoff_integrity") +
        0.12 * num(row, "resource_alignment") +
        0.12 * num(row, "incentive_fit") +
        0.10 * num(row, "interpretive_consistency") +
        0.11 * num(row, "governance_strength") +
        0.09 * num(row, "feedback_quality") +
        0.06 * num(row, "decision_memory") +
        0.07 * num(row, "ethical_coherence") +
        0.07 * num(row, "adaptive_capacity")

    drift =
        0.13 * (1 - num(row, "purpose_clarity")) +
        0.12 * (1 - num(row, "priority_discipline")) +
        0.11 * (1 - num(row, "tradeoff_integrity")) +
        0.12 * (1 - num(row, "resource_alignment")) +
        0.13 * (1 - num(row, "incentive_fit")) +
        0.10 * (1 - num(row, "interpretive_consistency")) +
        0.11 * (1 - num(row, "governance_strength")) +
        0.08 * (1 - num(row, "feedback_quality")) +
        0.06 * (1 - num(row, "decision_memory")) +
        0.07 * (1 - num(row, "ethical_coherence")) +
        0.07 * (1 - num(row, "adaptive_capacity"))

    push!(output, [
        row[col("context_id")],
        row[col("context_name")],
        round(coherence, digits = 4),
        round(drift, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_coherence_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_coherence_sensitivity.csv")
