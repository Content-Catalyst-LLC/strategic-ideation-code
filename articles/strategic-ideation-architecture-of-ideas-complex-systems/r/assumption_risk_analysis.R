# Strategic Ideation: Assumption Risk Analysis in R
# Educational example only.

library(tidyverse)

assumptions <- read_csv("../data/assumption_register.csv", show_col_types = FALSE)

assumptions <- assumptions |>
  mutate(
    assumption_risk_score = (1 - confidence) * impact_if_wrong,
    priority_band = case_when(
      assumption_risk_score >= 0.35 ~ "High priority",
      assumption_risk_score >= 0.20 ~ "Medium priority",
      TRUE ~ "Lower priority"
    )
  ) |>
  arrange(desc(assumption_risk_score))

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(assumptions, "../outputs/r_assumption_risk_scores.csv")

print(assumptions)
