# Advanced Julia strategic interaction sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "strategic_interaction_profiles.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["setting_id", "setting_name", "mechanism_opportunity", "cooperation_fragility", "projected_stability_after_40_steps"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    mechanism_opportunity =
        0.30 * num(row, "mechanism_design_potential") +
        0.18 * num(row, "coordination_potential") +
        0.16 * num(row, "information_asymmetry") +
        0.14 * num(row, "ethical_complexity") +
        0.12 * num(row, "institutional_support") +
        0.10 * num(row, "behavioral_realism")

    cooperation_fragility =
        0.22 * num(row, "rivalry") +
        0.20 * num(row, "retaliation_risk") +
        0.16 * num(row, "information_asymmetry") +
        0.12 * num(row, "ethical_complexity") -
        0.15 * num(row, "institutional_support") -
        0.15 * num(row, "coordination_potential")

    state = 0.60
    cooperation = num(row, "coordination_potential")

    for t in 2:40
        cooperation = min(1.2, max(0.0,
            cooperation +
            0.04 * num(row, "institutional_support") +
            0.04 * num(row, "mechanism_design_potential") +
            0.03 * num(row, "behavioral_realism") -
            0.05 * num(row, "retaliation_risk") -
            0.03 * num(row, "rivalry")
        ))

        gain = 0.16 * cooperation + 0.14 * num(row, "institutional_support") + 0.12 * num(row, "mechanism_design_potential")
        friction = 0.18 * num(row, "retaliation_risk") + 0.10 * num(row, "rivalry")
        state = min(1.6, max(0.0, state + gain / 5 - friction / 5))
    end

    push!(output, [
        row[col("setting_id")],
        row[col("setting_name")],
        round(mechanism_opportunity, digits = 4),
        round(cooperation_fragility, digits = 4),
        round(state, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_strategic_interaction_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_strategic_interaction_sensitivity.csv")
