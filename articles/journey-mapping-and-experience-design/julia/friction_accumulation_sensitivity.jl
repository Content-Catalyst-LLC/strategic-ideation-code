# Advanced Julia friction accumulation sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "journey_contexts.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["journey_id", "journey_name", "journey_profile", "redesign_need", "projected_quality_after_10_stages", "transition_penalty"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    profile =
        0.15 * num(row, "clarity") +
        0.12 * num(row, "emotional_confidence") -
        0.18 * num(row, "friction") +
        0.14 * num(row, "transition_quality") +
        0.12 * num(row, "accessibility") +
        0.12 * num(row, "trust") +
        0.10 * num(row, "completion_support") +
        0.10 * num(row, "backstage_alignment") +
        0.07 * num(row, "measurement_quality")

    redesign =
        0.22 * num(row, "friction") +
        0.16 * (1 - num(row, "transition_quality")) +
        0.14 * (1 - num(row, "accessibility")) +
        0.13 * (1 - num(row, "trust")) +
        0.12 * (1 - num(row, "clarity")) +
        0.11 * (1 - num(row, "backstage_alignment")) +
        0.07 * (1 - num(row, "completion_support")) +
        0.05 * (1 - num(row, "measurement_quality"))

    quality = 0.80
    transition_penalty = 0.05 * (1 - num(row, "transition_quality"))

    for t in 2:10
        gain =
            0.10 * num(row, "clarity") +
            0.08 * num(row, "transition_quality") +
            0.08 * num(row, "completion_support") +
            0.07 * num(row, "accessibility") +
            0.07 * num(row, "trust")

        burden = 0.12 * num(row, "friction")
        access_penalty = 0.04 * (1 - num(row, "accessibility"))
        quality = min(1.5, max(0.0, quality + gain / 5 - burden / 5 - transition_penalty / 5 - access_penalty / 5))
    end

    push!(output, [
        row[col("journey_id")],
        row[col("journey_name")],
        round(profile, digits = 4),
        round(redesign, digits = 4),
        round(quality, digits = 4),
        round(transition_penalty, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_friction_accumulation_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_friction_accumulation_sensitivity.csv")
