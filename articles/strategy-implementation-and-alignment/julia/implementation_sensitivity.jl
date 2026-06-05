# Advanced Julia implementation sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "implementation_profiles.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["organization_id", "organization_name", "implementation_profile_score", "alignment_drift_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    profile =
        0.12 * num(row, "goal_clarity") +
        0.15 * num(row, "coordination_quality") +
        0.12 * num(row, "structural_support") +
        0.12 * num(row, "cultural_support") +
        0.13 * num(row, "incentive_alignment") +
        0.12 * num(row, "resource_sufficiency") +
        0.11 * num(row, "communication_quality") +
        0.10 * num(row, "accountability_strength") +
        0.10 * num(row, "adaptive_execution") +
        0.08 * num(row, "external_alignment") +
        0.05 * num(row, "ethical_resilience")

    drift =
        0.16 * (1 - num(row, "coordination_quality")) +
        0.14 * (1 - num(row, "cultural_support")) +
        0.14 * (1 - num(row, "incentive_alignment")) +
        0.12 * (1 - num(row, "communication_quality")) +
        0.12 * (1 - num(row, "adaptive_execution")) +
        0.10 * (1 - num(row, "external_alignment")) +
        0.10 * (1 - num(row, "accountability_strength")) +
        0.06 * (1 - num(row, "ethical_resilience")) +
        0.06 * (1 - num(row, "structural_support"))

    push!(output, [
        row[col("organization_id")],
        row[col("organization_name")],
        round(profile, digits = 4),
        round(drift, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_implementation_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_implementation_sensitivity.csv")
