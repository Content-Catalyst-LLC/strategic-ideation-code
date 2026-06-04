# Advanced Julia scenario model for divergence-convergence balance.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "ideation_contexts.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("exploratory_breadth" => 0.16, "evaluative_discipline" => 0.16, "iteration_quality" => 0.18, "constraint_clarity" => 0.14, "stakeholder_inclusion" => 0.12, "evidence_contact" => 0.12, "action_readiness" => 0.08, "decision_memory_quality" => 0.04),
    "innovation_pressure" => Dict("exploratory_breadth" => 0.24, "evaluative_discipline" => 0.12, "iteration_quality" => 0.18, "constraint_clarity" => 0.10, "stakeholder_inclusion" => 0.12, "evidence_contact" => 0.12, "action_readiness" => 0.07, "decision_memory_quality" => 0.05),
    "implementation_pressure" => Dict("exploratory_breadth" => 0.10, "evaluative_discipline" => 0.22, "iteration_quality" => 0.16, "constraint_clarity" => 0.16, "stakeholder_inclusion" => 0.10, "evidence_contact" => 0.12, "action_readiness" => 0.10, "decision_memory_quality" => 0.04),
    "legitimacy_pressure" => Dict("exploratory_breadth" => 0.14, "evaluative_discipline" => 0.12, "iteration_quality" => 0.16, "constraint_clarity" => 0.12, "stakeholder_inclusion" => 0.24, "evidence_contact" => 0.12, "action_readiness" => 0.06, "decision_memory_quality" => 0.04)
)

dimensions = ["exploratory_breadth", "evaluative_discipline", "iteration_quality", "constraint_clarity", "stakeholder_inclusion", "evidence_contact", "action_readiness", "decision_memory_quality"]

output = [["scenario", "context_id", "context_name", "profile_score", "weakest_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("context_id")], row[col("context_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_search_balance_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_search_balance_scenarios.csv")
