# Advanced Julia learning-efficiency sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "experimentation_systems.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["system_id", "system_name", "experimentation_profile", "superficial_testing_risk", "learning_efficiency", "projected_learning_after_40_cycles"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    profile =
        0.10 * num(row, "speed") +
        0.09 * num(row, "cost_efficiency") +
        0.15 * num(row, "insight_depth") +
        0.12 * num(row, "user_validation") +
        0.12 * num(row, "assumption_criticality") +
        0.14 * num(row, "evidence_quality") +
        0.10 * num(row, "systems_awareness") +
        0.08 * num(row, "ethical_review") +
        0.10 * num(row, "decision_linkage") +
        0.10 * num(row, "learning_memory")

    superficial =
        0.14 * num(row, "speed") +
        0.16 * (1 - num(row, "insight_depth")) +
        0.15 * (1 - num(row, "evidence_quality")) +
        0.13 * (1 - num(row, "systems_awareness")) +
        0.13 * (1 - num(row, "ethical_review")) +
        0.13 * (1 - num(row, "decision_linkage")) +
        0.09 * (1 - num(row, "assumption_criticality")) +
        0.07 * (1 - num(row, "learning_memory"))

    learning_efficiency =
        (num(row, "insight_depth") + num(row, "evidence_quality") + num(row, "decision_linkage")) /
        (1 + (1 - num(row, "cost_efficiency")) + (1 - num(row, "speed")))

    learning = 0.30
    for t in 2:40
        gain =
            0.10 * num(row, "speed") +
            0.16 * num(row, "insight_depth") +
            0.12 * num(row, "user_validation") +
            0.14 * num(row, "evidence_quality") +
            0.10 * num(row, "systems_awareness") +
            0.08 * num(row, "ethical_review") +
            0.12 * num(row, "decision_linkage") +
            0.08 * num(row, "learning_memory")

        penalty = 0.06 * num(row, "speed") * (1 - num(row, "insight_depth")) + 0.05 * (1 - num(row, "decision_linkage"))
        learning = min(1.8, max(0.0, learning + gain / 5 - penalty / 5))
    end

    push!(output, [
        row[col("system_id")],
        row[col("system_name")],
        round(profile, digits = 4),
        round(superficial, digits = 4),
        round(learning_efficiency, digits = 4),
        round(learning, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_learning_efficiency_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_learning_efficiency_sensitivity.csv")
