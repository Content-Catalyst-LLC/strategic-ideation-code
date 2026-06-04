# Advanced R workflow for heuristics in strategic ideation.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

contexts <- read.csv(file.path(raw_dir, "heuristic_contexts.csv"))
ideas <- read.csv(file.path(raw_dir, "idea_search_inventory.csv"))

contexts$closure_pressure <- contexts$anchoring_intensity * contexts$satisficing_tendency
contexts$recognition_trap_risk <- contexts$recognition_comfort * (1 - contexts$exploratory_diversity)

contexts$heuristic_profile_score <-
  -0.11 * contexts$availability_dependence -
  0.11 * contexts$anchoring_intensity -
  0.10 * contexts$recognition_comfort -
  0.11 * contexts$satisficing_tendency -
  0.07 * contexts$affect_pressure -
  0.08 * contexts$default_gravity -
  0.06 * contexts$social_proof_pressure +
  0.17 * contexts$exploratory_diversity +
  0.13 * contexts$stakeholder_variation +
  0.13 * contexts$source_domain_diversity +
  0.14 * contexts$systems_check_quality +
  0.07 * contexts$political_safety +
  0.08 * contexts$decision_memory_quality

contexts$diagnosis <- ifelse(
  contexts$closure_pressure >= 0.55,
  "premature_closure_risk",
  ifelse(
    contexts$recognition_trap_risk >= 0.50,
    "recognition_trap_risk",
    ifelse(
      contexts$heuristic_profile_score >= 0.20,
      "stronger_heuristic_ecology",
      "requires_heuristic_review"
    )
  )
)

ideas$search_breadth_score <-
  0.12 * ideas$stakeholder_visibility +
  0.12 * ideas$novelty_level +
  0.12 * ideas$evidence_pathway +
  0.14 * ideas$strategic_relevance +
  0.10 * ideas$implementation_pathway +
  0.16 * ideas$search_breadth -
  0.12 * ideas$closure_pressure -
  0.08 * ideas$assumption_burden

write.csv(contexts[order(-contexts$heuristic_profile_score), ], file.path(out_tables, "r_heuristic_context_profiles.csv"), row.names = FALSE)
write.csv(ideas[order(-ideas$search_breadth_score), ], file.path(out_tables, "r_search_breadth_scores.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(contexts, aes(x = reorder(context_name, heuristic_profile_score), y = heuristic_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Heuristic Profile Scores",
      x = "Context",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_heuristic_context_profiles.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_heuristic_context_profiles_base.png"), width = 1100, height = 800)
  barplot(
    contexts$heuristic_profile_score,
    names.arg = contexts$context_id,
    main = "Heuristic Profile Scores",
    ylab = "Profile score"
  )
  dev.off()
}

print(contexts[, c("context_id", "context_name", "heuristic_profile_score", "closure_pressure", "recognition_trap_risk", "diagnosis")])
