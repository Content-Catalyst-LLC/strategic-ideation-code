# Advanced Julia scenario model for heuristic search and premature convergence.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "heuristic_contexts.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("availability_dependence" => -0.11, "anchoring_intensity" => -0.11, "recognition_comfort" => -0.10, "satisficing_tendency" => -0.11, "affect_pressure" => -0.07, "default_gravity" => -0.08, "social_proof_pressure" => -0.06, "exploratory_diversity" => 0.17, "stakeholder_variation" => 0.13, "source_domain_diversity" => 0.13, "systems_check_quality" => 0.14, "political_safety" => 0.07, "decision_memory_quality" => 0.08),
    "speed_pressure" => Dict("availability_dependence" => -0.06, "anchoring_intensity" => -0.08, "recognition_comfort" => -0.06, "satisficing_tendency" => -0.08, "affect_pressure" => -0.06, "default_gravity" => -0.06, "social_proof_pressure" => -0.04, "exploratory_diversity" => 0.12, "stakeholder_variation" => 0.10, "source_domain_diversity" => 0.10, "systems_check_quality" => 0.10, "political_safety" => 0.06, "decision_memory_quality" => 0.08),
    "systems_pressure" => Dict("availability_dependence" => -0.08, "anchoring_intensity" => -0.09, "recognition_comfort" => -0.08, "satisficing_tendency" => -0.10, "affect_pressure" => -0.05, "default_gravity" => -0.08, "social_proof_pressure" => -0.05, "exploratory_diversity" => 0.14, "stakeholder_variation" => 0.12, "source_domain_diversity" => 0.12, "systems_check_quality" => 0.24, "political_safety" => 0.06, "decision_memory_quality" => 0.08),
    "stakeholder_pressure" => Dict("availability_dependence" => -0.08, "anchoring_intensity" => -0.09, "recognition_comfort" => -0.08, "satisficing_tendency" => -0.09, "affect_pressure" => -0.05, "default_gravity" => -0.06, "social_proof_pressure" => -0.05, "exploratory_diversity" => 0.14, "stakeholder_variation" => 0.24, "source_domain_diversity" => 0.12, "systems_check_quality" => 0.12, "political_safety" => 0.10, "decision_memory_quality" => 0.08)
)

dimensions = ["availability_dependence", "anchoring_intensity", "recognition_comfort", "satisficing_tendency", "affect_pressure", "default_gravity", "social_proof_pressure", "exploratory_diversity", "stakeholder_variation", "source_domain_diversity", "systems_check_quality", "political_safety", "decision_memory_quality"]
positive_dimensions = ["exploratory_diversity", "stakeholder_variation", "source_domain_diversity", "systems_check_quality", "political_safety", "decision_memory_quality"]

output = [["scenario", "context_id", "context_name", "heuristic_score", "closure_pressure", "weakest_positive_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        closure = num(row, "anchoring_intensity") * num(row, "satisficing_tendency")
        values = [(d, num(row, d)) for d in positive_dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("context_id")], row[col("context_name")], round(score, digits = 4), round(closure, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_heuristic_search_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_heuristic_search_scenarios.csv")
