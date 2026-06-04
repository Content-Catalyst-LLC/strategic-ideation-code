# Advanced Julia scenario model for competing problem frames.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "problem_frames.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

scenarios = Dict(
    "baseline" => Dict("boundary_breadth" => 0.16, "stakeholder_inclusion" => 0.15, "systems_awareness" => 0.15, "causal_depth" => 0.16, "assumption_clarity" => 0.12, "reframing_capacity" => 0.13, "actionability" => 0.11, "institutional_lock_in_risk" => -0.10, "political_convenience_risk" => -0.08),
    "stakeholder_priority" => Dict("boundary_breadth" => 0.14, "stakeholder_inclusion" => 0.26, "systems_awareness" => 0.12, "causal_depth" => 0.14, "assumption_clarity" => 0.10, "reframing_capacity" => 0.12, "actionability" => 0.10, "institutional_lock_in_risk" => -0.10, "political_convenience_risk" => -0.10),
    "systems_priority" => Dict("boundary_breadth" => 0.18, "stakeholder_inclusion" => 0.12, "systems_awareness" => 0.26, "causal_depth" => 0.18, "assumption_clarity" => 0.10, "reframing_capacity" => 0.12, "actionability" => 0.08, "institutional_lock_in_risk" => -0.10, "political_convenience_risk" => -0.08),
    "actionability_priority" => Dict("boundary_breadth" => 0.12, "stakeholder_inclusion" => 0.12, "systems_awareness" => 0.12, "causal_depth" => 0.14, "assumption_clarity" => 0.12, "reframing_capacity" => 0.14, "actionability" => 0.24, "institutional_lock_in_risk" => -0.10, "political_convenience_risk" => -0.08)
)

dimensions = ["boundary_breadth", "stakeholder_inclusion", "systems_awareness", "causal_depth", "assumption_clarity", "reframing_capacity", "actionability", "institutional_lock_in_risk", "political_convenience_risk"]
positive_dimensions = ["boundary_breadth", "stakeholder_inclusion", "systems_awareness", "causal_depth", "assumption_clarity", "reframing_capacity", "actionability"]

output = [["scenario", "frame_id", "frame_name", "framing_score", "weakest_positive_dimension"]]

for (scenario, weights) in scenarios
    for i in 1:size(rows, 1)
        row = rows[i, :]
        score = sum(weights[d] * num(row, d) for d in dimensions)
        values = [(d, num(row, d)) for d in positive_dimensions]
        weakest = sort(values, by = x -> x[2])[1][1]
        push!(output, [scenario, row[col("frame_id")], row[col("frame_name")], round(score, digits = 4), weakest])
    end
end

writedlm(joinpath(out_dir, "julia_framing_scenarios.csv"), output, ',')
println("Wrote outputs/tables/julia_framing_scenarios.csv")
