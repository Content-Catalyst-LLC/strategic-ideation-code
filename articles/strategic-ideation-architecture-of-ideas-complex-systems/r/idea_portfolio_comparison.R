# Strategic Ideation: Idea Portfolio Comparison in R
# Educational example only.

library(tidyverse)

ideas <- read_csv("../data/strategic_idea_portfolio.csv", show_col_types = FALSE)

ideas <- ideas |>
  mutate(
    idea_score =
      0.16 * novelty +
      0.20 * relevance +
      0.16 * feasibility +
      0.20 * strategic_fit +
      0.14 * learning_potential -
      0.08 * risk +
      0.14 * implementation_readiness
  )

ideas_long <- ideas |>
  pivot_longer(
    cols = c(
      novelty,
      relevance,
      feasibility,
      strategic_fit,
      learning_potential,
      risk,
      implementation_readiness
    ),
    names_to = "dimension",
    values_to = "value"
  )

revision_flags <- ideas |>
  mutate(
    low_feasibility = feasibility < 0.60,
    high_risk = risk > 0.45,
    low_readiness = implementation_readiness < 0.60,
    needs_revision = low_feasibility | high_risk | low_readiness
  )

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(ideas, "../outputs/r_strategic_idea_portfolio.csv")
write_csv(ideas_long, "../outputs/r_strategic_idea_dimensions_long.csv")
write_csv(revision_flags, "../outputs/r_strategic_idea_revision_flags.csv")

print(ideas)
print(revision_flags)
