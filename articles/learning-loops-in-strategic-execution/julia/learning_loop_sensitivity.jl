# Advanced Julia learning loop sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "learning_contexts.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["context_id", "context_name", "learning_loop_strength", "learning_failure_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    strength =
        0.12 * num(row, "feedback_quality") +
        0.12 * num(row, "assumption_review") +
        0.11 * num(row, "interpretation_discipline") +
        0.13 * num(row, "decision_authority") +
        0.13 * num(row, "learning_closure") +
        0.10 * num(row, "decision_memory") +
        0.08 * num(row, "psychological_safety") +
        0.08 * num(row, "knowledge_scaling") +
        0.08 * num(row, "ethical_learning") +
        0.07 * num(row, "strategic_coherence") +
        0.08 * num(row, "adaptive_capacity")

    risk =
        0.11 * (1 - num(row, "feedback_quality")) +
        0.12 * (1 - num(row, "assumption_review")) +
        0.10 * (1 - num(row, "interpretation_discipline")) +
        0.14 * (1 - num(row, "decision_authority")) +
        0.14 * (1 - num(row, "learning_closure")) +
        0.11 * (1 - num(row, "decision_memory")) +
        0.08 * (1 - num(row, "psychological_safety")) +
        0.08 * (1 - num(row, "knowledge_scaling")) +
        0.08 * (1 - num(row, "ethical_learning")) +
        0.07 * (1 - num(row, "strategic_coherence")) +
        0.07 * (1 - num(row, "adaptive_capacity"))

    push!(output, [
        row[col("context_id")],
        row[col("context_name")],
        round(strength, digits = 4),
        round(risk, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_learning_loop_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_learning_loop_sensitivity.csv")
