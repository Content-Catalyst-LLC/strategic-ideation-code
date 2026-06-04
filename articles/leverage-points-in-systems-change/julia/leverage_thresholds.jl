# Advanced Julia leverage sensitivity and threshold model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "leverage_points.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("implementation_ease" => 0.06, "structural_depth" => 0.16, "system_sensitivity" => 0.14, "feedback_influence" => 0.13, "information_effect" => 0.11, "rule_power" => 0.13, "goal_alignment" => 0.13, "paradigm_relevance" => 0.08, "transformative_potential" => 0.14, "learning_capacity" => 0.08, "unintended_consequence_risk" => -0.06),
    "feedback_priority" => Dict("implementation_ease" => 0.04, "structural_depth" => 0.14, "system_sensitivity" => 0.14, "feedback_influence" => 0.26, "information_effect" => 0.08, "rule_power" => 0.10, "goal_alignment" => 0.10, "paradigm_relevance" => 0.06, "transformative_potential" => 0.12, "learning_capacity" => 0.08, "unintended_consequence_risk" => -0.06),
    "governance_priority" => Dict("implementation_ease" => 0.04, "structural_depth" => 0.14, "system_sensitivity" => 0.12, "feedback_influence" => 0.12, "information_effect" => 0.10, "rule_power" => 0.14, "goal_alignment" => 0.14, "paradigm_relevance" => 0.10, "transformative_potential" => 0.12, "learning_capacity" => 0.14, "unintended_consequence_risk" => -0.10),
    "transformation_priority" => Dict("implementation_ease" => 0.02, "structural_depth" => 0.18, "system_sensitivity" => 0.14, "feedback_influence" => 0.12, "information_effect" => 0.08, "rule_power" => 0.14, "goal_alignment" => 0.16, "paradigm_relevance" => 0.12, "transformative_potential" => 0.18, "learning_capacity" => 0.08, "unintended_consequence_risk" => -0.08)
)

dimensions = ["implementation_ease", "structural_depth", "system_sensitivity", "feedback_influence", "information_effect", "rule_power", "goal_alignment", "paradigm_relevance", "transformative_potential", "learning_capacity", "unintended_consequence_risk"]

output = [["scenario", "leverage_id", "intervention_name", "leverage_score", "dominant_dimension"]]

positive_dimensions = ["structural_depth", "system_sensitivity", "feedback_influence", "information_effect", "rule_power", "goal_alignment", "paradigm_relevance", "transformative_potential", "learning_capacity"]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in positive_dimensions]
        dominant = sort(values, by = x -> -x[2])[1][1]
        push!(output, [scenario, row[col("leverage_id")], row[col("intervention_name")], round(score, digits = 4), dominant])
    end
end

writedlm(joinpath(out_dir, "julia_leverage_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_leverage_scenarios.csv")
