# Strategic scoring and scenario-comparison example.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
data_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

ideas_file = joinpath(data_dir, "synthetic_ideas.csv")
raw = readdlm(ideas_file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)

function parse_col(row, name)
    parse(Float64, row[col(name)])
end

scenarios = Dict(
    "baseline" => Dict("strategic_fit" => 0.24, "feasibility" => 0.16, "systems_leverage" => 0.20, "learning_value" => 0.14, "ethical_legitimacy" => 0.18, "uncertainty" => -0.08),
    "resilience_emphasis" => Dict("strategic_fit" => 0.18, "feasibility" => 0.12, "systems_leverage" => 0.28, "learning_value" => 0.16, "ethical_legitimacy" => 0.18, "uncertainty" => -0.08),
    "implementation_emphasis" => Dict("strategic_fit" => 0.22, "feasibility" => 0.26, "systems_leverage" => 0.15, "learning_value" => 0.11, "ethical_legitimacy" => 0.18, "uncertainty" => -0.08)
)

output = [["scenario", "idea_id", "idea_name", "score"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score =
            weights["strategic_fit"] * parse_col(row, "strategic_fit") +
            weights["feasibility"] * parse_col(row, "feasibility") +
            weights["systems_leverage"] * parse_col(row, "systems_leverage") +
            weights["learning_value"] * parse_col(row, "learning_value") +
            weights["ethical_legitimacy"] * parse_col(row, "ethical_legitimacy") +
            weights["uncertainty"] * parse_col(row, "uncertainty")

        push!(output, [scenario, row[col("idea_id")], row[col("idea_name")], round(score, digits = 4)])
    end
end

writedlm(joinpath(out_dir, "julia_scenario_comparison.csv"), output, ',')

println("Scenario comparison written to outputs/tables/julia_scenario_comparison.csv")
