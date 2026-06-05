# Advanced R workflow for implementation and alignment profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/implementation_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

orgs <- read.csv(file.path(raw_dir, "implementation_profiles.csv"))

orgs$implementation_profile_score <-
  0.12 * orgs$goal_clarity +
  0.15 * orgs$coordination_quality +
  0.12 * orgs$structural_support +
  0.12 * orgs$cultural_support +
  0.13 * orgs$incentive_alignment +
  0.12 * orgs$resource_sufficiency +
  0.11 * orgs$communication_quality +
  0.10 * orgs$accountability_strength +
  0.10 * orgs$adaptive_execution +
  0.08 * orgs$external_alignment +
  0.05 * orgs$ethical_resilience

orgs$alignment_drift_risk <-
  0.16 * (1 - orgs$coordination_quality) +
  0.14 * (1 - orgs$cultural_support) +
  0.14 * (1 - orgs$incentive_alignment) +
  0.12 * (1 - orgs$communication_quality) +
  0.12 * (1 - orgs$adaptive_execution) +
  0.10 * (1 - orgs$external_alignment) +
  0.10 * (1 - orgs$accountability_strength) +
  0.06 * (1 - orgs$ethical_resilience) +
  0.06 * (1 - orgs$structural_support)

write.csv(
  orgs[order(-orgs$implementation_profile_score), ],
  file.path(out_tables, "r_implementation_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(orgs, aes(x = reorder(organization_name, implementation_profile_score), y = implementation_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategy Implementation Profile Scores",
      x = "Organization",
      y = "Implementation Profile Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_implementation_profile_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(orgs, aes(x = alignment_drift_risk, y = adaptive_execution, size = resource_sufficiency, label = organization_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Alignment Drift Risk and Adaptive Execution",
      x = "Alignment Drift Risk",
      y = "Adaptive Execution",
      size = "Resource Sufficiency"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_drift_adaptation_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_implementation_profile_scores_base.png"), width = 1100, height = 800)
  barplot(
    orgs$implementation_profile_score,
    names.arg = orgs$organization_id,
    main = "Implementation Profile Scores",
    ylab = "Profile Score"
  )
  dev.off()
}

print(orgs[, c("organization_id", "organization_name", "implementation_profile_score", "alignment_drift_risk")])
