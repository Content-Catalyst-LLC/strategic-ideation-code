# Advanced Julia taxonomy sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "taxonomy_records.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["record_id", "idea_record", "taxonomy_strength", "taxonomy_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    strength =
        0.12 * num(row, "category_clarity") +
        0.10 * num(row, "level_fit") +
        0.10 * num(row, "maturity_accuracy") +
        0.12 * num(row, "evidence_classification") +
        0.12 * num(row, "function_clarity") +
        0.10 * num(row, "relationship_mapping") +
        0.12 * num(row, "retrieval_value") +
        0.09 * num(row, "governance_strength") +
        0.08 * num(row, "ethical_visibility") +
        0.05 * num(row, "ai_classification_quality")

    risk =
        0.12 * (1 - num(row, "category_clarity")) +
        0.10 * (1 - num(row, "level_fit")) +
        0.10 * (1 - num(row, "maturity_accuracy")) +
        0.12 * (1 - num(row, "evidence_classification")) +
        0.12 * (1 - num(row, "function_clarity")) +
        0.10 * (1 - num(row, "relationship_mapping")) +
        0.12 * (1 - num(row, "retrieval_value")) +
        0.09 * (1 - num(row, "governance_strength")) +
        0.08 * (1 - num(row, "ethical_visibility")) +
        0.05 * (1 - num(row, "ai_classification_quality"))

    push!(output, [
        row[col("record_id")],
        row[col("idea_record")],
        round(strength, digits = 4),
        round(risk, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_taxonomy_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_taxonomy_sensitivity.csv")
