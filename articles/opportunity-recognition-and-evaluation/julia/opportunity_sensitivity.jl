# Advanced Julia opportunity sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "opportunities.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["opportunity_id", "opportunity_name", "profile_score", "confidence_adjusted_score", "risk_adjusted_learning"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    profile =
        0.13 * num(row, "signal_strength") +
        0.14 * num(row, "capability_alignment") +
        0.12 * num(row, "desirability") +
        0.12 * num(row, "viability") +
        0.10 * num(row, "timing") +
        0.12 * num(row, "learning_value") +
        0.11 * num(row, "option_value") +
        0.10 * num(row, "strategic_fit") +
        0.10 * num(row, "ethical_resilience") -
        0.14 * num(row, "risk")

    confidence_adjusted = profile * num(row, "evidence_confidence")
    risk_adjusted_learning = num(row, "learning_value") + num(row, "option_value") - num(row, "risk")

    push!(output, [
        row[col("opportunity_id")],
        row[col("opportunity_name")],
        round(profile, digits = 4),
        round(confidence_adjusted, digits = 4),
        round(risk_adjusted_learning, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_opportunity_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_opportunity_sensitivity.csv")
