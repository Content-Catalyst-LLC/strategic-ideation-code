# Advanced Julia prototype evidence learning sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "prototype_systems.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["system_id", "system_name", "prototype_learning_quality", "validation_theater_risk", "projected_learning_after_40_cycles", "remaining_uncertainty"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    quality =
        0.13 * num(row, "assumption_clarity") +
        0.13 * num(row, "learning_target_fit") +
        0.15 * num(row, "evidence_quality") +
        0.13 * num(row, "behavioral_grounding") +
        0.11 * num(row, "context_realism") +
        0.11 * num(row, "systems_awareness") +
        0.11 * num(row, "decision_linkage") +
        0.07 * num(row, "ethical_review") +
        0.06 * num(row, "learning_memory")

    theater =
        0.17 * (1 - num(row, "assumption_clarity")) +
        0.16 * (1 - num(row, "evidence_quality")) +
        0.14 * (1 - num(row, "behavioral_grounding")) +
        0.13 * (1 - num(row, "decision_linkage")) +
        0.12 * (1 - num(row, "learning_memory")) +
        0.11 * (1 - num(row, "systems_awareness")) +
        0.09 * (1 - num(row, "ethical_review")) +
        0.08 * (1 - num(row, "context_realism"))

    learning = 0.30

    for t in 2:40
        gain =
            0.12 * num(row, "assumption_clarity") +
            0.12 * num(row, "learning_target_fit") +
            0.16 * num(row, "evidence_quality") +
            0.12 * num(row, "behavioral_grounding") +
            0.10 * num(row, "context_realism") +
            0.10 * num(row, "systems_awareness") +
            0.12 * num(row, "decision_linkage") +
            0.07 * num(row, "ethical_review") +
            0.07 * num(row, "learning_memory")

        theater_penalty = 0.07 * (1 - num(row, "assumption_clarity")) + 0.07 * (1 - num(row, "evidence_quality"))
        overgeneralization_penalty = 0.05 * (1 - num(row, "context_realism")) + 0.05 * (1 - num(row, "systems_awareness"))
        ethics_penalty = 0.04 * (1 - num(row, "ethical_review"))

        learning = min(1.8, max(0.0, learning + gain / 5 - theater_penalty / 5 - overgeneralization_penalty / 5 - ethics_penalty / 5))
    end

    remaining_uncertainty = max(0.0, 1.0 - min(1.0, learning))

    push!(output, [
        row[col("system_id")],
        row[col("system_name")],
        round(quality, digits = 4),
        round(theater, digits = 4),
        round(learning, digits = 4),
        round(remaining_uncertainty, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_prototype_learning_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_prototype_learning_sensitivity.csv")
