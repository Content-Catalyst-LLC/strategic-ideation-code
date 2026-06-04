# Advanced R workflow for analogical transfer diagnostics.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

strategies <- read.csv(file.path(raw_dir, "analogical_strategies.csv"))
mappings <- read.csv(file.path(raw_dir, "source_target_mappings.csv"))

strategies$analogy_profile_score <-
  0.20 * strategies$structural_fit +
  0.16 * strategies$functional_fit -
  0.16 * strategies$surface_distraction +
  0.16 * strategies$adaptation_quality +
  0.12 * strategies$context_sensitivity +
  0.08 * strategies$stakeholder_legitimacy +
  0.08 * strategies$dynamic_compatibility +
  0.12 * strategies$innovation_potential +
  0.08 * strategies$evidence_strength

strategies$surface_distraction_risk <- strategies$surface_distraction * (1 - strategies$structural_fit)

strategies$diagnosis <- ifelse(
  strategies$surface_distraction_risk >= 0.50,
  "surface_analogy_risk",
  ifelse(
    strategies$adaptation_quality < 0.45,
    "weak_adaptation",
    ifelse(
      strategies$dynamic_compatibility < 0.50,
      "dynamic_compatibility_gap",
      ifelse(strategies$analogy_profile_score >= 0.60, "strong_transfer_candidate", "requires_analogy_review")
    )
  )
)

mappings$mapping_score <-
  0.14 * mappings$actor_correspondence +
  0.20 * mappings$relation_correspondence +
  0.14 * mappings$flow_correspondence +
  0.14 * mappings$constraint_correspondence +
  0.14 * mappings$feedback_correspondence +
  0.12 * mappings$failure_mode_correspondence +
  0.08 * mappings$breakpoint_visibility +
  0.04 * mappings$mapping_confidence

write.csv(strategies[order(-strategies$analogy_profile_score), ], file.path(out_tables, "r_analogical_strategy_profiles.csv"), row.names = FALSE)
write.csv(mappings[order(-mappings$mapping_score), ], file.path(out_tables, "r_source_target_mapping_scores.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(strategies, aes(x = reorder(strategy_name, analogy_profile_score), y = analogy_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Analogical Transfer Profile Scores",
      x = "Strategy",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_analogical_strategy_profiles.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_analogical_strategy_profiles_base.png"), width = 1100, height = 800)
  barplot(
    strategies$analogy_profile_score,
    names.arg = strategies$strategy_id,
    main = "Analogical Transfer Profile Scores",
    ylab = "Profile score"
  )
  dev.off()
}

print(strategies[, c("strategy_id", "strategy_name", "analogy_profile_score", "surface_distraction_risk", "diagnosis")])
