# Advanced Julia scenario model for strategic ideation portfolios.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "idea_portfolio.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("strategic_fit" => 0.20, "feasibility" => 0.12, "systems_leverage" => 0.18, "learning_value" => 0.13, "ethical_legitimacy" => 0.16, "knowledge_reusability" => 0.09, "uncertainty" => -0.07),
    "systems_change" => Dict("strategic_fit" => 0.17, "feasibility" => 0.09, "systems_leverage" => 0.27, "learning_value" => 0.14, "ethical_legitimacy" => 0.16, "knowledge_reusability" => 0.10, "uncertainty" => -0.07),
    "implementation_focus" => Dict("strategic_fit" => 0.22, "feasibility" => 0.22, "systems_leverage" => 0.12, "learning_value" => 0.10, "ethical_legitimacy" => 0.15, "knowledge_reusability" => 0.08, "uncertainty" => -0.11),
    "learning_governance" => Dict("strategic_fit" => 0.16, "feasibility" => 0.10, "systems_leverage" => 0.16, "learning_value" => 0.24, "ethical_legitimacy" => 0.16, "knowledge_reusability" => 0.12, "uncertainty" => -0.06)
)

output = [["scenario", "idea_id", "idea_name", "score", "primary_strength"]]

dimensions = ["strategic_fit", "feasibility", "systems_leverage", "learning_value", "ethical_legitimacy", "knowledge_reusability"]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions) + weights["uncertainty"] * num(row, "uncertainty")
        values = [(d, num(row, d)) for d in dimensions]
        primary_strength = sort(values, by = x -> x[2], rev = true)[1][1]
        push!(output, [scenario, row[col("idea_id")], row[col("idea_name")], round(score, digits = 4), primary_strength])
    end
end

writedlm(joinpath(out_dir, "julia_ideation_scenario_scores.csv"), output, ',')
println("Wrote outputs/tables/julia_ideation_scenario_scores.csv")
