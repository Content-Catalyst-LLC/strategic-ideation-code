using DelimitedFiles
root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)
raw = readdlm(joinpath(raw_dir, "strategic_options.csv"), ',', String)
header = raw[1, :]
rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])
output = [["option_id", "option_name", "option_value_score", "lock_in_warning"]]
for i in 1:size(rows, 1)
    row = rows[i, :]
    score = 0.10*num(row,"initial_return") + 0.17*num(row,"learning_value") + 0.17*num(row,"flexibility") + 0.12*num(row,"reversibility") + 0.11*num(row,"scalability") + 0.13*num(row,"modularity") - 0.14*num(row,"lock_in_exposure") - 0.06*num(row,"carrying_cost") + 0.11*num(row,"governance_readiness") + 0.09*num(row,"ethical_resilience")
    warning = 0.30*num(row,"lock_in_exposure") + 0.18*(1-num(row,"reversibility")) + 0.16*(1-num(row,"flexibility")) + 0.14*(1-num(row,"modularity")) + 0.12*(1-num(row,"governance_readiness")) + 0.10*(1-num(row,"ethical_resilience"))
    push!(output, [row[col("option_id")], row[col("option_name")], round(score, digits=4), round(warning, digits=4)])
end
writedlm(joinpath(out_dir, "julia_option_value_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_option_value_sensitivity.csv")
