# Advanced Julia institutional memory sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "memory_systems.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["system_id", "system_area", "memory_strength", "memory_failure_risk"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    strength =
        0.09 * num(row, "capture_quality") +
        0.11 * num(row, "metadata_completeness") +
        0.11 * num(row, "context_preservation") +
        0.13 * num(row, "decision_memory") +
        0.12 * num(row, "learning_integration") +
        0.12 * num(row, "retrieval_readiness") +
        0.10 * num(row, "reuse_potential") +
        0.08 * num(row, "stewardship_quality") +
        0.06 * num(row, "continuity_resilience") +
        0.05 * num(row, "ethical_memory") +
        0.03 * num(row, "ai_governance")

    risk =
        0.09 * (1 - num(row, "capture_quality")) +
        0.11 * (1 - num(row, "metadata_completeness")) +
        0.11 * (1 - num(row, "context_preservation")) +
        0.13 * (1 - num(row, "decision_memory")) +
        0.12 * (1 - num(row, "learning_integration")) +
        0.12 * (1 - num(row, "retrieval_readiness")) +
        0.09 * (1 - num(row, "reuse_potential")) +
        0.08 * (1 - num(row, "stewardship_quality")) +
        0.07 * (1 - num(row, "continuity_resilience")) +
        0.05 * (1 - num(row, "ethical_memory")) +
        0.03 * (1 - num(row, "ai_governance"))

    push!(output, [
        row[col("system_id")],
        row[col("system_area")],
        round(strength, digits = 4),
        round(risk, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_institutional_memory_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_institutional_memory_sensitivity.csv")
