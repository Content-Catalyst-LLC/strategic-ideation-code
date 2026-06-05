# Advanced Julia empathy-learning sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "empathy_contexts.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["context_id", "context_name", "empathy_profile", "interpretive_distance", "projected_idea_quality_after_30_cycles", "superficiality_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    profile =
        0.16 * num(row, "observational_depth") -
        0.14 * num(row, "projection_risk") +
        0.16 * num(row, "unmet_need_visibility") +
        0.12 * num(row, "stakeholder_breadth") +
        0.16 * num(row, "reframing_potential") +
        0.10 * num(row, "ethical_review") +
        0.10 * num(row, "systems_awareness") +
        0.14 * num(row, "decision_linkage") +
        0.10 * num(row, "institutional_memory")

    interpretive_distance = num(row, "projection_risk") * (1 - num(row, "observational_depth"))

    projected = 0.35
    for t in 2:30
        gain =
            0.16 * num(row, "observational_depth") +
            0.18 * num(row, "reframing_potential") +
            0.12 * num(row, "systems_awareness") +
            0.10 * num(row, "ethical_review") +
            0.16 * num(row, "decision_linkage") -
            0.14 * num(row, "projection_risk")

        drift = 0.03 * (1 - num(row, "decision_linkage"))
        projected = min(1.8, max(0.0, projected + gain / 5 - drift))
    end

    superficiality =
        0.20 * num(row, "projection_risk") +
        0.16 * (1 - num(row, "decision_linkage")) +
        0.14 * (1 - num(row, "observational_depth")) +
        0.12 * (1 - num(row, "unmet_need_visibility")) +
        0.12 * (1 - num(row, "ethical_review")) +
        0.10 * (1 - num(row, "systems_awareness")) +
        0.08 * (1 - num(row, "stakeholder_breadth")) +
        0.08 * (1 - num(row, "institutional_memory"))

    push!(output, [
        row[col("context_id")],
        row[col("context_name")],
        round(profile, digits = 4),
        round(interpretive_distance, digits = 4),
        round(projected, digits = 4),
        round(superficiality, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_empathy_learning_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_empathy_learning_sensitivity.csv")
