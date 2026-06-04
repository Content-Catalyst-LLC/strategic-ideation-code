# Advanced Julia scenario model for hypothesis robustness under different strategic pressures.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "hypotheses.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("explanatory_strength" => 0.16, "testability" => 0.14, "evidence_quality" => 0.14, "strategic_relevance" => 0.16, "stakeholder_visibility" => 0.12, "systems_fit" => 0.12, "actionability" => 0.10, "reversibility" => 0.06, "implementation_risk" => -0.10),
    "stakeholder_legitimacy" => Dict("explanatory_strength" => 0.14, "testability" => 0.12, "evidence_quality" => 0.12, "strategic_relevance" => 0.14, "stakeholder_visibility" => 0.24, "systems_fit" => 0.12, "actionability" => 0.08, "reversibility" => 0.06, "implementation_risk" => -0.10),
    "systems_uncertainty" => Dict("explanatory_strength" => 0.14, "testability" => 0.12, "evidence_quality" => 0.12, "strategic_relevance" => 0.14, "stakeholder_visibility" => 0.10, "systems_fit" => 0.24, "actionability" => 0.08, "reversibility" => 0.08, "implementation_risk" => -0.12),
    "prototype_speed" => Dict("explanatory_strength" => 0.12, "testability" => 0.18, "evidence_quality" => 0.12, "strategic_relevance" => 0.14, "stakeholder_visibility" => 0.10, "systems_fit" => 0.10, "actionability" => 0.18, "reversibility" => 0.10, "implementation_risk" => -0.10)
)

dimensions = ["explanatory_strength", "testability", "evidence_quality", "strategic_relevance", "stakeholder_visibility", "systems_fit", "actionability", "reversibility", "implementation_risk"]
positive_dimensions = ["explanatory_strength", "testability", "evidence_quality", "strategic_relevance", "stakeholder_visibility", "systems_fit", "actionability", "reversibility"]

output = [["scenario", "hypothesis_id", "hypothesis_name", "hypothesis_score", "weakest_positive_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in positive_dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("hypothesis_id")], row[col("hypothesis_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_hypothesis_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_hypothesis_scenarios.csv")
