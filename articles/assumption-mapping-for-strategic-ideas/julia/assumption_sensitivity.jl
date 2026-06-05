# Advanced Julia assumption sensitivity and option confidence model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "assumptions.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("criticality" => 1.0, "uncertainty" => 1.0, "evidence_penalty" => 1.0),
    "evidence_strict" => Dict("criticality" => 1.0, "uncertainty" => 1.0, "evidence_penalty" => 1.35),
    "uncertainty_strict" => Dict("criticality" => 1.0, "uncertainty" => 1.30, "evidence_penalty" => 1.0),
    "commitment_guardrail" => Dict("criticality" => 1.20, "uncertainty" => 1.10, "evidence_penalty" => 1.20)
)

output = [["scenario", "assumption_id", "idea_id", "risk_score", "priority_class"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        evidence_composite =
            0.40 * num(row, "evidence_strength") +
            0.30 * num(row, "evidence_relevance") +
            0.30 * num(row, "evidence_transferability")

        risk =
            weights["criticality"] * num(row, "criticality") *
            weights["uncertainty"] * num(row, "uncertainty") *
            weights["evidence_penalty"] * (1 - evidence_composite)

        priority_class = risk >= 0.35 ? "test_first" : (risk >= 0.25 ? "review" : "monitor")

        push!(output, [
            scenario,
            row[col("assumption_id")],
            row[col("idea_id")],
            round(risk, digits = 4),
            priority_class
        ])
    end
end

writedlm(joinpath(out_dir, "julia_assumption_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_assumption_sensitivity.csv")
