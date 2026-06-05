# Advanced Julia content framework sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "frameworks.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["framework_id", "framework_name", "framework_strength", "framework_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    strength =
        0.10 * num(row, "structure_quality") +
        0.10 * num(row, "conceptual_clarity") +
        0.11 * num(row, "evidence_discipline") +
        0.10 * num(row, "assumption_visibility") +
        0.10 * num(row, "narrative_coherence") +
        0.12 * num(row, "decision_relevance") +
        0.10 * num(row, "modularity") +
        0.10 * num(row, "reuse_readiness") +
        0.08 * num(row, "governance_strength") +
        0.06 * num(row, "ethical_visibility") +
        0.03 * num(row, "ai_governance")

    risk =
        0.10 * (1 - num(row, "structure_quality")) +
        0.11 * (1 - num(row, "conceptual_clarity")) +
        0.12 * (1 - num(row, "evidence_discipline")) +
        0.11 * (1 - num(row, "assumption_visibility")) +
        0.09 * (1 - num(row, "narrative_coherence")) +
        0.12 * (1 - num(row, "decision_relevance")) +
        0.09 * (1 - num(row, "modularity")) +
        0.09 * (1 - num(row, "reuse_readiness")) +
        0.08 * (1 - num(row, "governance_strength")) +
        0.06 * (1 - num(row, "ethical_visibility")) +
        0.03 * (1 - num(row, "ai_governance"))

    push!(output, [
        row[col("framework_id")],
        row[col("framework_name")],
        round(strength, digits = 4),
        round(risk, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_content_framework_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_content_framework_sensitivity.csv")
