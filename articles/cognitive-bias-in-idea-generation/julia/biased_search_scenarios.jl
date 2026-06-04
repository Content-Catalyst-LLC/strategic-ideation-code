using DelimitedFiles
root = normpath(joinpath(@__DIR__, "..")); raw_dir = joinpath(root, "data", "raw"); out_dir = joinpath(root, "outputs", "tables"); mkpath(out_dir)
raw = readdlm(joinpath(raw_dir, "bias_contexts.csv"), ',', String); header = raw[1, :]; rows = raw[2:end, :]
col(name) = findfirst(==(name), header); num(row, name) = parse(Float64, row[col(name)])
weights = Dict("availability_pressure"=>-0.12,"anchoring_intensity"=>-0.12,"conformity_pressure"=>-0.13,"framing_rigidity"=>-0.12,"institutional_lock_in"=>-0.10,"expert_enclosure"=>-0.08,"ai_familiarity_pressure"=>-0.07,"stakeholder_diversity"=>0.16,"exploratory_variation"=>0.18,"evidence_discipline"=>0.12,"political_safety"=>0.08,"decision_memory_quality"=>0.08)
output = [["context_id", "context_name", "bias_adjusted_score", "premature_convergence_risk"]]
for i in 1:size(rows, 1)
 row = rows[i, :]; score = sum(weights[k]*num(row,k) for k in keys(weights)); convergence = num(row,"anchoring_intensity")*num(row,"conformity_pressure")*num(row,"framing_rigidity"); push!(output, [row[col("context_id")], row[col("context_name")], round(score, digits=4), round(convergence, digits=4)])
end
writedlm(joinpath(out_dir, "julia_biased_search_scenarios.csv"), output, ','); println("Wrote outputs/tables/julia_biased_search_scenarios.csv")
