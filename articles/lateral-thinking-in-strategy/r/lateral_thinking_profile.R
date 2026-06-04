# Advanced R workflow for lateral thinking diagnostics.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

contexts <- read.csv(file.path(raw_dir, "lateral_contexts.csv"))
moves <- read.csv(file.path(raw_dir, "lateral_moves.csv"))

contexts$lateral_profile_score <-
  -0.14 * contexts$frame_rigidity +
  0.14 * contexts$provocation_strength +
  0.12 * contexts$analogical_distance +
  0.09 * contexts$random_entry_capacity +
  0.10 * contexts$reversal_capacity +
  0.10 * contexts$challenge_quality +
  0.14 * contexts$convergence_discipline +
  0.12 * contexts$systems_integration +
  0.08 * contexts$stakeholder_legitimacy +
  0.07 * contexts$political_safety +
  0.14 * contexts$transformational_potential

contexts$frame_rigidity_risk <- contexts$frame_rigidity * (1 - contexts$provocation_strength)
contexts$drift_risk <- contexts$transformational_potential * (1 - contexts$convergence_discipline)
contexts$legitimacy_gap <- pmax(0, 0.60 - contexts$stakeholder_legitimacy)

contexts$diagnosis <- ifelse(
  contexts$frame_rigidity_risk >= 0.55,
  "frame_rigidity_risk",
  ifelse(
    contexts$drift_risk >= 0.45,
    "unintegrated_novelty_risk",
    ifelse(
      contexts$legitimacy_gap >= 0.20,
      "stakeholder_legitimacy_gap",
      ifelse(contexts$lateral_profile_score >= 0.50, "strong_lateral_system", "requires_lateral_process_review")
    )
  )
)

moves$lateral_move_score <-
  0.16 * moves$frame_disruption +
  0.18 * moves$strategic_relevance +
  0.16 * moves$reconstruction_quality +
  0.12 * moves$evidence_pathway +
  0.12 * moves$stakeholder_fit +
  0.12 * moves$systems_fit +
  0.10 * moves$novelty_value -
  0.14 * moves$drift_risk

write.csv(contexts[order(-contexts$lateral_profile_score), ], file.path(out_tables, "r_lateral_context_profiles.csv"), row.names = FALSE)
write.csv(moves[order(-moves$lateral_move_score), ], file.path(out_tables, "r_lateral_move_scores.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(contexts, aes(x = reorder(context_name, lateral_profile_score), y = lateral_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Lateral Thinking Profile Scores",
      x = "Context",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_lateral_context_profiles.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_lateral_context_profiles_base.png"), width = 1100, height = 800)
  barplot(
    contexts$lateral_profile_score,
    names.arg = contexts$context_id,
    main = "Lateral Thinking Profile Scores",
    ylab = "Profile score"
  )
  dev.off()
}

print(contexts[, c("context_id", "context_name", "lateral_profile_score", "frame_rigidity_risk", "drift_risk", "diagnosis")])
