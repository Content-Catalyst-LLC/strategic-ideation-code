# Advanced Julia scenario model for lateral search and frame shift.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "lateral_contexts.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("frame_rigidity" => -0.14, "provocation_strength" => 0.14, "analogical_distance" => 0.12, "random_entry_capacity" => 0.09, "reversal_capacity" => 0.10, "challenge_quality" => 0.10, "convergence_discipline" => 0.14, "systems_integration" => 0.12, "stakeholder_legitimacy" => 0.08, "political_safety" => 0.07, "transformational_potential" => 0.14),
    "systems_pressure" => Dict("frame_rigidity" => -0.12, "provocation_strength" => 0.12, "analogical_distance" => 0.10, "random_entry_capacity" => 0.06, "reversal_capacity" => 0.08, "challenge_quality" => 0.10, "convergence_discipline" => 0.12, "systems_integration" => 0.24, "stakeholder_legitimacy" => 0.08, "political_safety" => 0.06, "transformational_potential" => 0.12),
    "legitimacy_pressure" => Dict("frame_rigidity" => -0.12, "provocation_strength" => 0.10, "analogical_distance" => 0.08, "random_entry_capacity" => 0.06, "reversal_capacity" => 0.08, "challenge_quality" => 0.12, "convergence_discipline" => 0.12, "systems_integration" => 0.10, "stakeholder_legitimacy" => 0.20, "political_safety" => 0.16, "transformational_potential" => 0.10),
    "transformation_pressure" => Dict("frame_rigidity" => -0.12, "provocation_strength" => 0.18, "analogical_distance" => 0.14, "random_entry_capacity" => 0.10, "reversal_capacity" => 0.12, "challenge_quality" => 0.10, "convergence_discipline" => 0.10, "systems_integration" => 0.10, "stakeholder_legitimacy" => 0.06, "political_safety" => 0.06, "transformational_potential" => 0.22)
)

dimensions = ["frame_rigidity", "provocation_strength", "analogical_distance", "random_entry_capacity", "reversal_capacity", "challenge_quality", "convergence_discipline", "systems_integration", "stakeholder_legitimacy", "political_safety", "transformational_potential"]
positive_dimensions = ["provocation_strength", "analogical_distance", "random_entry_capacity", "reversal_capacity", "challenge_quality", "convergence_discipline", "systems_integration", "stakeholder_legitimacy", "political_safety", "transformational_potential"]

output = [["scenario", "context_id", "context_name", "lateral_score", "weakest_positive_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in positive_dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("context_id")], row[col("context_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_lateral_search_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_lateral_search_scenarios.csv")
