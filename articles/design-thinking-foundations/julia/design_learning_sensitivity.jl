# Advanced Julia iterative design learning model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "design_contexts.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["context_id", "context_name", "baseline_capability", "learning_rate", "projected_learning_after_30_cycles", "superficiality_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    capability =
        0.12 * num(row, "empathy_depth") +
        0.13 * num(row, "reframing_capacity") +
        0.10 * num(row, "divergence_quality") +
        0.10 * num(row, "convergence_quality") +
        0.12 * num(row, "prototyping_strength") +
        0.12 * num(row, "testing_quality") +
        0.11 * num(row, "systems_awareness") +
        0.10 * num(row, "ethical_review") +
        0.10 * num(row, "decision_linkage") +
        0.06 * num(row, "adaptability") +
        0.04 * num(row, "institutional_memory")

    learning_rate =
        0.14 * num(row, "empathy_depth") +
        0.16 * num(row, "reframing_capacity") +
        0.18 * num(row, "prototyping_strength") +
        0.14 * num(row, "systems_awareness") +
        0.18 * num(row, "decision_linkage") +
        0.10 * num(row, "institutional_memory")

    friction = 0.04 * (1 - num(row, "decision_linkage"))
    projected = 0.35

    for t in 2:30
        projected = min(1.8, max(0.0, projected + learning_rate / 6 - friction))
    end

    superficiality =
        0.18 * (1 - num(row, "empathy_depth")) +
        0.14 * (1 - num(row, "reframing_capacity")) +
        0.12 * (1 - num(row, "testing_quality")) +
        0.12 * (1 - num(row, "systems_awareness")) +
        0.12 * (1 - num(row, "ethical_review")) +
        0.16 * (1 - num(row, "decision_linkage")) +
        0.10 * (1 - num(row, "institutional_memory")) +
        0.06 * (1 - num(row, "adaptability"))

    push!(output, [
        row[col("context_id")],
        row[col("context_name")],
        round(capability, digits = 4),
        round(learning_rate, digits = 4),
        round(projected, digits = 4),
        round(superficiality, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_design_learning_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_design_learning_sensitivity.csv")
