# Advanced R workflow for conceptual clarity diagnostics.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

concepts <- read.csv(file.path(raw_dir, "concept_inventory.csv"))
metrics <- read.csv(file.path(raw_dir, "metric_register.csv"))
drift <- read.csv(file.path(raw_dir, "drift_events.csv"))

concepts$conceptual_clarity_score <-
  0.17 * concepts$definition_clarity +
  0.14 * concepts$boundary_clarity +
  0.14 * concepts$distinction_quality +
  0.13 * concepts$operational_implication +
  0.15 * concepts$measurement_validity +
  0.10 * concepts$revision_capacity +
  0.07 * concepts$stakeholder_visibility +
  0.06 * concepts$ethical_visibility +
  0.04 * concepts$governance_maturity

concepts$ambiguity_risk <- 1 - concepts$conceptual_clarity_score

concepts$diagnosis <- ifelse(
  concepts$definition_clarity < 0.45 & concepts$measurement_validity < 0.45,
  "high_false_precision_risk",
  ifelse(
    concepts$boundary_clarity < 0.40,
    "concept_expansion_or_boundary_risk",
    ifelse(
      concepts$revision_capacity < 0.35,
      "conceptual_drift_risk",
      ifelse(concepts$conceptual_clarity_score >= 0.64, "usable_for_strategy", "requires_clarity_review")
    )
  )
)

metrics$proxy_failure_risk <-
  0.28 * metrics$proxy_risk +
  0.26 * metrics$incentive_distortion_risk +
  0.22 * metrics$qualitative_gap +
  0.24 * (1 - metrics$validity_confidence)

drift$drift_priority <-
  0.34 * drift$drift_severity +
  0.34 * drift$strategic_exposure +
  0.18 * drift$detection_confidence

write.csv(concepts[order(concepts$conceptual_clarity_score), ], file.path(out_tables, "r_conceptual_clarity_scores.csv"), row.names = FALSE)
write.csv(metrics[order(-metrics$proxy_failure_risk), ], file.path(out_tables, "r_metric_proxy_risk.csv"), row.names = FALSE)
write.csv(drift[order(-drift$drift_priority), ], file.path(out_tables, "r_conceptual_drift_priority.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(concepts, aes(x = reorder(concept_name, conceptual_clarity_score), y = conceptual_clarity_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Conceptual Clarity Scores",
      x = "Concept",
      y = "Clarity score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_conceptual_clarity_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_conceptual_clarity_scores_base.png"), width = 1100, height = 800)
  barplot(
    concepts$conceptual_clarity_score,
    names.arg = concepts$concept_id,
    main = "Conceptual Clarity Scores",
    ylab = "Clarity score"
  )
  dev.off()
}

print(concepts[, c("concept_id", "concept_name", "conceptual_clarity_score", "ambiguity_risk", "diagnosis")])
