# Advanced Julia sequencing sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "pathways.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["pathway_id", "pathway_name", "sequencing_readiness_score", "premature_commitment_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    readiness =
        0.15 * num(row, "capability_readiness") +
        0.14 * num(row, "evidence_strength") +
        0.14 * num(row, "governance_readiness") +
        0.13 * num(row, "legitimacy") -
        0.10 * num(row, "dependency_load") +
        0.09 * num(row, "reversibility") -
        0.09 * num(row, "capacity_demand") +
        0.07 * num(row, "timing_urgency") +
        0.11 * num(row, "ethical_resilience") +
        0.09 * num(row, "feedback_strength") +
        0.10 * num(row, "strategic_fit")

    risk =
        0.22 * num(row, "dependency_load") +
        0.20 * num(row, "capacity_demand") +
        0.16 * (1 - num(row, "evidence_strength")) +
        0.14 * (1 - num(row, "governance_readiness")) +
        0.12 * (1 - num(row, "reversibility")) +
        0.10 * (1 - num(row, "ethical_resilience")) +
        0.06 * (1 - num(row, "feedback_strength"))

    push!(output, [
        row[col("pathway_id")],
        row[col("pathway_name")],
        round(readiness, digits = 4),
        round(risk, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_sequencing_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_sequencing_sensitivity.csv")
