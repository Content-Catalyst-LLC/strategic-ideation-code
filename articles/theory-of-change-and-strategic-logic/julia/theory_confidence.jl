# Advanced Julia causal-link sensitivity and theory confidence model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "theory_links.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["link_id", "idea_id", "link_risk", "link_quality", "test_priority"]]

idea_quality = Dict{String, Vector{Float64}}()

for i in 1:size(rows, 1)
    row = rows[i, :]
    risk =
        0.16 * (1 - num(row, "mechanism_clarity")) +
        0.18 * (1 - num(row, "evidence_strength")) +
        0.13 * num(row, "actor_dependency") +
        0.11 * num(row, "capacity_dependency") +
        0.14 * num(row, "system_dependency") +
        0.12 * num(row, "ethical_dependency") +
        0.16 * num(row, "failure_consequence")

    quality = max(0.0, 1.0 - risk)
    test_priority = risk * num(row, "testability")
    idea_id = row[col("idea_id")]

    if !haskey(idea_quality, idea_id)
        idea_quality[idea_id] = Float64[]
    end
    push!(idea_quality[idea_id], quality)

    push!(output, [
        row[col("link_id")],
        idea_id,
        round(risk, digits = 4),
        round(quality, digits = 4),
        round(test_priority, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_theory_link_risk.csv"), output, ',')

confidence_output = [["idea_id", "mean_link_quality", "pathway_confidence_product"]]

for (idea_id, qualities) in idea_quality
    product_confidence = prod(qualities)
    push!(confidence_output, [
        idea_id,
        round(mean(qualities), digits = 4),
        round(product_confidence, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_theory_confidence.csv"), confidence_output, ',')
println("Wrote outputs/tables/julia_theory_link_risk.csv")
println("Wrote outputs/tables/julia_theory_confidence.csv")
