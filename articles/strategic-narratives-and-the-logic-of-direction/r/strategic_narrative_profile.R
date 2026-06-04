# Advanced R workflow for strategic narrative diagnostics.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

profiles <- read.csv(file.path(raw_dir, "narrative_profiles.csv"))
performance <- read.csv(file.path(raw_dir, "performance_evidence.csv"))
drift <- read.csv(file.path(raw_dir, "narrative_drift_events.csv"))

profiles$narrative_coherence_score <-
  0.14 * profiles$diagnosis_clarity +
  0.12 * profiles$purpose_clarity +
  0.14 * profiles$choice_clarity +
  0.12 * profiles$sequencing_logic +
  0.11 * profiles$role_clarity +
  0.10 * profiles$future_credibility +
  0.11 * profiles$accountability_strength +
  0.08 * profiles$evidence_grounding +
  0.05 * profiles$stakeholder_visibility +
  0.03 * profiles$ethical_visibility

profiles$drift_risk <- 1 - profiles$narrative_coherence_score

profiles$diagnosis <- ifelse(
  profiles$choice_clarity < 0.40,
  "weak_choice_logic",
  ifelse(
    profiles$sequencing_logic < 0.40,
    "weak_pathway_logic",
    ifelse(
      profiles$accountability_strength < 0.40,
      "narrative_performance_gap_risk",
      ifelse(profiles$narrative_coherence_score >= 0.72, "strong_directional_narrative", "requires_review")
    )
  )
)

performance$narrative_performance_gap <-
  0.26 * (1 - performance$evidence_strength) +
  0.28 * (1 - performance$action_alignment) +
  0.26 * performance$contradiction_risk +
  0.12 * performance$stakeholder_signal +
  0.08 * ifelse(performance$revision_required == "true", 1, 0)

drift$drift_priority <-
  0.34 * drift$drift_severity +
  0.34 * drift$strategic_exposure +
  0.18 * drift$detection_confidence

write.csv(profiles[order(-profiles$narrative_coherence_score), ], file.path(out_tables, "r_narrative_coherence_scores.csv"), row.names = FALSE)
write.csv(performance[order(-performance$narrative_performance_gap), ], file.path(out_tables, "r_narrative_performance_gap.csv"), row.names = FALSE)
write.csv(drift[order(-drift$drift_priority), ], file.path(out_tables, "r_narrative_drift_priority.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(profiles, aes(x = reorder(narrative_name, narrative_coherence_score), y = narrative_coherence_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Narrative Coherence Scores",
      x = "Narrative",
      y = "Coherence score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_narrative_coherence_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_narrative_coherence_scores_base.png"), width = 1100, height = 800)
  barplot(
    profiles$narrative_coherence_score,
    names.arg = profiles$narrative_id,
    main = "Strategic Narrative Coherence Scores",
    ylab = "Coherence score"
  )
  dev.off()
}

print(profiles[, c("narrative_id", "narrative_name", "narrative_coherence_score", "drift_risk", "diagnosis")])
