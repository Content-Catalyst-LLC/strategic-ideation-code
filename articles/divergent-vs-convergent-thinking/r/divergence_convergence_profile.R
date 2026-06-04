# Advanced R workflow for divergence-convergence diagnostics.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

contexts <- read.csv(file.path(raw_dir, "ideation_contexts.csv"))
ideas <- read.csv(file.path(raw_dir, "idea_portfolio.csv"))

contexts$profile_score <-
  0.16 * contexts$exploratory_breadth +
  0.16 * contexts$evaluative_discipline +
  0.18 * contexts$iteration_quality +
  0.14 * contexts$constraint_clarity +
  0.12 * contexts$stakeholder_inclusion +
  0.12 * contexts$evidence_contact +
  0.08 * contexts$action_readiness +
  0.04 * contexts$decision_memory_quality

contexts$premature_convergence_risk <- (1 - contexts$exploratory_breadth) * contexts$closure_pressure
contexts$unbounded_divergence_risk <- contexts$exploratory_breadth * (1 - contexts$evaluative_discipline)
contexts$legitimacy_gap <- pmax(0, contexts$evaluative_discipline - contexts$stakeholder_inclusion)

contexts$diagnosis <- ifelse(
  contexts$premature_convergence_risk >= 0.55,
  "premature_convergence_risk",
  ifelse(
    contexts$unbounded_divergence_risk >= 0.55,
    "unbounded_divergence_risk",
    ifelse(
      contexts$legitimacy_gap >= 0.35,
      "power_or_inclusion_gap",
      ifelse(contexts$profile_score >= 0.70, "balanced_and_adaptive", "requires_process_review")
    )
  )
)

ideas$idea_score <-
  0.12 * ideas$novelty +
  0.18 * ideas$strategic_fit +
  0.14 * ideas$evidence_strength +
  0.12 * ideas$feasibility +
  0.14 * ideas$stakeholder_value +
  0.10 * ideas$risk_visibility +
  0.12 * ideas$ethical_legitimacy +
  0.10 * ideas$implementation_readiness -
  0.08 * ideas$assumption_burden

write.csv(contexts[order(-contexts$profile_score), ], file.path(out_tables, "r_divergence_convergence_profiles.csv"), row.names = FALSE)
write.csv(ideas[order(-ideas$idea_score), ], file.path(out_tables, "r_idea_portfolio_scores.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(contexts, aes(x = reorder(context_name, profile_score), y = profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Divergence-Convergence Profile Scores",
      x = "Context",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_divergence_convergence_profiles.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_divergence_convergence_profiles_base.png"), width = 1100, height = 800)
  barplot(
    contexts$profile_score,
    names.arg = contexts$context_id,
    main = "Divergence-Convergence Profile Scores",
    ylab = "Profile score"
  )
  dev.off()
}

print(contexts[, c("context_id", "context_name", "profile_score", "premature_convergence_risk", "unbounded_divergence_risk", "diagnosis")])
