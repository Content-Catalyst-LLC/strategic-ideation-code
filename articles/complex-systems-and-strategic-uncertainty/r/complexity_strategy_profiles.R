# Advanced R workflow for complex systems and strategic uncertainty.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

envs <- read.csv(file.path(raw_dir, "complexity_environments.csv"))

envs$complexity_profile_score <-
  0.13 * envs$interdependence +
  0.13 * envs$nonlinearity +
  0.14 * envs$feedback_intensity +
  0.12 * envs$adaptation_pressure +
  0.11 * envs$path_dependence +
  0.10 * envs$boundary_ambiguity +
  0.10 * envs$emergence_potential +
  0.09 * envs$deep_uncertainty +
  0.09 * envs$scenario_need +
  0.09 * envs$learning_capacity_need

envs$linear_planning_risk <-
  0.20 * envs$nonlinearity +
  0.20 * envs$feedback_intensity +
  0.18 * envs$adaptation_pressure +
  0.16 * envs$deep_uncertainty +
  0.14 * envs$boundary_ambiguity +
  0.12 * envs$emergence_potential

envs$diagnosis <- ifelse(
  envs$complexity_profile_score >= 0.76,
  "adaptive_scenario_strategy_required",
  ifelse(
    envs$complexity_profile_score >= 0.60,
    "complexity_aware_strategy_recommended",
    "standard_planning_may_be_sufficient"
  )
)

write.csv(
  envs[order(-envs$complexity_profile_score), ],
  file.path(out_tables, "r_complexity_strategy_profiles.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(envs, aes(x = reorder(environment_name, complexity_profile_score), y = complexity_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Complexity-Aware Strategy Profile Scores",
      x = "Environment",
      y = "Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_complexity_profile_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_complexity_profile_scores_base.png"), width = 1100, height = 800)
  barplot(
    envs$complexity_profile_score,
    names.arg = envs$environment_id,
    main = "Complexity-Aware Strategy Profile Scores",
    ylab = "Score"
  )
  dev.off()
}

print(envs[, c("environment_id", "environment_name", "complexity_profile_score", "linear_planning_risk", "diagnosis")])
