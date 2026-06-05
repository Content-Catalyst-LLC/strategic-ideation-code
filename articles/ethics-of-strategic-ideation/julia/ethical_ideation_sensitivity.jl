# Advanced Julia ethical ideation sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "ethical_ideas.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["idea_id", "idea", "ethical_legitimacy", "ethical_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    legitimacy =
        0.12 * num(row, "stakeholder_voice") +
        0.12 * num(row, "evidence_integrity") +
        0.10 * num(row, "burden_visibility") +
        0.09 * num(row, "uncertainty_visibility") +
        0.08 * num(row, "reversibility") +
        0.11 * num(row, "long_term_responsibility") +
        0.07 * num(row, "ai_governance") +
        0.09 * num(row, "accountability") +
        0.07 * num(row, "redress_quality") +
        0.08 * num(row, "problem_frame_integrity") +
        0.07 * num(row, "power_review")

    risk =
        0.13 * (1 - num(row, "stakeholder_voice")) +
        0.12 * (1 - num(row, "evidence_integrity")) +
        0.12 * (1 - num(row, "burden_visibility")) +
        0.10 * (1 - num(row, "uncertainty_visibility")) +
        0.09 * (1 - num(row, "reversibility")) +
        0.10 * (1 - num(row, "long_term_responsibility")) +
        0.10 * (1 - num(row, "ai_governance")) +
        0.08 * (1 - num(row, "accountability")) +
        0.07 * (1 - num(row, "redress_quality")) +
        0.05 * (1 - num(row, "problem_frame_integrity")) +
        0.04 * (1 - num(row, "power_review"))

    push!(output, [
        row[col("idea_id")],
        row[col("idea")],
        round(legitimacy, digits = 4),
        round(risk, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_ethical_ideation_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_ethical_ideation_sensitivity.csv")
