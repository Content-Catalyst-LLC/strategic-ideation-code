# Advanced Julia scenario model for second-order effects and unintended consequences.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "interventions.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("first_order_gain" => 0.14, "adaptation_pressure" => -0.13, "feedback_amplification" => -0.13, "delay_risk" => -0.11, "burden_shift_risk" => -0.12, "gaming_risk" => -0.12, "long_term_fragility" => -0.15, "learning_capacity" => 0.14, "stakeholder_legitimacy" => 0.08, "strategic_reversibility" => 0.08),
    "burden_sensitive" => Dict("first_order_gain" => 0.10, "adaptation_pressure" => -0.12, "feedback_amplification" => -0.12, "delay_risk" => -0.10, "burden_shift_risk" => -0.24, "gaming_risk" => -0.10, "long_term_fragility" => -0.12, "learning_capacity" => 0.12, "stakeholder_legitimacy" => 0.12, "strategic_reversibility" => 0.08),
    "fragility_sensitive" => Dict("first_order_gain" => 0.10, "adaptation_pressure" => -0.12, "feedback_amplification" => -0.13, "delay_risk" => -0.12, "burden_shift_risk" => -0.10, "gaming_risk" => -0.10, "long_term_fragility" => -0.26, "learning_capacity" => 0.12, "stakeholder_legitimacy" => 0.10, "strategic_reversibility" => 0.10),
    "learning_priority" => Dict("first_order_gain" => 0.12, "adaptation_pressure" => -0.10, "feedback_amplification" => -0.10, "delay_risk" => -0.09, "burden_shift_risk" => -0.10, "gaming_risk" => -0.09, "long_term_fragility" => -0.10, "learning_capacity" => 0.26, "stakeholder_legitimacy" => 0.14, "strategic_reversibility" => 0.14)
)

dimensions = ["first_order_gain", "adaptation_pressure", "feedback_amplification", "delay_risk", "burden_shift_risk", "gaming_risk", "long_term_fragility", "learning_capacity", "stakeholder_legitimacy", "strategic_reversibility"]

output = [["scenario", "intervention_id", "intervention_name", "second_order_profile_score", "highest_risk_dimension"]]

risk_dimensions = ["adaptation_pressure", "feedback_amplification", "delay_risk", "burden_shift_risk", "gaming_risk", "long_term_fragility"]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        risks = [(d, num(row, d)) for d in risk_dimensions]
        highest_risk = sort(risks, by = x -> -x[2])[1][1]
        push!(output, [scenario, row[col("intervention_id")], row[col("intervention_name")], round(score, digits = 4), highest_risk])
    end
end

writedlm(joinpath(out_dir, "julia_second_order_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_second_order_scenarios.csv")
