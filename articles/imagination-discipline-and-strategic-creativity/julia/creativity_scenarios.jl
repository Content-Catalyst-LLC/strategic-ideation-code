# Advanced Julia scenario model for creative option robustness.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "creative_ideas.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("novelty" => 0.14, "strategic_relevance" => 0.16, "conceptual_coherence" => 0.13, "mechanism_clarity" => 0.14, "testability" => 0.11, "stakeholder_grounding" => 0.13, "systems_fit" => 0.13, "developmental_potential" => 0.12, "revision_capacity" => 0.08, "implementation_risk" => -0.12),
    "stakeholder_priority" => Dict("novelty" => 0.12, "strategic_relevance" => 0.14, "conceptual_coherence" => 0.10, "mechanism_clarity" => 0.12, "testability" => 0.10, "stakeholder_grounding" => 0.26, "systems_fit" => 0.12, "developmental_potential" => 0.10, "revision_capacity" => 0.08, "implementation_risk" => -0.12),
    "systems_priority" => Dict("novelty" => 0.12, "strategic_relevance" => 0.14, "conceptual_coherence" => 0.12, "mechanism_clarity" => 0.12, "testability" => 0.10, "stakeholder_grounding" => 0.10, "systems_fit" => 0.26, "developmental_potential" => 0.10, "revision_capacity" => 0.08, "implementation_risk" => -0.14),
    "prototype_priority" => Dict("novelty" => 0.10, "strategic_relevance" => 0.14, "conceptual_coherence" => 0.12, "mechanism_clarity" => 0.14, "testability" => 0.22, "stakeholder_grounding" => 0.10, "systems_fit" => 0.10, "developmental_potential" => 0.10, "revision_capacity" => 0.10, "implementation_risk" => -0.12)
)

dimensions = ["novelty", "strategic_relevance", "conceptual_coherence", "mechanism_clarity", "testability", "stakeholder_grounding", "systems_fit", "developmental_potential", "revision_capacity", "implementation_risk"]
positive_dimensions = ["novelty", "strategic_relevance", "conceptual_coherence", "mechanism_clarity", "testability", "stakeholder_grounding", "systems_fit", "developmental_potential", "revision_capacity"]

output = [["scenario", "idea_id", "idea_name", "creativity_score", "weakest_positive_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in positive_dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("idea_id")], row[col("idea_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_creativity_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_creativity_scenarios.csv")
