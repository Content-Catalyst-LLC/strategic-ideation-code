# Advanced Julia scenario model for creative constraint calibration.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "constraint_contexts.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("resource_pressure" => -0.10, "technical_rigidity" => -0.10, "institutional_rigidity" => -0.10, "ecological_boundary_pressure" => 0.12, "ethical_constraint_visibility" => 0.16, "search_focus" => 0.16, "adaptive_opportunity" => 0.16, "stakeholder_legitimacy" => 0.14, "learning_capacity" => 0.14, "implementation_readiness" => 0.12),
    "frugal_pressure" => Dict("resource_pressure" => 0.02, "technical_rigidity" => -0.08, "institutional_rigidity" => -0.08, "ecological_boundary_pressure" => 0.10, "ethical_constraint_visibility" => 0.12, "search_focus" => 0.18, "adaptive_opportunity" => 0.18, "stakeholder_legitimacy" => 0.12, "learning_capacity" => 0.14, "implementation_readiness" => 0.12),
    "public_legitimacy_pressure" => Dict("resource_pressure" => -0.08, "technical_rigidity" => -0.08, "institutional_rigidity" => -0.06, "ecological_boundary_pressure" => 0.12, "ethical_constraint_visibility" => 0.20, "search_focus" => 0.12, "adaptive_opportunity" => 0.12, "stakeholder_legitimacy" => 0.22, "learning_capacity" => 0.14, "implementation_readiness" => 0.10),
    "ecological_boundary_pressure" => Dict("resource_pressure" => -0.06, "technical_rigidity" => -0.06, "institutional_rigidity" => -0.06, "ecological_boundary_pressure" => 0.24, "ethical_constraint_visibility" => 0.18, "search_focus" => 0.14, "adaptive_opportunity" => 0.12, "stakeholder_legitimacy" => 0.16, "learning_capacity" => 0.16, "implementation_readiness" => 0.08)
)

dimensions = ["resource_pressure", "technical_rigidity", "institutional_rigidity", "ecological_boundary_pressure", "ethical_constraint_visibility", "search_focus", "adaptive_opportunity", "stakeholder_legitimacy", "learning_capacity", "implementation_readiness"]

output = [["scenario", "context_id", "context_name", "constraint_profile_score", "weakest_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("context_id")], row[col("context_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_constraint_calibration_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_constraint_calibration_scenarios.csv")
