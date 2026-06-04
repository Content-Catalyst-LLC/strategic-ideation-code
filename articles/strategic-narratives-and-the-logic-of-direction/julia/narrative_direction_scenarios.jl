# Advanced Julia scenario model for strategic narrative coherence.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "narrative_profiles.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("diagnosis_clarity" => 0.14, "purpose_clarity" => 0.12, "choice_clarity" => 0.14, "sequencing_logic" => 0.12, "role_clarity" => 0.11, "future_credibility" => 0.10, "accountability_strength" => 0.11, "evidence_grounding" => 0.08, "stakeholder_visibility" => 0.05, "ethical_visibility" => 0.03),
    "implementation_stress" => Dict("diagnosis_clarity" => 0.12, "purpose_clarity" => 0.10, "choice_clarity" => 0.16, "sequencing_logic" => 0.17, "role_clarity" => 0.16, "future_credibility" => 0.08, "accountability_strength" => 0.12, "evidence_grounding" => 0.05, "stakeholder_visibility" => 0.03, "ethical_visibility" => 0.01),
    "legitimacy_stress" => Dict("diagnosis_clarity" => 0.12, "purpose_clarity" => 0.12, "choice_clarity" => 0.10, "sequencing_logic" => 0.08, "role_clarity" => 0.09, "future_credibility" => 0.08, "accountability_strength" => 0.13, "evidence_grounding" => 0.08, "stakeholder_visibility" => 0.12, "ethical_visibility" => 0.08),
    "foresight_stress" => Dict("diagnosis_clarity" => 0.13, "purpose_clarity" => 0.10, "choice_clarity" => 0.12, "sequencing_logic" => 0.16, "role_clarity" => 0.08, "future_credibility" => 0.18, "accountability_strength" => 0.09, "evidence_grounding" => 0.08, "stakeholder_visibility" => 0.04, "ethical_visibility" => 0.02)
)

dimensions = ["diagnosis_clarity", "purpose_clarity", "choice_clarity", "sequencing_logic", "role_clarity", "future_credibility", "accountability_strength", "evidence_grounding", "stakeholder_visibility", "ethical_visibility"]

output = [["scenario", "narrative_id", "narrative_name", "coherence_score", "weakest_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("narrative_id")], row[col("narrative_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_narrative_direction_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_narrative_direction_scenarios.csv")
