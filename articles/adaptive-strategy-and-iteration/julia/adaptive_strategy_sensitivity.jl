# Advanced Julia adaptive strategy sensitivity model.
# Uses Julia standard library only.

using DelimitedFiles
using Statistics

root = normpath(joinpath(@__DIR__, ".."))
raw_dir = joinpath(root, "data", "raw")
out_dir = joinpath(root, "outputs", "tables")
mkpath(out_dir)

file = joinpath(raw_dir, "strategy_profiles.csv")
raw = readdlm(file, ',', String)
header = raw[1, :]
rows = raw[2:end, :]

col(name) = findfirst(==(name), header)
num(row, name) = parse(Float64, row[col(name)])

output = [["strategy_id", "strategy_name", "adaptive_strategy_score", "over_adaptation_risk", "projected_viability_after_40_steps"]]

for i in 1:size(rows, 1)
    row = rows[i, :]

    score =
        0.13 * num(row, "flexibility") +
        0.15 * num(row, "learning_capacity") +
        0.09 * num(row, "exploration") +
        0.11 * num(row, "exploitation_balance") +
        0.15 * num(row, "coherence") +
        0.13 * num(row, "feedback_intelligence") +
        0.10 * num(row, "governance") +
        0.08 * num(row, "systems_awareness") +
        0.06 * num(row, "learning_memory")

    risk =
        0.20 * num(row, "flexibility") * (1 - num(row, "coherence")) +
        0.18 * (1 - num(row, "governance")) +
        0.16 * (1 - num(row, "feedback_intelligence")) +
        0.14 * (1 - num(row, "learning_capacity")) +
        0.12 * (1 - num(row, "exploitation_balance")) +
        0.10 * (1 - num(row, "learning_memory")) +
        0.10 * (1 - num(row, "systems_awareness"))

    state = 1.0
    for t in 2:40
        if t < 20
            shock = 0.03
            gain = 0.14 * num(row, "coherence") + 0.08 * num(row, "learning_capacity") + 0.06 * num(row, "feedback_intelligence")
        else
            shock = 0.14
            gain =
                0.10 * num(row, "coherence") +
                0.16 * num(row, "flexibility") +
                0.18 * num(row, "learning_capacity") +
                0.12 * num(row, "feedback_intelligence") +
                0.08 * num(row, "systems_awareness")
        end

        over_penalty =
            0.10 * num(row, "flexibility") * (1 - num(row, "coherence")) +
            0.08 * (1 - num(row, "governance")) +
            0.06 * (1 - num(row, "feedback_intelligence"))

        state = min(1.8, max(0.0, state + gain / 4 - shock / 5 - over_penalty / 4))
    end

    push!(output, [
        row[col("strategy_id")],
        row[col("strategy_name")],
        round(score, digits = 4),
        round(risk, digits = 4),
        round(state, digits = 4)
    ])
end

writedlm(joinpath(out_dir, "julia_adaptive_strategy_sensitivity.csv"), output, ',')
println("Wrote outputs/tables/julia_adaptive_strategy_sensitivity.csv")
