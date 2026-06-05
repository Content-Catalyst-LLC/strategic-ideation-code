# Advanced Julia communication coherence sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "communication_profiles.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["profile_id", "communication_profile", "coherence_strength", "meaning_loss_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    strength =
        0.11 * num(row, "concept_definition") +
        0.11 * num(row, "narrative_coherence") +
        0.13 * num(row, "evidence_integrity") +
        0.10 * num(row, "audience_adaptation") +
        0.13 * num(row, "decision_alignment") +
        0.11 * num(row, "implementation_translatability") +
        0.08 * num(row, "feedback_quality") +
        0.10 * num(row, "governance_strength") +
        0.09 * num(row, "ethical_visibility") +
        0.04 * num(row, "ai_governance")

    risk =
        0.12 * (1 - num(row, "concept_definition")) +
        0.10 * (1 - num(row, "narrative_coherence")) +
        0.13 * (1 - num(row, "evidence_integrity")) +
        0.10 * (1 - num(row, "audience_adaptation")) +
        0.13 * (1 - num(row, "decision_alignment")) +
        0.11 * (1 - num(row, "implementation_translatability")) +
        0.08 * (1 - num(row, "feedback_quality")) +
        0.09 * (1 - num(row, "governance_strength")) +
        0.10 * (1 - num(row, "ethical_visibility")) +
        0.04 * (1 - num(row, "ai_governance"))

    push!(output, [
        row[col("profile_id")],
        row[col("communication_profile")],
        round(strength, digits = 4),
        round(risk, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_communication_coherence_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_communication_coherence_sensitivity.csv")
