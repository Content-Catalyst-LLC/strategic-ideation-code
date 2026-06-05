# Advanced Julia feedback stability sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "feedback_systems.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["system_id", "system_name", "feedback_profile", "noisy_churn_risk", "projected_learning_after_40_cycles", "stability_penalty"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    profile =
        0.13 * num(row, "signal_quality") +
        0.13 * num(row, "interpretation_capacity") +
        0.10 * num(row, "adjustment_speed") +
        0.13 * num(row, "user_insight_depth") +
        0.10 * num(row, "stability") +
        0.11 * num(row, "ethical_integrity") +
        0.10 * num(row, "systems_awareness") +
        0.10 * num(row, "decision_linkage") +
        0.10 * num(row, "learning_memory")

    churn =
        0.16 * num(row, "adjustment_speed") +
        0.15 * (1 - num(row, "signal_quality")) +
        0.15 * (1 - num(row, "interpretation_capacity")) +
        0.13 * (1 - num(row, "stability")) +
        0.12 * (1 - num(row, "systems_awareness")) +
        0.12 * (1 - num(row, "ethical_integrity")) +
        0.10 * (1 - num(row, "decision_linkage")) +
        0.07 * (1 - num(row, "learning_memory"))

    learning = 0.30
    stability_penalty = 0.04 * (1 - num(row, "stability"))

    for t in 2:40
        gain =
            0.12 * num(row, "signal_quality") +
            0.12 * num(row, "interpretation_capacity") +
            0.08 * num(row, "adjustment_speed") +
            0.12 * num(row, "user_insight_depth") +
            0.09 * num(row, "systems_awareness") +
            0.08 * num(row, "ethical_integrity") +
            0.10 * num(row, "decision_linkage") +
            0.08 * num(row, "learning_memory")

        churn_penalty = 0.06 * num(row, "adjustment_speed") * (1 - num(row, "interpretation_capacity"))
        decision_drift = 0.05 * (1 - num(row, "decision_linkage"))
        learning = min(1.8, max(0.0, learning + gain / 5 - churn_penalty / 5 - decision_drift / 5 - stability_penalty / 5))
    end

    push!(output, [
        row[col("system_id")],
        row[col("system_name")],
        round(profile, digits = 4),
        round(churn, digits = 4),
        round(learning, digits = 4),
        round(stability_penalty, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_feedback_stability_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_feedback_stability_sensitivity.csv")
