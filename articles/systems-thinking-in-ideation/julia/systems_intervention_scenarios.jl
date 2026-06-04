# Advanced Julia scenario model for systems-ideation intervention robustness.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "systems_profiles.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("feedback_awareness" => 0.14, "leverage_sensitivity" => 0.14, "root_cause_depth" => 0.13, "stakeholder_visibility" => 0.12, "boundary_quality" => 0.12, "stock_flow_awareness" => 0.10, "delay_awareness" => 0.10, "adaptive_learning" => 0.13, "unintended_consequence_risk" => -0.10, "local_optimization_risk" => -0.08),
    "stakeholder_priority" => Dict("feedback_awareness" => 0.12, "leverage_sensitivity" => 0.12, "root_cause_depth" => 0.12, "stakeholder_visibility" => 0.24, "boundary_quality" => 0.16, "stock_flow_awareness" => 0.08, "delay_awareness" => 0.08, "adaptive_learning" => 0.12, "unintended_consequence_risk" => -0.12, "local_optimization_risk" => -0.08),
    "high_leverage_priority" => Dict("feedback_awareness" => 0.12, "leverage_sensitivity" => 0.24, "root_cause_depth" => 0.18, "stakeholder_visibility" => 0.10, "boundary_quality" => 0.10, "stock_flow_awareness" => 0.08, "delay_awareness" => 0.08, "adaptive_learning" => 0.10, "unintended_consequence_risk" => -0.12, "local_optimization_risk" => -0.08),
    "adaptive_learning_priority" => Dict("feedback_awareness" => 0.16, "leverage_sensitivity" => 0.12, "root_cause_depth" => 0.12, "stakeholder_visibility" => 0.10, "boundary_quality" => 0.10, "stock_flow_awareness" => 0.08, "delay_awareness" => 0.10, "adaptive_learning" => 0.24, "unintended_consequence_risk" => -0.10, "local_optimization_risk" => -0.08)
)

dimensions = ["feedback_awareness", "leverage_sensitivity", "root_cause_depth", "stakeholder_visibility", "boundary_quality", "stock_flow_awareness", "delay_awareness", "adaptive_learning", "unintended_consequence_risk", "local_optimization_risk"]
positive_dimensions = ["feedback_awareness", "leverage_sensitivity", "root_cause_depth", "stakeholder_visibility", "boundary_quality", "stock_flow_awareness", "delay_awareness", "adaptive_learning"]

output = [["scenario", "system_id", "system_name", "systems_ideation_score", "weakest_positive_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in positive_dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("system_id")], row[col("system_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_systems_intervention_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_systems_intervention_scenarios.csv")
