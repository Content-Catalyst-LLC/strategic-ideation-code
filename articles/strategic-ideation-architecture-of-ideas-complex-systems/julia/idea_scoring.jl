# Strategic Ideation: Idea Scoring in Julia
# Educational example only.

ideas = Dict(
    "Community Evidence Platform" => [0.62, 0.86, 0.68, 0.88, 0.74, 0.35, 0.63],
    "Scenario-Based Policy Lab" => [0.71, 0.82, 0.59, 0.85, 0.81, 0.42, 0.55],
    "AI-Assisted Knowledge Repository" => [0.78, 0.80, 0.64, 0.82, 0.76, 0.48, 0.60]
)

weights = [0.16, 0.20, 0.16, 0.20, 0.14, -0.08, 0.14]

function idea_score(values, weights)
    return sum(values .* weights)
end

for (idea, values) in ideas
    println(idea, ": ", idea_score(values, weights))
end
