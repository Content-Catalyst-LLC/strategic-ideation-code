# Advanced Julia scenario model for strategic mental-model revision.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "mental_model_profiles.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("systems_richness" => 0.17, "probabilistic_depth" => 0.13, "model_flexibility" => 0.16, "model_plurality" => 0.14, "revision_capacity" => 0.16, "institutional_embedding" => -0.08, "ethical_visibility" => 0.12, "stakeholder_visibility" => 0.10, "evidence_responsiveness" => 0.10),
    "complexity_shock" => Dict("systems_richness" => 0.24, "probabilistic_depth" => 0.13, "model_flexibility" => 0.16, "model_plurality" => 0.12, "revision_capacity" => 0.16, "institutional_embedding" => -0.10, "ethical_visibility" => 0.08, "stakeholder_visibility" => 0.07, "evidence_responsiveness" => 0.14),
    "legitimacy_crisis" => Dict("systems_richness" => 0.12, "probabilistic_depth" => 0.08, "model_flexibility" => 0.14, "model_plurality" => 0.12, "revision_capacity" => 0.14, "institutional_embedding" => -0.08, "ethical_visibility" => 0.22, "stakeholder_visibility" => 0.22, "evidence_responsiveness" => 0.10),
    "institutional_lock_in" => Dict("systems_richness" => 0.14, "probabilistic_depth" => 0.10, "model_flexibility" => 0.20, "model_plurality" => 0.16, "revision_capacity" => 0.22, "institutional_embedding" => -0.18, "ethical_visibility" => 0.08, "stakeholder_visibility" => 0.06, "evidence_responsiveness" => 0.12)
)

dimensions = ["systems_richness", "probabilistic_depth", "model_flexibility", "model_plurality", "revision_capacity", "institutional_embedding", "ethical_visibility", "stakeholder_visibility", "evidence_responsiveness"]

output = [["scenario", "model_id", "model_name", "score", "weakest_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in dimensions if d != "institutional_embedding"]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("model_id")], row[col("model_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_model_revision_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_model_revision_scenarios.csv")
