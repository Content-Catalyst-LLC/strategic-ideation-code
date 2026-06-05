# Advanced Julia institutional power sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "power_ideas.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["idea_id", "idea", "merit_score", "institutional_support", "power_distortion", "voice_gap"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    merit =
        0.28 * num(row, "strategic_merit") +
        0.21 * num(row, "evidence_strength") +
        0.16 * num(row, "stakeholder_influence") +
        0.13 * num(row, "dissent_protection") +
        0.12 * num(row, "classification_visibility") +
        0.10 * num(row, "ethical_visibility")

    support =
        0.28 * num(row, "executive_sponsorship") +
        0.24 * num(row, "resource_fit") +
        0.24 * num(row, "power_alignment") +
        0.24 * num(row, "advancement_likelihood")

    distortion = support - merit
    voice_gap = num(row, "advancement_likelihood") - num(row, "stakeholder_influence")

    push!(output, [
        row[col("idea_id")],
        row[col("idea")],
        round(merit, digits = 4),
        round(support, digits = 4),
        round(distortion, digits = 4),
        round(voice_gap, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_institutional_power_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_institutional_power_sensitivity.csv")
