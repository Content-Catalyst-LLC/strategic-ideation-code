# Advanced Julia scenario model for conceptual ambiguity and governance.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "concept_inventory.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("definition_clarity" => 0.17, "boundary_clarity" => 0.14, "distinction_quality" => 0.14, "operational_implication" => 0.13, "measurement_validity" => 0.15, "revision_capacity" => 0.10, "stakeholder_visibility" => 0.07, "ethical_visibility" => 0.06, "governance_maturity" => 0.04),
    "measurement_sensitive" => Dict("definition_clarity" => 0.15, "boundary_clarity" => 0.12, "distinction_quality" => 0.12, "operational_implication" => 0.12, "measurement_validity" => 0.26, "revision_capacity" => 0.09, "stakeholder_visibility" => 0.06, "ethical_visibility" => 0.06, "governance_maturity" => 0.02),
    "governance_sensitive" => Dict("definition_clarity" => 0.14, "boundary_clarity" => 0.13, "distinction_quality" => 0.13, "operational_implication" => 0.12, "measurement_validity" => 0.13, "revision_capacity" => 0.16, "stakeholder_visibility" => 0.08, "ethical_visibility" => 0.07, "governance_maturity" => 0.04),
    "stakeholder_sensitive" => Dict("definition_clarity" => 0.13, "boundary_clarity" => 0.12, "distinction_quality" => 0.12, "operational_implication" => 0.11, "measurement_validity" => 0.12, "revision_capacity" => 0.10, "stakeholder_visibility" => 0.18, "ethical_visibility" => 0.17, "governance_maturity" => 0.05)
)

dimensions = ["definition_clarity", "boundary_clarity", "distinction_quality", "operational_implication", "measurement_validity", "revision_capacity", "stakeholder_visibility", "ethical_visibility", "governance_maturity"]

output = [["scenario", "concept_id", "concept_name", "clarity_score", "weakest_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("concept_id")], row[col("concept_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_concept_governance_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_concept_governance_scenarios.csv")
