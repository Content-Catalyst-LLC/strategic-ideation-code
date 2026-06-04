# Advanced R workflow for systems thinking in ideation.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read.csv(file.path(raw_dir, "systems_profiles.csv"))
leverage <- read.csv(file.path(raw_dir, "leverage_points.csv"))

systems$systems_ideation_score <-
  0.14 * systems$feedback_awareness +
  0.14 * systems$leverage_sensitivity +
  0.13 * systems$root_cause_depth +
  0.12 * systems$stakeholder_visibility +
  0.12 * systems$boundary_quality +
  0.10 * systems$stock_flow_awareness +
  0.10 * systems$delay_awareness +
  0.13 * systems$adaptive_learning -
  0.10 * systems$unintended_consequence_risk -
  0.08 * systems$local_optimization_risk

systems$symptom_focus_risk <-
  (1 - systems$root_cause_depth) * 0.30 +
  (1 - systems$leverage_sensitivity) * 0.25 +
  systems$local_optimization_risk * 0.25 +
  systems$unintended_consequence_risk * 0.20

systems$diagnosis <- ifelse(
  systems$systems_ideation_score >= 0.68,
  "strong_systems_ideation_capacity",
  ifelse(
    systems$symptom_focus_risk >= 0.62,
    "symptom_or_local_optimization_risk",
    "develop_with_structural_review"
  )
)

leverage$leverage_value_score <-
  0.22 * leverage$leverage_depth +
  0.12 * leverage$implementation_feasibility +
  0.12 * leverage$evidence_quality +
  0.12 * leverage$stakeholder_legitimacy +
  0.08 * leverage$reversibility +
  0.16 * leverage$system_sensitivity -
  0.10 * leverage$risk_exposure -
  0.08 * leverage$time_to_effect

write.csv(
  systems[order(-systems$systems_ideation_score), ],
  file.path(out_tables, "r_systems_ideation_profiles.csv"),
  row.names = FALSE
)

write.csv(
  leverage[order(-leverage$leverage_value_score), ],
  file.path(out_tables, "r_leverage_point_scores.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(systems, aes(x = reorder(system_name, systems_ideation_score), y = systems_ideation_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Systems-Ideation Profile Scores",
      x = "System",
      y = "Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_systems_ideation_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_systems_ideation_scores_base.png"), width = 1100, height = 800)
  barplot(
    systems$systems_ideation_score,
    names.arg = systems$system_id,
    main = "Systems-Ideation Profile Scores",
    ylab = "Score"
  )
  dev.off()
}

print(systems[, c("system_id", "system_name", "systems_ideation_score", "symptom_focus_risk", "diagnosis")])
