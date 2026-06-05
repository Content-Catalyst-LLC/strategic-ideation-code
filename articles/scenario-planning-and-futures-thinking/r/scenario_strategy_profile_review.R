# Advanced R workflow for scenario planning and futures thinking profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/scenario_strategy_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

stress <- read.csv(file.path(raw_dir, "strategy_stress_tests.csv"))

scenario_cols <- c(
  "scenario_stable_growth",
  "scenario_tech_disruption",
  "scenario_environmental_stress",
  "scenario_institutional_fragmentation",
  "scenario_supply_disruption"
)

stress$mean_performance <- rowMeans(stress[, scenario_cols])
stress$worst_case <- apply(stress[, scenario_cols], 1, min)
stress$best_case <- apply(stress[, scenario_cols], 1, max)
stress$volatility <- apply(stress[, scenario_cols], 1, sd)

stress$robustness_profile <-
  0.30 * stress$worst_case +
  0.24 * stress$mean_performance +
  0.16 * stress$flexibility +
  0.12 * stress$implementation_readiness +
  0.10 * stress$ethical_resilience +
  0.10 * stress$option_value -
  0.12 * stress$volatility

stress$fragility_risk <-
  0.30 * (1 - stress$worst_case) +
  0.18 * stress$volatility +
  0.14 * (1 - stress$flexibility) +
  0.12 * (1 - stress$option_value) +
  0.10 * (1 - stress$ethical_resilience) +
  0.08 * (1 - stress$implementation_readiness)

write.csv(
  stress[order(-stress$robustness_profile), ],
  file.path(out_tables, "r_scenario_strategy_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(stress, aes(x = reorder(strategy_name, robustness_profile), y = robustness_profile)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Scenario-Based Strategy Robustness",
      x = "Strategy",
      y = "Robustness profile"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_scenario_strategy_robustness.png"), width = 11, height = 8, dpi = 160)

  ggplot(stress, aes(x = reorder(strategy_name, fragility_risk), y = fragility_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Scenario Fragility Risk",
      x = "Strategy",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_scenario_fragility_risk.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_scenario_strategy_robustness_base.png"), width = 1100, height = 800)
  barplot(
    stress$robustness_profile,
    names.arg = stress$test_id,
    main = "Scenario-Based Strategy Robustness",
    ylab = "Robustness profile"
  )
  dev.off()
}

print(stress[, c("test_id", "strategy_name", "mean_performance", "worst_case", "robustness_profile", "fragility_risk")])
