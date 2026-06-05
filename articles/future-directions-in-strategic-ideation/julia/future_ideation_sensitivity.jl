# Advanced Julia future-ready strategic ideation sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "future_ideas.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["idea_id", "idea", "future_ready_score", "future_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    score =
        0.10 * num(row, "problem_frame_quality") +
        0.10 * num(row, "evidence_quality") +
        0.10 * num(row, "adaptability") +
        0.11 * num(row, "scenario_robustness") +
        0.10 * num(row, "stakeholder_legitimacy") +
        0.09 * num(row, "implementation_readiness") +
        0.10 * num(row, "ethical_visibility") +
        0.11 * num(row, "learning_design") +
        0.08 * num(row, "option_value") +
        0.06 * num(row, "ai_governance") +
        0.05 * num(row, "systems_responsibility")

    push!(output, [
        row[col("idea_id")],
        row[col("idea")],
        round(score, digits = 4),
        round(1.0 - score, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_future_ideation_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_future_ideation_sensitivity.csv")
