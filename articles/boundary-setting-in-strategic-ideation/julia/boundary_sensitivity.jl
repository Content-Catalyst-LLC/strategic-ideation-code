# Advanced Julia boundary sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "options.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

weights = Dict(
    "internal_boundary" => Dict("internal_efficiency" => 0.38, "stakeholder_value" => 0.10, "system_leverage" => 0.10, "long_term_resilience" => 0.10, "ethical_responsibility" => 0.08, "implementation_feasibility" => 0.16, "learning_value" => 0.04, "strategic_reversibility" => 0.04),
    "stakeholder_boundary" => Dict("internal_efficiency" => 0.08, "stakeholder_value" => 0.34, "system_leverage" => 0.12, "long_term_resilience" => 0.10, "ethical_responsibility" => 0.20, "implementation_feasibility" => 0.08, "learning_value" => 0.05, "strategic_reversibility" => 0.03),
    "system_boundary" => Dict("internal_efficiency" => 0.08, "stakeholder_value" => 0.12, "system_leverage" => 0.34, "long_term_resilience" => 0.18, "ethical_responsibility" => 0.10, "implementation_feasibility" => 0.06, "learning_value" => 0.08, "strategic_reversibility" => 0.04),
    "long_term_boundary" => Dict("internal_efficiency" => 0.06, "stakeholder_value" => 0.12, "system_leverage" => 0.20, "long_term_resilience" => 0.32, "ethical_responsibility" => 0.14, "implementation_feasibility" => 0.05, "learning_value" => 0.08, "strategic_reversibility" => 0.03),
    "ethical_boundary" => Dict("internal_efficiency" => 0.06, "stakeholder_value" => 0.22, "system_leverage" => 0.12, "long_term_resilience" => 0.16, "ethical_responsibility" => 0.28, "implementation_feasibility" => 0.05, "learning_value" => 0.07, "strategic_reversibility" => 0.04)
)

output = [["option_id", "option_name", "mean_score", "boundary_sensitivity", "strongest_boundary", "weakest_boundary"]]

for i in 1:size(rows, 1)
    row = rows[i, :]
    scores = Dict{String, Float64}()

    for (boundary, w) in weights
        scores[boundary] = sum(w[k] * num(row, k) for k in keys(w))
    end

    values = collect(values(scores))
    strongest = sort(collect(scores), by = x -> -x.second)[1].first
    weakest = sort(collect(scores), by = x -> x.second)[1].first

    push!(output, [
        row[col("option_id")],
        row[col("option_name")],
        round(mean(values), digits = 4),
        round(maximum(values) - minimum(values), digits = 4),
        strongest,
        weakest
    ])
end

writedlm(joinpath(out_dir, "julia_boundary_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_boundary_sensitivity.csv")
