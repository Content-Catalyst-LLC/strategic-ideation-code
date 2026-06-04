using DelimitedFiles
root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)
raw = readdlm(joinpath(raw_dir, "strategy_contexts.csv"), ',', String)
header = raw[1, :]; rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])
output = [["context_id", "context_name", "baseline_score", "disruption_score"]]
for i in 1:size(rows, 1)
    row = rows[i, :]
    baseline = -0.16*num(row,"assumption_load") + 0.18*num(row,"structural_clarity") + 0.18*num(row,"constraint_discrimination") + 0.18*num(row,"reconstruction_quality") + 0.14*num(row,"adaptive_potential") + 0.10*num(row,"evidence_contact") + 0.10*num(row,"ethical_visibility") + 0.08*num(row,"implementation_feasibility")
    disruption = -0.22*num(row,"assumption_load") + 0.18*num(row,"structural_clarity") + 0.22*num(row,"constraint_discrimination") + 0.18*num(row,"reconstruction_quality") + 0.16*num(row,"adaptive_potential") + 0.10*num(row,"evidence_contact") + 0.06*num(row,"ethical_visibility") + 0.08*num(row,"implementation_feasibility")
    push!(output, [row[col("context_id")], row[col("context_name")], round(baseline, digits=4), round(disruption, digits=4)])
end
writedlm(joinpath(out_dir, "julia_constraint_sensitivity_scores.csv"), output, ',')
println("Wrote outputs/tables/julia_constraint_sensitivity_scores.csv")
