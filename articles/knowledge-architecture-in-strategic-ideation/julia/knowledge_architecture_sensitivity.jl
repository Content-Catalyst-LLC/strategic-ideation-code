# Advanced Julia knowledge architecture sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "idea_records.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["idea_id", "idea_title", "architecture_strength", "architecture_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    strength =
        0.11 * num(row, "taxonomy_quality") +
        0.12 * num(row, "metadata_completeness") +
        0.11 * num(row, "semantic_clarity") +
        0.12 * num(row, "evidence_linkage") +
        0.11 * num(row, "assumption_clarity") +
        0.11 * num(row, "relationship_mapping") +
        0.12 * num(row, "retrieval_readiness") +
        0.09 * num(row, "decision_memory") +
        0.07 * num(row, "stewardship_quality") +
        0.04 * num(row, "ethical_representation")

    risk =
        0.11 * (1 - num(row, "taxonomy_quality")) +
        0.12 * (1 - num(row, "metadata_completeness")) +
        0.12 * (1 - num(row, "semantic_clarity")) +
        0.13 * (1 - num(row, "evidence_linkage")) +
        0.12 * (1 - num(row, "assumption_clarity")) +
        0.10 * (1 - num(row, "relationship_mapping")) +
        0.12 * (1 - num(row, "retrieval_readiness")) +
        0.09 * (1 - num(row, "decision_memory")) +
        0.06 * (1 - num(row, "stewardship_quality")) +
        0.03 * (1 - num(row, "ethical_representation"))

    push!(output, [
        row[col("idea_id")],
        row[col("idea_title")],
        round(strength, digits = 4),
        round(risk, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_knowledge_architecture_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_knowledge_architecture_sensitivity.csv")
