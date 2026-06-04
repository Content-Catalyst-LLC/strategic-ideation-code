# Advanced Julia scenario model for complex systems and strategic uncertainty.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "complexity_environments.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("interdependence" => 0.13, "nonlinearity" => 0.13, "feedback_intensity" => 0.14, "adaptation_pressure" => 0.12, "path_dependence" => 0.11, "boundary_ambiguity" => 0.10, "emergence_potential" => 0.10, "deep_uncertainty" => 0.09, "scenario_need" => 0.09, "learning_capacity_need" => 0.09),
    "foresight_priority" => Dict("interdependence" => 0.10, "nonlinearity" => 0.12, "feedback_intensity" => 0.12, "adaptation_pressure" => 0.10, "path_dependence" => 0.10, "boundary_ambiguity" => 0.10, "emergence_potential" => 0.10, "deep_uncertainty" => 0.12, "scenario_need" => 0.16, "learning_capacity_need" => 0.08),
    "adaptive_priority" => Dict("interdependence" => 0.11, "nonlinearity" => 0.11, "feedback_intensity" => 0.13, "adaptation_pressure" => 0.18, "path_dependence" => 0.10, "boundary_ambiguity" => 0.08, "emergence_potential" => 0.09, "deep_uncertainty" => 0.10, "scenario_need" => 0.08, "learning_capacity_need" => 0.14),
    "pathway_priority" => Dict("interdependence" => 0.10, "nonlinearity" => 0.10, "feedback_intensity" => 0.12, "adaptation_pressure" => 0.12, "path_dependence" => 0.18, "boundary_ambiguity" => 0.10, "emergence_potential" => 0.08, "deep_uncertainty" => 0.10, "scenario_need" => 0.10, "learning_capacity_need" => 0.10)
)

dimensions = ["interdependence", "nonlinearity", "feedback_intensity", "adaptation_pressure", "path_dependence", "boundary_ambiguity", "emergence_potential", "deep_uncertainty", "scenario_need", "learning_capacity_need"]

output = [["scenario", "environment_id", "environment_name", "complexity_score", "highest_complexity_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in dimensions]
        strongest = sort(values, by = x -> -x[2])[1][1]
        push!(output, [scenario, row[col("environment_id")], row[col("environment_name")], round(score, digits = 4), strongest])
    end
end

writedlm(joinpath(out_dir, "julia_complexity_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_complexity_scenarios.csv")
