# Advanced Julia scenario model for analogical transfer sensitivity.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "analogical_strategies.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("structural_fit" => 0.20, "functional_fit" => 0.16, "surface_distraction" => -0.16, "adaptation_quality" => 0.16, "context_sensitivity" => 0.12, "stakeholder_legitimacy" => 0.08, "dynamic_compatibility" => 0.08, "innovation_potential" => 0.12, "evidence_strength" => 0.08),
    "complex_systems_pressure" => Dict("structural_fit" => 0.18, "functional_fit" => 0.12, "surface_distraction" => -0.14, "adaptation_quality" => 0.16, "context_sensitivity" => 0.12, "stakeholder_legitimacy" => 0.08, "dynamic_compatibility" => 0.22, "innovation_potential" => 0.08, "evidence_strength" => 0.08),
    "legitimacy_pressure" => Dict("structural_fit" => 0.16, "functional_fit" => 0.12, "surface_distraction" => -0.12, "adaptation_quality" => 0.14, "context_sensitivity" => 0.14, "stakeholder_legitimacy" => 0.22, "dynamic_compatibility" => 0.08, "innovation_potential" => 0.08, "evidence_strength" => 0.08),
    "innovation_pressure" => Dict("structural_fit" => 0.20, "functional_fit" => 0.16, "surface_distraction" => -0.14, "adaptation_quality" => 0.14, "context_sensitivity" => 0.10, "stakeholder_legitimacy" => 0.06, "dynamic_compatibility" => 0.08, "innovation_potential" => 0.22, "evidence_strength" => 0.08)
)

dimensions = ["structural_fit", "functional_fit", "surface_distraction", "adaptation_quality", "context_sensitivity", "stakeholder_legitimacy", "dynamic_compatibility", "innovation_potential", "evidence_strength"]

output = [["scenario", "strategy_id", "strategy_name", "analogy_score", "weakest_positive_dimension"]]

positive_dimensions = ["structural_fit", "functional_fit", "adaptation_quality", "context_sensitivity", "stakeholder_legitimacy", "dynamic_compatibility", "innovation_potential", "evidence_strength"]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in positive_dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("strategy_id")], row[col("strategy_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_analogical_transfer_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_analogical_transfer_scenarios.csv")
