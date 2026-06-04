# Advanced Julia scenario model for ideation-strategy-tactics alignment.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "layer_profile_contexts.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("ideation_quality" => 0.16, "strategic_clarity" => 0.20, "tactical_alignment" => 0.18, "feedback_quality" => 0.14, "adaptive_learning" => 0.14, "decision_memory" => 0.08, "ethical_legitimacy" => 0.10),
    "execution_stress" => Dict("ideation_quality" => 0.12, "strategic_clarity" => 0.22, "tactical_alignment" => 0.26, "feedback_quality" => 0.12, "adaptive_learning" => 0.12, "decision_memory" => 0.06, "ethical_legitimacy" => 0.10),
    "learning_system" => Dict("ideation_quality" => 0.16, "strategic_clarity" => 0.16, "tactical_alignment" => 0.14, "feedback_quality" => 0.20, "adaptive_learning" => 0.20, "decision_memory" => 0.08, "ethical_legitimacy" => 0.06),
    "legitimacy_sensitive" => Dict("ideation_quality" => 0.14, "strategic_clarity" => 0.17, "tactical_alignment" => 0.15, "feedback_quality" => 0.14, "adaptive_learning" => 0.13, "decision_memory" => 0.07, "ethical_legitimacy" => 0.20)
)

output = [["scenario", "context_id", "context_name", "alignment_score", "weakest_layer"]]

layers = ["ideation_quality", "strategic_clarity", "tactical_alignment", "feedback_quality", "adaptive_learning", "decision_memory", "ethical_legitimacy"]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[layer] * num(row, layer) for layer in layers)
        values = [(layer, num(row, layer)) for layer in layers]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("context_id")], row[col("context_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_layer_scenario_scores.csv"), output, ',')
println("Wrote outputs/tables/julia_layer_scenario_scores.csv")
