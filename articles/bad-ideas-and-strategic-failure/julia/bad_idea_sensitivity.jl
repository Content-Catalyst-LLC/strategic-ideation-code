# Advanced Julia bad-idea risk sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "bad_ideas.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["idea_id", "idea", "idea_quality", "failure_risk", "power_distortion"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    quality =
        0.12 * num(row, "problem_frame_integrity") +
        0.11 * num(row, "mechanism_clarity") +
        0.13 * num(row, "evidence_quality") +
        0.10 * num(row, "context_fit") +
        0.12 * num(row, "implementation_readiness") +
        0.10 * num(row, "incentive_alignment") +
        0.10 * num(row, "ethical_visibility") +
        0.09 * num(row, "strategic_merit") +
        0.08 * num(row, "learning_design") +
        0.05 * num(row, "narrative_honesty")

    distortion = num(row, "institutional_support") - num(row, "strategic_merit")
    positive_distortion = max(0.0, distortion)

    risk =
        0.12 * (1 - num(row, "problem_frame_integrity")) +
        0.11 * (1 - num(row, "mechanism_clarity")) +
        0.13 * (1 - num(row, "evidence_quality")) +
        0.10 * (1 - num(row, "context_fit")) +
        0.12 * (1 - num(row, "implementation_readiness")) +
        0.10 * (1 - num(row, "incentive_alignment")) +
        0.10 * (1 - num(row, "ethical_visibility")) +
        0.08 * (1 - num(row, "learning_design")) +
        0.05 * (1 - num(row, "narrative_honesty")) +
        0.05 * positive_distortion +
        0.04 * num(row, "ai_fluency_risk")

    push!(output, [
        row[col("idea_id")],
        row[col("idea")],
        round(quality, digits = 4),
        round(risk, digits = 4),
        round(distortion, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_bad_idea_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_bad_idea_sensitivity.csv")
