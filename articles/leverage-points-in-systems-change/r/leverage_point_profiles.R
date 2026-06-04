# Advanced R workflow for leverage points in systems change.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

leverage <- read.csv(file.path(raw_dir, "leverage_points.csv"))

leverage$leverage_profile_score <-
  0.06 * leverage$implementation_ease +
  0.16 * leverage$structural_depth +
  0.14 * leverage$system_sensitivity +
  0.13 * leverage$feedback_influence +
  0.11 * leverage$information_effect +
  0.13 * leverage$rule_power +
  0.13 * leverage$goal_alignment +
  0.08 * leverage$paradigm_relevance +
  0.14 * leverage$transformative_potential +
  0.08 * leverage$learning_capacity -
  0.06 * leverage$unintended_consequence_risk

leverage$governance_need_score <-
  0.26 * leverage$legitimacy_requirement +
  0.24 * leverage$unintended_consequence_risk +
  0.22 * leverage$transformative_potential +
  0.14 * (1 - leverage$implementation_ease) +
  0.14 * leverage$paradigm_relevance

leverage$diagnosis <- ifelse(
  leverage$leverage_profile_score >= 0.72 & leverage$governance_need_score >= 0.68,
  "high_leverage_high_governance_need",
  ifelse(
    leverage$leverage_profile_score >= 0.68,
    "high_leverage_candidate",
    ifelse(
      leverage$implementation_ease >= 0.70 & leverage$structural_depth <= 0.45,
      "easy_but_shallow",
      "moderate_leverage_review"
    )
  )
)

write.csv(
  leverage[order(-leverage$leverage_profile_score), ],
  file.path(out_tables, "r_leverage_point_profiles.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(leverage, aes(x = reorder(intervention_name, leverage_profile_score), y = leverage_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Leverage Profile Scores",
      x = "Intervention",
      y = "Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_leverage_profile_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(leverage, aes(x = governance_need_score, y = leverage_profile_score, label = leverage_id)) +
    geom_point(size = 3) +
    geom_text(nudge_y = 0.02, check_overlap = TRUE) +
    labs(
      title = "Leverage Profile vs Governance Need",
      x = "Governance Need",
      y = "Leverage Profile"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_leverage_vs_governance.png"), width = 10, height = 7, dpi = 160)
} else {
  png(file.path(out_figures, "r_leverage_profile_scores_base.png"), width = 1100, height = 800)
  barplot(
    leverage$leverage_profile_score,
    names.arg = leverage$leverage_id,
    main = "Leverage Profile Scores",
    ylab = "Score"
  )
  dev.off()
}

print(leverage[, c("leverage_id", "intervention_name", "leverage_profile_score", "governance_need_score", "diagnosis")])
