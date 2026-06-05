# Advanced Julia participation quality sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "participation_systems.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["system_id", "system_name", "participation_quality", "tokenism_extraction_risk", "projected_idea_quality_after_40_cycles"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    quality =
        0.13 * num(row, "representation") +
        0.15 * num(row, "influence") +
        0.11 * num(row, "accessibility") +
        0.11 * num(row, "reciprocity") +
        0.13 * num(row, "power_awareness") +
        0.12 * num(row, "knowledge_integration") +
        0.11 * num(row, "decision_linkage") +
        0.10 * num(row, "accountability") +
        0.04 * num(row, "learning_memory")

    tokenism =
        0.16 * (1 - num(row, "influence")) +
        0.14 * (1 - num(row, "decision_linkage")) +
        0.14 * (1 - num(row, "accountability")) +
        0.13 * (1 - num(row, "reciprocity")) +
        0.13 * (1 - num(row, "power_awareness")) +
        0.11 * (1 - num(row, "representation")) +
        0.10 * (1 - num(row, "accessibility")) +
        0.09 * (1 - num(row, "learning_memory"))

    idea_quality = 0.30
    for t in 2:40
        gain =
            0.12 * num(row, "representation") +
            0.15 * num(row, "influence") +
            0.10 * num(row, "accessibility") +
            0.10 * num(row, "reciprocity") +
            0.13 * num(row, "power_awareness") +
            0.12 * num(row, "knowledge_integration") +
            0.10 * num(row, "decision_linkage") +
            0.10 * num(row, "accountability") +
            0.05 * num(row, "learning_memory")

        token_penalty = 0.08 * (1 - num(row, "influence")) + 0.06 * (1 - num(row, "decision_linkage"))
        extraction_penalty = 0.05 * (1 - num(row, "reciprocity"))
        power_penalty = 0.05 * (1 - num(row, "power_awareness"))

        idea_quality = min(1.8, max(0.0, idea_quality + gain / 5 - token_penalty / 5 - extraction_penalty / 5 - power_penalty / 5))
    end

    push!(output, [
        row[col("system_id")],
        row[col("system_name")],
        round(quality, digits = 4),
        round(tokenism, digits = 4),
        round(idea_quality, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_participation_quality_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_participation_quality_sensitivity.csv")
